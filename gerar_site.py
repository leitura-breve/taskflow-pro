"""Gerador do site Leitura Breve.

Cria um site estatico (HTML/CSS/JS vanilla) usando os dados de cakto_products.py.
Inclui:
  - Landing page com hero, sobre a colecao, galeria interativa dos 38 livros,
    planos de assinatura, FAQ e footer
  - Estilos coerentes com a identidade editorial da colecao
  - Links pro checkout Cakto (placeholders ate o usuario subir os produtos no painel)
"""

import os
import json
from cakto_products import BOOKS_META, PRECO_INDIVIDUAL, PRECO_ASSINATURA_MENSAL, PRECO_ASSINATURA_ANUAL

OUT_DIR = "/home/user/taskflow-pro"
SITE_DIR = os.path.join(OUT_DIR, "site")
os.makedirs(SITE_DIR, exist_ok=True)


def price_brl(cents):
    return f"R$ {cents/100:.2f}".replace(".", ",")


# Paletas das capas (replicadas dos generators originais)
BOOK_PALETTES = {
    "01": {"paper": "#FAFAF7", "accent": "#1B4D3E"},
    "02": {"paper": "#F2EAD3", "accent": "#9C6B1F"},
    "03": {"paper": "#0E0E0E", "accent": "#E55A1F"},
    "04": {"paper": "#F1ECE3", "accent": "#B8662E"},
    "05": {"paper": "#F0EDE5", "accent": "#A52A2A"},
    "06": {"paper": "#FBF5E9", "accent": "#E07B2E"},
    "07": {"paper": "#EEEFE7", "accent": "#9C7E2F"},
    "08": {"paper": "#F0EDE3", "accent": "#7A2025"},
    "09": {"paper": "#F2EBD8", "accent": "#9C6B1F"},
    "10": {"paper": "#EFE7CE", "accent": "#8C6F1A"},
    "11": {"paper": "#EBEDE5", "accent": "#557361"},
    "12": {"paper": "#EFEEEA", "accent": "#C46266"},
    "13": {"paper": "#F1EEEA", "accent": "#A89E2A"},
    "14": {"paper": "#F4F1E9", "accent": "#00AAA6"},
    "15": {"paper": "#F5F1E5", "accent": "#B89A2E"},
    "16": {"paper": "#EDE5D2", "accent": "#7A2025"},
    "17": {"paper": "#EDE2C6", "accent": "#9C5E1F"},
    "18": {"paper": "#EDF3F6", "accent": "#C2A030"},
    "19": {"paper": "#F0EDE3", "accent": "#D49B2C"},
    "20": {"paper": "#F2EBE0", "accent": "#8B5A8E"},
    "21": {"paper": "#F1F0EB", "accent": "#1F6F4A"},
    "22": {"paper": "#EEEDE7", "accent": "#A52A2A"},
    "23": {"paper": "#EFEAD9", "accent": "#7A2025"},
    "24": {"paper": "#EFEAD8", "accent": "#5C5A36"},
    "25": {"paper": "#F0EDE2", "accent": "#9C7E2F"},
    "26": {"paper": "#EAF0F4", "accent": "#00857E"},
    "27": {"paper": "#F0EFEB", "accent": "#1B4D3E"},
    "28": {"paper": "#F1EDE5", "accent": "#3A8DBC"},
    "29": {"paper": "#ECECE7", "accent": "#2E5C3F"},
    "30": {"paper": "#EBE3CC", "accent": "#9C5E22"},
    "31": {"paper": "#EAE3D3", "accent": "#8B4513"},
    "32": {"paper": "#EDE9DC", "accent": "#B83A4B"},
    "33": {"paper": "#E9DECC", "accent": "#8C3C1F"},
    "34": {"paper": "#F0EAD6", "accent": "#A23E1F"},
    "35": {"paper": "#E8E5DA", "accent": "#5C5C5C"},
    "36": {"paper": "#EEEBE0", "accent": "#7A2025"},
    "37": {"paper": "#EDE9DC", "accent": "#A52A2A"},
    "38": {"paper": "#EFEDE3", "accent": "#6B3F1F"},
}

# Placeholder URLs do Cakto — o usuario substitui depois de criar os produtos no painel
def cakto_url(vol):
    return f"https://app.cakto.com.br/checkout/REPLACE_ME_VOL_{vol}"

CAKTO_SUB_MENSAL = "https://app.cakto.com.br/checkout/REPLACE_ME_ASSINATURA_MENSAL"
CAKTO_SUB_ANUAL = "https://app.cakto.com.br/checkout/REPLACE_ME_ASSINATURA_ANUAL"


