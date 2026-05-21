"""
Gerador de PDF — Resumo de "A Sutil Arte de Ligar o F*da-Se" (Mark Manson).
Vol. 03 da série. Design tipo manifesto: alto contraste, páginas pretas,
laranja Manson, tipografia super-display.
"""

import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, Table, TableStyle, NextPageTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.flowables import Flowable

OUTPUT = "/home/user/taskflow-pro/A_Sutil_Arte_Resumo.pdf"

# ─── Patch setCharSpace ──────────────────────────────────
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

# ─────────────────────────────────────────────────────
# PALETA — alto contraste · Manson signature
# ─────────────────────────────────────────────────────
PAPER     = HexColor("#F6F1E7")  # cream-bege quente, levemente off-white
INK       = HexColor("#0E0E0E")  # preto
DARK      = HexColor("#0E0E0E")  # fundo escuro nas pgs pretas
SUBINK    = HexColor("#2A2A2A")
MUTED     = HexColor("#7A736A")
HAIRLINE  = HexColor("#D7D0BF")
ORANGE    = HexColor("#E55A1F")  # laranja Manson
ORANGE_DK = HexColor("#C24E1A")
CREAM     = HexColor("#F6F1E7")
CREAM_DIM = HexColor("#B8AE96")   # creme escurecido (para texto em fundo preto)

PAGE_W, PAGE_H = A4
MARGIN_L = 2.4*cm
MARGIN_R = 2.4*cm
MARGIN_T = 2.6*cm
MARGIN_B = 2.4*cm


# ─────────────────────────────────────────────────────
# FLOWABLES
# ─────────────────────────────────────────────────────

class HLine(Flowable):
    def __init__(self, width, thickness=0.4, color=HAIRLINE, space_after=0):
        Flowable.__init__(self)
        self.width = width; self.thickness = thickness
        self.color = color; self.space_after = space_after
        self.height = thickness + space_after
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.space_after, self.width, self.space_after)


class BigChapterNum(Flowable):
    """Numeral display em laranja gigante — abre cada capítulo."""
    def __init__(self, width, number, kicker=None):
        Flowable.__init__(self)
        self.width = width; self.number = str(number)
        self.kicker = kicker
        self.height = 3.4*cm

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 96)
        c.setFillColor(ORANGE)
        c.setCharSpace(-5)
        c.drawString(0, 0.3*cm, self.number)
        c.setCharSpace(0)
        from reportlab.pdfbase.pdfmetrics import stringWidth
        w = stringWidth(self.number, "Helvetica-Bold", 96)
        # marca de asterisco do lado
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(w + 0.4*cm, 0.4*cm, "*")
        # kicker em maiúsculas
        if self.kicker:
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(INK)
            c.setCharSpace(2.5)
            c.drawString(w + 0.4*cm, 2.7*cm, self.kicker.upper())
            c.setCharSpace(0)


