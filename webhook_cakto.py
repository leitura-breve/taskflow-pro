"""Webhook handler para a Cakto — entrega dos PDFs apos a venda.

Fluxo:
  1. Cakto avisa este endpoint quando ha venda (POST /webhook/cakto)
  2. Validamos a autenticidade do request (assinatura HMAC se configurada)
  3. Processamos o evento (purchase_approved, subscription_created, refunded, etc.)
  4. Geramos um token unico de download, salvamos no SQLite e
     simulamos envio de email com o link
  5. Cliente acessa GET /download/<token> e recebe o PDF

Dependencias: pip install flask python-dotenv

Para rodar localmente:
  python3 webhook_cakto.py
  # Abre em http://localhost:5000

Para producao: por tras de gunicorn/uwsgi + nginx, com HTTPS.
"""

import os
import json
import hmac
import hashlib
import sqlite3
import secrets
import logging
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, request, jsonify, send_file, abort, redirect

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv eh opcional

# ─────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "leitura_breve.db"
LOG_PATH = BASE_DIR / "webhook.log"

# Secret compartilhado com a Cakto para validar HMAC dos webhooks.
# Setar via .env: CAKTO_WEBHOOK_SECRET=xxx
WEBHOOK_SECRET = os.environ.get("CAKTO_WEBHOOK_SECRET", "")

# Mapeamento product_id (da Cakto) -> PDF local.
# Apos criar os produtos no painel da Cakto, voce pega os IDs reais e
# troca neste dicionario. Por enquanto usa o external_id como chave.
PRODUCT_TO_PDF = {
    "leitura_breve_vol_01": "Habitos_Atomicos_Resumo.pdf",
    "leitura_breve_vol_02": "O_Alquimista_Resumo.pdf",
    "leitura_breve_vol_03": "A_Sutil_Arte_Resumo.pdf",
    "leitura_breve_vol_04": "Vol_04_poder_habito.pdf",
    "leitura_breve_vol_05": "Vol_05_mindset.pdf",
    "leitura_breve_vol_06": "Vol_06_milagre_manha.pdf",
    "leitura_breve_vol_07": "Vol_07_pai_rico.pdf",
    "leitura_breve_vol_08": "Vol_08_sete_habitos.pdf",
    "leitura_breve_vol_09": "Vol_09_amigos.pdf",
    "leitura_breve_vol_10": "Vol_10_babilonia.pdf",
    "leitura_breve_vol_11": "Vol_11_monge.pdf",
    "leitura_breve_vol_12": "Vol_12_ie.pdf",
    "leitura_breve_vol_13": "Vol_13_rapido_devagar.pdf",
    "leitura_breve_vol_14": "Vol_14_trabalhe4h.pdf",
    "leitura_breve_vol_15": "Vol_15_mente_milionaria.pdf",
    "leitura_breve_vol_16": "Vol_16_dom_casmurro.pdf",
    "leitura_breve_vol_17": "Vol_17_capitaes_areia.pdf",
    "leitura_breve_vol_18": "Vol_18_pequeno_principe.pdf",
    "leitura_breve_vol_19": "Vol_19_comece_porque.pdf",
    "leitura_breve_vol_20": "Vol_20_coragem_imperfeito.pdf",
    "leitura_breve_vol_21": "Vol_21_essencialismo.pdf",
    "leitura_breve_vol_22": "Vol_22_antifragil.pdf",
    "leitura_breve_vol_23": "Vol_23_arte_guerra.pdf",
    "leitura_breve_vol_24": "Vol_24_meditacoes.pdf",
    "leitura_breve_vol_25": "Vol_25_leis_poder.pdf",
    "leitura_breve_vol_26": "Vol_26_oceano_azul.pdf",
    "leitura_breve_vol_27": "Vol_27_zero_a_um.pdf",
    "leitura_breve_vol_28": "Vol_28_tudo_foda.pdf",
    "leitura_breve_vol_29": "Vol_29_busca_sentido.pdf",
    "leitura_breve_vol_30": "Vol_30_vidas_secas.pdf",
    "leitura_breve_vol_31": "Vol_31_bras_cubas.pdf",
    "leitura_breve_vol_32": "Vol_32_hora_estrela.pdf",
    "leitura_breve_vol_33": "Vol_33_quarto_despejo.pdf",
    "leitura_breve_vol_34": "Vol_34_cem_anos.pdf",
    "leitura_breve_vol_35": "Vol_35_1984.pdf",
    "leitura_breve_vol_36": "Vol_36_anne_frank.pdf",
    "leitura_breve_vol_37": "Vol_37_revolucao_bichos.pdf",
    "leitura_breve_vol_38": "Vol_38_sapiens.pdf",
    "leitura_breve_vol_39": "Vol_39_poder_agora.pdf",
    "leitura_breve_vol_40": "Vol_40_pense_enriqueca.pdf",
    "leitura_breve_vol_41": "Vol_41_linguagens_amor.pdf",
    "leitura_breve_vol_42": "Vol_42_cnv.pdf",
    "leitura_breve_vol_43": "Vol_43_coragem_nao_agradar.pdf",
    "leitura_breve_vol_44": "Vol_44_12_regras.pdf",
    "leitura_breve_vol_45": "Vol_45_garra.pdf",
    "leitura_breve_vol_46": "Vol_46_ansiedade_cury.pdf",
    "leitura_breve_vol_47": "Vol_47_mulheres_lobos.pdf",
    "leitura_breve_vol_48": "Vol_48_menina_livros.pdf",
    "leitura_breve_vol_49": "Vol_49_cabana.pdf",
    "leitura_breve_vol_50": "Vol_50_cortico.pdf",
    "leitura_breve_vol_51": "Vol_51_policarpo.pdf",
    "leitura_breve_vol_52": "Vol_52_crime_castigo.pdf",
    "leitura_breve_vol_53": "Vol_53_metamorfose.pdf",
}