# ─────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────
CSS = """*{box-sizing:border-box;margin:0;padding:0}
:root{
  --paper:#F5F1E8;
  --ink:#0E0E0E;
  --subink:#2A2A2A;
  --muted:#7A7569;
  --hairline:#D8D3C5;
  --accent:#1B4D3E;
  --accent-alt:#C24E1A;
  --max:1200px;
  --font-display:'Helvetica Neue',-apple-system,'Segoe UI',sans-serif;
  --font-body:'Inter','Helvetica Neue',-apple-system,'Segoe UI',sans-serif;
  --font-serif:'Times New Roman',Times,Georgia,serif;
}
html{scroll-behavior:smooth}
body{
  font-family:var(--font-body);background:var(--paper);color:var(--ink);
  font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased;
  min-height:100vh;
}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
button{font:inherit;cursor:pointer;border:none;background:none}
.wrap{max-width:var(--max);margin:0 auto;padding:0 2rem}

/* ============ NAV ============ */
.nav{
  position:sticky;top:0;z-index:100;
  background:var(--paper);
  border-bottom:1px solid var(--hairline);
}
.nav-inner{
  display:flex;align-items:center;justify-content:space-between;
  padding:1rem 2rem;max-width:var(--max);margin:0 auto;
}
.logo{
  font-family:var(--font-display);font-weight:700;font-size:1.05rem;
  letter-spacing:0.02em;display:flex;align-items:center;gap:.6rem;
}
.logo::before{
  content:'';display:inline-block;width:24px;height:24px;
  border:1.5px solid var(--ink);border-radius:50%;
  background:radial-gradient(circle at 50% 50%, var(--accent) 0 4px, transparent 5px);
}
.nav-links{display:flex;gap:2rem;font-size:.85rem;font-weight:500;letter-spacing:.02em;text-transform:uppercase}
.nav-links a{position:relative;padding:.3rem 0;color:var(--subink);transition:color .2s}
.nav-links a:hover{color:var(--ink)}
.nav-cta{
  display:inline-block;padding:.5rem 1rem;font-size:.78rem;
  background:var(--ink);color:var(--paper);border-radius:99px;
  font-weight:600;letter-spacing:.04em;text-transform:uppercase;transition:transform .15s;
}
.nav-cta:hover{transform:translateY(-1px)}

@media (max-width:768px){
  .nav-links{display:none}
}

/* ============ HERO ============ */
.hero{
  padding:5rem 0 4rem;
  background:var(--paper);
  position:relative;overflow:hidden;
}
.hero-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:4rem;align-items:end}
.hero-eyebrow{
  font-family:var(--font-body);font-weight:700;font-size:.78rem;
  color:var(--accent);text-transform:uppercase;letter-spacing:.2em;
  margin-bottom:1.5rem;
}
.hero-title{
  font-family:var(--font-display);font-weight:800;
  font-size:clamp(3rem, 7vw, 5.5rem);line-height:.95;
  letter-spacing:-0.03em;margin-bottom:1.5rem;
}
.hero-title em{font-style:italic;color:var(--accent);font-family:var(--font-serif)}
.hero-sub{
  font-family:var(--font-serif);font-style:italic;font-size:clamp(1.1rem, 2vw, 1.35rem);
  color:var(--subink);line-height:1.5;margin-bottom:2.5rem;max-width:520px;
}
.hero-ctas{display:flex;gap:1rem;flex-wrap:wrap}
.btn-primary{
  display:inline-flex;align-items:center;gap:.6rem;padding:1rem 1.8rem;
  background:var(--ink);color:var(--paper);border-radius:99px;
  font-weight:600;letter-spacing:.04em;font-size:.9rem;text-transform:uppercase;
  transition:transform .15s,background .15s;
}
.btn-primary:hover{background:var(--accent);transform:translateY(-2px)}
.btn-secondary{
  display:inline-flex;align-items:center;gap:.6rem;padding:1rem 1.8rem;
  background:transparent;color:var(--ink);border:1.5px solid var(--ink);border-radius:99px;
  font-weight:600;letter-spacing:.04em;font-size:.9rem;text-transform:uppercase;
  transition:background .15s,color .15s;
}
.btn-secondary:hover{background:var(--ink);color:var(--paper)}
.hero-stats{
  display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;
  border-top:1px solid var(--hairline);padding-top:2rem;margin-top:3rem;
}
.stat-num{font-family:var(--font-display);font-size:2.5rem;font-weight:700;line-height:1;color:var(--accent)}
.stat-label{font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:.4rem}
.hero-cover{
  position:relative;
  display:flex;align-items:flex-end;justify-content:center;
}
.cover-stack{position:relative;width:100%;max-width:340px;height:480px}
.cover-card{
  position:absolute;width:240px;height:340px;background:var(--paper);
  border:1px solid var(--hairline);box-shadow:0 12px 40px -8px rgba(0,0,0,.18);
  border-radius:4px;padding:1.4rem;display:flex;flex-direction:column;justify-content:space-between;
  transition:transform .4s cubic-bezier(.16,1,.3,1);
}
.cover-card:nth-child(1){transform:translate(-40px, 30px) rotate(-6deg);z-index:1}
.cover-card:nth-child(2){transform:translate(20px, -10px) rotate(3deg);z-index:2}
.cover-card:nth-child(3){transform:translate(60px, -50px) rotate(8deg);z-index:3}
.cover-stack:hover .cover-card:nth-child(1){transform:translate(-80px, 30px) rotate(-12deg)}
.cover-stack:hover .cover-card:nth-child(3){transform:translate(100px, -50px) rotate(14deg)}
.cover-vol{font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:700}
.cover-num{font-family:var(--font-display);font-size:4.5rem;font-weight:800;line-height:1;color:rgba(0,0,0,.07)}
.cover-title{font-family:var(--font-display);font-weight:700;font-size:1.4rem;line-height:1.05;letter-spacing:-.01em}
.cover-author{font-family:var(--font-serif);font-style:italic;font-size:.85rem;color:var(--muted)}

@media (max-width:768px){
  .hero{padding:3rem 0 2rem}
  .hero-grid{grid-template-columns:1fr;gap:3rem}
  .hero-cover{display:none}
}

/* ============ SOBRE ============ */
.about{padding:5rem 0;background:var(--ink);color:var(--paper)}
.about-grid{display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start}
.about-eyebrow{font-weight:700;font-size:.78rem;color:var(--accent-alt);text-transform:uppercase;letter-spacing:.2em;margin-bottom:1rem}
.about h2{font-family:var(--font-display);font-weight:700;font-size:clamp(2rem,4vw,3.2rem);line-height:1.05;letter-spacing:-.02em;margin-bottom:2rem}
.about p{font-size:1.05rem;line-height:1.7;margin-bottom:1.2rem;color:#D4CDB8}
.about p em{color:#fff;font-style:italic;font-family:var(--font-serif)}
.about-features{margin-top:3rem;display:grid;grid-template-columns:1fr 1fr;gap:2rem 3rem}
.feature{display:flex;gap:1rem}
.feature-mark{
  flex-shrink:0;width:32px;height:32px;border-radius:50%;background:var(--accent-alt);
  display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:.85rem;
}
.feature h3{font-size:.95rem;letter-spacing:.02em;margin-bottom:.4rem;color:#fff;font-weight:700}
.feature p{font-size:.9rem;margin:0;color:#A9A294;line-height:1.5}

@media (max-width:768px){
  .about{padding:3rem 0}
  .about-grid{grid-template-columns:1fr;gap:2rem}
  .about-features{grid-template-columns:1fr;gap:1.5rem;margin-top:2rem}
}

/* ============ GALERIA ============ */
.gallery{padding:5rem 0;background:var(--paper)}
.section-head{display:flex;justify-content:space-between;align-items:end;margin-bottom:3rem;gap:2rem}
.section-head .left{flex:1}
.section-eyebrow{font-weight:700;font-size:.78rem;color:var(--accent);text-transform:uppercase;letter-spacing:.2em;margin-bottom:1rem}
.section-head h2{font-family:var(--font-display);font-weight:700;font-size:clamp(2rem,4vw,3rem);line-height:1.05;letter-spacing:-.02em}
.section-head em{font-style:italic;color:var(--accent);font-family:var(--font-serif)}

.filters{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:2.5rem}
.filter-btn{
  padding:.45rem 1rem;font-size:.78rem;letter-spacing:.05em;font-weight:600;
  background:transparent;color:var(--subink);border:1px solid var(--hairline);
  border-radius:99px;text-transform:uppercase;transition:all .15s;
}
.filter-btn:hover{border-color:var(--ink)}
.filter-btn.active{background:var(--ink);color:var(--paper);border-color:var(--ink)}

.book-grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1.5rem;
}
.book-card{
  position:relative;cursor:pointer;
  display:flex;flex-direction:column;
  transition:transform .2s;
}
.book-card:hover{transform:translateY(-4px)}
.book-cover{
  aspect-ratio:0.72/1;
  border-radius:4px;
  padding:1.2rem;
  display:flex;flex-direction:column;justify-content:space-between;
  position:relative;overflow:hidden;
  border:1px solid rgba(0,0,0,.08);
  box-shadow:0 4px 16px -4px rgba(0,0,0,.1);
}
.book-cover-vol{font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;font-weight:700;opacity:.8}
.book-cover-num{font-family:var(--font-display);font-size:3rem;font-weight:800;line-height:1;opacity:.18}
.book-cover-cat{font-size:.6rem;letter-spacing:.15em;text-transform:uppercase;font-weight:700;margin-bottom:.4rem}
.book-cover-title{font-family:var(--font-display);font-weight:700;font-size:1.15rem;line-height:1.05;letter-spacing:-.01em;margin-bottom:.3rem}
.book-cover-author{font-family:var(--font-serif);font-style:italic;font-size:.78rem;opacity:.7}
.book-info{padding:.8rem .2rem 0}
.book-title-row{display:flex;justify-content:space-between;align-items:start;gap:.6rem;margin-bottom:.3rem}
.book-info-title{font-weight:700;font-size:.95rem;line-height:1.2}
.book-info-vol{font-size:.7rem;color:var(--muted);font-weight:600;letter-spacing:.05em;white-space:nowrap}
.book-info-author{font-family:var(--font-serif);font-style:italic;font-size:.82rem;color:var(--muted)}
.book-price{margin-top:.5rem;font-weight:700;font-size:.9rem;color:var(--accent)}

/* ============ PLANOS ============ */
.plans{padding:5rem 0;background:#EFEAD8;border-top:1px solid var(--hairline);border-bottom:1px solid var(--hairline)}
.plans-head{text-align:center;margin-bottom:3rem;max-width:680px;margin-left:auto;margin-right:auto}
.plans-head h2{font-family:var(--font-display);font-weight:700;font-size:clamp(2rem,4vw,3rem);line-height:1.05;letter-spacing:-.02em;margin-bottom:1rem}
.plans-head em{font-style:italic;color:var(--accent);font-family:var(--font-serif)}
.plans-head p{font-family:var(--font-serif);font-style:italic;font-size:1.1rem;color:var(--subink)}
.plans-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;max-width:880px;margin:0 auto}
.plan-card{
  background:var(--paper);padding:2.5rem;border-radius:8px;
  border:1px solid var(--hairline);position:relative;
  display:flex;flex-direction:column;
}
.plan-card.featured{border:2px solid var(--accent);transform:scale(1.02)}
.plan-badge{
  position:absolute;top:-12px;left:50%;transform:translateX(-50%);
  background:var(--accent);color:var(--paper);padding:.25rem .9rem;
  font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;font-weight:700;border-radius:99px;
}
.plan-name{font-size:.85rem;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--muted);margin-bottom:.6rem}
.plan-price{display:flex;align-items:baseline;gap:.4rem;margin-bottom:.3rem}
.plan-price-value{font-family:var(--font-display);font-size:3rem;font-weight:800;letter-spacing:-.02em;line-height:1}
.plan-price-unit{color:var(--muted);font-size:.95rem;font-weight:500}
.plan-savings{color:var(--accent);font-size:.85rem;font-weight:700;margin-bottom:1.5rem;min-height:1.2em}
.plan-features{list-style:none;padding:0;margin:1.5rem 0;flex:1}
.plan-features li{padding:.7rem 0;border-top:1px solid var(--hairline);display:flex;gap:.7rem;font-size:.92rem;align-items:start}
.plan-features li:last-child{border-bottom:1px solid var(--hairline)}
.plan-features li::before{content:'';flex-shrink:0;width:18px;height:18px;margin-top:1px;border-radius:50%;background:var(--accent);background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'/%3E%3C/svg%3E");background-size:64%;background-position:center;background-repeat:no-repeat}
.plan-cta{display:block;text-align:center;padding:1rem;background:var(--ink);color:var(--paper);border-radius:99px;font-weight:700;letter-spacing:.04em;font-size:.85rem;text-transform:uppercase;transition:background .15s,transform .15s;margin-top:1rem}
.plan-cta:hover{background:var(--accent);transform:translateY(-1px)}
.plan-card.featured .plan-cta{background:var(--accent)}
.plan-card.featured .plan-cta:hover{background:var(--ink)}

@media (max-width:768px){
  .plans{padding:3rem 0}
  .plans-grid{grid-template-columns:1fr}
  .plan-card.featured{transform:none}
}

/* ============ FAQ ============ */
.faq{padding:5rem 0;background:var(--paper)}
.faq-grid{display:grid;grid-template-columns:1fr 1.5fr;gap:4rem}
.faq-grid h2{font-family:var(--font-display);font-weight:700;font-size:clamp(2rem,4vw,2.8rem);line-height:1.1;letter-spacing:-.02em}
.faq-grid em{font-style:italic;color:var(--accent);font-family:var(--font-serif)}
.faq-list{display:flex;flex-direction:column}
details.faq-item{border-bottom:1px solid var(--hairline);padding:1.2rem 0}
details.faq-item summary{cursor:pointer;list-style:none;font-weight:600;font-size:1.02rem;display:flex;justify-content:space-between;align-items:center;gap:1rem}
details.faq-item summary::-webkit-details-marker{display:none}
details.faq-item summary::after{content:'+';font-size:1.4rem;font-weight:300;color:var(--muted);transition:transform .2s}
details.faq-item[open] summary::after{transform:rotate(45deg)}
details.faq-item p{margin-top:1rem;color:var(--subink);line-height:1.7;font-size:.95rem}

@media (max-width:768px){.faq{padding:3rem 0}.faq-grid{grid-template-columns:1fr;gap:2rem}}

/* ============ FOOTER ============ */
footer{background:var(--ink);color:#A9A294;padding:4rem 0 2rem;font-size:.9rem}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:3rem;margin-bottom:3rem}
footer h3{color:#fff;font-size:.85rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:1.2rem;font-weight:700}
footer .logo{color:#fff;font-size:1.4rem;margin-bottom:1rem}
footer .logo::before{border-color:#fff}
footer p{line-height:1.7;margin-bottom:1rem;max-width:380px}
footer ul{list-style:none;padding:0}
footer ul li{margin-bottom:.8rem}
footer ul li a:hover{color:#fff}
.footer-bottom{border-top:1px solid #2A2A2A;padding-top:2rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem;font-size:.8rem}
@media (max-width:768px){.footer-grid{grid-template-columns:1fr;gap:2rem}}

/* ============ MODAL DE LIVRO ============ */
.modal-overlay{
  position:fixed;inset:0;background:rgba(14,14,14,.85);
  display:none;align-items:center;justify-content:center;z-index:1000;
  padding:2rem;backdrop-filter:blur(4px);
}
.modal-overlay.active{display:flex}
.modal{
  background:var(--paper);max-width:760px;width:100%;max-height:90vh;
  border-radius:8px;overflow-y:auto;position:relative;
  display:grid;grid-template-columns:280px 1fr;
}
.modal-close{
  position:absolute;top:1rem;right:1rem;width:36px;height:36px;
  border-radius:50%;background:rgba(0,0,0,.06);color:var(--ink);font-size:1.4rem;line-height:1;
  display:flex;align-items:center;justify-content:center;
}
.modal-cover{
  padding:1.6rem;display:flex;flex-direction:column;justify-content:space-between;
  border-right:1px solid var(--hairline);
}
.modal-cover-vol{font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;font-weight:700;opacity:.8}
.modal-cover-num{font-family:var(--font-display);font-size:6rem;font-weight:800;line-height:1;opacity:.15;margin:.5rem 0}
.modal-cover-cat{font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;font-weight:700;margin-bottom:.4rem}
.modal-cover-title{font-family:var(--font-display);font-weight:700;font-size:1.4rem;line-height:1.05;letter-spacing:-.01em;margin-bottom:.4rem}
.modal-cover-author{font-family:var(--font-serif);font-style:italic;font-size:.9rem;opacity:.7}
.modal-body{padding:2rem 2rem 2rem 2rem;display:flex;flex-direction:column}
.modal-eyebrow{font-weight:700;font-size:.7rem;color:var(--accent);text-transform:uppercase;letter-spacing:.2em;margin-bottom:.6rem}
.modal-title{font-family:var(--font-display);font-weight:700;font-size:1.6rem;line-height:1.1;margin-bottom:.4rem}
.modal-author{font-family:var(--font-serif);font-style:italic;color:var(--muted);margin-bottom:1.5rem}
.modal-tese{padding:1rem 1rem 1rem 1.2rem;border-left:3px solid var(--accent);background:rgba(0,0,0,.02);margin-bottom:1.5rem;font-family:var(--font-serif);font-style:italic;font-size:1rem;line-height:1.5}
.modal-section h4{font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:.7rem;font-weight:700}
.modal-section ul{list-style:none;padding:0;margin-bottom:1.5rem}
.modal-section ul li{padding:.4rem 0;border-bottom:1px dashed var(--hairline);font-size:.92rem;display:flex;gap:.6rem}
.modal-section ul li::before{content:'·';color:var(--accent);font-weight:900}
.modal-cta{margin-top:auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;padding-top:1.5rem;border-top:1px solid var(--hairline)}
.modal-price{font-family:var(--font-display);font-weight:700;font-size:1.6rem;color:var(--accent)}
.modal-buy{padding:1rem 1.6rem;background:var(--ink);color:var(--paper);border-radius:99px;font-weight:700;letter-spacing:.04em;font-size:.85rem;text-transform:uppercase;transition:background .15s;display:inline-flex;align-items:center;gap:.6rem}
.modal-buy:hover{background:var(--accent)}

@media (max-width:768px){
  .modal{grid-template-columns:1fr;max-height:100vh;border-radius:0}
  .modal-cover{border-right:none;border-bottom:1px solid var(--hairline);padding:1.4rem}
}

/* ============ STREAM / TICKER ============ */
.ticker{
  background:var(--ink);color:var(--paper);padding:.9rem 0;overflow:hidden;
  border-top:1px solid #1f1f1f;border-bottom:1px solid #1f1f1f;
}
.ticker-inner{display:flex;gap:3rem;animation:tickerScroll 40s linear infinite;white-space:nowrap}
.ticker-inner span{font-family:var(--font-serif);font-style:italic;font-size:1.05rem;display:inline-flex;align-items:center;gap:1.5rem}
.ticker-inner span::after{content:'✦';color:var(--accent-alt);margin-left:1.5rem}
@keyframes tickerScroll{
  0%{transform:translateX(0)}
  100%{transform:translateX(-50%)}
}
"""


