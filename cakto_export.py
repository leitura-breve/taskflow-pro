"""Exporta os 38 livros + 2 assinaturas em formatos prontos para uso na Cakto.

Gera:
  1. cakto_import.csv          — planilha com todos os campos
  2. cakto_textos_venda.md     — textos persuasivos prontos pra copiar/colar
  3. cakto_resumo.txt          — auditoria rápida
"""

import csv
import os
from cakto_products import get_products, BOOKS_META, PRECO_INDIVIDUAL, PRECO_ASSINATURA_MENSAL, PRECO_ASSINATURA_ANUAL

OUT_DIR = "/home/user/taskflow-pro"


def price_brl(cents):
    """1990 (centavos) -> 'R$ 19,90'"""
    return f"R$ {cents/100:.2f}".replace(".", ",")


# ─────────────────────────────────────────────────────
# 1. CSV — campos padronizados para importação no painel
# ─────────────────────────────────────────────────────
def export_csv():
    path = os.path.join(OUT_DIR, "cakto_import.csv")
    fields = [
        "Tipo",                       # digital / subscription
        "Vol",
        "Nome do produto",
        "Categoria",
        "Tags",
        "Descricao curta",
        "Descricao longa (HTML)",
        "Preco (BRL)",
        "Preco (centavos)",
        "Ciclo de cobranca",          # vazio p/ digital; monthly/yearly p/ assinatura
        "Tipo de entrega",
        "Arquivo PDF",
        "ID externo",
    ]
    products = get_products()
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(fields)
        for p in products:
            writer.writerow([
                p["type"],
                p.get("vol", ""),
                p["name"],
                p["category"],
                "; ".join(p.get("tags", [])),
                p["short_description"],
                p["long_description"].replace("\n", " ").strip(),
                price_brl(p["price_cents"]),
                p["price_cents"],
                p.get("billing_cycle", ""),
                p.get("delivery", ""),
                os.path.basename(p.get("file_path", "")) if p.get("file_path") else "",
                p["external_id"],
            ])
    return path


# ─────────────────────────────────────────────────────
# 2. Textos de venda — Markdown pronto pra copiar/colar
# ─────────────────────────────────────────────────────
def headline(book):
    """Headline persuasivo (até 70 caracteres)."""
    vol, _id, titulo, autor, _categoria, _tese, _quote, _pdf = book
    # padrão: "[Título] em uma sessão · Resumo Leitura Breve"
    return f"{titulo} em uma sessão de leitura · Vol. {vol}"


def bullets(book):
    """5 bullets persuasivos."""
    vol, _id, titulo, autor, categoria, tese, _quote, _pdf = book
    return [
        f"Resumo editorial completo de \"{titulo}\" — 25-39 páginas em PDF A4",
        f"Tese central, capítulos comentados e citações em destaque",
        f"Aplicação prática + cronograma de 4 semanas para implantar as ideias",
        f"Caderno de leitura com espaço para anotações e provocações pessoais",
        f"Design minimalista moderno, formatado para impressão ou tablet",
    ]


def faq_text(book):
    """FAQ padronizado."""
    return [
        ("Esse é o livro completo?",
         "Não. É um <strong>resumo editorial</strong> em PDF com a tese, capítulos comentados, citações, aplicação prática e caderno de leitura. Pensado pra você ler em uma sessão e voltar quando quiser revisitar."),
        ("Em quanto tempo recebo?",
         "Acesso imediato após confirmação do pagamento. PDF para download."),
        ("Posso imprimir?",
         "Sim. O PDF é em A4, otimizado para leitura digital e impressão doméstica."),
        ("Funciona em celular/tablet?",
         "Sim. PDF abre em qualquer leitor (Adobe, Apple Books, Google Drive, etc.)."),
        ("Posso pedir reembolso?",
         "Sim, em até 7 dias após a compra, conforme o Código de Defesa do Consumidor."),
    ]


