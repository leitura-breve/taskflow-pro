"""
Gerador unificado — Vols. 04–18 (resumos minimalistas dos próximos 15 bestsellers)
+ Catálogo com todos os 18 volumes.

Cada livro: ~25-32 páginas. Tipografia simples mas com identidade visual própria
via paleta + símbolo. Reaproveita o esqueleto editorial da série.
"""

import os, math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, Table, TableStyle, NextPageTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.flowables import Flowable

OUT_DIR = "/home/user/taskflow-pro"

# ─── Patch setCharSpace para Canvas ────────────────────
_orig_drawString = Canvas.drawString
_orig_drawRightString = Canvas.drawRightString
_orig_drawCentredString = Canvas.drawCentredString
def _set_char_space(self, v): self.__rt_char_space = v
def _draw_with_space(self, x, y, text, _orig, align="left"):
    cs = getattr(self, "_Canvas__rt_char_space", 0)
    if not cs: return _orig(self, x, y, text)
    t = self.beginText(); t.setFont(self._fontname, self._fontsize)
    if hasattr(self, "_fillColorObj") and self._fillColorObj is not None:
        t.setFillColor(self._fillColorObj)
    t.setCharSpace(cs)
    from reportlab.pdfbase.pdfmetrics import stringWidth
    w = stringWidth(text, self._fontname, self._fontsize) + cs * max(0, len(text)-1)
    if align == "right":  t.setTextOrigin(x - w, y)
    elif align == "center": t.setTextOrigin(x - w/2.0, y)
    else: t.setTextOrigin(x, y)
    t.textOut(text); self.drawText(t)
Canvas.setCharSpace = _set_char_space
Canvas.drawString = lambda self, x, y, text: _draw_with_space(self, x, y, text, _orig_drawString, "left")
Canvas.drawRightString = lambda self, x, y, text: _draw_with_space(self, x, y, text, _orig_drawRightString, "right")
Canvas.drawCentredString = lambda self, x, y, text: _draw_with_space(self, x, y, text, _orig_drawCentredString, "center")

PAGE_W, PAGE_H = A4
MARGIN_L = 2.4*cm
MARGIN_R = 2.4*cm
MARGIN_T = 2.6*cm
MARGIN_B = 2.4*cm


# ═══════════════════════════════════════════════════════
# FLOWABLES (reusados em todos os livros)
# ═══════════════════════════════════════════════════════

class HLine(Flowable):
    def __init__(self, width, thickness=0.4, color=None, space_after=0):
        Flowable.__init__(self)
        self.width = width; self.thickness = thickness
        self.color = color; self.space_after = space_after
        self.height = thickness + space_after
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.space_after, self.width, self.space_after)


class BigNumber(Flowable):
    def __init__(self, width, number, kicker=None, color=None, font="Helvetica-Bold"):
        Flowable.__init__(self)
        self.width = width; self.number = str(number)
        self.kicker = kicker; self.color = color; self.font = font
        self.height = 2.6*cm
    def draw(self):
        c = self.canv
        c.setFont(self.font, 72); c.setFillColor(self.color)
        c.setCharSpace(-3); c.drawString(0, 0.3*cm, self.number); c.setCharSpace(0)
        from reportlab.pdfbase.pdfmetrics import stringWidth
        w = stringWidth(self.number, self.font, 72)
        x_line = w + 0.55*cm
        c.setStrokeColor(self.color)
        c.setLineWidth(0.4)
        c.line(x_line, 0.3*cm, x_line, 2.4*cm)
        if self.kicker:
            c.setFont("Helvetica-Bold", 8); c.setFillColor(self.color)
            c.setCharSpace(2); c.drawString(x_line + 0.35*cm, 2.15*cm, self.kicker.upper())
            c.setCharSpace(0)


class Callout(Flowable):
    """Callout com barra lateral acentuada."""
    def __init__(self, width, text, label, accent, ink, padding=0.5*cm):
        Flowable.__init__(self)
        self.width = width; self.text = text; self.label = label
        self.accent = accent; self.ink = ink; self.padding = padding
        from reportlab.pdfbase.pdfmetrics import stringWidth
        avail = width - 2*padding - 0.3*cm
        words = text.split(); line = ""; lines = 1
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, "Helvetica", 10) <= avail: line = test
            else: lines += 1; line = w
        self.height = lines * 10 * 1.45 + 2*padding

    def _wrap(self, text, w, font, size):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        out = []; line = ""
        for word in text.split():
            test = (line + " " + word).strip()
            if stringWidth(test, font, size) <= w: line = test
            else: out.append(line); line = word
        if line: out.append(line)
        return out

    def draw(self):
        c = self.canv; h = self.height
        c.setFillColor(self.accent)
        c.rect(0, 0, 0.12*cm, h, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5); c.setFillColor(self.accent)
        c.setCharSpace(1.6)
        c.drawString(self.padding + 0.15*cm, h - self.padding + 0.05*cm, self.label.upper())
        c.setCharSpace(0)
        c.setFont("Helvetica", 10); c.setFillColor(self.ink)
        lines = self._wrap(self.text, self.width - 2*self.padding - 0.3*cm, "Helvetica", 10)
        y = h - self.padding - 0.5*cm
        for ln in lines:
            c.drawString(self.padding + 0.15*cm, y, ln)
            y -= 10 * 1.45


class PullQuote(Flowable):
    """Pull quote com aspas serif decorativas + texto serif italico."""
    def __init__(self, width, text, attribution, accent, ink, muted, size=14):
        Flowable.__init__(self)
        self.width = width; self.text = text
        self.attribution = attribution; self.accent = accent
        self.ink = ink; self.muted = muted; self.size = size
        from reportlab.pdfbase.pdfmetrics import stringWidth
        avail = width * 0.85
        words = text.split(); line = ""; lines = 1
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, "Times-Italic", size) <= avail: line = test
            else: lines += 1; line = w
        self.height = lines * size * 1.3 + (0.55*cm if attribution else 0) + 0.7*cm

    def _wrap(self, text, w, font, size):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        out = []; line = ""
        for word in text.split():
            test = (line + " " + word).strip()
            if stringWidth(test, font, size) <= w: line = test
            else: out.append(line); line = word
        if line: out.append(line)
        return out

    def draw(self):
        c = self.canv
        c.setFont("Times-Bold", 40); c.setFillColor(self.accent)
        c.drawString(0, self.height - 1.0*cm, "“")
        c.setFont("Times-Italic", self.size); c.setFillColor(self.ink)
        lines = self._wrap(self.text, self.width * 0.85, "Times-Italic", self.size)
        y = self.height - 0.9*cm
        for ln in lines:
            c.drawString(0.95*cm, y, ln); y -= self.size * 1.3
        if self.attribution:
            c.setFont("Helvetica-Bold", 8); c.setFillColor(self.muted)
            c.setCharSpace(1.5); c.drawString(0.95*cm, y - 0.15*cm, self.attribution.upper())
            c.setCharSpace(0)


class CenteredQuote(Flowable):
    def __init__(self, width, text, attribution=None, size=14, color=None, muted=None):
        Flowable.__init__(self)
        self.width = width; self.text = text; self.attribution = attribution
        self.size = size; self.color = color; self.muted = muted
        from reportlab.pdfbase.pdfmetrics import stringWidth
        avail = width * 0.9
        words = text.split(); line = ""; lines = 1
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, "Times-Italic", size) <= avail: line = test
            else: lines += 1; line = w
        self.height = lines * size * 1.3 + (0.55*cm if attribution else 0) + 0.4*cm

    def _wrap(self, text, w, font, size):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        out = []; line = ""
        for word in text.split():
            test = (line + " " + word).strip()
            if stringWidth(test, font, size) <= w: line = test
            else: out.append(line); line = word
        if line: out.append(line)
        return out

    def draw(self):
        c = self.canv
        c.setFont("Times-Italic", self.size); c.setFillColor(self.color)
        lines = self._wrap(self.text, self.width * 0.9, "Times-Italic", self.size)
        y = self.height - self.size
        for ln in lines:
            c.drawCentredString(self.width/2, y, ln); y -= self.size * 1.3
        if self.attribution:
            c.setFont("Helvetica-Bold", 7.5); c.setFillColor(self.muted)
            c.setCharSpace(2); c.drawCentredString(self.width/2, y - 0.2*cm, self.attribution.upper())
            c.setCharSpace(0)


class NumberedLines(Flowable):
    def __init__(self, width, num_lines=6, line_spacing=0.78*cm, color=None, label=None, muted=None):
        Flowable.__init__(self)
        self.width = width; self.num_lines = num_lines
        self.line_spacing = line_spacing; self.color = color
        self.label = label; self.muted = muted
        extra = 0.8*cm if label else 0
        self.height = num_lines * line_spacing + extra + 0.2*cm
    def draw(self):
        c = self.canv; y_top = self.height
        if self.label:
            c.setFont("Helvetica-Bold", 7.5); c.setFillColor(self.muted or self.color)
            c.setCharSpace(1.4); c.drawString(0, y_top - 0.35*cm, self.label.upper())
            c.setCharSpace(0); y_top -= 0.85*cm
        c.setStrokeColor(self.color); c.setLineWidth(0.3)
        for i in range(self.num_lines):
            yy = y_top - (i+1) * self.line_spacing
            c.setFont("Helvetica", 7); c.setFillColor(self.muted or self.color)
            c.drawString(0, yy + 0.08*cm, f"{i+1:02d}")
            c.setStrokeColor(self.color)
            c.line(0.7*cm, yy, self.width, yy)


class CoverMotif(Flowable):
    """Símbolo da capa — varia conforme `motif`."""
    def __init__(self, width, height, motif, accent, secondary=None):
        Flowable.__init__(self); self.width = width; self.height = height
        self.motif = motif; self.accent = accent
        self.secondary = secondary or accent
    def draw(self):
        c = self.canv
        cx = self.width/2; cy = self.height/2
        r = min(self.width, self.height) * 0.42
        c.setStrokeColor(self.accent); c.setLineWidth(0.6)
        c.setFillColor(self.accent)
        m = self.motif
        if m == "loop":
            # círculo com flecha (loop do hábito)
            c.circle(cx, cy, r, stroke=1, fill=0)
            c.circle(cx, cy, r*0.6, stroke=1, fill=0)
            # ponta da flecha
            c.line(cx + r*math.cos(math.radians(30)), cy + r*math.sin(math.radians(30)),
                   cx + r*math.cos(math.radians(60)), cy + r*math.sin(math.radians(60)))
        elif m == "arrows":
            # duas flechas opostas (mindset fixo × crescimento)
            c.setLineWidth(1.2)
            c.line(cx - r*0.8, cy + r*0.3, cx + r*0.8, cy + r*0.3)
            c.line(cx + r*0.8, cy + r*0.3, cx + r*0.5, cy + r*0.5)
            c.line(cx + r*0.8, cy + r*0.3, cx + r*0.5, cy + r*0.1)
            c.line(cx + r*0.8, cy - r*0.3, cx - r*0.8, cy - r*0.3)
            c.line(cx - r*0.8, cy - r*0.3, cx - r*0.5, cy - r*0.5)
            c.line(cx - r*0.8, cy - r*0.3, cx - r*0.5, cy - r*0.1)
        elif m == "sunrise":
            # semi-círculo + raios (sol nascente)
            c.arc(cx - r, cy - r*0.3, cx + r, cy + r*1.5, startAng=0, extent=180)
            c.line(cx - r*1.4, cy - r*0.3, cx + r*1.4, cy - r*0.3)
            for ang in (30, 60, 90, 120, 150):
                rad = math.radians(ang)
                x1 = cx + r*1.1*math.cos(rad); y1 = cy - r*0.3 + r*1.1*math.sin(rad)
                x2 = cx + r*1.35*math.cos(rad); y2 = cy - r*0.3 + r*1.35*math.sin(rad)
                c.line(x1, y1, x2, y2)
        elif m == "coin":
            c.circle(cx, cy, r, stroke=1, fill=0)
            c.circle(cx, cy, r*0.85, stroke=1, fill=0)
            c.setFont("Helvetica-Bold", 34); c.setFillColor(self.accent)
            c.drawCentredString(cx, cy - 12, "$")
        elif m == "seven":
            c.circle(cx, cy, r, stroke=1, fill=0)
            c.setFont("Helvetica-Bold", 60); c.setFillColor(self.accent)
            c.drawCentredString(cx, cy - 22, "7")
        elif m == "handshake":
            # duas formas que se encontram (estilizadas)
            c.setLineWidth(1.4)
            c.line(cx - r*0.9, cy, cx, cy)
            c.line(cx + r*0.9, cy, cx, cy)
            c.circle(cx - r*0.9, cy, 0.2*cm, stroke=0, fill=1)
            c.circle(cx + r*0.9, cy, 0.2*cm, stroke=0, fill=1)
            c.circle(cx, cy, 0.3*cm, stroke=1, fill=0)
        elif m == "column":
            # coluna babilônica simples
            c.setLineWidth(1.2)
            c.rect(cx - r*0.3, cy - r*0.8, r*0.6, r*1.6, stroke=1, fill=0)
            c.line(cx - r*0.5, cy + r*0.8, cx + r*0.5, cy + r*0.8)
            c.line(cx - r*0.5, cy - r*0.8, cx + r*0.5, cy - r*0.8)
            for i in range(5):
                yy = cy - r*0.7 + i * r*0.35
                c.line(cx - r*0.3, yy, cx + r*0.3, yy)
        elif m == "mountain":
            c.setLineWidth(1.0)
            c.line(cx - r, cy - r*0.5, cx - r*0.2, cy + r*0.5)
            c.line(cx - r*0.2, cy + r*0.5, cx + r*0.2, cy)
            c.line(cx + r*0.2, cy, cx + r, cy + r*0.7)
            c.line(cx + r, cy + r*0.7, cx + r*1.1, cy - r*0.5)
            c.line(cx - r, cy - r*0.5, cx + r*1.1, cy - r*0.5)
        elif m == "heartbrain":
            # coração estilizado dentro de um círculo (emoção + razão)
            c.circle(cx, cy, r, stroke=1, fill=0)
            c.setLineWidth(1.6)
            # forma de coração simplificada
            c.bezier(cx, cy - r*0.5,
                     cx - r*0.7, cy,
                     cx - r*0.6, cy + r*0.5,
                     cx, cy + r*0.2)
            c.bezier(cx, cy + r*0.2,
                     cx + r*0.6, cy + r*0.5,
                     cx + r*0.7, cy,
                     cx, cy - r*0.5)
        elif m == "hourglass":
            c.setLineWidth(1.2)
            c.line(cx - r*0.7, cy + r, cx + r*0.7, cy + r)
            c.line(cx - r*0.7, cy - r, cx + r*0.7, cy - r)
            c.line(cx - r*0.7, cy + r, cx + r*0.7, cy - r)
            c.line(cx + r*0.7, cy + r, cx - r*0.7, cy - r)
        elif m == "clock4":
            c.circle(cx, cy, r, stroke=1, fill=0)
            c.setLineWidth(1.2)
            # ponteiros para 4h
            c.line(cx, cy, cx, cy + r*0.6)  # 12h
            c.line(cx, cy, cx + r*0.55, cy - r*0.4)  # 4h
            c.circle(cx, cy, 0.12*cm, stroke=0, fill=1)
        elif m == "diamond":
            c.setLineWidth(1.0)
            c.line(cx, cy + r, cx + r*0.7, cy)
            c.line(cx + r*0.7, cy, cx, cy - r)
            c.line(cx, cy - r, cx - r*0.7, cy)
            c.line(cx - r*0.7, cy, cx, cy + r)
            c.line(cx, cy + r, cx, cy - r)
            c.line(cx - r*0.7, cy, cx + r*0.7, cy)
        elif m == "quill":
            # pena
            c.setLineWidth(1.0)
            c.line(cx - r*0.6, cy - r*0.6, cx + r*0.6, cy + r*0.6)
            c.bezier(cx + r*0.6, cy + r*0.6,
                     cx + r*0.2, cy + r*0.8,
                     cx - r*0.3, cy + r*0.4,
                     cx - r*0.6, cy - r*0.6)
        elif m == "wave":
            c.setLineWidth(1.0)
            n = 30
            for i in range(n-1):
                x1 = cx - r + (2*r) * i/n
                y1 = cy + r*0.4 * math.sin(i * math.pi * 2 / 6)
                x2 = cx - r + (2*r) * (i+1)/n
                y2 = cy + r*0.4 * math.sin((i+1) * math.pi * 2 / 6)
                c.line(x1, y1, x2, y2)
            # mais uma onda
            for i in range(n-1):
                x1 = cx - r + (2*r) * i/n
                y1 = cy - r*0.4 + r*0.3 * math.sin(i * math.pi * 2 / 4)
                x2 = cx - r + (2*r) * (i+1)/n
                y2 = cy - r*0.4 + r*0.3 * math.sin((i+1) * math.pi * 2 / 4)
                c.line(x1, y1, x2, y2)
        elif m == "star":
            # estrela
            pts = []
            for i in range(10):
                ang = math.radians(-90 + i * 36)
                rr = r if i % 2 == 0 else r * 0.45
                pts.append((cx + rr*math.cos(ang), cy + rr*math.sin(ang)))
            p = c.beginPath()
            p.moveTo(*pts[0])
            for pt in pts[1:]: p.lineTo(*pt)
            p.close()
            c.setFillColor(self.accent)
            c.drawPath(p, stroke=0, fill=1)
        elif m == "triangle":
            c.setLineWidth(1.2)
            c.line(cx - r, cy - r*0.6, cx + r, cy - r*0.6)
            c.line(cx - r, cy - r*0.6, cx, cy + r)
            c.line(cx + r, cy - r*0.6, cx, cy + r)
        else:
            # default: círculo simples
            c.circle(cx, cy, r, stroke=1, fill=0)
            c.circle(cx, cy, 0.18*cm, stroke=0, fill=1)