# ─────────────────────────────────────────────────────
# JS
# ─────────────────────────────────────────────────────
JS = """// Galeria — filtros e busca
(function(){
  const grid = document.getElementById('book-grid');
  const cards = grid ? Array.from(grid.querySelectorAll('.book-card')) : [];
  const filterBtns = document.querySelectorAll('.filter-btn');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      cards.forEach(card => {
        const cat = card.dataset.category;
        if (filter === 'all' || cat.toLowerCase().includes(filter.toLowerCase())) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
})();

// Modal de livro
(function(){
  const overlay = document.getElementById('modal-overlay');
  const modal = document.getElementById('modal');
  const closeBtn = document.querySelector('.modal-close');
  const cards = document.querySelectorAll('.book-card');

  const BOOKS = window.LB_BOOKS || {};

  function openBook(vol){
    const book = BOOKS[vol];
    if (!book) return;
    modal.querySelector('.modal-cover').style.background = book.paper;
    modal.querySelector('.modal-cover').style.color = book.ink || '#0E0E0E';
    modal.querySelector('.modal-cover-vol').textContent = 'Vol. ' + book.vol;
    modal.querySelector('.modal-cover-num').textContent = book.vol;
    modal.querySelector('.modal-cover-num').style.color = book.accent + '33';
    modal.querySelector('.modal-cover-cat').textContent = book.category;
    modal.querySelector('.modal-cover-cat').style.color = book.accent;
    modal.querySelector('.modal-cover-title').textContent = book.title;
    modal.querySelector('.modal-cover-author').textContent = book.author;
    modal.querySelector('.modal-eyebrow').textContent = book.category;
    modal.querySelector('.modal-title').textContent = book.title;
    modal.querySelector('.modal-author').textContent = book.author;
    modal.querySelector('.modal-tese').textContent = book.tese;
    const bulletsEl = modal.querySelector('.modal-section ul');
    bulletsEl.innerHTML = book.bullets.map(b => '<li><span>' + b + '</span></li>').join('');
    modal.querySelector('.modal-buy').href = book.cakto;
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeBook(){
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  cards.forEach(card => {
    card.addEventListener('click', () => openBook(card.dataset.vol));
  });
  closeBtn.addEventListener('click', closeBook);
  overlay.addEventListener('click', e => {
    if (e.target === overlay) closeBook();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeBook();
  });
})();

// Smooth reveal on scroll
(function(){
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = 1;
        e.target.style.transform = 'translateY(0)';
        observer.unobserve(e.target);
      }
    });
  }, {threshold: 0.1, rootMargin: '0px 0px -50px 0px'});

  document.querySelectorAll('.book-card, .plan-card, .feature, details.faq-item').forEach(el => {
    el.style.opacity = 0;
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity .6s, transform .6s';
    observer.observe(el);
  });
})();
"""