def export_textos_md():
    path = os.path.join(OUT_DIR, "cakto_textos_venda.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Textos de venda — Coleção Leitura Breve (38 volumes + assinatura)\n\n")
        f.write("Pronto para copiar/colar no painel da Cakto, campo a campo.\n\n")
        f.write("---\n\n")

        # --- 38 livros ---
        for book in BOOKS_META:
            vol, _id, titulo, autor, categoria, tese, quote, pdf = book
            f.write(f"## Vol. {vol} — {titulo}\n\n")
            f.write(f"**Autor:** {autor}  \n")
            f.write(f"**Categoria:** {categoria}  \n")
            f.write(f"**Preço sugerido:** {price_brl(PRECO_INDIVIDUAL)}  \n")
            f.write(f"**Arquivo:** `{pdf}`  \n\n")

            f.write(f"### Nome do produto\n")
            f.write(f"```\nVol. {vol} · {titulo} — Resumo Leitura Breve\n```\n\n")

            f.write(f"### Headline / Slogan\n")
            f.write(f"```\n{headline(book)}\n```\n\n")

            f.write(f"### Descrição curta (listagem)\n")
            f.write(f"```\n")
            f.write(f"Resumo editorial de \"{titulo}\" ({autor}). 25-39 páginas com tese, ")
            f.write(f"capítulos comentados, citações e caderno de leitura.\n")
            f.write(f"```\n\n")

            f.write(f"### Bullets (página de venda)\n")
            for b in bullets(book):
                f.write(f"- {b}\n")
            f.write("\n")

            f.write(f"### Frase de impacto (pull quote)\n")
            f.write(f"> *\"{quote}\"*\n>\n> — {autor}\n\n")

            f.write(f"### Tese central\n")
            f.write(f"> {tese}\n\n")

            f.write(f"### Descrição longa (HTML — colar em editor rich-text)\n")
            f.write("```html\n")
            f.write(f"<h2>Resumo editorial de <em>{titulo}</em></h2>\n")
            f.write(f"<p><strong>Autor:</strong> {autor}<br>\n")
            f.write(f"<strong>Categoria:</strong> {categoria}<br>\n")
            f.write(f"<strong>Coleção:</strong> Leitura Breve · Vol. {vol}</p>\n\n")
            f.write(f"<h3>A tese, em uma frase</h3>\n")
            f.write(f"<p><em>{tese}</em></p>\n\n")
            f.write(f"<h3>O que você recebe</h3>\n<ul>\n")
            for b in bullets(book):
                f.write(f"  <li>{b}</li>\n")
            f.write(f"</ul>\n\n")
            f.write(f"<blockquote>\"{quote}\" — {autor}</blockquote>\n")
            f.write("```\n\n")

            f.write(f"### FAQ\n")
            for q, a in faq_text(book):
                f.write(f"**{q}**  \n{a}\n\n")

            f.write(f"### Tags (separadas por vírgula)\n")
            tags = [t.strip() for t in categoria.split("·")] + [autor, "Leitura Breve", "Resumo"]
            f.write(f"```\n{', '.join(tags)}\n```\n\n")
            f.write("---\n\n")

        # --- 2 assinaturas ---
        f.write("## Assinatura Mensal — Coleção Leitura Breve\n\n")
        f.write(f"**Preço:** {price_brl(PRECO_ASSINATURA_MENSAL)}/mês  \n")
        f.write(f"**Tipo:** Recorrência mensal  \n\n")
        f.write("### Nome do produto\n```\nAssinatura Leitura Breve — Mensal\n```\n\n")
        f.write("### Headline\n```\n38 resumos editoriais + novos lançamentos · Acesso ilimitado\n```\n\n")
        f.write("### Descrição curta\n```\n")
        f.write("Acesso a todos os 38 volumes da Coleção Leitura Breve + novos volumes que forem lançados. ")
        f.write("Cancele quando quiser.\n```\n\n")
        f.write("### Bullets\n")
        f.write("- Acesso imediato a 38 resumos editoriais em PDF\n")
        f.write("- Novos volumes incluídos automaticamente durante a assinatura\n")
        f.write("- Catálogo navegável com índice dos 38 volumes\n")
        f.write("- Cancele a qualquer momento, sem multa\n")
        f.write("- Versões revisadas dos volumes existentes incluídas\n\n")
        f.write("---\n\n")

        f.write("## Assinatura Anual — Coleção Leitura Breve (37% OFF)\n\n")
        f.write(f"**Preço:** {price_brl(PRECO_ASSINATURA_ANUAL)}/ano  \n")
        f.write(f"**Equivalente mensal:** {price_brl(PRECO_ASSINATURA_ANUAL // 12)}/mês  \n")
        f.write(f"**Tipo:** Recorrência anual  \n\n")
        f.write("### Nome do produto\n```\nAssinatura Leitura Breve — Anual (37% OFF)\n```\n\n")
        f.write("### Headline\n```\nColeção completa por R$12,42/mês · 37% de desconto na anual\n```\n\n")
        f.write("### Descrição curta\n```\n")
        f.write("Acesso anual a todos os 38 volumes + novos lançamentos. ")
        f.write("Pague uma vez e leia o ano inteiro com 37% de desconto.\n```\n\n")
        f.write("### Bullets\n")
        f.write("- Acesso imediato a 38 resumos editoriais em PDF\n")
        f.write("- 37% de desconto em relação ao plano mensal\n")
        f.write("- Novos volumes incluídos durante o ano de assinatura\n")
        f.write("- Catálogo completo navegável\n")
        f.write("- Para o leitor compromissado com hábito de leitura anual\n\n")

    return path