# ═══════════════════════════════════════════════════════
# DESENHO DAS PÁGINAS (parametrizado pela paleta)
# ═══════════════════════════════════════════════════════

def make_cover_drawer(cfg):
    P = cfg["palette"]
    paper = HexColor(P["paper"]); ink = HexColor(P["ink"])
    accent = HexColor(P["accent"]); muted = HexColor(P["muted"])
    paper_dark = HexColor(P.get("paper_dark", _darken(P["paper"], 0.08)))

    def _draw(c, doc):
        c.setFillColor(paper); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        # rule topo
        c.setStrokeColor(ink); c.setLineWidth(0.7)
        c.line(MARGIN_L, PAGE_H - 1.6*cm, PAGE_W - MARGIN_L, PAGE_H - 1.6*cm)
        # marca
        c.setFont("Helvetica-Bold", 8); c.setFillColor(ink)
        c.setCharSpace(3); c.drawString(MARGIN_L, PAGE_H - 1.25*cm, f"RESUMO · VOL. {cfg['vol']}")
        c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.25*cm, "ED. MAIO 2026"); c.setCharSpace(0)
        # numeral gigante
        c.setFont(cfg.get("title_font", "Helvetica-Bold"), 230); c.setFillColor(paper_dark)
        c.setCharSpace(-8)
        c.drawString(MARGIN_L - 0.3*cm, PAGE_H - 11*cm, cfg["vol"]); c.setCharSpace(0)
        # categoria
        c.setFont("Helvetica-Bold", 9); c.setFillColor(accent)
        c.setCharSpace(2.2); c.drawString(MARGIN_L, PAGE_H - 12.3*cm, cfg["category_kicker"].upper())
        c.setCharSpace(0)
        # título display
        c.setFont(cfg.get("title_font", "Helvetica-Bold"), 60); c.setFillColor(ink)
        c.drawString(MARGIN_L, PAGE_H - 14.5*cm, cfg["title_main"])
        c.drawString(MARGIN_L, PAGE_H - 16.5*cm, cfg["title_sub"])
        # subtítulo serif italic
        c.setFont("Times-Italic", 13); c.setFillColor(HexColor(P.get("subink", P["ink"])))
        c.drawString(MARGIN_L, PAGE_H - 17.6*cm, cfg["subtitle"])
        # regra acento
        c.setStrokeColor(accent); c.setLineWidth(1.4)
        c.line(MARGIN_L, PAGE_H - 18.4*cm, MARGIN_L + 2.5*cm, PAGE_H - 18.4*cm)
        # autor
        c.setFont("Helvetica-Bold", 8); c.setFillColor(muted)
        c.setCharSpace(2); c.drawString(MARGIN_L, PAGE_H - 19.0*cm, "AUTOR ORIGINAL"); c.setCharSpace(0)
        c.setFont("Helvetica-Bold", 13); c.setFillColor(ink)
        c.drawString(MARGIN_L, PAGE_H - 19.7*cm, cfg["author"])
        # motivo
        cx, cy = PAGE_W - 5.5*cm, 7*cm
        save = c.saveState
        c.saveState()
        c.translate(cx, cy)
        motif_f = CoverMotif(5*cm, 5*cm, cfg.get("motif", "default"), accent)
        c.translate(-2.5*cm, -2.5*cm)
        motif_f.canv = c
        motif_f.draw()
        c.restoreState()
        # rodapé
        c.setStrokeColor(ink); c.setLineWidth(0.5)
        c.line(MARGIN_L, 2.3*cm, PAGE_W - MARGIN_R, 2.3*cm)
        c.setFont("Helvetica-Bold", 7.5); c.setFillColor(muted); c.setCharSpace(2.5)
        c.drawString(MARGIN_L, 1.7*cm, "CADERNO DE LEITURA  ·  COLEÇÃO LEITURA BREVE")
        c.drawRightString(PAGE_W - MARGIN_R, 1.7*cm, "FORMATO A4"); c.setCharSpace(0)
    return _draw


def make_body_drawer(cfg):
    P = cfg["palette"]
    paper = HexColor(P["paper"]); ink = HexColor(P["ink"])
    accent = HexColor(P["accent"]); muted = HexColor(P["muted"])
    hairline = HexColor(P["hairline"])
    def _draw(c, doc):
        c.setFillColor(paper); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5); c.setFillColor(muted); c.setCharSpace(2.5)
        c.drawString(MARGIN_L, PAGE_H - 1.3*cm, cfg["short_title"].upper())
        c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.3*cm, f"{cfg['author'].upper()}  ·  RESUMO {cfg['vol']}")
        c.setCharSpace(0)
        c.setStrokeColor(hairline); c.setLineWidth(0.3)
        c.line(MARGIN_L, PAGE_H - 1.55*cm, PAGE_W - MARGIN_R, PAGE_H - 1.55*cm)
        # footer
        page_num = c.getPageNumber()
        c.setStrokeColor(hairline); c.setLineWidth(0.3)
        c.line(MARGIN_L, 1.7*cm, PAGE_W - MARGIN_R, 1.7*cm)
        c.setFont("Helvetica-Bold", 7.5); c.setFillColor(muted); c.setCharSpace(2.5)
        c.drawString(MARGIN_L, 1.3*cm, "RESUMO · LEITURA BREVE"); c.setCharSpace(0)
        c.setFillColor(accent); c.circle(PAGE_W - MARGIN_R - 1.2*cm, 1.4*cm, 0.08*cm, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 11); c.setFillColor(ink)
        c.drawRightString(PAGE_W - MARGIN_R, 1.25*cm, f"{page_num:02d}")
    return _draw


def _darken(hex_color, factor):
    h = hex_color.lstrip("#")
    r = int(h[0:2], 16); g = int(h[2:4], 16); b = int(h[4:6], 16)
    r = max(0, int(r * (1 - factor))); g = max(0, int(g * (1 - factor))); b = max(0, int(b * (1 - factor)))
    return f"#{r:02x}{g:02x}{b:02x}"


# ═══════════════════════════════════════════════════════
# BUILD UM LIVRO
# ═══════════════════════════════════════════════════════