# ─────────────────────────────────────────────────────
# Geração das categorias para filtros
# ─────────────────────────────────────────────────────
def get_categories():
    """Retorna as 5-6 grandes categorias da coleção."""
    return [
        ("all", "Todos"),
        ("desenvolvimento", "Desenvolvimento pessoal"),
        ("negócios", "Negócios & Finanças"),
        ("filosofia", "Filosofia"),
        ("psicologia", "Psicologia"),
        ("literatura brasileira", "Literatura brasileira"),
        ("literatura", "Literatura mundial"),
    ]


# ─────────────────────────────────────────────────────
# HTML — Landing
# ─────────────────────────────────────────────────────
def render_book_card(book):
    vol, _id, titulo, autor, categoria, tese, quote, pdf = book
    p = BOOK_PALETTES.get(vol, {"paper": "#F5F1E8", "accent": "#1B4D3E"})
    paper = p["paper"]; accent = p["accent"]
    # Definir cor da tinta: se paper for muito escuro (manson vol 3), tinta clara
    is_dark = paper in ("#0E0E0E",)
    ink = "#F6F1E7" if is_dark else "#0E0E0E"
    return f"""
<article class="book-card" data-vol="{vol}" data-category="{categoria}">
  <div class="book-cover" style="background:{paper};color:{ink}">
    <div>
      <div class="book-cover-vol" style="color:{accent}">VOL. {vol}</div>
      <div class="book-cover-num" style="color:{accent}33">{vol}</div>
    </div>
    <div>
      <div class="book-cover-cat" style="color:{accent}">{categoria.split(' · ')[0]}</div>
      <div class="book-cover-title">{titulo}</div>
      <div class="book-cover-author">{autor}</div>
    </div>
  </div>
  <div class="book-info">
    <div class="book-title-row">
      <div class="book-info-title">{titulo}</div>
      <div class="book-info-vol">VOL. {vol}</div>
    </div>
    <div class="book-info-author">{autor}</div>
    <div class="book-price">{price_brl(PRECO_INDIVIDUAL)}</div>
  </div>
</article>"""