class BlackCallout(Flowable):
    """Callout inverso: fundo preto, texto creme, acento laranja."""
    def __init__(self, width, text, label="REGRA", padding=0.55*cm):
        Flowable.__init__(self)
        self.width = width; self.text = text
        self.label = label; self.padding = padding
        # remove tags para o cálculo de quebra
        plain = text.replace("<b>", "").replace("</b>", "")
        from reportlab.pdfbase.pdfmetrics import stringWidth
        font, size = "Helvetica", 10
        avail = width - 2*padding
        line = ""; lines = 1
        for w in plain.split():
            test = (line + " " + w).strip()
            if stringWidth(test, font, size) <= avail: line = test
            else: lines += 1; line = w
        self.height = lines * size * 1.45 + 2*padding

    def _tokenize(self, text):
        """Quebra texto em (word, bold) tokens preservando <b>...</b>."""
        out = []; i = 0; bold = False
        buf = ""
        while i < len(text):
            if text[i:i+3] == "<b>":
                if buf:
                    for w in buf.split(): out.append((w, bold))
                    buf = ""
                bold = True; i += 3
            elif text[i:i+4] == "</b>":
                if buf:
                    for w in buf.split(): out.append((w, bold))
                    buf = ""
                bold = False; i += 4
            else:
                buf += text[i]; i += 1
        if buf:
            for w in buf.split(): out.append((w, bold))
        return out

    def _wrap_rich(self, tokens, avail, base_font, bold_font, size):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        lines = [[]]; line_w = 0
        for word, b in tokens:
            f = bold_font if b else base_font
            ww = stringWidth(word + " ", f, size)
            if line_w + ww > avail and lines[-1]:
                lines.append([]); line_w = 0
            lines[-1].append((word, b)); line_w += ww
        return lines

    def draw(self):
        c = self.canv
        h = self.height; w = self.width
        c.setFillColor(INK); c.rect(0, 0, w, h, stroke=0, fill=1)
        c.setFillColor(ORANGE); c.rect(0, 0, 0.18*cm, h, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(ORANGE); c.setCharSpace(2)
        c.drawString(self.padding, h - self.padding + 0.05*cm, self.label.upper())
        c.setCharSpace(0)
        # texto rico
        tokens = self._tokenize(self.text)
        avail = w - 2*self.padding
        lines = self._wrap_rich(tokens, avail, "Helvetica", "Helvetica-Bold", 10)
        y = h - self.padding - 0.5*cm
        from reportlab.pdfbase.pdfmetrics import stringWidth
        for line in lines:
            x = self.padding
            for word, b in line:
                f = "Helvetica-Bold" if b else "Helvetica"
                c.setFont(f, 10)
                c.setFillColor(CREAM)
                c.drawString(x, y, word)
                x += stringWidth(word + " ", f, 10)
            y -= 10 * 1.45


class ContrastQuote(Flowable):
    """Pull quote: barra laranja vertical + texto preto em itálico."""
    def __init__(self, width, text, attribution=None):
        Flowable.__init__(self)
        self.width = width; self.text = text
        self.attribution = attribution
        from reportlab.pdfbase.pdfmetrics import stringWidth
        font, size = "Helvetica-Oblique", 15
        avail = width - 0.8*cm
        line = ""; lines = 1
        for w in text.split():
            test = (line + " " + w).strip()
            if stringWidth(test, font, size) <= avail: line = test
            else: lines += 1; line = w
        self.height = lines * size * 1.35 + (0.5*cm if attribution else 0) + 0.6*cm

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
        # barra laranja grossa à esquerda
        c.setFillColor(ORANGE)
        c.rect(0, 0, 0.18*cm, self.height, stroke=0, fill=1)
        # texto em itálico bold sans (não serif — coerente com manifesto)
        c.setFont("Helvetica-Oblique", 15)
        c.setFillColor(INK)
        lines = self._wrap(self.text, self.width - 0.8*cm, "Helvetica-Oblique", 15)
        y = self.height - 15
        for ln in lines:
            c.drawString(0.6*cm, y, ln)
            y -= 15 * 1.35
        if self.attribution:
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(MUTED)
            c.setCharSpace(2)
            c.drawString(0.6*cm, y - 0.15*cm, self.attribution.upper())
            c.setCharSpace(0)


class StrikeList(Flowable):
    """Lista com checkbox — itens com possibilidade de risco (estilo "não dou a mínima para...")."""
    def __init__(self, width, items, box_size=0.32*cm, line_height=0.62*cm):
        Flowable.__init__(self)
        self.width = width; self.items = items
        self.box_size = box_size; self.line_height = line_height
        self.height = 0
        from reportlab.pdfbase.pdfmetrics import stringWidth
        font, size = "Helvetica", 10
        avail = width - box_size - 0.5*cm
        for item, _ in items:
            words = item.split()
            line = ""; lines = 1
            for w in words:
                test = (line + " " + w).strip()
                if stringWidth(test, font, size) <= avail: line = test
                else: lines += 1; line = w
            self.height += lines * size * 1.35 + 0.22*cm
        self.height += 0.3*cm

    def draw(self):
        c = self.canv
        font, size = "Helvetica", 10
        y = self.height - size
        for item, struck in self.items:
            # checkbox quadrado (não preenchido se não struck, X laranja se struck)
            c.setStrokeColor(INK)
            c.setLineWidth(0.6)
            box_y = y + size * 0.05
            c.rect(0, box_y, self.box_size, self.box_size, stroke=1, fill=0)
            if struck:
                # X laranja
                c.setStrokeColor(ORANGE)
                c.setLineWidth(1.4)
                c.line(0, box_y, self.box_size, box_y + self.box_size)
                c.line(0, box_y + self.box_size, self.box_size, box_y)
            # texto
            from reportlab.pdfbase.pdfmetrics import stringWidth
            tx = self.box_size + 0.35*cm
            avail = self.width - tx
            words = item.split()
            lines = []; line = ""
            for w in words:
                test = (line + " " + w).strip()
                if stringWidth(test, font, size) <= avail: line = test
                else: lines.append(line); line = w
            if line: lines.append(line)
            c.setFont(font, size)
            c.setFillColor(INK)
            ly = y
            for ln in lines:
                c.drawString(tx, ly, ln)
                # se struck, risca por cima
                if struck:
                    c.setStrokeColor(ORANGE)
                    c.setLineWidth(1.0)
                    w_ln = stringWidth(ln, font, size)
                    c.line(tx, ly + size*0.3, tx + w_ln, ly + size*0.3)
                ly -= size * 1.35
            y -= len(lines) * size * 1.35 + 0.22*cm


class ValueComparison(Flowable):
    """Tabela visual: valor ruim ←→ valor bom. Pares lado a lado com flecha."""
    def __init__(self, width, pairs):
        Flowable.__init__(self)
        self.width = width; self.pairs = pairs
        # cada par ocupa altura proporcional ao número de linhas do texto
        self.row_h = 1.6*cm
        self.height = len(pairs) * self.row_h + 0.5*cm

    def draw(self):
        c = self.canv
        n = len(self.pairs)
        col_w = (self.width - 1.6*cm) / 2  # 1.6cm para a flecha + paddings
        for i, (bad, good) in enumerate(self.pairs):
            y_top = self.height - i * self.row_h
            y_mid = y_top - self.row_h / 2
            # caixa esquerda (mau valor)
            c.setStrokeColor(HAIRLINE)
            c.setLineWidth(0.4)
            c.line(0, y_top - self.row_h, self.width, y_top - self.row_h)
            # lado esquerdo
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(INK)
            c.drawString(0, y_mid - 4, f"{i+1:02d}.")
            c.setFont("Helvetica", 10.5)
            c.setFillColor(SUBINK)
            c.drawString(0.9*cm, y_mid - 4, bad)
            # flecha laranja no meio
            ax = col_w + 0.2*cm
            c.setStrokeColor(ORANGE)
            c.setLineWidth(1.4)
            c.line(ax, y_mid, ax + 1.2*cm, y_mid)
            # ponta da flecha
            c.line(ax + 1.2*cm, y_mid, ax + 1.0*cm, y_mid + 0.15*cm)
            c.line(ax + 1.2*cm, y_mid, ax + 1.0*cm, y_mid - 0.15*cm)
            # lado direito
            c.setFont("Helvetica-Bold", 10.5)
            c.setFillColor(ORANGE_DK)
            c.drawString(col_w + 1.6*cm, y_mid - 4, good)


class ReflectionLines(Flowable):
    """Pergunta provocadora + linhas pautadas."""
    def __init__(self, width, prompt, num_lines=3, line_spacing=0.78*cm):
        Flowable.__init__(self)
        self.width = width; self.prompt = prompt
        self.num_lines = num_lines; self.line_spacing = line_spacing
        from reportlab.pdfbase.pdfmetrics import stringWidth
        font, size = "Helvetica-Bold", 11
        avail = width
        words = prompt.split()
        line = ""; lines = 1
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, font, size) <= avail: line = test
            else: lines += 1; line = w
        self.q_height = lines * size * 1.35 + 0.3*cm
        self.height = self.q_height + num_lines * line_spacing + 0.2*cm

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
        # asterisco laranja como bullet
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(ORANGE)
        c.drawString(0, self.height - 12, "*")
        # pergunta em bold sans
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(INK)
        lines = self._wrap(self.prompt, self.width - 0.7*cm, "Helvetica-Bold", 11)
        y = self.height - 11
        for ln in lines:
            c.drawString(0.55*cm, y, ln)
            y -= 11 * 1.35
        # linhas
        c.setStrokeColor(HAIRLINE)
        c.setLineWidth(0.3)
        y_base = self.height - self.q_height
        for i in range(self.num_lines):
            yy = y_base - (i+1) * self.line_spacing
            c.line(0, yy, self.width, yy)


# ─────────────────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────────────────

def make_styles():
    s = {}
    s["label"] = ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=8, leading=11,
                                 textColor=ORANGE, alignment=TA_LEFT, spaceAfter=4)
    s["label_dark"] = ParagraphStyle("label_dark", fontName="Helvetica-Bold", fontSize=8, leading=11,
                                      textColor=ORANGE, alignment=TA_LEFT, spaceAfter=4)
    s["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=26, leading=30,
                                   textColor=INK, alignment=TA_LEFT, spaceBefore=2, spaceAfter=4)
    s["h2"] = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12.5, leading=16,
                              textColor=INK, alignment=TA_LEFT, spaceBefore=10, spaceAfter=3)
    s["h3"] = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10, leading=14,
                              textColor=ORANGE_DK, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4)
    s["body"] = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=15.5,
                                textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)
    s["body_small"] = ParagraphStyle("body_small", fontName="Helvetica", fontSize=9, leading=13,
                                      textColor=SUBINK, alignment=TA_JUSTIFY, spaceAfter=4)
    s["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.7, leading=14,
                                  textColor=INK, alignment=TA_LEFT, leftIndent=14, bulletIndent=2,
                                  spaceAfter=2)
    s["lead"] = ParagraphStyle("lead", fontName="Helvetica", fontSize=12, leading=18,
                                textColor=SUBINK, alignment=TA_LEFT, spaceAfter=8)
    s["caption"] = ParagraphStyle("caption", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
                                   textColor=MUTED, alignment=TA_LEFT, spaceAfter=4)
    return s