# Para assinatura: todos os PDFs disponiveis
SUBSCRIPTION_PRODUCTS = {"leitura_breve_assinatura_mensal",
                         "leitura_breve_assinatura_anual"}

# Validade do link de download (em dias)
DOWNLOAD_TOKEN_TTL_DAYS = 30
MAX_DOWNLOADS_PER_TOKEN = 5

# ─────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("cakto-webhook")


# ─────────────────────────────────────────────────────
# Banco de dados — SQLite simples
# ─────────────────────────────────────────────────────
def db_init():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        received_at TEXT NOT NULL,
        event_type TEXT NOT NULL,
        product_id TEXT,
        customer_email TEXT,
        customer_name TEXT,
        order_id TEXT,
        raw_payload TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS download_tokens (
        token TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        customer_email TEXT NOT NULL,
        product_id TEXT NOT NULL,
        downloads_used INTEGER DEFAULT 0,
        order_id TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_events_order ON events(order_id);
    CREATE INDEX IF NOT EXISTS idx_tokens_email ON download_tokens(customer_email);
    """)
    conn.commit()
    conn.close()


def db_log_event(event_type, product_id, customer_email, customer_name, order_id, payload):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO events
           (received_at, event_type, product_id, customer_email, customer_name, order_id, raw_payload)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (datetime.utcnow().isoformat(), event_type, product_id, customer_email,
         customer_name, order_id, json.dumps(payload, ensure_ascii=False)),
    )
    conn.commit()
    conn.close()


def db_create_token(customer_email, product_id, order_id):
    token = secrets.token_urlsafe(24)
    expires_at = datetime.utcnow() + timedelta(days=DOWNLOAD_TOKEN_TTL_DAYS)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO download_tokens
           (token, created_at, expires_at, customer_email, product_id, downloads_used, order_id)
           VALUES (?, ?, ?, ?, ?, 0, ?)""",
        (token, datetime.utcnow().isoformat(), expires_at.isoformat(),
         customer_email, product_id, order_id),
    )
    conn.commit()
    conn.close()
    return token


def db_get_token(token):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM download_tokens WHERE token = ?", (token,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def db_register_download(token):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE download_tokens SET downloads_used = downloads_used + 1 WHERE token = ?",
        (token,),
    )
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────────
# Validacao do webhook
# ─────────────────────────────────────────────────────
def validate_signature(payload_bytes: bytes, received_sig: str) -> bool:
    """Valida assinatura HMAC-SHA256 do payload.

    Cakto usa header 'X-Cakto-Signature' (ou similar) com hex do HMAC.
    Se WEBHOOK_SECRET nao estiver setado, log warning e aceita
    (so para desenvolvimento — NAO usar em producao).
    """
    if not WEBHOOK_SECRET:
        log.warning("CAKTO_WEBHOOK_SECRET nao configurado — validacao desativada")
        return True
    if not received_sig:
        return False
    expected = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload_bytes,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, received_sig)