def render_landing():
    book_cards = "\n".join(render_book_card(b) for b in BOOKS_META)
    cats = get_categories()
    filter_btns = "\n".join(
        f'    <button class="filter-btn{" active" if cat_id == "all" else ""}" data-filter="{cat_id}">{cat_label}</button>'
        for cat_id, cat_label in cats
    )

    # Dados JS para o modal
    books_data = {}
    for b in BOOKS_META:
        vol, _id, titulo, autor, categoria, tese, quote, pdf = b
        p = BOOK_PALETTES.get(vol, {"paper": "#F5F1E8", "accent": "#1B4D3E"})
        books_data[vol] = {
            "vol": vol,
            "title": titulo,
            "author": autor,
            "category": categoria,
            "tese": tese,
            "quote": quote,
            "paper": p["paper"],
            "accent": p["accent"],
            "ink": "#F6F1E7" if p["paper"] == "#0E0E0E" else "#0E0E0E",
            "cakto": cakto_url(vol),
            "bullets": [
                f"Resumo editorial de 25-39 páginas",
                f"Tese central, capítulos comentados e citações",
                f"Aplicação prática + cronograma de 4 semanas",
                f"Caderno de leitura com espaço para anotações",
                f"PDF em A4, design minimalista moderno",
            ],
        }
    books_json = json.dumps(books_data, ensure_ascii=False)

    # Primeiros 3 livros para o hero
    hero_books = BOOKS_META[:3]
    hero_covers = ""
    for b in hero_books:
        vol, _id, titulo, autor, _cat, _tese, _q, _pdf = b
        p = BOOK_PALETTES.get(vol)
        ink = "#F6F1E7" if p["paper"] == "#0E0E0E" else "#0E0E0E"
        hero_covers += f"""
    <div class="cover-card" style="background:{p['paper']};color:{ink}">
      <div>
        <div class="cover-vol" style="color:{p['accent']}">VOL. {vol}</div>
        <div class="cover-num" style="color:{p['accent']}22">{vol}</div>
      </div>
      <div>
        <div class="cover-title">{titulo}</div>
        <div class="cover-author">{autor}</div>
      </div>
    </div>"""

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Leitura Breve — 38 bestsellers em resumos editoriais</title>
<meta name="description" content="38 resumos editoriais de bestsellers (Hábitos Atômicos, O Alquimista, 1984, Cem Anos de Solidão e mais). PDFs com tese, capítulos comentados, citações e caderno de leitura.">
<meta property="og:title" content="Leitura Breve — Coleção de 38 resumos editoriais">
<meta property="og:description" content="Os bestsellers que mais venderam no Brasil em resumos editoriais de 25 a 39 páginas.">
<link rel="icon" href="data:image/svg+xml,&lt;svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'&gt;&lt;circle cx='50' cy='50' r='44' fill='none' stroke='%231B4D3E' stroke-width='6'/&gt;&lt;circle cx='50' cy='50' r='10' fill='%231B4D3E'/&gt;&lt;/svg&gt;">
<link rel="stylesheet" href="styles.css">
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <a href="#" class="logo">Leitura Breve</a>
    <div class="nav-links">
      <a href="#sobre">Sobre</a>
      <a href="#galeria">Coleção</a>
      <a href="#planos">Assinatura</a>
      <a href="#faq">FAQ</a>
    </div>
    <a href="#planos" class="nav-cta">Assinar</a>
  </div>