# ─────────────────────────────────────────────────────
# DESENHO DAS PÁGINAS
# ─────────────────────────────────────────────────────

def draw_paper_bg(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

def draw_dark_bg(c):
    c.setFillColor(DARK)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)


def draw_cover(c, doc):
    draw_dark_bg(c)
    # rule topo creme
    c.setStrokeColor(CREAM)
    c.setLineWidth(0.7)
    c.line(MARGIN_L, PAGE_H - 1.6*cm, PAGE_W - MARGIN_L, PAGE_H - 1.6*cm)
    # marca topo
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(CREAM)
    c.setCharSpace(3)
    c.drawString(MARGIN_L, PAGE_H - 1.25*cm, "RESUMO · VOL. 03")
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.25*cm, "ED. MAIO 2026")
    c.setCharSpace(0)

    # numeral "03" gigante em laranja
    c.setFont("Helvetica-Bold", 260)
    c.setFillColor(ORANGE)
    c.setCharSpace(-12)
    c.drawString(MARGIN_L - 0.5*cm, PAGE_H - 11.5*cm, "03")
    c.setCharSpace(0)

    # asterisco gigante atrás
    c.setFont("Helvetica-Bold", 200)
    c.setFillColor(HexColor("#1A1A1A"))
    c.drawString(PAGE_W - 11*cm, PAGE_H - 14.5*cm, "*")

    # categoria
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(ORANGE)
    c.setCharSpace(2.5)
    c.drawString(MARGIN_L, PAGE_H - 13.2*cm, "DESENVOLVIMENTO PESSOAL  ·  CONTRAINTUITIVO  ·  MANIFESTO")
    c.setCharSpace(0)

    # título display — palavras grandes em creme
    c.setFont("Helvetica-Bold", 44)
    c.setFillColor(CREAM)
    c.setCharSpace(-1.5)
    c.drawString(MARGIN_L, PAGE_H - 15.4*cm, "A sutil arte")
    c.drawString(MARGIN_L, PAGE_H - 16.9*cm, "de ligar o")
    # "f*da-se" em LARANJA gigante
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 66)
    c.setCharSpace(-2)
    c.drawString(MARGIN_L, PAGE_H - 19.0*cm, "f*da-se.")
    c.setCharSpace(0)

    # subtítulo creme
    c.setFont("Helvetica", 12)
    c.setFillColor(CREAM_DIM)
    c.drawString(MARGIN_L, PAGE_H - 20.0*cm, "Uma estratégia inusitada para uma vida melhor.")

    # rule laranja
    c.setStrokeColor(ORANGE)
    c.setLineWidth(1.4)
    c.line(MARGIN_L, PAGE_H - 20.7*cm, MARGIN_L + 2.5*cm, PAGE_H - 20.7*cm)

    # autor
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(CREAM_DIM)
    c.setCharSpace(2)
    c.drawString(MARGIN_L, PAGE_H - 21.3*cm, "AUTOR ORIGINAL")
    c.setCharSpace(0)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(CREAM)
    c.drawString(MARGIN_L, PAGE_H - 22.0*cm, "Mark Manson")

    # rodapé
    c.setStrokeColor(CREAM)
    c.setLineWidth(0.5)
    c.line(MARGIN_L, 2.3*cm, PAGE_W - MARGIN_R, 2.3*cm)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(CREAM_DIM)
    c.setCharSpace(2.5)
    c.drawString(MARGIN_L, 1.7*cm, "CADERNO DE LEITURA  ·  RESUMO · MANIFESTO · CADERNO")
    c.drawRightString(PAGE_W - MARGIN_R, 1.7*cm, "FORMATO A4")
    c.setCharSpace(0)


def draw_body_chrome(c, doc):
    draw_paper_bg(c)
    # Header
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(MUTED)
    c.setCharSpace(2.5)
    c.drawString(MARGIN_L, PAGE_H - 1.3*cm, "A SUTIL ARTE")
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.3*cm, "MARK MANSON  ·  RESUMO 03")
    c.setCharSpace(0)
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.3)
    c.line(MARGIN_L, PAGE_H - 1.55*cm, PAGE_W - MARGIN_R, PAGE_H - 1.55*cm)
    # Footer
    page_num = c.getPageNumber()
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.3)
    c.line(MARGIN_L, 1.7*cm, PAGE_W - MARGIN_R, 1.7*cm)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(MUTED)
    c.setCharSpace(2.5)
    c.drawString(MARGIN_L, 1.3*cm, "RESUMO · LEITURA BREVE")
    c.setCharSpace(0)
    # asterisco laranja como marca
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(PAGE_W - MARGIN_R - 1.5*cm, 1.22*cm, "*")
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(INK)
    c.drawRightString(PAGE_W - MARGIN_R, 1.25*cm, f"{page_num:02d}")


def draw_dark_page(c, doc):
    """Página inteira preta — para manifesto, mantras, última palavra."""
    draw_dark_bg(c)
    # Header
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(MUTED)
    c.setCharSpace(2.5)
    c.drawString(MARGIN_L, PAGE_H - 1.3*cm, "A SUTIL ARTE")
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.3*cm, "MARK MANSON  ·  RESUMO 03")
    c.setCharSpace(0)
    c.setStrokeColor(HexColor("#2A2A2A"))
    c.setLineWidth(0.3)
    c.line(MARGIN_L, PAGE_H - 1.55*cm, PAGE_W - MARGIN_R, PAGE_H - 1.55*cm)
    # Footer
    page_num = c.getPageNumber()
    c.setStrokeColor(HexColor("#2A2A2A"))
    c.setLineWidth(0.3)
    c.line(MARGIN_L, 1.7*cm, PAGE_W - MARGIN_R, 1.7*cm)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(MUTED)
    c.setCharSpace(2.5)
    c.drawString(MARGIN_L, 1.3*cm, "RESUMO · LEITURA BREVE")
    c.setCharSpace(0)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(PAGE_W - MARGIN_R - 1.5*cm, 1.22*cm, "*")
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(CREAM)
    c.drawRightString(PAGE_W - MARGIN_R, 1.25*cm, f"{page_num:02d}")