def send_delivery_email(customer_email, customer_name, product_name, download_url):
    """Envia email com link de download.

    Implementacao real: usar SES, Sendgrid, SMTP, etc.
    Aqui apenas logamos (para o exemplo funcionar sem credenciais externas).
    """
    log.info(f"[EMAIL] Para: {customer_email} ({customer_name})")
    log.info(f"[EMAIL] Assunto: Seu acesso a '{product_name}' — Leitura Breve")
    log.info(f"[EMAIL] Link de download: {download_url}")
    # TODO: substituir por chamada real ao seu provedor de email


# ─────────────────────────────────────────────────────
# Flask app
# ─────────────────────────────────────────────────────
app = Flask(__name__)
db_init()


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Leitura Breve — Cakto webhook handler",
        "status": "running",
        "endpoints": {
            "POST /webhook/cakto": "Recebe notificacoes da Cakto",
            "GET /download/<token>": "Download autenticado do PDF",
            "GET /admin/events": "Lista eventos recebidos (dev only)",
        },
    })


@app.route("/webhook/cakto", methods=["POST"])
def webhook_cakto():
    payload_bytes = request.get_data()
    received_sig = (
        request.headers.get("X-Cakto-Signature")
        or request.headers.get("X-Signature")
        or request.headers.get("Signature")
        or ""
    )

    if not validate_signature(payload_bytes, received_sig):
        log.warning("Webhook recusado: assinatura invalida")
        return jsonify({"error": "invalid signature"}), 401

    try:
        payload = request.get_json(force=True)
    except Exception as e:
        log.error(f"Payload invalido: {e}")
        return jsonify({"error": "invalid payload"}), 400

    event_type = payload.get("event") or payload.get("type") or "unknown"

    # Cakto envia diferentes estruturas conforme o evento.
    # Estes nomes de campo sao tentativas — ajuste apos receber o primeiro
    # webhook real para mapear corretamente.
    data = payload.get("data", payload)
    product_id = (
        data.get("product_id")
        or data.get("product", {}).get("id")
        or data.get("offer_id")
        or data.get("external_id")
        or ""
    )
    customer = data.get("customer") or data.get("buyer") or {}
    customer_email = customer.get("email") or data.get("customer_email") or ""
    customer_name = customer.get("name") or data.get("customer_name") or ""
    order_id = data.get("order_id") or data.get("transaction_id") or data.get("id") or ""

    log.info(f"Evento recebido: {event_type} | produto={product_id} | "
             f"cliente={customer_email} | order={order_id}")

    db_log_event(event_type, product_id, customer_email, customer_name, order_id, payload)

    # Acao por tipo de evento
    if event_type in {"purchase.approved", "purchase_approved", "order.paid",
                      "compra.aprovada", "approved"}:
        return _handle_purchase_approved(product_id, customer_email, customer_name, order_id)
    elif event_type in {"subscription.created", "subscription_created",
                        "subscription.renewed", "subscription_renewed",
                        "assinatura.criada", "assinatura.renovada"}:
        return _handle_subscription(product_id, customer_email, customer_name, order_id)
    elif event_type in {"purchase.refunded", "purchase_refunded",
                        "subscription.cancelled", "subscription_cancelled",
                        "chargeback"}:
        log.info(f"Acesso revogavel registrado para order={order_id}")
        # TODO: revogar acesso (deletar tokens, marcar conta como inativa)
        return jsonify({"status": "noted"}), 200
    else:
        log.info(f"Evento sem acao mapeada: {event_type}")
        return jsonify({"status": "ignored", "event": event_type}), 200


def _handle_purchase_approved(product_id, customer_email, customer_name, order_id):
    """Compra unica aprovada: gera token e envia email com link do PDF."""
    if not product_id or not customer_email:
        log.error("Compra aprovada sem product_id ou customer_email")
        return jsonify({"error": "missing fields"}), 400

    if product_id not in PRODUCT_TO_PDF:
        log.error(f"Produto desconhecido: {product_id}")
        return jsonify({"error": "unknown product"}), 400

    token = db_create_token(customer_email, product_id, order_id)
    base = request.host_url.rstrip("/")
    download_url = f"{base}/download/{token}"
    product_name = product_id.replace("leitura_breve_", "").replace("_", " ").title()

    send_delivery_email(customer_email, customer_name, product_name, download_url)

    return jsonify({
        "status": "delivered",
        "product": product_id,
        "download_url": download_url,
        "expires_in_days": DOWNLOAD_TOKEN_TTL_DAYS,
    }), 200