</nav>

<header class="hero">
  <div class="wrap hero-grid">
    <div>
      <div class="hero-eyebrow">38 volumes · Coleção 2026</div>
      <h1 class="hero-title">Os bestsellers,<br><em>em uma sessão</em><br>de leitura.</h1>
      <p class="hero-sub">Resumos editoriais de 25 a 39 páginas dos livros que mais venderam no Brasil. Tese central, capítulos comentados, citações em destaque e caderno de leitura — em PDF minimalista.</p>
      <div class="hero-ctas">
        <a href="#planos" class="btn-primary">Assinar coleção →</a>
        <a href="#galeria" class="btn-secondary">Ver os 38 livros</a>
      </div>
      <div class="hero-stats">
        <div><div class="stat-num">38</div><div class="stat-label">Volumes lançados</div></div>
        <div><div class="stat-num">980+</div><div class="stat-label">Páginas editoriais</div></div>
        <div><div class="stat-num">7</div><div class="stat-label">Categorias</div></div>
      </div>
    </div>
    <div class="hero-cover">
      <div class="cover-stack">{hero_covers}
      </div>
    </div>
  </div>
</header>

<div class="ticker">
  <div class="ticker-inner">
    <span>Hábitos Atômicos</span><span>O Alquimista</span><span>A Sutil Arte</span>
    <span>O Poder do Hábito</span><span>Mindset</span><span>Pai Rico, Pai Pobre</span>
    <span>Os 7 Hábitos</span><span>Sapiens</span><span>1984</span>
    <span>Dom Casmurro</span><span>O Pequeno Príncipe</span><span>Cem Anos de Solidão</span>
    <span>Hábitos Atômicos</span><span>O Alquimista</span><span>A Sutil Arte</span>
    <span>O Poder do Hábito</span><span>Mindset</span><span>Pai Rico, Pai Pobre</span>
    <span>Os 7 Hábitos</span><span>Sapiens</span><span>1984</span>
    <span>Dom Casmurro</span><span>O Pequeno Príncipe</span><span>Cem Anos de Solidão</span>
  </div>