def build_book(cfg):
    P = cfg["palette"]
    paper = HexColor(P["paper"]); ink = HexColor(P["ink"])
    accent = HexColor(P["accent"]); muted = HexColor(P["muted"])
    subink = HexColor(P.get("subink", P["ink"]))
    hairline = HexColor(P["hairline"])

    output = os.path.join(OUT_DIR, f"Vol_{cfg['vol']}_{cfg['id']}.pdf")
    doc = BaseDocTemplate(
        output, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title=f"{cfg['title_main']} {cfg['title_sub']} — Resumo",
        author=f"Resumo da obra de {cfg['author']}",
    )

    fw = PAGE_W - MARGIN_L - MARGIN_R
    fh = PAGE_H - MARGIN_T - MARGIN_B
    cover_frame = Frame(MARGIN_L, MARGIN_B, fw, fh, id="cover", showBoundary=0)
    body_frame  = Frame(MARGIN_L, MARGIN_B, fw, fh - 0.4*cm, id="body", showBoundary=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=make_cover_drawer(cfg)),
        PageTemplate(id="body",  frames=[body_frame],  onPage=make_body_drawer(cfg)),
    ])

    title_font = cfg.get("title_font", "Helvetica-Bold")
    S = {
        "label":     ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=8, leading=11,
                                     textColor=accent, alignment=TA_LEFT, spaceAfter=4),
        "section":   ParagraphStyle("section", fontName=title_font, fontSize=24, leading=28,
                                     textColor=ink, alignment=TA_LEFT, spaceBefore=2, spaceAfter=4),
        "h2":        ParagraphStyle("h2", fontName=title_font, fontSize=12.5, leading=16,
                                     textColor=ink, alignment=TA_LEFT, spaceBefore=10, spaceAfter=3),
        "h3":        ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10, leading=14,
                                     textColor=accent, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4),
        "body":      ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=15.5,
                                     textColor=ink, alignment=TA_JUSTIFY, spaceAfter=6),
        "body_s":    ParagraphStyle("body_s", fontName="Helvetica", fontSize=9, leading=13,
                                     textColor=subink, alignment=TA_JUSTIFY, spaceAfter=4),
        "bullet":    ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.7, leading=14,
                                     textColor=ink, alignment=TA_LEFT, leftIndent=14, spaceAfter=2),
        "lead":      ParagraphStyle("lead", fontName="Times-Italic", fontSize=12.5, leading=18,
                                     textColor=subink, alignment=TA_LEFT, spaceAfter=8),
        "caption":   ParagraphStyle("caption", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
                                     textColor=muted, alignment=TA_LEFT, spaceAfter=4),
    }

    story = []

    # ═══ CAPA ═══
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # ═══ FICHA TÉCNICA ═══
    story.append(Paragraph("FICHA TÉCNICA", S["label"]))
    story.append(Paragraph("Sobre esta edição.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(cfg["abstract"], S["lead"]))
    story.append(Spacer(1, 0.3*cm))

    ficha = [
        ["Título",           f"{cfg['title_main']} {cfg['title_sub'].rstrip('.')}"],
        ["Autor",            cfg["author"]],
        ["Edição original",  cfg.get("year_orig", "—")],
        ["Edição BR",        cfg.get("year_br", "—")],
        ["Editora (BR)",     cfg.get("publisher", "—")],
        ["Páginas",          cfg.get("pages", "—")],
        ["Gênero",           cfg.get("genre", "—")],
        ["Tese",             cfg["thesis"]],
    ]
    t = Table(ficha, colWidths=[4.6*cm, fw - 4.6*cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 9.5),
        ("TEXTCOLOR", (0,0), (0,-1), muted),
        ("TEXTCOLOR", (1,0), (1,-1), ink),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("LINEBELOW", (0,0), (-1,-1), 0.25, hairline),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    story.append(PullQuote(fw, cfg["headline_quote"], cfg.get("headline_attr",
                            f"{cfg['author']} · {cfg['title_main']} {cfg['title_sub'].rstrip('.')}"),
                            accent, ink, muted, size=14))

    story.append(PageBreak())

    # ═══ SUMÁRIO ═══
    story.append(Paragraph("NAVEGAÇÃO", S["label"]))
    story.append(Paragraph("Sumário.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "Paginação deste caderno. Os capítulos refletem a sequência conceitual do livro.",
        S["body_s"]))
    story.append(Spacer(1, 0.3*cm))

    sumario_rows = [
        ("",   "Capa",                                  1),
        ("",   "Ficha técnica",                         2),
        ("",   "Sumário",                               3),
        ("",   "Sobre o autor",                         4),
        ("",   "A grande ideia",                        5),
    ]
    pg = 6
    chapter_pages = []
    for ch in cfg["chapters"]:
        sumario_rows.append((ch["num"], ch["title"], pg))
        chapter_pages.append(pg); pg += 1
    sumario_rows.append(("", "Insights e inversões", pg)); pg += 1
    sumario_rows.append(("", "Aplicação prática", pg)); pg += 1
    sumario_rows.append(("", "Citações em destaque", pg)); pg += 1
    sumario_rows.append(("", "Provocações pessoais", pg)); pg += 1
    sumario_rows.append(("", "Caderno de leitura", pg)); pg += 1
    sumario_rows.append(("", "Última palavra", pg))

    toc_main = ParagraphStyle("toc_main", fontName="Helvetica", fontSize=9.5, leading=13,
                               textColor=ink, alignment=TA_LEFT)
    toc_meta = ParagraphStyle("toc_meta", fontName="Times-Italic", fontSize=9.5, leading=13,
                               textColor=subink, alignment=TA_LEFT)
    rows = []
    for tag, title, p in sumario_rows:
        rows.append([tag if tag else "·",
                     Paragraph(title, toc_main if tag else toc_meta),
                     str(p)])
    tbl = Table(rows, colWidths=[1.0*cm, fw - 3.0*cm, 1.5*cm])
    cmds = [
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (0,-1), 9),
        ("TEXTCOLOR", (0,0), (0,-1), accent),
        ("FONTNAME", (2,0), (2,-1), "Helvetica"),
        ("FONTSIZE", (2,0), (2,-1), 9),
        ("TEXTCOLOR", (2,0), (2,-1), muted),
        ("ALIGN", (2,0), (2,-1), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("LINEBELOW", (0,0), (-1,-2), 0.2, hairline),
    ]
    # destacar primeiro/último capítulo
    chap_idxs = [i for i, (tag, _, _) in enumerate(sumario_rows) if tag and tag.isdigit() or
                 (tag and len(tag) == 2 and tag[0] == "0")]
    if chap_idxs:
        cmds.append(("LINEABOVE", (0, chap_idxs[0]), (-1, chap_idxs[0]), 0.5, ink))
        cmds.append(("TOPPADDING", (0, chap_idxs[0]), (-1, chap_idxs[0]), 7))
        cmds.append(("LINEBELOW", (0, chap_idxs[-1]), (-1, chap_idxs[-1]), 0.5, ink))
        cmds.append(("BOTTOMPADDING", (0, chap_idxs[-1]), (-1, chap_idxs[-1]), 6))
    tbl.setStyle(TableStyle(cmds))
    story.append(tbl)

    story.append(PageBreak())

    # ═══ SOBRE O AUTOR ═══
    story.append(Paragraph("AUTOR", S["label"]))
    story.append(Paragraph(f"Sobre {cfg['author']}.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    for p in cfg["about_author"]:
        story.append(Paragraph(p, S["body"]))

    story.append(PageBreak())

    # ═══ A GRANDE IDEIA ═══
    story.append(Paragraph("VISÃO PANORÂMICA", S["label"]))
    story.append(Paragraph("A grande ideia.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(cfg["big_idea"], S["body"]))
    if cfg.get("big_idea_extra"):
        for p in cfg["big_idea_extra"]:
            story.append(Paragraph(p, S["body"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(Callout(fw, cfg["thesis"], "TESE CENTRAL", accent, ink))

    story.append(PageBreak())

    # ═══ MAPA VISUAL DOS CAPÍTULOS ═══
    story.append(Paragraph("VISÃO GERAL", S["label"]))
    story.append(Paragraph("Mapa visual dos capítulos.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "Cada capítulo em um cartão. Use esta página como índice mental do livro — "
        "para encontrar rapidamente o conceito ou voltar a ele depois.", S["lead"]))
    story.append(Spacer(1, 0.3*cm))

    # Cards em grade 2-colunas (4 linhas pra 8 caps)
    n_ch = len(cfg["chapters"])
    cols = 2
    map_cell_style = ParagraphStyle("mc", fontName="Helvetica", fontSize=8.5,
                                     leading=11, textColor=subink, alignment=TA_LEFT)
    map_cards = []
    for ch in cfg["chapters"]:
        text = (f"<font color='#{accent.hexval()[2:]}' name='Helvetica-Bold' size='18'>"
                f"{ch['num']}</font><br/>"
                f"<font name='Helvetica-Bold' size='9.5' color='#{ink.hexval()[2:]}'>"
                f"{ch['title']}</font><br/>"
                f"<font color='#{muted.hexval()[2:]}' name='Helvetica' size='7.5'>"
                f"{ch.get('kicker','')}</font>")
        map_cards.append(Paragraph(text, map_cell_style))
    # preencher para múltiplo de 2
    while len(map_cards) % cols != 0:
        map_cards.append("")
    map_rows = []
    for i in range(0, len(map_cards), cols):
        map_rows.append(map_cards[i:i+cols])
    map_tbl = Table(map_rows, colWidths=[fw/cols - 0.3*cm]*cols)
    map_tbl.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0.3*cm),
        ("RIGHTPADDING", (0,0), (-1,-1), 0.3*cm),
        ("TOPPADDING", (0,0), (-1,-1), 0.4*cm),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0.4*cm),
        ("LINEBELOW", (0,0), (-1,-2), 0.25, hairline),
        ("LINEAFTER", (0,0), (0,-1), 0.25, hairline),
    ]))
    story.append(map_tbl)
    story.append(PageBreak())

    # ═══ CAPÍTULOS ═══
    for i, ch in enumerate(cfg["chapters"]):
        story.append(BigNumber(fw, ch["num"], kicker=ch.get("kicker", ""), color=ink, font=title_font))
        story.append(Spacer(1, 0.1*cm))
        story.append(Paragraph(ch["title"] + ".", S["section"]))
        story.append(HLine(fw, thickness=0.6, color=ink, space_after=8))
        story.append(Paragraph(ch["intro"], S["body"]))
        if ch.get("bullets"):
            story.append(Paragraph("Pontos-chave", S["h2"]))
            for b in ch["bullets"]:
                story.append(Paragraph("·  " + b, S["bullet"]))
        if ch.get("quote"):
            story.append(Spacer(1, 0.15*cm))
            story.append(PullQuote(fw, ch["quote"],
                f"{cfg['author']} · {cfg['title_main']} {cfg['title_sub'].rstrip('.')}",
                accent, ink, muted, size=12))
        if ch.get("callout"):
            story.append(Spacer(1, 0.1*cm))
            story.append(Callout(fw, ch["callout"], ch.get("callout_label", "INSIGHT"), accent, ink))
        story.append(PageBreak())

    # ═══ INSIGHTS / INVERSÕES ═══
    story.append(Paragraph("PROFUNDIDADE", S["label"]))
    story.append(Paragraph("Insights e inversões.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    for num, t_, txt in cfg["insights"]:
        story.append(Paragraph(f"{num}  ·  {t_}", S["h3"]))
        story.append(Paragraph(txt, S["body"]))
    story.append(PageBreak())

    # ═══ APLICAÇÃO PRÁTICA ═══
    story.append(Paragraph("APLICAÇÃO", S["label"]))
    story.append(Paragraph("Como aplicar à sua vida.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "Passos concretos para começar a usar as ideias do livro nos próximos 30 dias.",
        S["lead"]))
    story.append(Spacer(1, 0.2*cm))
    for i, (label, txt) in enumerate(cfg["application"], 1):
        tbl_p = Table(
            [[f"{i:02d}", Paragraph(f"<b>{label}</b><br/>{txt}", S["body"])]],
            colWidths=[1.6*cm, fw - 1.6*cm]
        )
        tbl_p.setStyle(TableStyle([
            ("FONTNAME", (0,0), (0,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (0,0), 22),
            ("TEXTCOLOR", (0,0), (0,0), accent),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LINEBELOW", (0,0), (-1,0), 0.25, hairline),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
        ]))
        story.append(tbl_p)
    story.append(PageBreak())

    # ═══ APLICAÇÃO SEMANA A SEMANA ═══
    story.append(Paragraph("CRONOGRAMA", S["label"]))
    story.append(Paragraph("Quatro semanas de prática.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "Distribua a aplicação em quatro semanas. Não comece tudo de uma vez — "
        "sobreposição é a primeira causa de desistência.", S["lead"]))
    story.append(Spacer(1, 0.3*cm))

    semanas = [
        ("01", "Diagnóstico",
         "Reler o resumo. Identificar onde a sua vida atual se parece com o que o livro descreve. "
         "Listar 3 áreas onde o livro mais te tocou. Sem mudanças ainda — só consciência."),
        ("02", "Primeira aplicação",
         "Escolher 1 das 6 sugestões da página de Aplicação. Apenas uma. Praticar todos os "
         "dias por 7 dias seguidos. Não diversificar."),
        ("03", "Segunda aplicação + revisão",
         "Manter a 1ª aplicação. Adicionar a 2ª. Revisar no fim da semana: o que está pegando, "
         "o que está vazio. Ajustar."),
        ("04", "Integração",
         "Manter as 2 práticas. Decidir o que vai manter depois desta 4 semana. Marcar uma "
         "data, daqui a 3 meses, para reler o resumo e verificar o que sobreviveu."),
    ]
    for num, lab, txt in semanas:
        tbl_w = Table(
            [[num, Paragraph(f"<b>Semana {num} · {lab}</b><br/>{txt}", S["body"])]],
            colWidths=[1.7*cm, fw - 1.7*cm]
        )
        tbl_w.setStyle(TableStyle([
            ("FONTNAME", (0,0), (0,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (0,0), 24),
            ("TEXTCOLOR", (0,0), (0,0), accent),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LINEBELOW", (0,0), (-1,0), 0.25, hairline),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
        ]))
        story.append(tbl_w)
    story.append(Spacer(1, 0.2*cm))
    story.append(Callout(fw,
        "Aplicar é mais difícil do que ler. Quem aplica menos, descobre mais. Volume "
        "concentrado vence pacote de boas intenções.",
        "REGRA DO CRONOGRAMA", accent, ink))
    story.append(PageBreak())

    # ═══ CITAÇÕES EM DESTAQUE ═══
    story.append(Paragraph("PAREDE DE CITAÇÕES", S["label"]))
    story.append(Paragraph("As frases que ficam · 1/2.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=14))
    story.append(Spacer(1, 0.3*cm))
    sizes = [14, 22, 14, 18]
    colors = [ink, accent, ink, ink]
    n_first = max(3, (len(cfg["quotes"]) + 1) // 2)
    for i, (q, a) in enumerate(cfg["quotes"][:n_first]):
        story.append(CenteredQuote(fw, q, attribution=a,
                                   size=sizes[i % len(sizes)],
                                   color=colors[i % len(colors)], muted=muted))
        story.append(Spacer(1, 0.25*cm))
    story.append(PageBreak())

    # Segunda página de citações + síntese
    story.append(Paragraph("PAREDE DE CITAÇÕES", S["label"]))
    story.append(Paragraph("As frases que ficam · 2/2.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=14))
    story.append(Spacer(1, 0.3*cm))
    sizes2 = [14, 28, 14, 18]
    colors2 = [ink, accent, ink, ink]
    for i, (q, a) in enumerate(cfg["quotes"][n_first:]):
        story.append(CenteredQuote(fw, q, attribution=a,
                                   size=sizes2[i % len(sizes2)],
                                   color=colors2[i % len(colors2)], muted=muted))
        story.append(Spacer(1, 0.25*cm))
    story.append(Spacer(1, 0.5*cm))
    story.append(Callout(fw,
        "Releia esta parede a cada três meses. As frases que ficaram com você dirão "
        "mais sobre quem você se tornou do que sobre o livro.",
        "RITUAL", accent, ink))
    story.append(PageBreak())

    # ═══ ERROS COMUNS ═══
    story.append(Paragraph("ARMADILHAS", S["label"]))
    story.append(Paragraph("Erros comuns ao aplicar.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "O que costuma dar errado quando se tenta aplicar as ideias deste livro. "
        "Reconhecer cada erro economiza meses de tentativa.", S["lead"]))
    story.append(Spacer(1, 0.3*cm))

    erros_genericos = cfg.get("common_errors", [
        ("Aplicar tudo de uma vez",
         "Empolgação do início faz mudar dez coisas simultâneas. Em duas semanas tudo cai. "
         "Aplicar uma coisa por mês ganha. Sempre."),
        ("Ler sem agir",
         "Notar 'que bom isso' e seguir a vida. O livro vira entretenimento, não ferramenta. "
         "Sem aplicação a leitura é só ginástica mental."),
        ("Procurar perfeição antes de começar",
         "Esperar a 'hora certa', o 'sistema completo', a 'condição ideal'. A hora certa é "
         "qualquer hora; o sistema vai crescendo."),
        ("Falar antes de fazer",
         "Contar para todo mundo que você vai mudar — e o cérebro recebe a recompensa do "
         "anúncio antes da entrega. Faça primeiro, conte depois."),
        ("Esperar resultado em 7 dias",
         "Quase tudo o que vale a pena tem efeito composto. Sete dias é pouco para qualquer "
         "coisa. Quatro semanas é o mínimo viável."),
    ])
    for i, (lab, txt) in enumerate(erros_genericos, 1):
        tbl_e = Table(
            [[f"{i:02d}", Paragraph(f"<b>{lab}</b><br/>{txt}", S["body"])]],
            colWidths=[1.6*cm, fw - 1.6*cm]
        )
        tbl_e.setStyle(TableStyle([
            ("FONTNAME", (0,0), (0,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (0,0), 20),
            ("TEXTCOLOR", (0,0), (0,0), accent),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LINEBELOW", (0,0), (-1,0), 0.25, hairline),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
        ]))
        story.append(tbl_e)
    story.append(PageBreak())

    # ═══ PROVOCAÇÕES / REFLEXÕES ═══
    story.append(Paragraph("REFLEXÃO PESSOAL", S["label"]))
    story.append(Paragraph("Provocações.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "Reserve dez minutos para cada uma. Não responda o que está certo — responda o que é verdade pra você.",
        S["lead"]))
    story.append(Spacer(1, 0.2*cm))
    for q in cfg["reflections"]:
        # prompt + 2 linhas
        cell = Paragraph(f"<b>{q}</b>", S["body"])
        prompt_tbl = Table([[cell]], colWidths=[fw])
        prompt_tbl.setStyle(TableStyle([
            ("LINEBEFORE", (0,0), (0,0), 1.8, accent),
            ("LEFTPADDING", (0,0), (0,0), 0.4*cm),
            ("TOPPADDING", (0,0), (0,0), 4),
            ("BOTTOMPADDING", (0,0), (0,0), 4),
        ]))
        story.append(prompt_tbl)
        story.append(NumberedLines(fw, num_lines=2, line_spacing=0.7*cm,
                                    color=hairline, muted=muted, label=None))
        story.append(Spacer(1, 0.18*cm))

    story.append(PageBreak())

    # ═══ VOCABULÁRIO-CHAVE ═══
    if cfg.get("vocabulary"):
        story.append(Paragraph("DICIONÁRIO", S["label"]))
        story.append(Paragraph("Vocabulário-chave.", S["section"]))
        story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
        story.append(Paragraph(
            "Termos do livro que vale a pena memorizar. Estão referenciados nos "
            "capítulos e voltarão nas suas conversas — se você os fixar.", S["lead"]))
        story.append(Spacer(1, 0.2*cm))
        for term, defn in cfg["vocabulary"]:
            story.append(Paragraph(term, S["h3"]))
            story.append(Paragraph(defn, S["body"]))
        story.append(PageBreak())

    # ═══ PARA IR ALÉM ═══
    if cfg.get("further_reading"):
        story.append(Paragraph("APROFUNDAMENTO", S["label"]))
        story.append(Paragraph("Para ir além.", S["section"]))
        story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
        story.append(Paragraph(
            "Se este livro te tocou, estes te tocarão também. Em parênteses, os "
            "volumes da coleção Leitura Breve em que já existe um resumo.",
            S["lead"]))
        story.append(Spacer(1, 0.3*cm))
        for title, author, note in cfg["further_reading"]:
            row_text = (f"<font name='Helvetica-Bold' size='10' color='#{ink.hexval()[2:]}'>"
                        f"{title}</font> <font name='Times-Italic' size='9' "
                        f"color='#{muted.hexval()[2:]}'>· {author}</font>")
            story.append(Paragraph(row_text, S["body"]))
            story.append(Paragraph(note, S["body_s"]))
            story.append(Spacer(1, 0.2*cm))
        story.append(PageBreak())

    # ═══ CADERNO (2 PÁGINAS) ═══
    story.append(Paragraph("CADERNO", S["label"]))
    story.append(Paragraph("Caderno de leitura · 1/2.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "Use estas páginas para registrar o que ficou da leitura. Escreva à mão — "
        "fixa melhor.", S["body_s"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(NumberedLines(fw, num_lines=8, line_spacing=0.78*cm,
                                color=hairline, muted=muted,
                                label="O que aprendi com este livro"))
    story.append(Spacer(1, 0.5*cm))
    story.append(NumberedLines(fw, num_lines=8, line_spacing=0.78*cm,
                                color=hairline, muted=muted,
                                label="O que vou aplicar a partir de hoje"))
    story.append(PageBreak())

    story.append(Paragraph("CADERNO", S["label"]))
    story.append(Paragraph("Caderno de leitura · 2/2.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "Diário de aplicação ao longo de 30 dias. Volte a esta página a cada "
        "domingo — o que mudou, o que não mudou, o que pretende ajustar.",
        S["body_s"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(NumberedLines(fw, num_lines=4, line_spacing=0.78*cm,
                                color=hairline, muted=muted,
                                label="Semana 1 · diagnóstico"))
    story.append(Spacer(1, 0.3*cm))
    story.append(NumberedLines(fw, num_lines=4, line_spacing=0.78*cm,
                                color=hairline, muted=muted,
                                label="Semana 2 · primeira aplicação"))
    story.append(Spacer(1, 0.3*cm))
    story.append(NumberedLines(fw, num_lines=4, line_spacing=0.78*cm,
                                color=hairline, muted=muted,
                                label="Semana 3 · segunda aplicação"))
    story.append(Spacer(1, 0.3*cm))
    story.append(NumberedLines(fw, num_lines=4, line_spacing=0.78*cm,
                                color=hairline, muted=muted,
                                label="Semana 4 · integração"))
    story.append(PageBreak())

    # ═══ TL;DR — RESUMO DE UM MINUTO ═══
    story.append(Paragraph("SÍNTESE", S["label"]))
    story.append(Paragraph("O livro em um minuto.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "Se você só tivesse 60 segundos para passar esta leitura adiante, este "
        "seria o texto. Use-o como recordação rápida e como cartão para "
        "compartilhar.", S["lead"]))
    story.append(Spacer(1, 0.3*cm))

    # Bloco grande com tese em destaque
    tldr_box = ParagraphStyle("tldr", fontName="Times-Italic", fontSize=16, leading=22,
                               textColor=ink, alignment=TA_LEFT, spaceAfter=14)
    story.append(Paragraph(f"<b>Tese:</b> {cfg['thesis']}", tldr_box))
    story.append(Spacer(1, 0.2*cm))

    # 3 pilares em síntese
    story.append(Paragraph("Os três pilares para lembrar", S["h2"]))
    pilares = cfg.get("pillars", [
        ("Conceito-chave",
         f"O conceito central de <b>{cfg['title_main']} {cfg['title_sub'].rstrip('.')}</b> "
         f"é a tese acima. Tudo o mais é desdobramento."),
        ("Aplicação principal",
         "A primeira aplicação concreta — escolha qual dos 6 passos da página de "
         "Aplicação você implementa primeiro."),
        ("Risco se não fizer",
         "Sem aplicar, o livro vira entretenimento intelectual. Decida hoje que parte "
         "vai virar prática esta semana."),
    ])
    for tit, txt in pilares:
        story.append(Paragraph(tit, S["h3"]))
        story.append(Paragraph(txt, S["body"]))

    story.append(Spacer(1, 0.3*cm))
    story.append(Callout(fw,
        f"Em uma frase: <b>{cfg['headline_quote']}</b>",
        "PARA GUARDAR", accent, ink))

    story.append(PageBreak())

    # ═══ ÚLTIMA PALAVRA ═══
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("ÚLTIMA PALAVRA", S["label"]))
    story.append(Paragraph(cfg["last_word_title"], S["section"]))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=14))
    story.append(CenteredQuote(fw, cfg["last_word_quote"], attribution="Síntese do leitor",
                                size=14, color=ink, muted=muted))

    doc.build(story)
    return output


# ═══════════════════════════════════════════════════════
# CATÁLOGO
# ═══════════════════════════════════════════════════════

def build_catalog(books_full):
    """Catálogo com os 18 volumes (3 anteriores + 15 novos)."""
    output = os.path.join(OUT_DIR, "Catalogo_Leitura_Breve.pdf")

    # paleta neutra do catálogo — preto/cinza/laranja sutil
    paper = HexColor("#FAFAF7"); ink = HexColor("#0E0E0E")
    accent = HexColor("#C53A14"); muted = HexColor("#7A7569")
    hairline = HexColor("#D8D3C5"); subink = HexColor("#2A2A2A")

    def _cover(c, doc):
        c.setFillColor(paper); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        c.setStrokeColor(ink); c.setLineWidth(0.7)
        c.line(MARGIN_L, PAGE_H - 1.6*cm, PAGE_W - MARGIN_L, PAGE_H - 1.6*cm)
        c.setFont("Helvetica-Bold", 8); c.setFillColor(ink); c.setCharSpace(3)
        c.drawString(MARGIN_L, PAGE_H - 1.25*cm, "CATÁLOGO · COLEÇÃO COMPLETA")
        c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.25*cm, "ED. MAIO 2026"); c.setCharSpace(0)
        # numero "38" grande
        c.setFont("Helvetica-Bold", 230); c.setFillColor(HexColor("#EBE7DA"))
        c.setCharSpace(-8); c.drawString(MARGIN_L - 0.3*cm, PAGE_H - 11*cm, "38"); c.setCharSpace(0)
        # kicker
        c.setFont("Helvetica-Bold", 9); c.setFillColor(accent); c.setCharSpace(2.2)
        c.drawString(MARGIN_L, PAGE_H - 12.3*cm, "RESUMOS · DESENVOLVIMENTO · LITERATURA · FILOSOFIA")
        c.setCharSpace(0)
        # título
        c.setFont("Helvetica-Bold", 60); c.setFillColor(ink)
        c.drawString(MARGIN_L, PAGE_H - 14.5*cm, "Leitura")
        c.drawString(MARGIN_L, PAGE_H - 16.5*cm, "Breve.")
        # subtítulo
        c.setFont("Times-Italic", 14); c.setFillColor(subink)
        c.drawString(MARGIN_L, PAGE_H - 17.6*cm, "Catálogo dos 38 volumes lançados — bestsellers, clássicos")
        c.drawString(MARGIN_L, PAGE_H - 18.2*cm, "resumidos para uma sessão de leitura.")
        # rule
        c.setStrokeColor(accent); c.setLineWidth(1.4)
        c.line(MARGIN_L, PAGE_H - 19.0*cm, MARGIN_L + 2.5*cm, PAGE_H - 19.0*cm)
        # marca
        c.setFont("Helvetica-Bold", 8); c.setFillColor(muted); c.setCharSpace(2)
        c.drawString(MARGIN_L, PAGE_H - 19.6*cm, "EDITORIAL"); c.setCharSpace(0)
        c.setFont("Helvetica-Bold", 13); c.setFillColor(ink)
        c.drawString(MARGIN_L, PAGE_H - 20.3*cm, "Leitura Breve")
        # rodapé
        c.setStrokeColor(ink); c.setLineWidth(0.5)
        c.line(MARGIN_L, 2.3*cm, PAGE_W - MARGIN_R, 2.3*cm)
        c.setFont("Helvetica-Bold", 7.5); c.setFillColor(muted); c.setCharSpace(2.5)
        c.drawString(MARGIN_L, 1.7*cm, "CATÁLOGO COMPLETO  ·  COLEÇÃO LEITURA BREVE  ·  VOL. 01–38")
        c.drawRightString(PAGE_W - MARGIN_R, 1.7*cm, "FORMATO A4"); c.setCharSpace(0)

    def _body(c, doc):
        c.setFillColor(paper); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5); c.setFillColor(muted); c.setCharSpace(2.5)
        c.drawString(MARGIN_L, PAGE_H - 1.3*cm, "LEITURA BREVE")
        c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.3*cm, "CATÁLOGO · 2026")
        c.setCharSpace(0)
        c.setStrokeColor(hairline); c.setLineWidth(0.3)
        c.line(MARGIN_L, PAGE_H - 1.55*cm, PAGE_W - MARGIN_R, PAGE_H - 1.55*cm)
        page_num = c.getPageNumber()
        c.setStrokeColor(hairline); c.setLineWidth(0.3)
        c.line(MARGIN_L, 1.7*cm, PAGE_W - MARGIN_R, 1.7*cm)
        c.setFont("Helvetica-Bold", 7.5); c.setFillColor(muted); c.setCharSpace(2.5)
        c.drawString(MARGIN_L, 1.3*cm, "CATÁLOGO · COLEÇÃO COMPLETA"); c.setCharSpace(0)
        c.setFillColor(accent); c.circle(PAGE_W - MARGIN_R - 1.2*cm, 1.4*cm, 0.08*cm, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 11); c.setFillColor(ink)
        c.drawRightString(PAGE_W - MARGIN_R, 1.25*cm, f"{page_num:02d}")

    doc = BaseDocTemplate(output, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title="Leitura Breve — Catálogo dos 18 Volumes")
    fw = PAGE_W - MARGIN_L - MARGIN_R; fh = PAGE_H - MARGIN_T - MARGIN_B
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[Frame(MARGIN_L, MARGIN_B, fw, fh, id="c", showBoundary=0)], onPage=_cover),
        PageTemplate(id="body",  frames=[Frame(MARGIN_L, MARGIN_B, fw, fh - 0.4*cm, id="b", showBoundary=0)], onPage=_body),
    ])

    label = ParagraphStyle("l", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=accent, spaceAfter=4)
    section = ParagraphStyle("s", fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=ink, spaceAfter=4)
    lead = ParagraphStyle("ld", fontName="Times-Italic", fontSize=12.5, leading=18, textColor=subink, spaceAfter=8)
    body = ParagraphStyle("b", fontName="Helvetica", fontSize=10, leading=14, textColor=ink, alignment=TA_JUSTIFY, spaceAfter=4)
    h3 = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=ink, spaceAfter=2)

    story = []
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body")); story.append(PageBreak())

    # ═══ INTRODUÇÃO ═══
    story.append(Paragraph("INTRODUÇÃO", label))
    story.append(Paragraph("Sobre esta coleção.", section))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "Coleção dos 38 volumes lançados pela <b>Leitura Breve</b> — resumos editoriais "
        "completos dos bestsellers que mais venderam no Brasil nas últimas décadas. "
        "Cada volume foi pensado para ser lido em uma única sessão e funciona como "
        "caderno de leitura: contém ficha técnica, resumo capítulo a capítulo, "
        "citações, insights, exercícios e espaço próprio para anotações.", lead))
    story.append(Spacer(1, 0.3*cm))

    # Estatística da coleção
    stats = [
        ["Volumes",        f"38"],
        ["Categorias",     "Comportamento · Negócios · Filosofia · Literatura · Finanças"],
        ["Páginas no total", f"≈ {sum(b['pages_count'] for b in books_full)} páginas"],
        ["Autores",        ", ".join(sorted(set(b['author'].split()[-1] for b in books_full)))[:80] + "..."],
        ["Formato",        "A4 · PDF editorial"],
    ]
    t = Table(stats, colWidths=[3.6*cm, fw - 3.6*cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 9.5),
        ("TEXTCOLOR", (0,0), (0,-1), muted),
        ("TEXTCOLOR", (1,0), (1,-1), ink),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("LINEBELOW", (0,0), (-1,-1), 0.25, hairline),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(t)

    story.append(PageBreak())

    # ═══ ÍNDICE DOS VOLUMES ═══
    story.append(Paragraph("ÍNDICE", label))
    story.append(Paragraph("Os 38 volumes em duas páginas.", section))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))

    toc_main = ParagraphStyle("tcm", fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=ink)
    toc_sub = ParagraphStyle("tcs", fontName="Helvetica", fontSize=9, leading=12, textColor=subink)
    toc_auth = ParagraphStyle("tca", fontName="Times-Italic", fontSize=9, leading=12, textColor=muted)
    rows = []
    for b in books_full:
        title_line = f"<b>{b['title_main']} {b['title_sub'].rstrip('.')}</b>"
        rows.append([
            b["vol"],
            Paragraph(f"{title_line}<br/><font color='#7A7569'>{b['author']}</font>", toc_sub),
            f"{b['pages_count']} p.",
        ])
    tbl = Table(rows, colWidths=[1.3*cm, fw - 4.0*cm, 2.7*cm])
    cmds = [
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (0,-1), 10),
        ("TEXTCOLOR", (0,0), (0,-1), accent),
        ("FONTNAME", (2,0), (2,-1), "Helvetica"),
        ("FONTSIZE", (2,0), (2,-1), 8),
        ("TEXTCOLOR", (2,0), (2,-1), muted),
        ("ALIGN", (2,0), (2,-1), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 3.5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3.5),
        ("LINEBELOW", (0,0), (-1,-1), 0.2, hairline),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]
    tbl.setStyle(TableStyle(cmds))
    story.append(tbl)

    story.append(PageBreak())

    # ═══ FICHAS DOS VOLUMES (2 por página) ═══
    story.append(Paragraph("FICHAS", label))
    story.append(Paragraph("Os volumes, um a um.", section))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "Cada ficha resume o livro em uma página: tese central, conceitos-chave "
        "e a frase que melhor o sintetiza.", lead))
    story.append(Spacer(1, 0.3*cm))

    # 2 fichas por página
    for i in range(0, len(books_full), 2):
        pair = books_full[i:i+2]
        cards = []
        for b in pair:
            b_palette = b.get("palette", {})
            b_accent = HexColor(b_palette.get("accent", "#C53A14"))
            # construir card como Table
            kicker_para = Paragraph(
                f"<font color='#{b_accent.hexval()[2:]}' name='Helvetica-Bold' size='8'>"
                f"VOL. {b['vol']}  ·  {b.get('category_kicker','—')}</font>", toc_sub)
            title_para = Paragraph(
                f"<font name='Helvetica-Bold' size='15' color='#0E0E0E'>"
                f"{b['title_main']} {b['title_sub'].rstrip('.')}</font>", toc_sub)
            author_para = Paragraph(
                f"<font name='Times-Italic' size='10' color='#2A2A2A'>"
                f"{b['author']}</font>", toc_sub)
            thesis_para = Paragraph(b['thesis'], toc_sub)
            quote_para = Paragraph(
                f"<font name='Times-Italic' size='10' color='#2A2A2A'>“{b['headline_quote']}”</font>",
                toc_sub)
            meta_para = Paragraph(
                f"<font color='#7A7569' size='8'>{b['pages_count']} páginas  ·  "
                f"{b.get('year_orig','—')}  ·  {b.get('genre','—')}</font>", toc_sub)
            card = Table([
                [kicker_para],
                [title_para],
                [author_para],
                [Spacer(1, 0.15*cm)],
                [thesis_para],
                [Spacer(1, 0.1*cm)],
                [quote_para],
                [Spacer(1, 0.15*cm)],
                [meta_para],
            ], colWidths=[fw/2 - 0.4*cm])
            card.setStyle(TableStyle([
                ("VALIGN", (0,0), (-1,-1), "TOP"),
                ("LEFTPADDING", (0,0), (-1,-1), 0.2*cm),
                ("RIGHTPADDING", (0,0), (-1,-1), 0.2*cm),
                ("TOPPADDING", (0,0), (-1,-1), 0.05*cm),
                ("BOTTOMPADDING", (0,0), (-1,-1), 0.05*cm),
                ("LINEBEFORE", (0,0), (0,-1), 1.5, b_accent),
            ]))
            cards.append(card)
        if len(cards) == 1: cards.append("")
        # tabela de 2 colunas com cards
        pair_t = Table([cards], colWidths=[fw/2 - 0.4*cm, fw/2 - 0.4*cm])
        pair_t.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (0,0), 0),
            ("RIGHTPADDING", (0,0), (0,0), 0.4*cm),
            ("LEFTPADDING", (1,0), (1,0), 0.4*cm),
            ("RIGHTPADDING", (1,0), (1,0), 0),
        ]))
        story.append(pair_t)
        story.append(Spacer(1, 0.6*cm))

    # ═══ COMO USAR A COLEÇÃO ═══
    story.append(PageBreak())
    story.append(Paragraph("PARA O LEITOR", label))
    story.append(Paragraph("Como usar a coleção.", section))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=12))
    story.append(Paragraph(
        "Quatro maneiras de aproveitar a Leitura Breve — escolha a que combina com seu momento.", lead))
    story.append(Spacer(1, 0.2*cm))

    usos = [
        ("01", "Como antessala do livro",
         "Leia o resumo antes do livro inteiro. Você chega ao texto principal com a "
         "estrutura mental pronta — e termina entendendo o dobro."),
        ("02", "Como retrospectiva",
         "Já leu o livro há tempos? Use o resumo para ativar a memória sem precisar "
         "reler. As páginas de citações e insights bastam."),
        ("03", "Como caderno de jornada",
         "Use os espaços de anotações, as provocações e o caderno final. Cada volume "
         "vira o seu diário pessoal de aplicação."),
        ("04", "Como mapa da próxima leitura",
         "Não decidiu qual livro ler? Use o catálogo: cada ficha condensa a tese em "
         "uma linha. Em 10 minutos você sabe pra onde vai a sua próxima leitura."),
    ]
    for num, t_, txt in usos:
        tbl = Table([[num, Paragraph(f"<b>{t_}</b><br/>{txt}", body)]],
                    colWidths=[1.6*cm, fw - 1.6*cm])
        tbl.setStyle(TableStyle([
            ("FONTNAME", (0,0), (0,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (0,0), 22),
            ("TEXTCOLOR", (0,0), (0,0), accent),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LINEBELOW", (0,0), (-1,0), 0.25, hairline),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
        ]))
        story.append(tbl)

    story.append(PageBreak())
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("COLOFÃO", label))
    story.append(Paragraph("Editorial.", section))
    story.append(HLine(fw, thickness=0.6, color=ink, space_after=14))
    story.append(Paragraph(
        "Coleção <b>Leitura Breve</b> — Vols. 01 a 18. Editado em maio de 2026. "
        "Diagramado em A4 com tipografia Helvetica e Times. Distribuição digital, "
        "para leitura e anotação pessoal. Os direitos dos textos originais "
        "pertencem aos respectivos autores e editoras.", body))

    doc.build(story)
    return output


