# Site Leitura Breve + Webhook Cakto

Tudo o que foi montado para vender e entregar a coleção dos 38 volumes.

## Estrutura

```
.
├── site/                          # Site estático (HTML/CSS/JS)
│   ├── index.html                 # Landing page
│   ├── styles.css                 # Estilos
│   └── app.js                     # Modal de livro, filtros, animações
├── gerar_site.py                  # Regenera o site a partir de cakto_products.py
├── webhook_cakto.py               # Backend Flask para entrega após venda
├── cakto_products.py              # Dados estruturados dos 40 produtos
├── cakto_export.py                # Gera CSV + textos de venda + resumo
├── cakto_import.csv               # Planilha para cadastro no painel da Cakto
├── cakto_textos_venda.md          # Textos prontos para copiar/colar
└── Vol_*.pdf                      # Os 38 PDFs + os 3 primeiros (Habitos, Alquimista, Sutil Arte)
```

---

## 1. Site estático

### Visualizar localmente
```bash
cd site
python3 -m http.server 8000
# http://localhost:8000
```

### Regenerar
```bash
python3 gerar_site.py
```

### Antes de subir em produção
Edite `gerar_site.py` e substitua os placeholders dos checkouts Cakto:

```python
def cakto_url(vol):
    return f"https://app.cakto.com.br/checkout/REPLACE_ME_VOL_{vol}"
```

Depois de criar cada produto no painel da Cakto, você terá URLs reais
do tipo `https://pay.cakto.com.br/abc123def`. Cole no dicionário e
regere o site.

### Deploy
Como é estático, sobe em qualquer:
- GitHub Pages
- Cloudflare Pages
- Vercel
- Netlify
- S3 + CloudFront

Recomendado: **Cloudflare Pages** (grátis, CDN global, HTTPS automático).

---

## 2. Webhook handler (entrega após venda)

### O que faz
1. Cakto manda POST quando há venda → este servidor recebe
2. Valida assinatura HMAC (segurança)
3. Registra o evento no SQLite
4. Para compra única: gera token, envia email com link de download
5. Para assinatura: cria área de membros com todos os 38 PDFs
6. Token expira em 30 dias com limite de 5 downloads

### Rodar localmente
```bash
pip install flask python-dotenv
export CAKTO_WEBHOOK_SECRET="seu_secret_aqui"  # ou põe no .env
python3 webhook_cakto.py
# http://localhost:5000
```

### Endpoints
- `POST /webhook/cakto` — Cakto chama aqui após cada evento
- `GET /download/<token>` — Download do PDF (compra única)
- `GET /members/<token>` — Área de membros (assinatura)
- `GET /admin/events` — Lista de eventos recebidos (proteja em prod!)

### Configurar na Cakto
1. Painel Cakto → Configurações → Webhooks
2. URL: `https://seudominio.com.br/webhook/cakto`
3. Eventos: marcar **Compra aprovada**, **Assinatura criada**,
   **Assinatura renovada**, **Reembolso**, **Cancelamento**
4. Copie o **secret** que a Cakto gera
5. Cole em `.env` como `CAKTO_WEBHOOK_SECRET=xxx`

### Deploy em produção
Servidor mínimo (1 vCPU, 1 GB RAM):

```bash
# Atrás de gunicorn (não use Flask dev em prod)
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5000 webhook_cakto:app
```

Atrás de nginx para HTTPS:
```nginx
server {
    listen 443 ssl;
    server_name api.leiturabreve.com.br;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        client_max_body_size 1m;
    }
}
```

### Email real
O código atual só **registra** o que seria enviado.
Substitua `send_delivery_email()` em `webhook_cakto.py` por chamada ao
seu provedor (SES, Sendgrid, Resend, Mailgun, etc.).

---

## 3. Fluxo completo de venda

```
┌─────────────┐    1. clica em      ┌─────────────┐
│  Site       │──── "Comprar" ────▶ │  Cakto      │
│  (estático) │                     │  Checkout   │
└─────────────┘                     └──────┬──────┘
                                           │ 2. cliente paga
                                           ▼
                                    ┌─────────────┐
                                    │  Cakto      │
                                    │  notifica   │
                                    └──────┬──────┘
                                           │ 3. POST webhook
                                           ▼
                                    ┌─────────────┐
                                    │  Webhook    │
                                    │  handler    │
                                    │  (Flask)    │
                                    └──────┬──────┘
                                           │ 4. gera token + envia email
                                           ▼
                                    ┌─────────────┐
                                    │  Cliente    │
                                    │  recebe     │
                                    │  link       │
                                    └──────┬──────┘
                                           │ 5. clica e baixa PDF
                                           ▼
                                    ┌─────────────┐
                                    │  GET        │
                                    │  /download  │
                                    └─────────────┘
```

---

## 4. Próximos passos sugeridos

1. **Criar os 38 produtos no painel da Cakto** usando `cakto_textos_venda.md`
2. **Pegar as URLs reais de checkout** de cada produto
3. **Editar `gerar_site.py`** com as URLs reais e regerar
4. **Deploy do site** em Cloudflare Pages/Vercel
5. **Deploy do webhook** em VPS pequena (ou Cloud Run, Railway, Render)
6. **Configurar email** (Resend é simples e barato pra esse volume)
7. **Configurar webhook na Cakto** apontando pra `https://seudominio/webhook/cakto`
8. **Testar com um produto real** comprando você mesmo R$ 1 com cupom 99% off