</div>

<section class="about" id="sobre">
  <div class="wrap about-grid">
    <div>
      <div class="about-eyebrow">A coleção</div>
      <h2>Para quem lê com pouco tempo<br>e não quer perder o <em>essencial</em>.</h2>
      <p>A <em>Leitura Breve</em> reúne 38 dos bestsellers mais influentes do Brasil em resumos editoriais autorais. Cada volume foi pensado para ser <em>lido em uma única sessão</em>, e ao mesmo tempo servir como caderno de estudo permanente.</p>
      <p>Não são fichamentos secos. São documentos editoriais com identidade visual própria — paleta, tipografia e símbolo distintos por livro — que cabem tanto na sua estante quanto no seu tablet.</p>
    </div>
    <div>
      <div class="about-features">
        <div class="feature">
          <div class="feature-mark">1</div>
          <div><h3>Tese em uma página</h3><p>A ideia central destacada antes dos detalhes.</p></div>
        </div>
        <div class="feature">
          <div class="feature-mark">2</div>
          <div><h3>Capítulos comentados</h3><p>Pontos-chave, callouts e quotes em destaque.</p></div>
        </div>
        <div class="feature">
          <div class="feature-mark">3</div>
          <div><h3>Aplicação prática</h3><p>Cronograma de 4 semanas para implantar.</p></div>
        </div>
        <div class="feature">
          <div class="feature-mark">4</div>
          <div><h3>Caderno de leitura</h3><p>Espaço para anotações e provocações pessoais.</p></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="gallery" id="galeria">
  <div class="wrap">
    <div class="section-head">
      <div class="left">
        <div class="section-eyebrow">A coleção completa</div>
        <h2>Os 38 <em>volumes</em>.</h2>
      </div>
    </div>
    <div class="filters">
{filter_btns}
    </div>
    <div class="book-grid" id="book-grid">
{book_cards}
    </div>
  </div>
</section>