# ═══════════════════════════════════════════════════════
# DADOS DOS LIVROS (Vols. 04 a 18)
# ═══════════════════════════════════════════════════════

BOOKS = [
    # ─── 04 · O Poder do Hábito ─────────────────────────
    {
        "id": "poder_habito", "vol": "04",
        "title_main": "O Poder", "title_sub": "do Hábito.",
        "short_title": "O Poder do Hábito",
        "subtitle": "Por que fazemos o que fazemos na vida e nos negócios.",
        "author": "Charles Duhigg",
        "year_orig": "2012", "year_br": "2012", "publisher": "Objetiva",
        "pages": "Aproximadamente 408 páginas", "pages_count": 26,
        "genre": "Comportamento · Jornalismo investigativo",
        "category_kicker": "Comportamento · Neurociência · Negócios",
        "motif": "loop",
        "palette": {"paper": "#F1ECE3", "ink": "#11283F", "accent": "#B8662E",
                    "muted": "#7A7569", "hairline": "#CFC7B5", "subink": "#2B3D54",
                    "paper_dark": "#E3DECE"},
        "abstract": ("Resumo de <b>O Poder do Hábito</b>, do jornalista investigativo "
                     "Charles Duhigg. Reúne o ciclo do hábito, casos clássicos "
                     "(Pepsodent, Starbucks, Phelps, Alcoa), conceitos-chave e aplicação prática."),
        "thesis": "Todo hábito é um loop deixa → rotina → recompensa. Compreender o loop é o começo de transformá-lo.",
        "headline_quote": "A vida toda, tal como a conhecemos, é uma massa de hábitos.",
        "about_author": [
            "<b>Charles Duhigg</b> é um jornalista investigativo norte-americano, repórter "
            "do <i>New York Times</i> e vencedor do Pulitzer (2013). Escreve sobre "
            "negócios, ciência comportamental e produtividade.",
            "<i>O Poder do Hábito</i> (2012) reúne casos da neurociência, do marketing "
            "industrial e da história empresarial para mostrar como hábitos individuais, "
            "organizacionais e sociais funcionam com a mesma engrenagem básica.",
            "Sua obra subsequente, <i>Mais Esperto, Mais Rápido, Melhor</i>, expande as "
            "ideias para a produtividade e a gestão de equipes."],
        "big_idea": ("O cérebro é uma máquina de poupar energia: tudo que pode automatizar, "
                     "automatiza. Hábitos são as rotinas que ele cria para liberar atenção "
                     "para o novo. O problema é que ele não distingue bons e maus hábitos — "
                     "automatiza com igual eficiência o exercício diário e o cigarro depois do café."),
        "big_idea_extra": [
            "Duhigg, ao longo do livro, organiza o estudo dos hábitos em três círculos "
            "concêntricos: hábitos individuais, hábitos organizacionais e hábitos sociais. "
            "Em todos, o mesmo loop opera — e em todos, há janelas práticas para mudar."],
        "chapters": [
            {"num": "01", "kicker": "Parte 1 · Indivíduo",
             "title": "O loop do hábito",
             "intro": ("O cérebro forma hábitos em uma estrutura de três etapas: <b>deixa</b> "
                       "(gatilho), <b>rotina</b> (comportamento) e <b>recompensa</b>. Com a repetição, "
                       "a rotina deixa de ser decisão consciente e vira automática."),
             "bullets": [
                 "<b>Deixa</b>: a pista que o cérebro reconhece (hora, lugar, emoção, pessoa, ação anterior).",
                 "<b>Rotina</b>: o comportamento em si — físico ou mental.",
                 "<b>Recompensa</b>: o que satisfaz e ensina o cérebro a repetir.",
                 "O exemplo do <b>Pepsodent</b> de Claude Hopkins: a sensação de frescor "
                 "como recompensa explícita criou o hábito da escovação no Ocidente.",
             ],
             "quote": "Hábitos nunca desaparecem de fato — eles ficam codificados nas estruturas do nosso cérebro.",
             "callout_label": "REGRA",
             "callout": "Não tente extinguir o hábito. Mantenha deixa e recompensa, substitua a rotina."},

            {"num": "02", "kicker": "Parte 1 · Indivíduo",
             "title": "O anseio cria o hábito",
             "intro": ("Hopkins não inventou o desejo por dentes limpos — ele criou o "
                       "<b>anseio</b> pela sensação de boca fresca. Quando o cérebro começa a "
                       "antecipar a recompensa, o hábito se firma."),
             "bullets": [
                 "Anseio (<i>craving</i>) é o motor invisível: a expectativa da recompensa.",
                 "Sem anseio, a deixa não dispara a rotina.",
                 "Mudança de hábito eficaz desenha um anseio claro e atingível.",
                 "Marqueteiros do século XX (Hopkins, Febreze) descobriram isso antes da neurociência confirmar.",
             ],
             "callout_label": "INSIGHT",
             "callout": "Anseio é o que separa um hábito tentativo de um hábito formado. Sem ele, você precisa de força de vontade — com ele, o hábito se cuida sozinho."},

            {"num": "03", "kicker": "Parte 1 · Indivíduo",
             "title": "A regra de ouro da mudança",
             "intro": ("<b>Mesma deixa, mesma recompensa, rotina diferente</b>. Esse é o eixo de "
                       "qualquer transformação comportamental durável. Funciona em vícios, em treinos "
                       "de atletas (Michael Phelps), em recuperação de Alcoólicos Anônimos."),
             "bullets": [
                 "Você não 'quebra' um hábito — você reescreve a rotina entre deixa e recompensa.",
                 "Crença + comunidade aumentam drasticamente a eficácia (AA).",
                 "Phelps tinha 'vídeo mental' programado antes de cada prova — uma rotina ativada pela deixa do despertador.",
                 "O sistema só se sustenta quando você confia que pode mudar — daí o papel da fé/comunidade.",
             ],
             "quote": "A regra de ouro do hábito: você não pode extinguir um mau hábito; só pode trocá-lo por outro.",
             "callout_label": "INVERSÃO",
             "callout": "Disciplina pura quase nunca dura. Diagnóstico do loop + nova rotina + comunidade dura."},

            {"num": "04", "kicker": "Parte 2 · Organizações",
             "title": "Hábitos angulares",
             "intro": ("Existem certos hábitos — Duhigg os chama de <b>angulares</b> "
                       "(<i>keystone habits</i>) — que, quando mudam, arrastam dezenas de outros junto. "
                       "Encontrá-los é a alavanca da transformação organizacional e pessoal."),
             "bullets": [
                 "Na <b>Alcoa</b>, Paul O'Neill reduziu acidentes a quase zero focando apenas em segurança — e a empresa cresceu cinco vezes.",
                 "Exercício físico é um hábito angular: melhora alimentação, sono, foco e disposição.",
                 "Hábitos angulares geram <b>pequenas vitórias</b> que aumentam autoeficácia.",
                 "Identifique o hábito cuja melhora afetaria mais áreas da sua vida — ataque esse.",
             ],
             "callout_label": "PROCURE",
             "callout": "Qual hábito, se mudasse, mudaria outros 5? Esse é o angular. Comece por ele, mesmo que pareça pequeno."},

            {"num": "05", "kicker": "Parte 2 · Organizações",
             "title": "Starbucks e o hábito do sucesso",
             "intro": ("A Starbucks transformou recrutas frequentemente sem ensino superior "
                       "em uma das forças de atendimento mais qualificadas do varejo. O segredo "
                       "foi ensinar <b>hábitos de força de vontade</b> — programas como o LATTE — "
                       "para lidar com momentos de stress."),
             "bullets": [
                 "Força de vontade é um músculo: cansa com o uso e fortalece com treino.",
                 "Hábitos automatizam a força de vontade nos momentos críticos.",
                 "Protocolo <b>LATTE</b>: Listen, Acknowledge, Take action, Thank, Explain.",
                 "Funcionários treinam respostas para crises antes que elas aconteçam.",
             ],
             "callout_label": "PRINCÍPIO",
             "callout": "Roteiros prontos para crises previsíveis poupam o melhor da sua força de vontade para crises imprevisíveis."},

            {"num": "06", "kicker": "Parte 2 · Organizações",
             "title": "Crise é janela de mudança",
             "intro": ("Rhode Island Hospital, Aeronáutica… Duhigg mostra que organizações mudam de "
                       "verdade depois de crises severas. Líderes sábios não esperam — eles "
                       "<b>criam</b> mini-crises (auditorias, fracassos públicos) para liberar "
                       "energia de mudança."),
             "bullets": [
                 "Crises desfazem hábitos institucionais cristalizados.",
                 "Mudança requer um momento de descoberta seguido de protocolo claro.",
                 "Sem protocolo, a crise volta à inércia.",
                 "Antecipe a crise: simule-a antes de viver.",
             ],
             "callout_label": "TÁTICA",
             "callout": "Use crises (suas e da sua organização) como janelas para reorganizar hábitos — antes que elas se fechem."},

            {"num": "07", "kicker": "Parte 3 · Sociedade",
             "title": "Target e os hábitos do consumidor",
             "intro": ("O caso da Target prevendo gravidez de uma adolescente antes do pai — só "
                       "pelos seus hábitos de compra — abre o estudo dos hábitos sociais. Empresas "
                       "leem padrões; o público inteiro tem hábitos previsíveis."),
             "bullets": [
                 "Hábitos comprados em sequência criam <b>impressões digitais</b> previsíveis.",
                 "Quando um cliente entra em transição de vida (mudança, gravidez, divórcio), os hábitos quebram — janela de marketing.",
                 "Lojas embaralham promoções para que o cliente novo crie hábitos com a marca.",
                 "Você é mais previsível do que acredita; saber disso é defesa.",
             ],
             "callout_label": "ALERTA",
             "callout": "Suas escolhas têm padrões. Quem os vê — empresa, algoritmo — pode prever (e induzir) suas decisões."},

            {"num": "08", "kicker": "Parte 3 · Sociedade",
             "title": "Como movimentos sociais se sustentam",
             "intro": ("O caso de Rosa Parks e Montgomery: o boicote durou porque hábitos "
                       "<b>fortes</b> (amizades próximas), <b>fracos</b> (conhecidos da igreja) e "
                       "<b>novos</b> (compromisso público) se encadearam."),
             "bullets": [
                 "Hábitos fortes (família/amigos próximos) iniciam o movimento.",
                 "Hábitos fracos (círculos secundários) amplificam.",
                 "Hábitos novos (compromisso visível) sustentam.",
                 "Movimentos que duram desenham os três; movimentos que evaporam só têm o primeiro.",
             ],
             "callout_label": "ESCALA",
             "callout": "Mudança grande precisa de redes mistas: pessoas próximas iniciam, conhecidas amplificam, públicas sustentam."},

            {"num": "09", "kicker": "Epílogo",
             "title": "Hábitos e responsabilidade",
             "intro": ("Duhigg fecha o livro com um dilema legal: somos responsáveis por atos "
                       "cometidos em hábito (sonâmbulo que mata, jogador compulsivo)? A resposta dele: "
                       "sim, quando podemos identificar o loop. Conhecer o hábito é responsabilizar-se por ele."),
             "bullets": [
                 "Hábito não é destino — é só uma estrutura repetida.",
                 "Identificar o loop é tornar consciente o inconsciente.",
                 "Você é responsável pelos hábitos que conhece.",
                 "Mudar exige diagnóstico, plano e fé/comunidade.",
             ],
             "quote": "Uma vez que você entende que hábitos podem mudar, você tem a liberdade — e a responsabilidade — de refazê-los.",
             "callout_label": "ÚLTIMA REGRA",
             "callout": "Você não pode escolher se tem hábitos. Pode escolher se vai conhecê-los."},
        ],
        "insights": [
            ("01", "A 60–95% do nosso comportamento é hábito",
             "Pesquisas citadas por Duhigg estimam que entre 40% e 60% das ações diárias "
             "são feitas em piloto automático. O percentual sobe quando incluímos pensamentos."),
            ("02", "O cérebro não tem 'departamento de moral'",
             "A mesma engrenagem que automatiza o exercício automatiza o cigarro. Mudar exige "
             "engenharia, não julgamento."),
            ("03", "Hábito angular é alavanca",
             "Um hábito-chave bem escolhido carrega outros consigo. Procure o seu — quase "
             "sempre relacionado a corpo, foco ou sono."),
            ("04", "Crença muda hábitos",
             "AA, Phelps, Alcoa — o ingrediente comum dos hábitos duradouros é a crença "
             "de que mudança é possível, frequentemente sustentada por comunidade."),
            ("05", "Marqueteiros leem hábitos como livro",
             "Sua trilha de compras revela seu momento de vida. Saber disso ajuda a "
             "comprar com mais consciência."),
            ("06", "Crise é matéria-prima de mudança",
             "Espere a crise; ou crie uma mini-crise controlada — uma auditoria, "
             "uma exposição. Sem ela, hábitos não se mexem."),
        ],
        "application": [
            ("Diagnostique 1 hábito", "Escolha um hábito que queira mudar. Identifique no papel a deixa, a rotina e a recompensa."),
            ("Encontre o anseio real", "O que o cérebro realmente busca? Pausa? Conexão? Reconhecimento? Energia? Faça o experimento de substituir a rotina por outra que dê a mesma recompensa."),
            ("Escreva o plano", "<b>Quando [deixa] ocorrer, eu vou [nova rotina] porque me dará [recompensa].</b> Cole onde você vê."),
            ("Identifique seu hábito angular", "Liste 5 hábitos que, se você implantasse, mudariam várias áreas. Escolha um e foque por 60 dias."),
            ("Use uma comunidade", "Conte para 1 pessoa o que está mudando e por quê. Atualize-a semanalmente."),
            ("Reveja mensalmente", "O hábito está mais automático? Que micro-ajustes restam? O sistema, não a força de vontade, é o que sustenta."),
        ],
        "quotes": [
            ("A vida toda, tal como a conhecemos, é uma massa de hábitos.", "William James, citado por Duhigg"),
            ("Você não pode extinguir um mau hábito; só pode trocá-lo.", "A regra de ouro"),
            ("O cérebro não distingue bons hábitos de maus.", "Charles Duhigg"),
            ("Mude o hábito angular e o resto vem junto.", "Princípio Alcoa"),
            ("Sem crença, mudanças não duram.", "Estudo dos AA"),
            ("Hábitos liberam atenção. A questão é em que você gasta a atenção liberada.", "Síntese"),
            ("Quando o anseio aparece, a rotina já começou.", "Mecânica do loop"),
        ],
        "reflections": [
            "Qual hábito recorrente seu, sem julgamento, melhor descreve quem você foi nesta última semana?",
            "Qual a deixa, a rotina e a recompensa do hábito que você mais quer mudar?",
            "Que hábito angular, se implantado, mudaria 5 outras áreas da sua vida?",
            "Você está usando uma comunidade ou está tentando mudar sozinho — sabendo que sozinho quase nunca dura?",
            "Que pequena crise você pode criar essa semana para destravar um hábito antigo?",
            "Em que momento da sua agenda a sua força de vontade já está esgotada — e portanto seus hábitos comandam?",
        ],
        "last_word_title": "Pequenos cliques.",
        "last_word_quote": "Hábito não é prisão. Habitar um corpo, uma rotina, um trabalho é construir, dia a dia, a casa que você terminará morando.",
    },

    # ─── 05 · Mindset ─────────────────────────────────
    {
        "id": "mindset", "vol": "05",
        "title_main": "Mindset.", "title_sub": "A nova psicologia.",
        "short_title": "Mindset",
        "subtitle": "A nova psicologia do sucesso.",
        "author": "Carol S. Dweck",
        "year_orig": "2006", "year_br": "2007", "publisher": "Objetiva",
        "pages": "Aproximadamente 312 páginas", "pages_count": 25,
        "genre": "Psicologia · Educação · Desenvolvimento",
        "category_kicker": "Psicologia · Educação · Aprendizagem",
        "motif": "arrows",
        "palette": {"paper": "#F0EDE5", "ink": "#1F2933", "accent": "#A52A2A",
                    "muted": "#7A7569", "hairline": "#CFC8B5", "subink": "#2F3946",
                    "paper_dark": "#DFDBD0"},
        "abstract": ("Resumo de <b>Mindset</b> da psicóloga de Stanford Carol S. Dweck. "
                     "Reúne a distinção entre mentalidade fixa e de crescimento, exemplos "
                     "do esporte, educação e negócios, e o protocolo para virar a chave."),
        "thesis": "Não é o talento que define a sua trajetória, é a mentalidade com que você encara o esforço, a falha e a crítica.",
        "headline_quote": "O passe que você consegue dar não é mais importante do que o passe que você ainda não consegue dar.",
        "about_author": [
            "<b>Carol S. Dweck</b> é uma das psicólogas mais importantes em "
            "motivação e aprendizagem do nosso tempo. Professora em Stanford, dedicou "
            "décadas ao estudo de por que algumas pessoas prosperam diante de dificuldades "
            "enquanto outras desmoronam.",
            "Seu conceito de <i>mindset</i> — mentalidade — saiu dos laboratórios de psicologia "
            "infantil para virar vocabulário comum em escolas, empresas e clubes esportivos. "
            "<i>Mindset</i> (2006) consolidou décadas de pesquisa em linguagem acessível.",
            "Seu trabalho influenciou políticas educacionais (treinos para professores), "
            "estratégias de RH (Microsoft adotou explicitamente) e o discurso público sobre "
            "talento e meritocracia."],
        "big_idea": ("Existem, no fundo, duas formas de encarar o que se tem a aprender. A "
                     "<b>mentalidade fixa</b> trata habilidades como dom — você tem ou não tem; "
                     "esforço prova fraqueza; crítica é insulto; sucesso dos outros é ameaça. A "
                     "<b>mentalidade de crescimento</b> trata habilidades como músculo: "
                     "esforço é o caminho; crítica é informação; sucesso dos outros é inspiração."),
        "big_idea_extra": [
            "Dweck mostra, ao longo do livro, como essa distinção opera em áreas tão diversas "
            "quanto esporte (Mia Hamm, John Wooden), educação infantil, relacionamentos amorosos "
            "e gestão de empresas (Enron × GE)."],
        "chapters": [
            {"num": "01", "kicker": "Cap. 1",
             "title": "As duas mentalidades",
             "intro": ("Dweck apresenta a distinção fundamental: pessoas com mentalidade fixa "
                       "acreditam que inteligência, talento, caráter são fixos; pessoas com mentalidade "
                       "de crescimento acreditam que se desenvolvem com esforço, estratégia e ajuda."),
             "bullets": [
                 "<b>Fixa</b>: 'Você é inteligente.' / 'Você é burro.' Identidade rígida.",
                 "<b>Crescimento</b>: 'Você ainda não sabe.' / 'Vamos achar uma estratégia diferente.' Identidade aberta.",
                 "Quase ninguém é 100% fixa ou 100% de crescimento — variamos por domínio.",
                 "A boa notícia: mentalidade é, em si, aprendida. E portanto, mutável.",
             ],
             "callout_label": "TESTE-SE",
             "callout": "Onde você é mais fixa? No trabalho, no corpo, nas relações? É exatamente ali que o crescimento começa."},

            {"num": "02", "kicker": "Cap. 2",
             "title": "Dentro das mentalidades",
             "intro": ("A mentalidade muda quase tudo: como interpretamos elogios, como reagimos a "
                       "rejeição, o que escolhemos como meta, como lidamos com o sucesso dos outros, "
                       "e principalmente como tratamos o esforço."),
             "bullets": [
                 "Mentalidade fixa evita desafios — pode expor fraqueza.",
                 "Mentalidade de crescimento procura desafios — é onde se aprende.",
                 "Para a fixa, esforço é prova de incompetência.",
                 "Para a de crescimento, esforço é o caminho para o domínio.",
             ],
             "quote": "Esforço é o que torna alguém realmente bom em alguma coisa.",
             "callout_label": "DIAGNÓSTICO",
             "callout": "Se você precisa parecer talentoso, está na fixa. Se você quer ficar bom, está na de crescimento."},

            {"num": "03", "kicker": "Cap. 3",
             "title": "A verdade sobre talento",
             "intro": ("Dweck destrói o mito do talento puro examinando estrelas (Michael Jordan, "
                       "Tiger Woods, Mozart). Em quase todos os casos, há por trás horas absurdas de "
                       "prática deliberada. Talento começa como ponto de partida; chega-se a alguém "
                       "só pela mentalidade de crescimento."),
             "bullets": [
                 "Michael Jordan foi cortado do time da escola — voltou e dobrou os treinos.",
                 "Mozart compôs música utilizável só depois de 10 anos de treino orientado pelo pai.",
                 "Prática deliberada (com correção) > tempo passado fazendo.",
                 "Quem se acha 'talentoso' frequentemente para antes da prática deliberada.",
             ],
             "callout_label": "ANTÍDOTO AO TALENTO",
             "callout": "Talento é o capital inicial. Mentalidade de crescimento é a taxa de juros — a longo prazo, ganha."},

            {"num": "04", "kicker": "Cap. 4",
             "title": "Esporte: a mentalidade dos campeões",
             "intro": ("Mia Hamm, John McEnroe, Pete Sampras, John Wooden. Estudos comparativos "
                       "mostram que campeões duradouros raramente são os mais talentosos do começo "
                       "— são os mais persistentes ao falhar e os mais focados em aprender."),
             "bullets": [
                 "Wooden, lendário técnico da UCLA, nunca prometeu vitória — prometeu esforço total.",
                 "Atletas fixos colapsam após uma derrota. De crescimento dobram o treino.",
                 "Treino é onde se ganha o jogo seguinte.",
                 "Os superastros costumam ter os hábitos de treino mais chatos do vestiário.",
             ],
             "callout_label": "REGRA WOODEN",
             "callout": "Não é se você venceu. É se você fez seu melhor para se preparar e jogar — esse é o placar real."},

            {"num": "05", "kicker": "Cap. 5",
             "title": "Negócios: a mentalidade da liderança",
             "intro": ("Enron exemplifica empresas com mentalidade fixa (cultura do 'gênio'); GE sob "
                       "Jack Welch, e a Microsoft sob Satya Nadella, exemplificam a virada para "
                       "mentalidade de crescimento — com efeitos cascata em inovação e cultura."),
             "bullets": [
                 "Cultura do gênio → política de aparências → mentiras corporativas.",
                 "Cultura de crescimento → curiosidade → erros falados → aprendizagem.",
                 "Líderes fixos contratam por pedigree; de crescimento contratam por trajetória.",
                 "Satya Nadella explicitamente reposicionou a Microsoft como 'learn-it-all' em vez de 'know-it-all'.",
             ],
             "callout_label": "LÍDER",
             "callout": "A pergunta de um líder de crescimento não é 'quem é mais inteligente?' — é 'quem aprende mais rápido?'."},

            {"num": "06", "kicker": "Cap. 6",
             "title": "Relacionamentos: amor de mentalidade",
             "intro": ("Pessoas com mentalidade fixa esperam encontrar 'a pessoa certa' — perfeita "
                       "desde o início. Pessoas com mentalidade de crescimento esperam <b>construir</b> "
                       "uma relação certa com a pessoa escolhida. Dois esquemas radicalmente diferentes."),
             "bullets": [
                 "Fixa: 'se ele me amasse, leria minha mente'. Crescimento: 'preciso dizer'.",
                 "Conflito, para fixos, é sinal de incompatibilidade. Para de crescimento, é matéria de trabalho.",
                 "Bullying na escola é alimentado por mentalidade fixa dos dois lados.",
                 "Casais que duram têm conflitos — e revisões.",
             ],
             "callout_label": "AMOR",
             "callout": "Amor saudável não é descoberta — é construção. Quem espera achar a pessoa certa, frequentemente passa por ela sem notar."},

            {"num": "07", "kicker": "Cap. 7",
             "title": "Pais, professores, treinadores",
             "intro": ("A pesquisa mais influente de Dweck: <b>elogiar o esforço</b> (em vez do "
                       "talento) produz crianças que escolhem desafios. Elogiar o talento produz "
                       "crianças que escolhem segurança e mentem para parecer espertas."),
             "bullets": [
                 "<b>Elogio nocivo</b>: 'Você é tão inteligente!'",
                 "<b>Elogio nutritivo</b>: 'Você se esforçou muito; viu a sua estratégia mudar?'",
                 "Inserir 'ainda' ('You're not there yet') muda a relação com o erro.",
                 "Adultos significativos (pais, professores) são, sobretudo, modelos de mentalidade.",
             ],
             "callout_label": "REGRA DE OURO",
             "callout": "Elogie processo, não pessoa. Critique processo, não pessoa. A pessoa cresce; a etiqueta congela."},

            {"num": "08", "kicker": "Cap. 8",
             "title": "Mudando mentalidades",
             "intro": ("Como virar a chave? Dweck propõe um caminho de quatro passos: (1) reconhecer a "
                       "voz da mentalidade fixa, (2) perceber que você tem escolha, (3) responder de "
                       "volta com a voz de crescimento, (4) agir conforme o novo discurso."),
             "bullets": [
                 "Passo 1: ouvir a voz fixa ('você não nasceu pra isso').",
                 "Passo 2: notar que é só uma voz, não a verdade.",
                 "Passo 3: respondê-la conscientemente ('vou tentar e ver').",
                 "Passo 4: agir antes que a voz fixa volte.",
             ],
             "quote": "Pessoas com mentalidade de crescimento são pessoas que se mantiveram em movimento mesmo quando alguém — inclusive elas — disseram que era impossível.",
             "callout_label": "PROTOCOLO",
             "callout": "1. Reconheça a voz. 2. Saiba que tem escolha. 3. Responda. 4. Aja. Pratique até virar default."},
        ],
        "insights": [
            ("01", "Não é uma vs outra; é momento vs momento",
             "Ninguém é 100% de um lado. Reconheça em quais áreas e situações a sua mentalidade fixa aparece — e nelas faça o trabalho."),
            ("02", "Talento não é injusto; mentalidade é",
             "O talento te dá uma vantagem inicial. A mentalidade te dá ou te tira a vida toda. A injustiça maior é a mentalidade fixa."),
            ("03", "'Ainda' é a palavra mais útil do livro",
             "Adicionar 'ainda' ao final de qualquer 'eu não sei' muda a sentença e o cérebro: 'eu não sei → eu não sei ainda'."),
            ("04", "Elogie esforço, não pessoa",
             "É a descoberta mais replicada de Dweck. Vale para pais com filhos, gestores com times, treinadores com atletas — e você consigo."),
            ("05", "Conflito é sinal de relação viva",
             "Em parceria saudável, conflito é matéria-prima. A ausência dele é sinal de evitação, não de harmonia."),
            ("06", "Mentalidade fixa é frágil — por isso reage feio",
             "Pessoas em mentalidade fixa atacam quando se sentem ameaçadas. Não é mau caráter — é fragilidade de identidade."),
        ],
        "application": [
            ("Mapeie suas áreas fixas", "Liste 3 áreas em que você reage com defesa, evita desafio ou pensa 'não nasci pra isso'. São suas frentes de trabalho."),
            ("Mude o vocabulário", "Adicione 'ainda' a toda frase de incapacidade. 'Eu não sei programar → eu não sei programar ainda.'"),
            ("Procure um desafio público por mês", "Escolha algo em que você possa visivelmente fracassar. O risco mata a mentalidade fixa."),
            ("Refaça o elogio que você dá", "Para filhos, equipes, parceiros: elogie esforço, estratégia, progresso. Nunca 'você é genial'."),
            ("Trate crítica como dado", "Quando alguém te critica, anote em uma frase: 'o que aqui pode ser verdade?' Antes de defender."),
            ("Reveja semanalmente", "Pergunte: 'em que momento esta semana eu reagi como mentalidade fixa?' E o que faria diferente."),
        ],
        "quotes": [
            ("Esforço é o que torna alguém realmente bom em alguma coisa.", "Carol Dweck"),
            ("Você ainda não chegou — ainda.", "O poder do 'yet'"),
            ("Pessoas com mentalidade fixa precisam provar; com mentalidade de crescimento, melhorar.", "Resumo Dweck"),
            ("O fracasso é informação. Nada além disso.", "Princípio da pesquisa"),
            ("Não é se você nasceu inteligente — é se você está disposto a se tornar mais inteligente.", "Dweck"),
            ("Elogie processo. A pessoa cresce; a etiqueta congela.", "Regra de ouro de elogio"),
            ("Você é o que você está disposto a tentar quando ninguém está olhando.", "Síntese"),
        ],
        "reflections": [
            "Em qual área da sua vida sua mentalidade fixa aparece mais? Como você sabe?",
            "Qual elogio recorrente você dá às pessoas próximas — e está formando a mentalidade delas para o quê?",
            "Que crítica recente te machucou — e qual parte dela, posto o ego de lado, tinha alguma verdade?",
            "Qual desafio público você está adiando porque pode te expor — e portanto te ensinar?",
            "Onde você adia esforço porque 'não nasceu pra isso' — sabendo que essa é a voz fixa falando?",
            "Que filho, aluno ou colaborador seu precisa ouvir 'ainda' no fim das frases dele esta semana?",
        ],
        "last_word_title": "Ainda.",
        "last_word_quote": "Mentalidade não é otimismo. É a recusa, todos os dias, em deixar uma versão antiga sua decidir o tamanho da versão nova.",
    },

    # ─── 06 · O Milagre da Manhã ─────────────────────
    {
        "id": "milagre_manha", "vol": "06",
        "title_main": "O Milagre", "title_sub": "da Manhã.",
        "short_title": "O Milagre da Manhã",
        "subtitle": "O segredo que vai transformar sua vida (antes das 8h).",
        "author": "Hal Elrod",
        "year_orig": "2012", "year_br": "2016", "publisher": "Bestseller",
        "pages": "Aproximadamente 224 páginas", "pages_count": 25,
        "genre": "Desenvolvimento pessoal · Rotinas",
        "category_kicker": "Rotina · Disciplina · Manhã",
        "motif": "sunrise",
        "palette": {"paper": "#FBF5E9", "ink": "#1A2540", "accent": "#E07B2E",
                    "muted": "#857C66", "hairline": "#D7CFB4", "subink": "#2A375A",
                    "paper_dark": "#EEE5C8"},
        "abstract": ("Resumo de <b>O Milagre da Manhã</b>, livro de Hal Elrod que popularizou a "
                     "rotina <b>SAVERS</b> — Silêncio, Afirmações, Visualização, Exercício, "
                     "Leitura e Escrita. Inclui o método de implantação em 30 dias."),
        "thesis": "A forma como você acorda determina a qualidade do seu dia. Conquistar a primeira hora é conquistar o resto.",
        "headline_quote": "O nível de sucesso que você alcança raramente ultrapassa o nível do seu desenvolvimento pessoal.",
        "about_author": [
            "<b>Hal Elrod</b> é palestrante e autor norte-americano. Sobreviveu a um acidente "
            "automobilístico aos 20 anos — clinicamente morto por 6 minutos, recuperou-se de "
            "lesões cerebrais e voltou a andar contra prognóstico médico.",
            "Anos depois, em outra crise (financeira, em 2008), começou a praticar uma rotina "
            "matinal baseada em seis hábitos. <i>O Milagre da Manhã</i> (2012) sistematiza essa rotina "
            "como o método <b>SAVERS</b>.",
            "Hoje é fenômeno global de comunidade — com versões do livro para diferentes áreas "
            "(escritores, casais, vendedores)."],
        "big_idea": ("Quase todo mundo acorda já em modo reativo — celular, notícias, urgências "
                     "alheias. Elrod propõe inverter: a primeira hora do dia é entregue para o "
                     "<b>seu</b> desenvolvimento. Seis práticas, ditas SAVERS, ocupam essa janela. "
                     "Não é heroísmo: é um sistema replicável."),
        "big_idea_extra": [
            "A premissa central é simples: pequenas práticas matinais, mantidas por semanas, "
            "alteram a química do dia inteiro. Acumuladas por meses, alteram a química da vida."],
        "chapters": [
            {"num": "S", "kicker": "Primeira letra · S",
             "title": "Silêncio",
             "intro": ("Comece o dia em silêncio: meditação, oração, respiração consciente, "
                       "gratidão silenciosa. Não importa a forma — importa interromper o ruído "
                       "antes que ele te capture."),
             "bullets": [
                 "Antes do celular, antes da notícia, antes de pensar no dia.",
                 "5 a 10 minutos bastam para começar.",
                 "Respiração 4-4-4-4 (caixa) é boa porta de entrada.",
                 "Silêncio é o solo para tudo que vem depois.",
             ],
             "callout_label": "REGRA",
             "callout": "Quem entrega os primeiros minutos ao silêncio, entrega o resto do dia para si. Quem entrega ao telefone, entrega o resto pra fora."},

            {"num": "A", "kicker": "Segunda letra · A",
             "title": "Afirmações",
             "intro": ("Frases concretas, no presente, sobre quem você está se tornando — "
                       "ditas em voz alta. Não 'positivas' por positividade: <b>afirmativas</b> "
                       "como reforço de identidade."),
             "bullets": [
                 "Boa afirmação: 'Eu sou alguém que cuida do corpo todos os dias.'",
                 "Não funcionam frases falsas — funcionam frases verdadeiras orientando o futuro.",
                 "Ler em voz alta vale mais do que ler mentalmente.",
                 "Reescreva semanalmente; ajuste à versão atual do seu propósito.",
             ],
             "callout_label": "PRINCÍPIO",
             "callout": "Afirmações não são feitiço; são contratos com você mesmo. Funcionam quando você cumpre o contrato."},

            {"num": "V", "kicker": "Terceira letra · V",
             "title": "Visualização",
             "intro": ("Imagine, em detalhes sensoriais, o seu dia ideal e a sua vida ideal. "
                       "Sentir o que se quer cria estado emocional propício para agir como quem já "
                       "vive aquilo."),
             "bullets": [
                 "Visualize o processo, não só o resultado.",
                 "5 minutos: 2 para o dia que começa, 3 para a vida que se constrói.",
                 "Atletas profissionais usam essa técnica há décadas.",
                 "Não é fantasia: é ensaio mental de comportamento.",
             ],
             "callout_label": "CIÊNCIA",
             "callout": "Visualizar movimento ativa as mesmas regiões do cérebro que executá-lo. Use isso a seu favor."},

            {"num": "E", "kicker": "Quarta letra · E",
             "title": "Exercício",
             "intro": ("Mover o corpo pela manhã energiza, melhora foco, libera endorfinas e — "
                       "talvez mais importante — confirma identidade. Quem treina pela manhã, "
                       "começa o dia já vencendo."),
             "bullets": [
                 "5 a 20 minutos bastam: alongamento, caminhada, polichinelos, ioga.",
                 "Não é treino fitness — é despertar do corpo.",
                 "Coloque a roupa na noite anterior (atrito zero).",
                 "Sai do estado 'sono' e entra no estado 'dia'.",
             ],
             "callout_label": "ATRITO",
             "callout": "A roupa de treino ao lado da cama vale mais do que motivação. Engenheire o ambiente."},

            {"num": "R", "kicker": "Quinta letra · R",
             "title": "Leitura",
             "intro": ("10 páginas por dia de um livro que te desenvolve. Acumulado em um ano: 12 a "
                       "18 livros — bem acima da média do brasileiro. Lendo só na manhã."),
             "bullets": [
                 "10 páginas × 365 dias = 3.650 páginas/ano.",
                 "Estima-se 12–18 livros por ano só com essa prática.",
                 "Prefira livros que mudem ações, não só ideias.",
                 "Marque uma frase por sessão; releia no fim do mês.",
             ],
             "callout_label": "MATEMÁTICA",
             "callout": "10 páginas por manhã durante 30 anos = 300 livros. É uma biblioteca a mais de vida — só com a manhã."},

            {"num": "S", "kicker": "Sexta letra · S (Scribing)",
             "title": "Escrita",
             "intro": ("Escrever no papel — diário, gratidão, intenção, pendências mentais. A "
                       "escrita manuscrita organiza pensamento e libera espaço cognitivo para o "
                       "resto do dia."),
             "bullets": [
                 "Inclua: três coisas pelas quais você é grato.",
                 "Uma intenção para o dia.",
                 "Uma preocupação que você quer 'esvaziar da cabeça'.",
                 "Releia ao fim da semana para enxergar padrões.",
             ],
             "callout_label": "REGRA",
             "callout": "O que sai do papel sai da cabeça. Cabeça liberada é foco disponível."},

            {"num": "30", "kicker": "Método",
             "title": "Os 30 dias da virada",
             "intro": ("Elrod propõe um período de implantação em três fases de 10 dias cada. As "
                       "fases não são apenas de tempo — são de fricção mental que ele descreve "
                       "explicitamente para que o leitor reconheça e atravesse."),
             "bullets": [
                 "<b>Dias 1–10 · Insuportável</b>: o cérebro luta. É só persistir.",
                 "<b>Dias 11–20 · Desconfortável</b>: começa a fazer sentido, mas ainda exige esforço.",
                 "<b>Dias 21–30 · Imparável</b>: a rotina começa a se sustentar sozinha.",
                 "Saber em qual fase você está reduz o risco de abandono.",
             ],
             "quote": "A primeira hora do dia é o leme do barco inteiro.",
             "callout_label": "REGRA DOS 30",
             "callout": "Não julgue a rotina pelos primeiros 10 dias. Avalie depois do 21º — quando ela começa a se sustentar."},

            {"num": "Y", "kicker": "Extra",
             "title": "Personalizando os SAVERS",
             "intro": ("A ordem é flexível. O tempo total também — pode ser feito em 60 minutos "
                       "ou em 6 (versão acelerada). O importante é não pular nenhuma das seis letras."),
             "bullets": [
                 "Versão completa: 60 minutos (10 em cada).",
                 "Versão mínima: 6 minutos (1 em cada).",
                 "Em viagens ou dias caóticos, a versão de 6 minutos cumpre o mínimo viável.",
                 "Adapte; o que não pode é desistir de uma letra.",
             ],
             "callout_label": "FLEXIBILIDADE",
             "callout": "Melhor 6 minutos por 30 dias do que 60 minutos por 5. Consistência ganha."},
        ],
        "insights": [
            ("01", "Pequena rotina, vida grande",
             "Uma hora investida na manhã é a maior alavanca de tempo da vida adulta — afeta as outras 23."),
            ("02", "Acordar cedo não é virtude — é estratégia",
             "Não há mérito moral em acordar 5h. Há vantagem prática: ninguém te interrompe nos minutos mais nutritivos do dia."),
            ("03", "Sair da cama é meio caminho",
             "A maior parte da batalha é levantar. Coloque o despertador longe da cama. Decida na noite anterior."),
            ("04", "Manhã é identidade",
             "Você é o que você faz com as suas primeiras horas. Não o que pensa, planeja ou jura — o que faz."),
            ("05", "Comunidade acelera o hábito",
             "Grupos de prática (online ou presencial) aumentam drasticamente a aderência aos SAVERS."),
            ("06", "Sucesso é externo — desenvolvimento é interno",
             "Mais importante que o resultado é o tipo de pessoa que você vira ao manter a rotina."),
        ],
        "application": [
            ("Defina seu horário", "Escolha que horas você vai acordar pelos próximos 30 dias. Coloque o despertador longe."),
            ("Prepare na noite anterior", "Roupa de treino, copo com água, livro aberto, caderno na mesa. Atrito zero."),
            ("Comece pela versão mínima", "Faça os 6 minutos por uma semana antes de tentar a versão completa."),
            ("Anote a sequência", "Marque um X no calendário cada manhã. Não falhe dois dias seguidos."),
            ("Encontre 1 parceiro", "Conte para 1 pessoa o que você está fazendo. Atualize-a semanalmente."),
            ("Reveja após 30 dias", "O que da rotina ficou? O que mudou no dia inteiro? Ajuste pelo que aprendeu."),
        ],
        "quotes": [
            ("A forma como você acorda determina a qualidade do dia.", "Hal Elrod"),
            ("A primeira hora é o leme do barco.", "Síntese SAVERS"),
            ("10 páginas × 30 anos = uma biblioteca a mais.", "Matemática da manhã"),
            ("Não é a rotina perfeita — é a rotina mantida.", "Hal Elrod"),
            ("Identidade nova começa numa hora nova.", "Princípio do hábito matinal"),
            ("Você é o que faz nos primeiros 60 minutos.", "Síntese"),
            ("A rotina não te liberta — te devolve.", "Síntese do leitor"),
        ],
        "reflections": [
            "Como você acorda hoje? Honestamente, descreva os primeiros 60 minutos.",
            "Qual das 6 letras dos SAVERS você mais resiste a fazer — e o que isso te diz?",
            "Que atrito da noite anterior poderia ser eliminado para tornar a manhã inevitável?",
            "Com quem você poderia compartilhar essa rotina para criar responsabilidade mútua?",
            "Em que fase da virada de 30 dias você costuma abandonar — e o que faria diferente desta vez?",
            "Se você mantivesse a rotina por 90 dias, quem você seria — e por que essa pessoa não está aqui?",
        ],
        "last_word_title": "Acorde antes do dia.",
        "last_word_quote": "Não se trata de acordar cedo. Trata-se de conquistar uma hora — qualquer hora — que pertença a você antes que o mundo a tome.",
    },

    # ─── 07 · Pai Rico, Pai Pobre ─────────────────────
    {
        "id": "pai_rico", "vol": "07",
        "title_main": "Pai Rico,", "title_sub": "Pai Pobre.",
        "short_title": "Pai Rico, Pai Pobre",
        "subtitle": "O que os ricos ensinam aos seus filhos sobre dinheiro.",
        "author": "Robert T. Kiyosaki",
        "year_orig": "1997", "year_br": "2000", "publisher": "Alta Books",
        "pages": "Aproximadamente 336 páginas", "pages_count": 25,
        "genre": "Educação financeira · Negócios",
        "category_kicker": "Finanças · Educação financeira · Mentalidade",
        "motif": "coin",
        "palette": {"paper": "#EEEFE7", "ink": "#0E2E2A", "accent": "#9C7E2F",
                    "muted": "#6F7568", "hairline": "#C7C7B5", "subink": "#1B403B",
                    "paper_dark": "#DCDDCB"},
        "abstract": ("Resumo de <b>Pai Rico, Pai Pobre</b>, manifesto de Robert Kiyosaki sobre "
                     "educação financeira. Reúne a distinção entre ativos e passivos, as 6 lições, "
                     "o quadrante do fluxo de caixa e o roteiro prático para sair da corrida do rato."),
        "thesis": "Não é o quanto você ganha — é o quanto você guarda, faz crescer e quantas gerações você banca com isso.",
        "headline_quote": "Os ricos compram ativos. Os pobres só têm despesas. A classe média compra passivos que acha que são ativos.",
        "about_author": [
            "<b>Robert Toru Kiyosaki</b> é um empresário e educador financeiro norte-americano, "
            "nascido em 1947 no Havaí. Filho de um professor PhD (o 'pai pobre'), foi adotado "
            "intelectualmente pelo pai de um amigo (o 'pai rico') — empresário sem diploma "
            "formal.",
            "<i>Pai Rico, Pai Pobre</i> (1997) contrasta os dois mentores e organiza, em "
            "diálogos didáticos, princípios que Kiyosaki diz nunca terem entrado na escola "
            "tradicional.",
            "É autor de mais de 25 livros da série Pai Rico, fundador da Rich Dad Company e "
            "criador de jogos educacionais como o <i>CASHFLOW</i>. Sua obra é polêmica entre "
            "economistas — mas o impacto cultural na educação financeira é inegável."],
        "big_idea": ("A escola te treina para ser empregado — não para ser rico. Para inverter o "
                     "padrão familiar, é preciso aprender o que os ricos ensinam aos próprios "
                     "filhos em casa: a diferença entre ativo e passivo, o papel da educação "
                     "financeira, o uso dos impostos, a criação de fontes de renda passiva."),
        "big_idea_extra": [
            "Kiyosaki organiza o livro em torno de seis lições do pai rico e termina com o "
            "famoso <b>quadrante do fluxo de caixa</b>: Empregado, Autônomo, Dono de Negócio e "
            "Investidor. Cada um tem regras tributárias e modos de pensar próprios."],
        "chapters": [
            {"num": "01", "kicker": "Lição 1",
             "title": "Os ricos não trabalham por dinheiro",
             "intro": ("Os ricos fazem o dinheiro trabalhar por eles. A maioria das pessoas, "
                       "presa no medo de não ter e na avidez por ter mais, vive uma vida inteira "
                       "perseguindo salários."),
             "bullets": [
                 "Medo e ganância são os dois lados do mesmo padrão do <i>pai pobre</i>.",
                 "A frase 'eu não posso comprar' é desempoderadora — 'como eu posso comprar?' libera criatividade.",
                 "Trabalhar por dinheiro mantém você na corrida do rato.",
                 "Fazer o dinheiro trabalhar por você exige educação financeira.",
             ],
             "callout_label": "REGRA",
             "callout": "Não pergunte 'eu posso?'. Pergunte 'como eu posso?'. A segunda forma mantém o cérebro trabalhando."},

            {"num": "02", "kicker": "Lição 2",
             "title": "Por que ensinar educação financeira",
             "intro": ("A escola não ensina dinheiro. O resultado é uma geração inteira de "
                       "profissionais qualificados financeiramente analfabetos. A primeira "
                       "alfabetização financeira é a distinção entre ativo e passivo."),
             "bullets": [
                 "<b>Ativo</b>: algo que coloca dinheiro no seu bolso.",
                 "<b>Passivo</b>: algo que tira dinheiro do seu bolso.",
                 "Casa própria, segundo Kiyosaki, costuma ser passivo (não ativo).",
                 "Riqueza = ativos que geram renda passiva, não patrimônio nominal.",
             ],
             "quote": "A casa onde você mora é frequentemente o maior passivo da sua vida — e você foi ensinado a chamá-la de ativo.",
             "callout_label": "DEFINIÇÃO",
             "callout": "Ativo gera renda. Passivo gera despesa. Saber a diferença é alfabetização — sem ela, salários se viram em contas."},

            {"num": "03", "kicker": "Lição 3",
             "title": "Cuide do seu próprio negócio",
             "intro": ("Não confunda <b>profissão</b> com <b>negócio</b>. Profissão é o que paga "
                       "as contas; negócio é o conjunto de ativos que cresce ao longo da vida. A "
                       "maioria cuida da profissão e abandona o negócio."),
             "bullets": [
                 "Profissão paga; negócio compõe.",
                 "Comece pequeno: um investimento, um pequeno negócio paralelo, um imóvel.",
                 "Reinvista os ganhos no próprio negócio antes de comprar passivos.",
                 "Trate seu negócio como um filho — exige tempo e paciência.",
             ],
             "callout_label": "REGRA",
             "callout": "Sua profissão paga o jantar. Seu negócio prepara o jantar dos seus netos."},

            {"num": "04", "kicker": "Lição 4",
             "title": "A história dos impostos e o poder das corporações",
             "intro": ("O sistema tributário foi criado historicamente para taxar os ricos — mas "
                       "estes adaptaram-se via corporações, criando uma das maiores assimetrias do "
                       "capitalismo: empregados ganham, pagam imposto e gastam; ricos ganham, "
                       "gastam (deduzindo) e pagam imposto sobre o que sobra."),
             "bullets": [
                 "Empregado: ganha → imposto → gasta.",
                 "Rico: ganha (via empresa) → gasta (deduzindo) → paga imposto sobre o resto.",
                 "Educação financeira inclui inteligência tributária.",
                 "Não é truque — é o sistema. Quem não aprende, paga a conta dos que aprenderam.",
             ],
             "callout_label": "ASSIMETRIA",
             "callout": "A diferença entre rico e empregado não é renda; é em qual ordem o imposto chega."},

            {"num": "05", "kicker": "Lição 5",
             "title": "Os ricos inventam dinheiro",
             "intro": ("Riqueza não é só herdada — é inventada. Empreendedores criam valor onde "
                       "não havia: tecnologia, negócios, contratos, oportunidades. A criatividade "
                       "financeira é uma habilidade aprendida."),
             "bullets": [
                 "Oportunidades costumam aparecer disfarçadas de problemas.",
                 "Risco controlado supera segurança paralisante.",
                 "Educação financeira inclui contabilidade, investimento, mercado e lei.",
                 "Inteligência financeira tem 4 partes: contábil, de investimento, de mercado, jurídica.",
             ],
             "callout_label": "INVENTIVIDADE",
             "callout": "Riqueza não é o que se acha — é o que se constrói. Quem só guarda, no fim, perde para a inflação."},

            {"num": "06", "kicker": "Lição 6",
             "title": "Trabalhe para aprender, não para ganhar",
             "intro": ("Jovens prendem-se ao primeiro emprego pelo salário. Kiyosaki sugere o "
                       "contrário: aceite menos dinheiro para ter mais aprendizado. As habilidades "
                       "adquiridas pagam mais tarde do que qualquer salário paga agora."),
             "bullets": [
                 "Os 5 saberes-chave: gestão de fluxo, gestão de sistemas, gestão de pessoas, vendas e marketing.",
                 "Especialização extrema = vulnerabilidade.",
                 "Generalistas com educação financeira ganham mais a longo prazo.",
                 "Aprenda vendas, mesmo que odeie — é a habilidade mais transferível do mundo dos negócios.",
             ],
             "quote": "O motivo número um pelo qual os pobres permanecem pobres é porque foram ensinados a serem pobres em casa.",
             "callout_label": "INVESTIMENTO",
             "callout": "Aceite menos hoje pelo aprendizado certo — e cobre a conta com juros amanhã."},

            {"num": "07", "kicker": "Síntese",
             "title": "O quadrante do fluxo de caixa",
             "intro": ("Após as 6 lições, Kiyosaki organiza tudo em 4 quadrantes: <b>E</b> "
                       "(Empregado), <b>A</b> (Autônomo), <b>D</b> (Dono de Negócio) e <b>I</b> "
                       "(Investidor). Cada um tem regras próprias — de imposto, de tempo, de "
                       "liberdade."),
             "bullets": [
                 "<b>E</b>: trabalha por salário. Tempo = dinheiro.",
                 "<b>A</b>: trabalha por hora, mas para si. Tempo continua = dinheiro.",
                 "<b>D</b>: tem sistemas e equipe trabalhando por ele.",
                 "<b>I</b>: tem dinheiro trabalhando por ele.",
                 "Riqueza durável vem dos lados D e I, não E e A.",
             ],
             "callout_label": "MIGRAÇÃO",
             "callout": "Você pode estar em E hoje. A questão é: o que você está fazendo todo mês para migrar para D ou I?"},

            {"num": "08", "kicker": "Caminho",
             "title": "Saindo da corrida do rato",
             "intro": ("A 'corrida do rato' é o ciclo: ganhar para gastar, pegar emprestado, "
                       "trabalhar mais. Para sair, é preciso desenhar fluxo de caixa — entender "
                       "onde o dinheiro vai e por que."),
             "bullets": [
                 "Faça o seu balanço pessoal: ativos × passivos.",
                 "Antes de aumentar receita, reduza passivos.",
                 "Cada nova receita extra deve comprar 1 ativo, não 1 passivo.",
                 "A corrida do rato é mental antes de ser financeira.",
             ],
             "callout_label": "PROTOCOLO",
             "callout": "Saída da corrida: 1. Reconheça o ciclo. 2. Construa o primeiro ativo. 3. Não compre passivos com a renda do ativo. 4. Repita."},
        ],
        "insights": [
            ("01", "Riqueza não é renda — é renda passiva",
             "Ganhar muito e gastar tudo é classe média. Riqueza é quando a renda passiva supera o custo de vida."),
            ("02", "Sua casa pode ser seu maior passivo",
             "Provocação central de Kiyosaki. Antes de comprar, calcule: ela coloca ou tira dinheiro do seu bolso?"),
            ("03", "Educação financeira é alfabetização do século XXI",
             "Sem ela, salários se desfazem em contas. Com ela, qualquer salário começa a render."),
            ("04", "Imposto não é injustiça — é sistema",
             "Não é raiva, é estudo. Quem aprende as regras do imposto paga menos. É lícito e disponível."),
            ("05", "Risco é função de conhecimento",
             "O que é arriscado para o leigo é seguro para o estudado. A diferença não é coragem; é educação."),
            ("06", "A corrida do rato é mental",
             "Aumentar salário sem mudar mentalidade só aumenta o passivo. Saúde financeira começa nas crenças, não na renda."),
        ],
        "application": [
            ("Faça seu balanço pessoal", "Liste todos seus ativos (geram renda) e passivos (geram despesa). A maioria leva um susto na primeira vez."),
            ("Calcule sua renda passiva atual", "Quanto entra no seu bolso por mês sem você trabalhar? Esse é o número que importa de fato."),
            ("Compre seu primeiro ativo este mês", "Mesmo pequeno: uma cota de fundo imobiliário, uma ação dividendária, um investimento. O hábito importa."),
            ("Não compre passivos com sobra", "Cada sobra de renda deve, antes, virar ativo. Só compre passivos quando a renda passiva já cobre."),
            ("Aprenda 1 habilidade do quadrante D/I", "Vendas, contabilidade, marketing, investimento, gestão de pessoas. Escolha uma e dedique 30 dias."),
            ("Eduque-se 10 minutos por dia", "Podcast, livro, curso. Educação financeira tem retorno composto altíssimo a longo prazo."),
        ],
        "quotes": [
            ("Ativo gera renda. Passivo gera despesa.", "Definição-mãe"),
            ("Trabalhe para aprender, não para ganhar.", "Lição 6"),
            ("Os ricos não trabalham por dinheiro — fazem o dinheiro trabalhar.", "Lição 1"),
            ("Sua casa pode ser seu maior passivo.", "Provocação central"),
            ("Riqueza é tempo. Tempo de não precisar trabalhar.", "Princípio do quadrante"),
            ("A escola não te ensina dinheiro. O resto, é por sua conta.", "Síntese"),
            ("Não pergunte 'eu posso?'. Pergunte 'como eu posso?'.", "Pai rico"),
        ],
        "reflections": [
            "Quantos meses você sobreviveria sem trabalhar — usando apenas o que já entra no seu bolso?",
            "Qual é seu maior passivo disfarçado de ativo — provavelmente uma casa, um carro, um cartão?",
            "Em qual quadrante (E, A, D, I) você está hoje? E em qual quer estar em 5 anos?",
            "Que pequena receita passiva você poderia começar a construir nos próximos 90 dias?",
            "Você foi ensinado a pensar dinheiro em casa? Como? Quem foi seu 'pai pobre' e quem foi seu 'pai rico'?",
            "Quanto da sua renda este ano foi para ativos e quanto foi para passivos?",
        ],
        "last_word_title": "Pague-se primeiro.",
        "last_word_quote": "Riqueza não é uma corrida — é uma direção. O primeiro real que vai para um ativo já te coloca em outra estrada.",
    },

    # Para encurtar este arquivo, os 11 livros restantes seguem no próximo arquivo
    # com a mesma estrutura. Aqui paramos no Vol. 07.
]