# ─────────────────────────────────────────────────────
# BUILD
# ─────────────────────────────────────────────────────

def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title="A Sutil Arte de Ligar o F*da-Se — Resumo",
        author="Resumo a partir da obra de Mark Manson",
    )

    fw = PAGE_W - MARGIN_L - MARGIN_R
    fh = PAGE_H - MARGIN_T - MARGIN_B

    cover_frame = Frame(MARGIN_L, MARGIN_B, fw, fh, id="cover", showBoundary=0)
    body_frame  = Frame(MARGIN_L, MARGIN_B, fw, fh - 0.4*cm, id="body", showBoundary=0)
    dark_frame  = Frame(MARGIN_L, MARGIN_B, fw, fh - 0.4*cm, id="dark", showBoundary=0)

    templates = [
        PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover),
        PageTemplate(id="body",  frames=[body_frame],  onPage=draw_body_chrome),
        PageTemplate(id="dark",  frames=[dark_frame],  onPage=draw_dark_page),
    ]
    doc.addPageTemplates(templates)

    S = make_styles()
    story = []

    # ============ CAPA ============
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # ============ FICHA TÉCNICA ============
    story.append(Paragraph("FICHA TÉCNICA", S["label"]))
    story.append(Paragraph("Sobre esta edição.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Caderno de leitura de <b>A Sutil Arte de Ligar o F*da-Se</b>, manifesto "
        "contraintuitivo de Mark Manson. Reúne tese central, resumo dos 9 capítulos, "
        "tabela dos 5 valores ruins × 5 valores bons, mantras, provocações pessoais "
        "e espaço próprio para anotar.", S["lead"]))
    story.append(Spacer(1, 0.4*cm))

    ficha = [
        ["Título original",   "The Subtle Art of Not Giving a F*ck"],
        ["Título no Brasil",  "A Sutil Arte de Ligar o F*da-Se"],
        ["Autor",             "Mark Manson"],
        ["Editora (BR)",      "Editora Intrínseca"],
        ["Publicação",        "2016 (orig.) · 2017 (BR)"],
        ["Páginas (BR)",      "Aproximadamente 224 páginas"],
        ["Gênero",            "Desenvolvimento pessoal · Contraintuitivo"],
        ["Vendas globais",    "Acima de 15 milhões de exemplares"],
        ["Status no Brasil",  "Líder de vendas anos seguidos, fenômeno editorial"],
    ]
    t = Table(ficha, colWidths=[5.2*cm, fw - 5.2*cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 9.5),
        ("TEXTCOLOR", (0,0), (0,-1), MUTED),
        ("TEXTCOLOR", (1,0), (1,-1), INK),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("TOPPADDING", (0,0), (-1,-1), 9),
        ("LINEBELOW", (0,0), (-1,-1), 0.25, HAIRLINE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.6*cm))
    story.append(BlackCallout(fw,
        "Não dar a mínima não é apatia. É escolher exatamente sobre o que se "
        "importar — e ter coragem de não se importar com o resto.",
        label="A SUTILEZA EM UMA FRASE"))

    story.append(PageBreak())

    # ============ SUMÁRIO ============
    story.append(Paragraph("NAVEGAÇÃO", S["label"]))
    story.append(Paragraph("Sumário.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    sumario = [
        ("",    "Capa",                                     "1"),
        ("",    "Ficha técnica",                            "2"),
        ("",    "Sumário",                                  "3"),
        ("",    "Sobre o autor",                            "4"),
        ("",    "Tese — manifesto em uma página",           "5"),
        ("",    "Como ler este livro",                      "6"),
        ("01",  "Não tente",                                "7"),
        ("02",  "A felicidade é um problema",               "8"),
        ("03",  "Você não é especial",                      "9"),
        ("04",  "O valor do sofrimento",                   "10"),
        ("05",  "Você está sempre escolhendo",             "11"),
        ("06",  "Você está errado sobre tudo",             "12"),
        ("07",  "Falha é o caminho do sucesso",            "13"),
        ("08",  "A importância de dizer não",              "14"),
        ("09",  "… e depois, você morre",                  "15"),
        ("",    "Valores ruins × valores bons",            "16"),
        ("",    "Inversões mentais",                       "17"),
        ("",    "Mantras (não é positividade)",            "18"),
        ("",    "Provocações pessoais",                    "19"),
        ("",    "Eu não dou a mínima para…",               "20"),
        ("",    "Caderno",                                  "21"),
        ("",    "Última palavra",                           "22"),
    ]
    toc_main = ParagraphStyle("tocm", fontName="Helvetica", fontSize=10, leading=14,
                               textColor=INK, alignment=TA_LEFT)
    toc_meta = ParagraphStyle("tocmm", fontName="Helvetica", fontSize=10, leading=14,
                               textColor=SUBINK, alignment=TA_LEFT)
    rows = []
    for tag, title, pg in sumario:
        is_chap = tag.isdigit() or (len(tag) == 2 and tag[0] == "0")
        rows.append([tag if tag else "*",
                     Paragraph(title, toc_main if is_chap else toc_meta),
                     pg])
    tbl = Table(rows, colWidths=[1.1*cm, fw - 3.1*cm, 1.5*cm])
    cmds = [
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (0,-1), 9.5),
        ("TEXTCOLOR", (0,0), (0,-1), ORANGE),
        ("FONTNAME", (2,0), (2,-1), "Helvetica-Bold"),
        ("FONTSIZE", (2,0), (2,-1), 9.5),
        ("TEXTCOLOR", (2,0), (2,-1), MUTED),
        ("ALIGN", (2,0), (2,-1), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("LINEBELOW", (0,0), (-1,-2), 0.2, HAIRLINE),
    ]
    # destacar bloco dos capítulos com uma linha mais grossa antes/depois
    for i, (tag, _, _) in enumerate(sumario):
        if tag == "01":
            cmds.append(("LINEABOVE", (0,i), (-1,i), 0.7, INK))
            cmds.append(("TOPPADDING", (0,i), (-1,i), 10))
        if tag == "09":
            cmds.append(("LINEBELOW", (0,i), (-1,i), 0.7, INK))
            cmds.append(("BOTTOMPADDING", (0,i), (-1,i), 8))
    tbl.setStyle(TableStyle(cmds))
    story.append(tbl)

    story.append(PageBreak())

    # ============ SOBRE O AUTOR ============
    story.append(Paragraph("AUTOR", S["label"]))
    story.append(Paragraph("Sobre Mark Manson.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "<b>Mark Manson</b> é um escritor e blogueiro norte-americano nascido em 1984. "
        "Começou a publicar online em 2008, com textos sobre relacionamentos, "
        "autodesenvolvimento e cultura, em um tom que mistura linguagem direta de pub "
        "com leituras de filosofia (estoicismo, existencialismo, budismo) e ciência "
        "social.", S["body"]))
    story.append(Paragraph(
        "<i>A Sutil Arte de Ligar o F*da-Se</i> (2016) foi escrito a partir de um "
        "ensaio viral no seu blog. Manteve o tom irreverente do original e tornou-se "
        "um dos maiores fenômenos editoriais do século XXI, vendendo mais de 15 milhões "
        "de cópias mundialmente.", S["body"]))

    story.append(Paragraph("Linha do autor", S["h2"]))
    story.append(Paragraph(
        "Manson trabalha com <b>inversões</b>. Pega uma ideia popular de "
        "autoajuda — pense positivo, seja especial, vá atrás do sucesso — e mostra "
        "como ela frequentemente funciona ao contrário. A receita: pegue a expectativa, "
        "vire-a do avesso, e veja a verdade aparecer.", S["body"]))

    story.append(Paragraph("Outras obras", S["h2"]))
    livros = [
        "<b>Modelos: Atraia mulheres pela honestidade</b> (2011)",
        "<b>Tudo é F*da</b> (2019) — sequência do best-seller; tese sobre esperança e desespero.",
        "<b>Will</b> (com Will Smith, 2021) — autobiografia em co-autoria.",
    ]
    for l in livros:
        story.append(Paragraph("·  " + l, S["bullet"]))

    story.append(Spacer(1, 0.4*cm))
    story.append(ContrastQuote(fw,
        "Não importa o que você faça, sempre haverá alguma coisa difícil. "
        "Escolha o seu sofrimento.",
        attribution="Mark Manson · entrevistas"))

    story.append(NextPageTemplate("dark"))
    story.append(PageBreak())

    # ============ TESE / MANIFESTO (página preta) ============
    # frame escuro
    manifesto_label = ParagraphStyle("ml", fontName="Helvetica-Bold", fontSize=8, leading=11,
                                      textColor=ORANGE, alignment=TA_LEFT, spaceAfter=6)
    manifesto_title = ParagraphStyle("mt", fontName="Helvetica-Bold", fontSize=36, leading=40,
                                      textColor=CREAM, alignment=TA_LEFT, spaceAfter=10)
    manifesto_body = ParagraphStyle("mb", fontName="Helvetica", fontSize=13, leading=20,
                                     textColor=CREAM, alignment=TA_LEFT, spaceAfter=10)
    manifesto_em = ParagraphStyle("me", fontName="Helvetica-Bold", fontSize=13, leading=20,
                                   textColor=ORANGE, alignment=TA_LEFT, spaceAfter=10)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("MANIFESTO", manifesto_label))
    story.append(Paragraph("A tese, em uma página.", manifesto_title))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Existe um circuito vicioso em que entramos sem perceber: a gente <b>se sente "
        "mal</b> por estar se sentindo mal. A gente <b>se ressente</b> de ter se "
        "ressentido. A gente <b>se cobra</b> por não estar à altura da própria cobrança.",
        manifesto_body))
    story.append(Paragraph(
        "Manson chama isso de <i>feedback loop do inferno</i> — e diz que a saída "
        "começa em três sutilezas que viram do avesso a auto-ajuda comum:",
        manifesto_body))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("1.  Não dar a mínima não é indiferença — é seletividade.", manifesto_em))
    story.append(Paragraph("2.  Para não se importar com o desconforto, é preciso importar-se com algo maior.", manifesto_em))
    story.append(Paragraph("3.  Você está, agora, escolhendo o que te importa — escolha melhor.", manifesto_em))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Não é um manual contra o cuidado. É um manual contra o cuidado <b>diluído</b>. "
        "Há um número limitado de coisas com as quais se importar em uma vida. "
        "A liberdade começa quando você decide quais.", manifesto_body))

    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # ============ COMO LER ESTE LIVRO ============
    story.append(Paragraph("ANTES DE COMEÇAR", S["label"]))
    story.append(Paragraph("Como ler este livro.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Três avisos para tirar proveito da próxima sessão. Sem nenhum deles, "
        "Manson lê como ofensa. Com os três, lê como acordar.", S["lead"]))
    story.append(Spacer(1, 0.2*cm))

    avisos = [
        ("01", "Aceite que ele vai te irritar",
         "Manson usa palavrões e generalizações de propósito. Não é grosseria — é "
         "<b>técnica retórica</b>. Ele precisa quebrar a polidez intelectual para "
         "passar a ideia."),
        ("02", "Não confunda contraintuitivo com errado",
         "Várias frases dele parecem contrárias ao bom-senso. <b>Releia-as devagar</b>. "
         "Em quase todos os casos, há uma inversão deliberada que só se entende quando "
         "se segura a primeira reação."),
        ("03", "Use-o como espelho, não como manual",
         "O livro não te diz <i>o que</i> fazer. Ele te ajuda a perceber <i>como</i> "
         "você decide. Anote suas reações nas margens — elas dizem mais sobre você do "
         "que sobre o autor."),
    ]
    for num, tit, txt in avisos:
        # tabela com numeral grande à esquerda
        tbl = Table(
            [[num, Paragraph(f"<b>{tit}</b><br/>{txt}", S["body"])]],
            colWidths=[1.7*cm, fw - 1.7*cm]
        )
        tbl.setStyle(TableStyle([
            ("FONTNAME", (0,0), (0,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (0,0), 24),
            ("TEXTCOLOR", (0,0), (0,0), ORANGE),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LINEBELOW", (0,0), (-1,0), 0.3, HAIRLINE),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
        ]))
        story.append(tbl)

    story.append(PageBreak())

    # ============ 9 CAPÍTULOS ============
    add_chapter(story, S, fw,
        num="01", kicker="Cap. 1 · Não tente",
        title="A virtude de não dar a mínima",
        intro=(
            "Charles Bukowski foi um pobre alcoólatra que escreveu obras-primas. Não "
            "porque “acreditou em si mesmo”, mas porque <b>não estava nem aí</b> para o "
            "que os outros achavam — inclusive sobre a sua falha. Manson abre o livro "
            "com o paradoxo: quem deseja muito ser bem-sucedido, raramente é."
        ),
        bullets=[
            "<b>Feedback loop do inferno</b>: sentir-se mal por sentir-se mal — e por aí em diante.",
            "Não dar a mínima ≠ apatia. É <b>escolha</b> de prioridade.",
            "Sutileza 1: você não evita o desconforto, você não <i>teme</i> ser diferente.",
            "Sutileza 2: para não se importar com o trivial, importe-se com algo maior.",
            "Sutileza 3: você já escolhe — só não percebeu. Escolha de novo, agora consciente.",
        ],
        rule=("REGRA",
              "Não tente ser positivo. Tente ser <b>específico</b> sobre o que te importa."),
        quote="A vida não é se livrar dos problemas — é trocar os ruins por melhores.",
    )

    story.append(PageBreak())

    add_chapter(story, S, fw,
        num="02", kicker="Cap. 2 · Felicidade",
        title="A felicidade é um problema",
        intro=(
            "A indústria da felicidade vende a ideia de que ela é um estado a alcançar. "
            "Manson, com Aristóteles, Buda e os estoicos, defende o contrário: felicidade "
            "não é uma equação a resolver — é uma <b>atividade</b>. E essa atividade "
            "consiste em resolver problemas que valem a pena."
        ),
        bullets=[
            "Problemas nunca acabam — só mudam de forma; é o sinal de progresso.",
            "“Problema bom” é o que você gosta de resolver: pais que querem ser melhores pais, atletas que adoram treinar.",
            "A pergunta certa não é “como ser feliz?”, é “<b>qual dor eu quero aguentar?</b>”",
            "Sofrimento + sentido = crescimento. Sofrimento sem sentido = trauma.",
        ],
        rule=("REGRA",
              "Não escolha o que te dá <b>prazer</b>. Escolha o que te dá <b>significado</b> — "
              "o resto vem junto, por contrabando."),
        quote="Você não vai sentir-se sempre bem. Mas pode escolher pelo o que vale a pena se sentir mal.",
    )

    story.append(PageBreak())

    add_chapter(story, S, fw,
        num="03", kicker="Cap. 3 · Mediocridade",
        title="Você não é especial",
        intro=(
            "A geração que cresceu ouvindo “você é único e merece tudo” virou adulta "
            "frágil, paralisada por expectativas absurdas. Manson defende, ao contrário, "
            "a <b>radicalidade da mediocridade</b>: ser comum é libertador — só assim sobra "
            "energia para construir algo de fato extraordinário."
        ),
        bullets=[
            "Narcisismo não é autoestima alta. É autoestima <b>frágil</b> precisando de constante validação.",
            "Pessoas excepcionais são auto<b>críticas</b>; não autoindulgentes.",
            "Aceitar que se é normal liberta da pressão de provar — e abre espaço pra fazer.",
            "Auto-reconhecimento (eu sou assim) é mais útil do que autoestima (eu sou ótimo).",
        ],
        rule=("REGRA",
              "Não persiga “ser especial”. Persiga <b>ser melhor que ontem</b> — só você "
              "consegue medir esse progresso."),
        quote="O incomum nasce do trabalho comum, repetido todo dia, sem ninguém olhando.",
    )

    story.append(PageBreak())

    add_chapter(story, S, fw,
        num="04", kicker="Cap. 4 · Valores",
        title="O valor do sofrimento",
        intro=(
            "Bons e maus valores. Esta é a chave operacional do livro. Nossos valores "
            "são as métricas inconscientes pelas quais julgamos o que vale a pena. "
            "Maus valores produzem vidas ruins, mesmo com sucesso aparente. Bons valores "
            "produzem vidas boas, mesmo com fracassos."
        ),
        bullets=[
            "<b>Maus valores</b>: prazer, sucesso material, ter sempre razão, sentir-se bem o tempo todo, fugir da morte.",
            "<b>Bons valores</b>: responsabilidade, abraçar a incerteza, falhar, dizer não, contemplar a morte.",
            "Critérios de um bom valor: (1) baseado em <b>realidade</b>; (2) <b>construtivo</b> a longo prazo; (3) sob o seu <b>controle</b>.",
            "Quando se muda de valores, a vida toda muda — porque os critérios mudaram.",
        ],
        rule=("REGRA",
              "Mude os valores antes de mudar os hábitos. O hábito é consequência do valor."),
        quote="Você não escolhe o que sente. Você escolhe o que valoriza.",
    )

    story.append(PageBreak())

    add_chapter(story, S, fw,
        num="05", kicker="Cap. 5 · Responsabilidade",
        title="Você está sempre escolhendo",
        intro=(
            "Você pode não ser culpado, mas é <b>responsável</b>. A inversão é "
            "fundamental: <b>culpa</b> olha para trás (quem fez); <b>responsabilidade</b> "
            "olha pra frente (o que fazer agora). Mesmo sem ter escolhido o evento, "
            "você sempre escolhe a resposta a ele."
        ),
        bullets=[
            "<b>Vitimismo</b> é vício: dá pertencimento e identidade sem exigir mudança.",
            "“Com grande responsabilidade vem grande responsabilidade” — Manson inverte o Homem-Aranha.",
            "Quanto mais responsabilidade você assume, mais poder real você tem.",
            "Genética, infância, azar — tudo conta. Mas a única alavanca útil é a sua resposta.",
        ],
        rule=("REGRA",
              "Pare de perguntar “de quem é a culpa?”. Pergunte “<b>o que vou fazer "
              "com isso?</b>”."),
        quote="A diferença não está no que te aconteceu. Está em quem você decide ser depois.",
    )

    story.append(PageBreak())

    add_chapter(story, S, fw,
        num="06", kicker="Cap. 6 · Certeza",
        title="Você está errado sobre tudo",
        intro=(
            "Você se sentirá certo várias vezes na vida — sobre pessoas, ideias, "
            "decisões — e estará errado em quase todas. É inevitável. O problema não "
            "é errar; é a <b>certeza</b> que impede a correção. Manson propõe abraçar a "
            "incerteza como ferramenta de crescimento."
        ),
        bullets=[
            "<b>Lei de Manson da evitação</b>: quanto mais ameaçada uma crença identitária, mais a evitamos.",
            "Estar mais aberto a estar errado = estar mais aberto a aprender.",
            "Você é tão certo quanto sua disposição em ser provado errado.",
            "Boas perguntas: O que eu posso estar errado? Se eu estivesse, como saberia?",
        ],
        rule=("REGRA",
              "Não defenda crenças — <b>investigue-as</b>. O ego se ressente; a vida agradece."),
        quote="O dia que você parou de mudar de ideia foi o dia que você parou de crescer.",
    )

    story.append(PageBreak())

    add_chapter(story, S, fw,
        num="07", kicker="Cap. 7 · Falha",
        title="Falha é o caminho do sucesso",
        intro=(
            "Crianças aprendem caindo. Adultos aprendem que cair é vergonhoso — e portanto "
            "param de aprender. Quem fracassa pouco é porque tenta pouco, não porque é "
            "talentoso. A coragem para fracassar é a infra-estrutura invisível de "
            "qualquer competência."
        ),
        bullets=[
            "“Princípio Faça-Algo” (Do Something Principle): faça algo, qualquer coisa — a motivação vem depois.",
            "Ação é causa, não consequência, de motivação.",
            "Se você é fácil de derrotar, é porque está tentando coisas fáceis.",
            "Quem evita falha está, de fato, falhando — falha em viver.",
        ],
        rule=("REGRA",
              "Comece antes de estar pronto. <b>Prontidão</b> é mito; <b>movimento</b> é fato."),
        quote="Faça algo — qualquer coisa. A clareza vem do movimento, não do pensamento.",
    )

    story.append(PageBreak())

    add_chapter(story, S, fw,
        num="08", kicker="Cap. 8 · Limites",
        title="A importância de dizer não",
        intro=(
            "Quando você se importa com tudo, na verdade não se importa com nada. "
            "Dizer “sim” para tudo é diluir todos os sins. O <b>não</b> é a manutenção "
            "do sim. Manson é didático: relacionamentos saudáveis precisam de "
            "discordância, fronteiras, e até de conflito ocasional."
        ),
        bullets=[
            "<b>“If it's not a Fuck Yes, it's a No”</b> — se não é um <i>“sim com vontade”</i>, é um não.",
            "Relacionamentos sem conflito são <b>relacionamentos por dependência</b>.",
            "Pessoas livres dizem sim por vontade, não por medo. E dizem não sem culpa.",
            "Confiança é construída quando você sustenta uma posição — não quando você se molda.",
        ],
        rule=("REGRA",
              "Diga não três vezes por semana sem se explicar. Veja o que acontece com a sua agenda."),
        quote="Cada sim que você dá hoje é um não que você está dando ao seu eu de amanhã.",
    )

    story.append(PageBreak())

    add_chapter(story, S, fw,
        num="09", kicker="Cap. 9 · Morte",
        title="… e depois, você morre",
        intro=(
            "Manson visita o penhasco onde seu amigo morreu, aos 19 anos. A morte, "
            "argumenta Manson com Ernest Becker, é o eixo invisível por trás de quase "
            "todos os comportamentos humanos. A maioria de nós tenta, sem perceber, "
            "criar uma “imortalidade simbólica” pelo dinheiro, fama, posse. É aí que "
            "valores ruins se enraízam."
        ),
        bullets=[
            "<b>Complexo de imortalidade</b> (Becker): toda a civilização é um esforço inconsciente contra a morte.",
            "Aceitar a morte ilumina o que importa. Sem ela, nada teria peso.",
            "Pergunta-chave: <b>“o que eu vou querer ter feito, no leito de morte?”</b>",
            "Memento mori — lembre-se de que você vai morrer — não é mórbido. É a única forma de viver desperto.",
        ],
        rule=("REGRA",
              "Mantenha um espelho discreto da sua morte por perto. Não para se "
              "deprimir — para <b>priorizar</b>."),
        quote="Tudo o que você é, faz e adquire um dia vai sumir. A pergunta é: o que você quer que continue?",
    )

    story.append(PageBreak())

    # ============ VALORES RUINS x BONS ============
    story.append(Paragraph("CHAVE OPERACIONAL", S["label"]))
    story.append(Paragraph("Valores ruins → valores bons.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "A engrenagem central do livro. Maus valores produzem dor sem sentido; "
        "bons valores produzem dor com sentido. Eis o quadro que Manson "
        "usa, ainda que disperso, ao longo dos capítulos.", S["lead"]))
    story.append(Spacer(1, 0.3*cm))

    pares = [
        ("Prazer (evitar desconforto)",     "Responsabilidade"),
        ("Sucesso material (medir-se em coisas)", "Aceitar a incerteza"),
        ("Ter sempre razão",                "Estar disposto a estar errado"),
        ("Sentir-se bem o tempo todo",      "Capacidade de falhar e seguir"),
        ("Aprovação social (agradar)",      "Liberdade de dizer não"),
        ("Fuga da morte (e da idade)",      "Contemplação consciente da morte"),
    ]
    story.append(ValueComparison(fw, pares))

    story.append(Spacer(1, 0.4*cm))
    story.append(BlackCallout(fw,
        "Mude o lado direito do quadro acima e a sua vida muda mais do que qualquer "
        "objetivo, sistema ou hábito. Valores são o sistema operacional silencioso.",
        label="ATALHO MENTAL"))

    story.append(PageBreak())

    # ============ INVERSÕES ============
    story.append(Paragraph("INVERSÕES", S["label"]))
    story.append(Paragraph("Os contrários do bom-senso.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    inversoes = [
        ("01", "Felicidade vem de PROBLEMAS — não da ausência deles",
         "A pergunta certa é “qual problema eu quero resolver?”, não “como ficar sem problemas?”."),
        ("02", "Sucesso é função do que você está disposto a sofrer",
         "O que separa quem chega de quem não chega não é o desejo do prêmio — é a disposição pelo preço."),
        ("03", "Você é mais livre quando se importa MENOS — com menos coisas",
         "Liberdade não é multiplicar opções; é cortar as que não importam."),
        ("04", "Quem evita rejeição vive a maior rejeição: a de si mesmo",
         "Tentar agradar a todos é o trajeto mais curto para se trair."),
        ("05", "Crise não é sinal de erro; é sinal de que algo precisa mudar",
         "A dor não te castiga — te informa. Escutá-la é mais útil que silenciá-la."),
        ("06", "A morte não tira o sentido da vida; é o que dá sentido",
         "Imortais não teriam pressa. A pressa que vale é a que escolhe o que importa."),
    ]
    for num, tit, txt in inversoes:
        story.append(Paragraph(f"{num}  ·  {tit}", S["h3"]))
        story.append(Paragraph(txt, S["body"]))
        story.append(Spacer(1, 0.1*cm))

    story.append(NextPageTemplate("dark"))
    story.append(PageBreak())

    # ============ MANTRAS (página preta) ============
    mantra_label = ParagraphStyle("manl", fontName="Helvetica-Bold", fontSize=8, leading=11,
                                   textColor=ORANGE, alignment=TA_LEFT, spaceAfter=18)
    mantra_disp = ParagraphStyle("mand", fontName="Helvetica-Bold", fontSize=30, leading=36,
                                  textColor=CREAM, alignment=TA_LEFT, spaceAfter=18)
    mantra_em = ParagraphStyle("mane", fontName="Helvetica-Bold", fontSize=30, leading=36,
                                textColor=ORANGE, alignment=TA_LEFT, spaceAfter=18)
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("MANTRAS", mantra_label))
    story.append(Paragraph("Não é positividade. É clareza.", ParagraphStyle(
        "mantit", fontName="Helvetica-Bold", fontSize=24, leading=28,
        textColor=CREAM, alignment=TA_LEFT, spaceAfter=24)))
    story.append(Paragraph("Não tente.", mantra_em))
    story.append(Paragraph("Você não é especial.", mantra_disp))
    story.append(Paragraph("Escolha o seu sofrimento.", mantra_em))
    story.append(Paragraph("Você não é a sua dor.", mantra_disp))
    story.append(Paragraph("Diga não para guardar o sim.", mantra_em))
    story.append(Paragraph("E depois, você morre.", mantra_disp))

    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # ============ PROVOCAÇÕES ============
    story.append(Paragraph("REFLEXÃO PESSOAL", S["label"]))
    story.append(Paragraph("Provocações.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Não são exercícios — são incômodos guiados. Responda sem se proteger. "
        "Quem responde com elegância está respondendo errado.", S["lead"]))
    story.append(Spacer(1, 0.2*cm))

    perguntas = [
        "Sobre o que você tem se importado que, sinceramente, não merece a sua energia?",
        "Qual sofrimento você está disposto a aguentar — e qual sofrimento está aguentando sem escolher?",
        "Em que situação recente você foi vítima — e que parte disso, agora, você pode assumir como responsabilidade?",
        "Em qual crença identitária forte você poderia estar fundamentalmente errado?",
        "Que “sim” você precisa transformar em “não” para a sua agenda voltar a fazer sentido?",
        "Se você morresse em um ano, o que ficaria pequeno demais para continuar levando a sério?",
    ]
    for p in perguntas:
        story.append(ReflectionLines(fw, p, num_lines=2, line_spacing=0.7*cm))
        story.append(Spacer(1, 0.1*cm))

    story.append(PageBreak())

    # ============ EU NÃO DOU A MÍNIMA PARA ============
    story.append(Paragraph("INVENTÁRIO", S["label"]))
    story.append(Paragraph("Eu não dou a mínima para…", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Marque os itens dos quais você acabou de se libertar nesta leitura. O X "
        "laranja é a sua declaração de independência. Use o caderno para adicionar "
        "os seus próprios.", S["lead"]))
    story.append(Spacer(1, 0.2*cm))

    lista_items = [
        ("Opinião de gente que você nem chama em um aniversário", False),
        ("Curtidas, números, métricas vazias", False),
        ("Conversas em que ninguém muda de ideia, só sobe a voz", False),
        ("A versão de você que tinha 20 anos e estava errada sobre quase tudo", False),
        ("Comparações com pessoas que vivem outra história", False),
        ("Polêmicas que não são suas, mas te roubam o domingo", False),
        ("O sucesso de quem você nunca achou referência mesmo", False),
        ("O elogio que vem antes de um pedido", False),
        ("Aprovação preventiva — autorização pra fazer o que já decidiu", False),
        ("O que “as pessoas vão pensar” — porque elas estão ocupadas pensando em si", False),
    ]
    story.append(StrikeList(fw, lista_items))

    story.append(Spacer(1, 0.3*cm))
    story.append(BlackCallout(fw,
        "O X laranja não é vandalismo — é declaração. Cada item riscado é energia "
        "que volta para o seu lado da página.",
        label="LEITURA DO X"))

    story.append(PageBreak())

    # ============ CADERNO ============
    story.append(Paragraph("CADERNO", S["label"]))
    story.append(Paragraph("Anotações livres.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Use estas linhas para escrever o que esse livro te fez reorganizar.",
        S["body_small"]))
    story.append(Spacer(1, 0.3*cm))

    journal_label = ParagraphStyle("jl", fontName="Helvetica-Bold", fontSize=7.5, leading=11,
                                    textColor=MUTED, alignment=TA_LEFT, spaceAfter=6)
    story.append(Paragraph("O QUE EU VOU DEIXAR DE LEVAR A SÉRIO  *", journal_label))
    # 8 linhas
    line_style = ParagraphStyle("ls", fontName="Helvetica", fontSize=9.5, leading=14,
                                 textColor=INK, alignment=TA_LEFT)
    # use NumberedLines-like via canvas custom flowable
    class JLines(Flowable):
        def __init__(self, width, n=8, sp=0.78*cm):
            Flowable.__init__(self); self.width = width; self.n = n; self.sp = sp
            self.height = n * sp + 0.2*cm
        def draw(self):
            c = self.canv
            c.setStrokeColor(HAIRLINE); c.setLineWidth(0.3)
            for i in range(self.n):
                yy = self.height - (i+1)*self.sp
                c.line(0, yy, self.width, yy)
    story.append(JLines(fw, n=8))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("O QUE EU VOU PRIORIZAR A PARTIR DE HOJE  *", journal_label))
    story.append(JLines(fw, n=8))

    story.append(NextPageTemplate("dark"))
    story.append(PageBreak())

    # ============ ÚLTIMA PALAVRA (página preta) ============
    last_label = ParagraphStyle("ll", fontName="Helvetica-Bold", fontSize=8, leading=11,
                                 textColor=ORANGE, alignment=TA_LEFT, spaceAfter=14)
    last_title = ParagraphStyle("lt", fontName="Helvetica-Bold", fontSize=40, leading=44,
                                 textColor=CREAM, alignment=TA_LEFT, spaceAfter=20)
    last_body = ParagraphStyle("lb", fontName="Helvetica", fontSize=13, leading=20,
                                textColor=CREAM, alignment=TA_LEFT, spaceAfter=14)
    last_em = ParagraphStyle("le", fontName="Helvetica-Oblique", fontSize=14, leading=22,
                              textColor=ORANGE, alignment=TA_LEFT, spaceAfter=14)
    story.append(Spacer(1, 3.5*cm))
    story.append(Paragraph("ÚLTIMA PALAVRA", last_label))
    story.append(Paragraph("Escolha bem.", last_title))
    story.append(Paragraph(
        "Você não tem tempo para se importar com tudo. Ninguém tem. "
        "A vida é, no fim, uma série de coisas a se importar — e a maioria delas "
        "vai ser entregue ao seu cuidado por descuido, não por escolha.",
        last_body))
    story.append(Paragraph(
        "A única coisa que esta sutil arte pede é que você comece a escolher.",
        last_em))

    doc.build(story)


# ─────────────────────────────────────────────────────
# HELPER — Capítulo
# ─────────────────────────────────────────────────────

def add_chapter(story, S, fw, num, kicker, title, intro, bullets, rule, quote):
    story.append(BigChapterNum(fw, num, kicker=kicker))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph(title + ".", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=10))
    story.append(Paragraph(intro, S["body"]))

    story.append(Paragraph("Pontos-chave", S["h2"]))
    for b in bullets:
        story.append(Paragraph("*  " + b, S["bullet"]))

    if quote:
        story.append(Spacer(1, 0.2*cm))
        story.append(ContrastQuote(fw, quote, attribution="Mark Manson · A Sutil Arte"))

    if rule:
        label, txt = rule
        story.append(Spacer(1, 0.15*cm))
        story.append(BlackCallout(fw, txt, label=label))


if __name__ == "__main__":
    build()
    print(f"PDF gerado: {OUTPUT}")