def _handle_subscription(product_id, customer_email, customer_name, order_id):
    """Assinatura: cria um token unico que da acesso a TODOS os PDFs."""
    if not customer_email:
        return jsonify({"error": "missing customer_email"}), 400

    # Para assinatura usamos product_id especial '__all__'
    token = db_create_token(customer_email, "__all__", order_id)
    base = request.host_url.rstrip("/")
    members_url = f"{base}/members/{token}"

    log.info(f"[ASSINATURA] {customer_email} -> {members_url}")
    send_delivery_email(customer_email, customer_name,
                        "Assinatura Leitura Breve", members_url)

    return jsonify({
        "status": "subscription_active",
        "members_url": members_url,
    }), 200


@app.route("/download/<token>", methods=["GET"])
def download(token):
    record = db_get_token(token)
    if not record:
        abort(404, description="Token nao encontrado")

    # Validar expiracao
    expires_at = datetime.fromisoformat(record["expires_at"])
    if datetime.utcnow() > expires_at:
        abort(410, description="Link expirado. Entre em contato para renovar.")

    if record["downloads_used"] >= MAX_DOWNLOADS_PER_TOKEN:
        abort(429, description="Limite de downloads atingido")

    product_id = record["product_id"]
    if product_id == "__all__":
        # Assinatura — redireciona pra members area
        return redirect(f"/members/{token}")

    pdf_name = PRODUCT_TO_PDF.get(product_id)
    if not pdf_name:
        abort(404, description="Produto sem PDF mapeado")

    pdf_path = BASE_DIR / pdf_name
    if not pdf_path.exists():
        log.error(f"PDF nao encontrado no disco: {pdf_path}")
        abort(500, description="Arquivo indisponivel")

    db_register_download(token)
    log.info(f"Download: token={token[:8]}... produto={product_id}")
    return send_file(pdf_path, as_attachment=True, download_name=pdf_name)


@app.route("/members/<token>", methods=["GET"])
def members_area(token):
    """Area de membros para assinantes — lista todos os PDFs disponiveis."""
    record = db_get_token(token)
    if not record:
        abort(404, description="Token nao encontrado")

    expires_at = datetime.fromisoformat(record["expires_at"])
    if datetime.utcnow() > expires_at:
        abort(410, description="Assinatura expirada")

    # HTML simples listando todos os PDFs
    rows = []
    for pid, pdf in sorted(PRODUCT_TO_PDF.items(), key=lambda x: x[0]):
        vol = pid.replace("leitura_breve_vol_", "")
        rows.append(f"<li><a href='/members/{token}/pdf/{pid}'>Vol. {vol} — {pdf}</a></li>")
    html = f"""<!doctype html>
    <html lang="pt-BR"><head><meta charset="utf-8">
    <title>Leitura Breve — Area de Membros</title>
    <style>body{{font-family:system-ui;max-width:760px;margin:3rem auto;padding:1rem;background:#F5F1E8;color:#0E0E0E}}
    h1{{font-weight:800}}h2{{color:#1B4D3E}}li{{margin:.5rem 0}}a{{color:#0E0E0E}}</style>
    </head><body>
    <h1>Leitura Breve</h1>
    <h2>Sua biblioteca — {record['customer_email']}</h2>
    <p>Acesso valido ate {expires_at.date().isoformat()}.</p>
    <ul>{''.join(rows)}</ul>
    </body></html>"""
    return html


@app.route("/members/<token>/pdf/<product_id>", methods=["GET"])
def members_download(token, product_id):
    record = db_get_token(token)
    if not record:
        abort(404)
    if record["product_id"] != "__all__":
        abort(403, description="Acesso so para assinantes")
    expires_at = datetime.fromisoformat(record["expires_at"])
    if datetime.utcnow() > expires_at:
        abort(410, description="Assinatura expirada")
    pdf_name = PRODUCT_TO_PDF.get(product_id)
    if not pdf_name:
        abort(404)
    pdf_path = BASE_DIR / pdf_name
    if not pdf_path.exists():
        abort(500)
    db_register_download(token)
    return send_file(pdf_path, as_attachment=True, download_name=pdf_name)


@app.route("/admin/events", methods=["GET"])
def admin_events():
    """Endpoint admin para inspecionar eventos recebidos.

    PRODUCAO: proteger com autenticacao (basic auth, IP allow-list, etc.)
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, received_at, event_type, product_id, customer_email, order_id "
        "FROM events ORDER BY id DESC LIMIT 50"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    log.info(f"Leitura Breve webhook handler iniciando em :{port}")
    log.info(f"PDFs em: {BASE_DIR}")
    log.info(f"DB: {DB_PATH}")
    log.info(f"HMAC ativo: {'SIM' if WEBHOOK_SECRET else 'NAO (configure CAKTO_WEBHOOK_SECRET)'}")
    app.run(host="0.0.0.0", port=port, debug=False)