# ─────────────────────────────────────────────────────
# 3. Resumo / auditoria
# ─────────────────────────────────────────────────────
def export_resumo():
    path = os.path.join(OUT_DIR, "cakto_resumo.txt")
    products = get_products()
    with open(path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("COLECAO LEITURA BREVE — RESUMO PARA CAKTO\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total de produtos: {len(products)}\n")
        f.write(f"  - {sum(1 for p in products if p['type']=='digital')} livros individuais\n")
        f.write(f"  - {sum(1 for p in products if p['type']=='subscription')} planos de assinatura\n\n")
        f.write(f"Precos:\n")
        f.write(f"  - Cada livro: {price_brl(PRECO_INDIVIDUAL)}\n")
        f.write(f"  - Assinatura mensal: {price_brl(PRECO_ASSINATURA_MENSAL)}\n")
        f.write(f"  - Assinatura anual: {price_brl(PRECO_ASSINATURA_ANUAL)} (37% off)\n\n")
        f.write("-" * 70 + "\n")
        f.write("LIVROS\n")
        f.write("-" * 70 + "\n")
        for p in products:
            if p["type"] != "digital": continue
            arquivo = os.path.basename(p["file_path"])
            tamanho_kb = os.path.getsize(p["file_path"]) // 1024 if os.path.exists(p["file_path"]) else 0
            f.write(f"Vol. {p['vol']}  {p['name'][:55]:55s}  {tamanho_kb:>3} KB  {arquivo}\n")
        f.write("\n")
        f.write("-" * 70 + "\n")
        f.write("ASSINATURAS\n")
        f.write("-" * 70 + "\n")
        for p in products:
            if p["type"] != "subscription": continue
            f.write(f"  {p['name']}  ({p.get('billing_cycle', '')})  {price_brl(p['price_cents'])}\n")
        f.write("\n")
        f.write("=" * 70 + "\n")
        f.write("PASSO A PASSO NA CAKTO\n")
        f.write("=" * 70 + "\n")
        f.write("1. Entre em https://app.cakto.com.br/\n")
        f.write("2. Crie cada um dos 38 produtos digitais individuais usando os textos\n")
        f.write("   prontos em cakto_textos_venda.md (copie/cole campo a campo).\n")
        f.write("3. No upload de arquivo, use o PDF correspondente (coluna 'Arquivo' do CSV).\n")
        f.write("4. Crie os 2 planos de assinatura (mensal e anual) — eles usam o mesmo\n")
        f.write("   acervo (todos os 38 PDFs anexados a area de membros).\n")
        f.write("5. Use cakto_import.csv como referencia para configurar precos, categorias\n")
        f.write("   e tags. Se a Cakto tiver importacao em massa, use direto.\n")
    return path


if __name__ == "__main__":
    print("Gerando arquivos para Cakto...")
    csv_path = export_csv()
    print(f"  [OK] CSV de importacao: {csv_path}")
    md_path = export_textos_md()
    print(f"  [OK] Textos de venda:   {md_path}")
    resumo_path = export_resumo()
    print(f"  [OK] Resumo:            {resumo_path}")
    print()
    print("Tudo pronto. Suba pela Cakto:")
    print(f"  https://app.cakto.com.br/")