<section class="plans" id="planos">
  <div class="wrap">
    <div class="plans-head">
      <div class="section-eyebrow">Assinatura</div>
      <h2>Acesso completo aos <em>38 volumes</em>.</h2>
      <p>Ou compre individualmente por {price_brl(PRECO_INDIVIDUAL)}. Quem assina, ganha também os próximos lançamentos.</p>
    </div>
    <div class="plans-grid">

      <div class="plan-card">
        <div class="plan-name">Mensal</div>
        <div class="plan-price">
          <span class="plan-price-value">{price_brl(PRECO_ASSINATURA_MENSAL)}</span>
          <span class="plan-price-unit">/ mês</span>
        </div>
        <div class="plan-savings">Ideal para experimentar</div>
        <ul class="plan-features">
          <li><span>Acesso imediato aos 38 volumes em PDF</span></li>
          <li><span>Novos volumes incluídos durante a assinatura</span></li>
          <li><span>Catálogo navegável com índice completo</span></li>
          <li><span>Cancele a qualquer momento, sem multa</span></li>
        </ul>
        <a href="{CAKTO_SUB_MENSAL}" class="plan-cta">Começar agora →</a>
      </div>

      <div class="plan-card featured">
        <div class="plan-badge">37% off</div>
        <div class="plan-name">Anual</div>
        <div class="plan-price">
          <span class="plan-price-value">{price_brl(PRECO_ASSINATURA_ANUAL)}</span>
          <span class="plan-price-unit">/ ano</span>
        </div>
        <div class="plan-savings">≈ {price_brl(PRECO_ASSINATURA_ANUAL // 12)}/mês</div>
        <ul class="plan-features">
          <li><span>Acesso imediato aos 38 volumes em PDF</span></li>
          <li><span>Novos volumes incluídos durante o ano</span></li>
          <li><span>Catálogo navegável com índice completo</span></li>
          <li><span>Versões revisadas dos volumes existentes</span></li>
          <li><span>37% de economia em relação à mensal</span></li>
        </ul>
        <a href="{CAKTO_SUB_ANUAL}" class="plan-cta">Assinar 1 ano →</a>
      </div>

    </div>
  </div>
</section>

<section class="faq" id="faq">
  <div class="wrap faq-grid">
    <div>
      <h2>Perguntas <em>frequentes</em>.</h2>
    </div>
    <div class="faq-list">
      <details class="faq-item">
        <summary>O que vem no PDF de cada volume?</summary>
        <p>Cada volume traz: ficha técnica, sumário, sobre o autor, tese central em uma página, capítulos comentados com pontos-chave e citações, insights, aplicação prática, cronograma de 4 semanas, provocações pessoais e caderno de leitura com espaço para anotação.</p>
      </details>
      <details class="faq-item">
        <summary>É o livro inteiro?</summary>
        <p>Não. São <strong>resumos editoriais autorais</strong> em PDF (25 a 39 páginas), feitos para você entender a essência do livro em uma sessão de leitura. Para o texto integral, recomendamos comprar o livro do autor.</p>
      </details>
      <details class="faq-item">
        <summary>Em quanto tempo recebo após pagar?</summary>
        <p>Imediato. Após confirmação do pagamento na Cakto, você recebe link de download ou acesso à área de membros (no caso da assinatura).</p>
      </details>
      <details class="faq-item">
        <summary>Funciona em celular?</summary>
        <p>Sim. PDF padrão A4 abre em qualquer leitor (iBooks, Adobe, Drive). Design otimizado para leitura digital e impressão doméstica.</p>
      </details>
      <details class="faq-item">
        <summary>Posso pedir reembolso?</summary>
        <p>Sim, em até 7 dias após a compra, conforme o Código de Defesa do Consumidor.</p>
      </details>
      <details class="faq-item">
        <summary>Como funciona a assinatura?</summary>
        <p>Você ganha acesso aos 38 volumes existentes + todos os próximos lançamentos enquanto a assinatura estiver ativa. Cancele quando quiser, sem multa. A renovação é automática (mensal ou anual).</p>
      </details>
      <details class="faq-item">
        <summary>Que livros vocês resumem?</summary>
        <p>Bestsellers brasileiros e mundiais nas áreas de desenvolvimento pessoal, negócios, filosofia, psicologia, literatura brasileira e literatura mundial. Veja a lista completa na <a href="#galeria" style="color:var(--accent);text-decoration:underline">galeria</a>.</p>
      </details>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="logo">Leitura Breve</div>
        <p>Resumos editoriais autorais dos bestsellers que mais venderam no Brasil. 38 volumes para uma sessão de leitura inteligente.</p>
      </div>
      <div>
        <h3>Coleção</h3>
        <ul>
          <li><a href="#galeria">Os 38 livros</a></li>
          <li><a href="#planos">Assinatura</a></li>
          <li><a href="#sobre">Sobre</a></li>
          <li><a href="#faq">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h3>Contato</h3>
        <ul>
          <li><a href="mailto:contato@leiturabreve.com.br">contato@leiturabreve.com.br</a></li>
          <li><a href="#">Termos de uso</a></li>
          <li><a href="#">Política de privacidade</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>© 2026 Leitura Breve. Todos os direitos reservados.</div>
      <div>Pagamento processado por Cakto</div>
    </div>
  </div>
</footer>

<!-- Modal -->
<div class="modal-overlay" id="modal-overlay">
  <div class="modal" id="modal">
    <button class="modal-close" aria-label="Fechar">×</button>
    <div class="modal-cover">
      <div>
        <div class="modal-cover-vol"></div>
        <div class="modal-cover-num"></div>
      </div>
      <div>
        <div class="modal-cover-cat"></div>
        <div class="modal-cover-title"></div>
        <div class="modal-cover-author"></div>
      </div>
    </div>
    <div class="modal-body">
      <div class="modal-eyebrow"></div>
      <div class="modal-title"></div>
      <div class="modal-author"></div>
      <div class="modal-tese"></div>
      <div class="modal-section">
        <h4>O que vem no volume</h4>
        <ul></ul>
      </div>
      <div class="modal-cta">
        <div class="modal-price">{price_brl(PRECO_INDIVIDUAL)}</div>
        <a class="modal-buy" href="#" target="_blank">Comprar via Cakto →</a>
      </div>
    </div>
  </div>
</div>

<script>window.LB_BOOKS = {books_json};</script>
<script src="app.js"></script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────
def build():
    landing = render_landing()
    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(landing)
    with open(os.path.join(SITE_DIR, "styles.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(SITE_DIR, "app.js"), "w", encoding="utf-8") as f:
        f.write(JS)
    print(f"Site gerado em {SITE_DIR}/")
    print(f"  - index.html ({len(landing)//1024} KB)")
    print(f"  - styles.css ({len(CSS)//1024} KB)")
    print(f"  - app.js     ({len(JS)//1024} KB)")
    print()
    print("Para visualizar localmente:")
    print(f"  cd {SITE_DIR} && python3 -m http.server 8000")


if __name__ == "__main__":
    build()