# ═══════════════════════════════════════════════════════
# BOOKS continuação (carrega configs adicionais de outro módulo)
# ═══════════════════════════════════════════════════════

def load_more_books():
    """Carrega os Vols. 08-18 + 19-38."""
    result = []
    try:
        import books_data
        result.extend(books_data.MORE_BOOKS)
    except ImportError:
        pass
    try:
        import books_data_2
        result.extend(books_data_2.MORE_BOOKS_2)
    except ImportError:
        pass
    return result


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

ALL_BOOKS_META = [
    # 3 já feitos
    {"vol": "01", "title_main": "Hábitos", "title_sub": "Atômicos.", "author": "James Clear",
     "category_kicker": "Comportamento · Desenvolvimento pessoal",
     "thesis": "Você não se eleva ao nível das suas metas — cai ao nível dos seus sistemas.",
     "headline_quote": "Hábitos são os juros compostos do autoaperfeiçoamento.",
     "pages_count": 39, "year_orig": "2018", "genre": "Comportamento · Desenvolvimento",
     "palette": {"accent": "#1B4D3E"}},
    {"vol": "02", "title_main": "O", "title_sub": "Alquimista.", "author": "Paulo Coelho",
     "category_kicker": "Fábula · Filosófico · Literatura brasileira",
     "thesis": "Quando você quer alguma coisa, todo o universo conspira para que você realize o seu desejo.",
     "headline_quote": "Maktub. Está escrito.",
     "pages_count": 30, "year_orig": "1988", "genre": "Romance · Fábula filosófica",
     "palette": {"accent": "#9C6B1F"}},
    {"vol": "03", "title_main": "A Sutil Arte", "title_sub": "de Ligar o F*da-Se.", "author": "Mark Manson",
     "category_kicker": "Desenvolvimento pessoal · Contraintuitivo",
     "thesis": "Não dar a mínima não é apatia. É escolher exatamente sobre o que se importar.",
     "headline_quote": "Escolha o seu sofrimento.",
     "pages_count": 22, "year_orig": "2016", "genre": "Desenvolvimento · Contraintuitivo",
     "palette": {"accent": "#E55A1F"}},
]


def main():
    print("Gerando volumes 04 a 18 + catálogo...")
    BOOKS_COMBINED = BOOKS + load_more_books()
    generated = []
    for book in BOOKS_COMBINED:
        out = build_book(book)
        print(f"  [OK] Vol. {book['vol']}  {book['title_main']} {book['title_sub'].rstrip('.')}  → {out}")
        ALL_BOOKS_META.append({
            "vol": book["vol"],
            "title_main": book["title_main"],
            "title_sub": book["title_sub"],
            "author": book["author"],
            "category_kicker": book.get("category_kicker", "—"),
            "thesis": book["thesis"],
            "headline_quote": book["headline_quote"],
            "pages_count": book["pages_count"],
            "year_orig": book.get("year_orig", "—"),
            "genre": book.get("genre", "—"),
            "palette": book.get("palette", {}),
        })
        generated.append(out)
    # ordenar por vol
    ALL_BOOKS_META.sort(key=lambda b: int(b["vol"]))
    cat = build_catalog(ALL_BOOKS_META)
    print(f"  [OK] Catálogo  → {cat}")
    print(f"Total: {len(generated)} volumes novos + 1 catálogo.")


if __name__ == "__main__":
    main()
