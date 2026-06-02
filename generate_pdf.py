"""
Gerador de PDF — Resumo de "Hábitos Atômicos" (James Clear)
Design editorial moderno, minimalista, com identidade visual forte.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, Table, TableStyle, KeepTogether, NextPageTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.flowables import Flowable

# ─── Patch: Canvas.setCharSpace + drawString com tracking ───────────
_orig_drawString = Canvas.drawString
_orig_drawRightString = Canvas.drawRightString
_orig_drawCentredString = Canvas.drawCentredString

def _set_char_space(self, v):
    self.__rt_char_space = v

def _draw_with_space(self, x, y, text, _orig, align="left"):
    cs = getattr(self, "_Canvas__rt_char_space", 0)
    if not cs:
        return _orig(self, x, y, text)
    t = self.beginText()
    t.setFont(self._fontname, self._fontsize)
    if hasattr(self, "_fillColorObj") and self._fillColorObj is not None:
        t.setFillColor(self._fillColorObj)
    t.setCharSpace(cs)
    from reportlab.pdfbase.pdfmetrics import stringWidth
    w = stringWidth(text, self._fontname, self._fontsize) + cs * max(0, len(text) - 1)
    if align == "right":
        t.setTextOrigin(x - w, y)
    elif align == "center":
        t.setTextOrigin(x - w / 2.0, y)
    else:
        t.setTextOrigin(x, y)
    t.textOut(text)
    self.drawText(t)

Canvas.setCharSpace = _set_char_space
Canvas.drawString = lambda self, x, y, text: _draw_with_space(self, x, y, text, _orig_drawString, "left")
Canvas.drawRightString = lambda self, x, y, text: _draw_with_space(self, x, y, text, _orig_drawRightString, "right")
Canvas.drawCentredString = lambda self, x, y, text: _draw_with_space(self, x, y, text, _orig_drawCentredString, "center")
# ────────────────────────────────────────────────────────────────────

OUTPUT = "/home/user/taskflow-pro/Habitos_Atomicos_Resumo.pdf"

# ─────────────────────────────────────────────────────
# IDENTIDADE VISUAL  ·  Paleta editorial, warm cream + ink + verde profundo
# ─────────────────────────────────────────────────────
PAPER    = HexColor("#F4EFE6")  # creme quente
INK      = HexColor("#0E0E0E")  # quase preto
SUBINK   = HexColor("#2B2B2B")
MUTED    = HexColor("#8B8479")  # rascunho/legenda
HAIRLINE = HexColor("#CFC8B8")  # linhas finas
ACCENT   = HexColor("#1B4D3E")  # verde profundo (editorial)
ACCENT_2 = HexColor("#C24D2C")  # acento quente para ênfase pontual
DOT      = HexColor("#CFC8B8")  # ponto da malha
INVERSE_INK = HexColor("#0E0E0E")  # fundo escuro para divisores

PAGE_W, PAGE_H = A4
MARGIN_L = 2.4 * cm
MARGIN_R = 2.4 * cm
MARGIN_T = 2.6 * cm
MARGIN_B = 2.4 * cm

# Estado global de seções para a renderização extra na página
_current_chapter = {"num": "", "title": "", "section": ""}


def draw_tracked(c, x, y, text, font, size, color, char_space=0, align="left"):
    """Desenha texto com letter-spacing usando um textObject (canvas não tem setCharSpace)."""
    t = c.beginText()
    t.setFont(font, size)
    t.setFillColor(color)
    t.setCharSpace(char_space)
    if align == "right":
        from reportlab.pdfbase.pdfmetrics import stringWidth
        w = stringWidth(text, font, size) + char_space * max(0, len(text) - 1)
        t.setTextOrigin(x - w, y)
    else:
        t.setTextOrigin(x, y)
    t.textOut(text)
    c.drawText(t)


# ─────────────────────────────────────────────────────
# FLOWABLES CUSTOMIZADOS
# ─────────────────────────────────────────────────────

class HLine(Flowable):
    def __init__(self, width, thickness=0.4, color=HAIRLINE, space_before=0, space_after=0):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness
        self.color = color
        self.space_before = space_before
        self.space_after = space_after
        self.height = thickness + space_before + space_after

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.space_after, self.width, self.space_after)


class DotGrid(Flowable):
    """Malha de pontos — estética bullet-journal moderna para anotações."""
    def __init__(self, width, height, spacing=0.5*cm, dot_size=0.045*cm, color=DOT, label=None):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.spacing = spacing
        self.dot_size = dot_size
        self.color = color
        self.label = label

    def draw(self):
        c = self.canv
        y0 = 0
        if self.label:
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(MUTED)
            # letter-spacing manual via charSpace
            c.setCharSpace(1.4)
            c.drawString(0, self.height - 0.3*cm, self.label.upper())
            c.setCharSpace(0)
        c.setFillColor(self.color)
        cols = int(self.width / self.spacing) + 1
        rows = int(self.height / self.spacing) + 1
        for i in range(rows):
            y = self.height - 0.6*cm - i * self.spacing if self.label else self.height - i * self.spacing
            if y < 0: break
            for j in range(cols):
                x = j * self.spacing
                if x > self.width: break
                c.circle(x, y, self.dot_size, stroke=0, fill=1)


class NumberedLines(Flowable):
    """Linhas pautadas com numeração discreta — moderna, ordenada."""
    def __init__(self, width, num_lines=8, line_spacing=0.78*cm, color=HAIRLINE, label=None, numbered=True):
        Flowable.__init__(self)
        self.width = width
        self.num_lines = num_lines
        self.line_spacing = line_spacing
        self.color = color
        self.label = label
        self.numbered = numbered
        extra = 0.8*cm if label else 0
        self.height = num_lines * line_spacing + extra + 0.2*cm

    def draw(self):
        c = self.canv
        y_top = self.height
        if self.label:
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(MUTED)
            c.setCharSpace(1.4)
            c.drawString(0, y_top - 0.35*cm, self.label.upper())
            c.setCharSpace(0)
            y_top -= 0.85*cm
        c.setStrokeColor(self.color)
        c.setLineWidth(0.3)
        indent = 0.7*cm if self.numbered else 0
        for i in range(self.num_lines):
            yy = y_top - (i+1) * self.line_spacing
            if self.numbered:
                c.setFont("Helvetica", 7.5)
                c.setFillColor(MUTED)
                c.drawString(0, yy + 0.08*cm, f"{i+1:02d}")
            c.setStrokeColor(self.color)
            c.line(indent, yy, self.width, yy)


class CheckboxList(Flowable):
    """Lista de exercícios com checkboxes modernos."""
    def __init__(self, width, items, box_size=0.32*cm, line_height=0.62*cm):
        Flowable.__init__(self)
        self.width = width
        self.items = items
        self.box_size = box_size
        self.line_height = line_height
        # estimativa
        self.height = 0
        font = "Helvetica"
        size = 9.7
        avail = width - box_size - 0.35*cm
        for item in items:
            from reportlab.pdfbase.pdfmetrics import stringWidth
            words = item.split()
            line = ""; lines = 1
            for w in words:
                test = (line + " " + w).strip()
                if stringWidth(test, font, size) <= avail:
                    line = test
                else:
                    lines += 1; line = w
            self.height += lines * (size * 1.35) + 0.18*cm
        self.height += 0.25*cm

    def draw(self):
        c = self.canv
        font = "Helvetica"
        size = 9.7
        # baseline da primeira linha
        y = self.height - size
        for item in self.items:
            # caixa alinhada com a linha do texto (topo da caixa ≈ topo da letra)
            box_y = y + size * 0.05
            c.setStrokeColor(INK)
            c.setLineWidth(0.6)
            c.rect(0, box_y, self.box_size, self.box_size, stroke=1, fill=0)
            from reportlab.pdfbase.pdfmetrics import stringWidth
            words = item.split()
            tx = self.box_size + 0.32*cm
            avail = self.width - tx
            lines = []; line = ""
            for w in words:
                test = (line + " " + w).strip()
                if stringWidth(test, font, size) <= avail:
                    line = test
                else:
                    lines.append(line); line = w
            if line: lines.append(line)
            c.setFont(font, size)
            c.setFillColor(INK)
            ly = y
            for ln in lines:
                c.drawString(tx, ly, ln)
                ly -= size * 1.35
            y -= len(lines) * (size * 1.35) + 0.22*cm


class Callout(Flowable):
    """Callout editorial: barra lateral + label vertical + texto."""
    def __init__(self, width, text, label="INSIGHT", border=ACCENT, padding=0.55*cm):
        Flowable.__init__(self)
        self.width = width
        self.text = text
        self.label = label
        self.border = border
        self.padding = padding
        from reportlab.pdfbase.pdfmetrics import stringWidth
        font = "Helvetica"
        size = 10
        avail = width - 2*padding - 0.5*cm
        words = text.split()
        line = ""; lines = 1
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, font, size) <= avail:
                line = test
            else:
                lines += 1; line = w
        self.height = lines * (size * 1.45) + 2*padding

    def _wrap(self, text, w, font, size):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        words = text.split()
        out = []; line = ""
        for word in words:
            test = (line + " " + word).strip()
            if stringWidth(test, font, size) <= w:
                line = test
            else:
                out.append(line); line = word
        if line: out.append(line)
        return out

    def draw(self):
        c = self.canv
        h = self.height
        # barra lateral grossa
        c.setFillColor(self.border)
        c.rect(0, 0, 0.14*cm, h, stroke=0, fill=1)
        # label minúsculo
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(self.border)
        c.setCharSpace(1.6)
        c.drawString(0.5*cm, h - self.padding + 0.05*cm, self.label.upper())
        c.setCharSpace(0)
        # texto
        c.setFont("Helvetica", 10)
        c.setFillColor(INK)
        lines = self._wrap(self.text, self.width - 2*self.padding - 0.4*cm, "Helvetica", 10)
        y = h - self.padding - 0.45*cm
        for ln in lines:
            c.drawString(0.5*cm, y, ln)
            y -= 10 * 1.45


class PullQuote(Flowable):
    """Pull quote em serif para contraste editorial."""
    def __init__(self, width, text, attribution=None, size=13):
        Flowable.__init__(self)
        self.width = width
        self.text = text
        self.attribution = attribution
        self.size = size
        from reportlab.pdfbase.pdfmetrics import stringWidth
        font = "Times-Italic"
        avail = width * 0.85
        words = text.split()
        line = ""; lines = 1
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, font, size) <= avail:
                line = test
            else:
                lines += 1; line = w
        self.height = lines * (size * 1.3) + (0.55*cm if attribution else 0) + 0.7*cm

    def _wrap(self, text, w, font, size):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        words = text.split()
        out = []; line = ""
        for word in words:
            test = (line + " " + word).strip()
            if stringWidth(test, font, size) <= w:
                line = test
            else:
                out.append(line); line = word
        if line: out.append(line)
        return out

    def draw(self):
        c = self.canv
        # aspas grandes decorativas
        c.setFont("Times-Bold", 40)
        c.setFillColor(ACCENT)
        c.drawString(0, self.height - 1.0*cm, "“")
        # texto da citação
        size = self.size
        c.setFont("Times-Italic", size)
        c.setFillColor(INK)
        avail = self.width * 0.85
        lines = self._wrap(self.text, avail, "Times-Italic", size)
        y = self.height - 0.9*cm
        for ln in lines:
            c.drawString(0.95*cm, y, ln)
            y -= size * 1.3
        if self.attribution:
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(MUTED)
            c.setCharSpace(1.5)
            c.drawString(0.95*cm, y - 0.15*cm, self.attribution.upper())
            c.setCharSpace(0)


class BigNumber(Flowable):
    """Numeral display — identidade visual de abertura de capítulo."""
    def __init__(self, width, number, kicker=None, color=INK):
        Flowable.__init__(self)
        self.width = width
        self.number = str(number)
        self.kicker = kicker
        self.color = color
        self.height = 2.6*cm

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 72)
        c.setFillColor(self.color)
        c.setCharSpace(-3)
        c.drawString(0, 0.3*cm, self.number)
        c.setCharSpace(0)
        from reportlab.pdfbase.pdfmetrics import stringWidth
        w = stringWidth(self.number, "Helvetica-Bold", 72)
        x_line = w + 0.55*cm
        c.setStrokeColor(HAIRLINE)
        c.setLineWidth(0.5)
        c.line(x_line, 0.3*cm, x_line, 2.4*cm)
        if self.kicker:
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(MUTED)
            c.setCharSpace(2)
            c.drawString(x_line + 0.35*cm, 2.15*cm, self.kicker.upper())
            c.setCharSpace(0)


# ─────────────────────────────────────────────────────
# ESTILOS DE TEXTO
# ─────────────────────────────────────────────────────

def make_styles():
    s = {}
    s["display"] = ParagraphStyle(
        "display", fontName="Helvetica-Bold", fontSize=56, leading=58,
        textColor=INK, alignment=TA_LEFT, spaceAfter=10,
    )
    s["title_sub"] = ParagraphStyle(
        "title_sub", fontName="Times-Italic", fontSize=16, leading=22,
        textColor=SUBINK, alignment=TA_LEFT, spaceAfter=8
    )
    s["label"] = ParagraphStyle(
        "label", fontName="Helvetica-Bold", fontSize=8, leading=11,
        textColor=ACCENT, alignment=TA_LEFT, spaceAfter=4
    )
    s["label_muted"] = ParagraphStyle(
        "label_muted", fontName="Helvetica-Bold", fontSize=8, leading=11,
        textColor=MUTED, alignment=TA_LEFT, spaceAfter=4
    )
    s["section"] = ParagraphStyle(
        "section", fontName="Helvetica-Bold", fontSize=24, leading=28,
        textColor=INK, alignment=TA_LEFT, spaceBefore=2, spaceAfter=4
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
        textColor=INK, alignment=TA_LEFT, spaceBefore=10, spaceAfter=3
    )
    s["h3"] = ParagraphStyle(
        "h3", fontName="Helvetica-Bold", fontSize=10, leading=14,
        textColor=ACCENT, alignment=TA_LEFT, spaceBefore=10, spaceAfter=6
    )
    s["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=10, leading=15.5,
        textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6
    )
    s["body_small"] = ParagraphStyle(
        "body_small", fontName="Helvetica", fontSize=9, leading=13,
        textColor=SUBINK, alignment=TA_JUSTIFY, spaceAfter=4
    )
    s["bullet"] = ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=9.5, leading=13.5,
        textColor=INK, alignment=TA_LEFT, leftIndent=14, bulletIndent=2,
        spaceAfter=2
    )
    s["serif_lead"] = ParagraphStyle(
        "serif_lead", fontName="Times-Italic", fontSize=12.5, leading=18,
        textColor=SUBINK, alignment=TA_LEFT, spaceAfter=8
    )
    s["caption"] = ParagraphStyle(
        "caption", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
        textColor=MUTED, alignment=TA_LEFT, spaceAfter=4
    )
    s["toc_title"] = ParagraphStyle(
        "toc_title", fontName="Helvetica", fontSize=10.5, leading=18,
        textColor=INK, alignment=TA_LEFT
    )
    return s


# ─────────────────────────────────────────────────────
# PAGE TEMPLATES — capa, divisores e corpo
# ─────────────────────────────────────────────────────

def draw_paper_background(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)


def draw_cover(c, doc):
    """Capa editorial."""
    draw_paper_background(c)

    # Linha geométrica superior — sutil, moderna
    c.setStrokeColor(INK)
    c.setLineWidth(0.7)
    c.line(MARGIN_L, PAGE_H - 1.6*cm, PAGE_W - MARGIN_L, PAGE_H - 1.6*cm)

    # Marca tipográfica no topo
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(INK)
    c.setCharSpace(3)
    c.drawString(MARGIN_L, PAGE_H - 1.25*cm, "RESUMO · VOL. 01")
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.25*cm, "ED. MAIO 2026")
    c.setCharSpace(0)

    # Marcador "01" gigante como número de volume — característica editorial
    c.setFont("Helvetica-Bold", 240)
    c.setFillColor(HexColor("#E6DFD0"))   # tom mais profundo que o paper
    c.setCharSpace(-10)
    c.drawString(MARGIN_L - 0.5*cm, PAGE_H - 11*cm, "01")
    c.setCharSpace(0)

    # Kicker — categoria
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(ACCENT)
    c.setCharSpace(2)
    c.drawString(MARGIN_L, PAGE_H - 12.3*cm, "COMPORTAMENTO  ·  DESENVOLVIMENTO PESSOAL")
    c.setCharSpace(0)

    # Título — display em duas linhas
    c.setFont("Helvetica-Bold", 64)
    c.setFillColor(INK)
    c.setCharSpace(-3)
    c.drawString(MARGIN_L, PAGE_H - 14.5*cm, "Hábitos")
    c.drawString(MARGIN_L, PAGE_H - 16.5*cm, "Atômicos.")
    c.setCharSpace(0)

    # Subtítulo em serif itálico
    c.setFont("Times-Italic", 14)
    c.setFillColor(SUBINK)
    c.drawString(MARGIN_L, PAGE_H - 17.7*cm,
                 "Um método fácil e comprovado de criar bons hábitos")
    c.drawString(MARGIN_L, PAGE_H - 18.3*cm,
                 "e se livrar dos maus.")

    # Linha divisora
    c.setStrokeColor(INK)
    c.setLineWidth(0.5)
    c.line(MARGIN_L, PAGE_H - 19.5*cm, MARGIN_L + 3*cm, PAGE_H - 19.5*cm)

    # Autor
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(MUTED)
    c.setCharSpace(2)
    c.drawString(MARGIN_L, PAGE_H - 20.1*cm, "AUTOR ORIGINAL")
    c.setCharSpace(0)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(INK)
    c.drawString(MARGIN_L, PAGE_H - 20.8*cm, "James Clear")

    # Símbolo "átomo" minimalista no canto inferior direito
    cx, cy = PAGE_W - 5*cm, 6*cm
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.5)
    c.circle(cx, cy, 2.5*cm, stroke=1, fill=0)
    # elipse rotacionada (uso de save/restore para rotação)
    c.saveState()
    c.translate(cx, cy)
    c.rotate(35)
    c.ellipse(-2.5*cm, -1.0*cm, 2.5*cm, 1.0*cm, stroke=1, fill=0)
    c.restoreState()
    c.setFillColor(ACCENT)
    c.circle(cx, cy, 0.18*cm, stroke=0, fill=1)
    # orbital
    import math
    ang = math.radians(35)
    px = cx + 2.5*cm * math.cos(ang) * 0.7
    py = cy + 1.0*cm * math.sin(ang) * 0.7
    c.setFillColor(ACCENT_2)
    c.circle(px, py, 0.12*cm, stroke=0, fill=1)

    # Rodapé editorial
    c.setStrokeColor(INK)
    c.setLineWidth(0.5)
    c.line(MARGIN_L, 2.3*cm, PAGE_W - MARGIN_R, 2.3*cm)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(MUTED)
    c.setCharSpace(2.5)
    c.drawString(MARGIN_L, 1.7*cm, "CADERNO DE LEITURA  ·  RESUMO · INSIGHTS · ANOTAÇÕES")
    c.drawRightString(PAGE_W - MARGIN_R, 1.7*cm, "FORMATO A4")
    c.setCharSpace(0)


def draw_body_chrome(c, doc):
    """Header e footer das páginas de conteúdo."""
    draw_paper_background(c)

    # ─ Header
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(MUTED)
    c.setCharSpace(2.5)
    c.drawString(MARGIN_L, PAGE_H - 1.3*cm, "HÁBITOS ATÔMICOS")
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.3*cm, "JAMES CLEAR  ·  RESUMO 01")
    c.setCharSpace(0)
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.3)
    c.line(MARGIN_L, PAGE_H - 1.55*cm, PAGE_W - MARGIN_R, PAGE_H - 1.55*cm)

    # ─ Footer com numeração editorial
    page_num = c.getPageNumber()
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.3)
    c.line(MARGIN_L, 1.7*cm, PAGE_W - MARGIN_R, 1.7*cm)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(MUTED)
    c.setCharSpace(2.5)
    c.drawString(MARGIN_L, 1.3*cm, "RESUMO · LEITURA BREVE")
    c.setCharSpace(0)
    # número grande à direita
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(INK)
    c.drawRightString(PAGE_W - MARGIN_R, 1.25*cm, f"{page_num:03d}")


def draw_section_divider_factory(eyebrow, title, subtitle):
    """Cria um onPage para uma página inteira de divisor com fundo escuro."""
    def _draw(c, doc):
        # fundo escuro (não usa paper)
        c.setFillColor(INVERSE_INK)
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        # rule superior
        c.setStrokeColor(HexColor("#3A3A3A"))
        c.setLineWidth(0.3)
        c.line(MARGIN_L, PAGE_H - 1.55*cm, PAGE_W - MARGIN_R, PAGE_H - 1.55*cm)
        # header
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(HexColor("#9A938A"))
        c.setCharSpace(2.5)
        c.drawString(MARGIN_L, PAGE_H - 1.3*cm, "HÁBITOS ATÔMICOS")
        c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.3*cm, "JAMES CLEAR  ·  RESUMO 01")
        c.setCharSpace(0)

        # eyebrow
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(ACCENT_2)
        c.setCharSpace(3)
        c.drawString(MARGIN_L, PAGE_H - 8*cm, eyebrow.upper())
        c.setCharSpace(0)

        # título display em branco
        c.setFont("Helvetica-Bold", 72)
        c.setFillColor(PAPER)
        c.setCharSpace(-3)
        # quebrar título se for longo
        lines = title.split("\n")
        y = PAGE_H - 11*cm
        for ln in lines:
            c.drawString(MARGIN_L, y, ln)
            y -= 4.5*cm
        c.setCharSpace(0)

        # rule horizontal pequena
        c.setStrokeColor(ACCENT_2)
        c.setLineWidth(1.4)
        c.line(MARGIN_L, y + 1.5*cm, MARGIN_L + 2.5*cm, y + 1.5*cm)

        # subtítulo em serif itálico
        c.setFont("Times-Italic", 15)
        c.setFillColor(HexColor("#D4CDB8"))
        # quebra simples por largura
        from reportlab.pdfbase.pdfmetrics import stringWidth
        words = subtitle.split()
        line = ""; cur_y = y + 0.5*cm
        avail = PAGE_W - MARGIN_L - MARGIN_R - 2*cm
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, "Times-Italic", 15) <= avail:
                line = test
            else:
                c.drawString(MARGIN_L, cur_y, line)
                cur_y -= 18; line = w
        if line:
            c.drawString(MARGIN_L, cur_y, line)

        # rodapé com numeração branca
        page_num = c.getPageNumber()
        c.setStrokeColor(HexColor("#3A3A3A"))
        c.setLineWidth(0.3)
        c.line(MARGIN_L, 1.7*cm, PAGE_W - MARGIN_R, 1.7*cm)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(HexColor("#9A938A"))
        c.setCharSpace(2.5)
        c.drawString(MARGIN_L, 1.3*cm, "RESUMO · LEITURA BREVE")
        c.setCharSpace(0)
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(PAPER)
        c.drawRightString(PAGE_W - MARGIN_R, 1.25*cm, f"{page_num:03d}")
    return _draw


# ─────────────────────────────────────────────────────
# CONSTRUÇÃO DO DOCUMENTO
# ─────────────────────────────────────────────────────

def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title="Hábitos Atômicos — Resumo",
        author="Resumo a partir da obra de James Clear",
    )

    fw = PAGE_W - MARGIN_L - MARGIN_R
    fh = PAGE_H - MARGIN_T - MARGIN_B

    cover_frame = Frame(MARGIN_L, MARGIN_B, fw, fh, id="cover", showBoundary=0)
    body_frame  = Frame(MARGIN_L, MARGIN_B, fw, fh - 0.4*cm, id="body", showBoundary=0)

    templates = [
        PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover),
        PageTemplate(id="body",  frames=[body_frame],  onPage=draw_body_chrome),
    ]

    # divisores das 4 leis + táticas
    dividers = [
        ("law1", "1ª Lei",     "Torne\nclaro.",
         "Tornar o que você quer fazer óbvio, e o que não quer, invisível."),
        ("law2", "2ª Lei",     "Torne\natraente.",
         "O desejo move a ação; engenheirar o desejo aumenta a probabilidade do hábito."),
        ("law3", "3ª Lei",     "Torne\nfácil.",
         "Reduza o atrito; remova obstáculos; menos passos, mais ação."),
        ("law4", "4ª Lei",     "Torne\nsatisfatório.",
         "O que é recompensado é repetido. Sem prazer no presente, o hábito não se fixa."),
        ("adv",  "Parte final","Táticas\navançadas.",
         "Quando os hábitos encontram o talento, a regra de Cachinhos Dourados e a revisão."),
    ]
    for tid, eyebrow, title, subtitle in dividers:
        templates.append(
            PageTemplate(
                id=tid,
                frames=[Frame(MARGIN_L, MARGIN_B, fw, fh, id=tid, showBoundary=0)],
                onPage=draw_section_divider_factory(eyebrow, title, subtitle))
        )

    doc.addPageTemplates(templates)

    S = make_styles()
    story = []

    # =================================================
    # CAPA  (page 1 — desenhada pelo onPage)
    # =================================================
    story.append(Spacer(1, 0.1*cm))   # frame vazio; capa é desenhada no onPage
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # =================================================
    # FICHA TÉCNICA
    # =================================================
    story.append(Paragraph("FICHA TÉCNICA", S["label"]))
    story.append(Paragraph("Sobre esta edição.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    story.append(Paragraph(
        "Este caderno é um resumo editorial denso da obra <b>Hábitos Atômicos</b>, "
        "de James Clear. Foi pensado para ser lido em uma única sessão e, ao mesmo "
        "tempo, servir de instrumento de estudo, anotação e prática.", S["serif_lead"]))
    story.append(Spacer(1, 0.4*cm))

    ficha = [
        ["Título original",   "Atomic Habits"],
        ["Título em português","Hábitos Atômicos"],
        ["Autor",             "James Clear"],
        ["Editora (BR)",      "Editora Sextante"],
        ["Publicação",        "2018 (orig.) · 2019 (BR)"],
        ["Páginas (BR)",      "Aproximadamente 320 páginas"],
        ["Gênero",            "Desenvolvimento pessoal · Comportamento"],
        ["Tema central",      "Pequenas mudanças, resultados notáveis"],
        ["Tese em uma linha", "Você cai ao nível do seu sistema — projete o sistema certo."],
    ]
    t = Table(ficha, colWidths=[4.8*cm, fw - 4.8*cm])
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

    story.append(PullQuote(fw,
        "Você não se eleva ao nível das suas metas. Você cai ao nível dos seus sistemas.",
        attribution="James Clear  ·  Hábitos Atômicos"))

    story.append(PageBreak())

    # =================================================
    # SUMÁRIO
    # =================================================
    story.append(Paragraph("NAVEGAÇÃO", S["label"]))
    story.append(Paragraph("Sumário.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Paginação deste caderno. Para a edição brasileira (Sextante, ~320 p.), "
        "veja a coluna <i>Livro</i>.",
        S["body_small"]))
    story.append(Spacer(1, 0.25*cm))

    sumario = [
        # (etiqueta, título, pg caderno, pg livro)
        ("",   "Capa",                                                                 1,    None),
        ("",   "Ficha técnica",                                                        2,    None),
        ("",   "Sumário",                                                              3,    None),
        ("",   "Sobre o autor",                                                        4,    None),
        ("",   "A grande ideia em uma página",                                         5,    None),
        ("01", "O surpreendente poder dos hábitos atômicos",                           6,   "13"),
        ("02", "Como seus hábitos moldam a sua identidade",                            7,   "32"),
        ("03", "Como construir hábitos melhores em quatro passos simples",             8,   "46"),
        ("",   "1ª Lei  ·  Torne claro",                                               9,   "59"),
        ("04", "O homem que não parecia certo",                                       10,   "60"),
        ("05", "A melhor maneira de começar um novo hábito",                          11,   "70"),
        ("06", "Motivação é superestimada; ambiente importa mais",                    12,   "82"),
        ("07", "O segredo do autocontrole",                                           13,   "94"),
        ("",   "2ª Lei  ·  Torne atraente",                                           14,  "103"),
        ("08", "Como tornar um hábito irresistível",                                  15,  "104"),
        ("09", "O papel da família e dos amigos na formação de hábitos",              16,  "117"),
        ("10", "Como encontrar e corrigir as causas dos seus maus hábitos",           17,  "129"),
        ("",   "3ª Lei  ·  Torne fácil",                                              18,  "141"),
        ("11", "Caminhe devagar, mas nunca para trás",                                19,  "142"),
        ("12", "A lei do mínimo esforço",                                             20,  "152"),
        ("13", "Como parar de procrastinar usando a regra dos dois minutos",          21,  "162"),
        ("14", "Como tornar bons hábitos inevitáveis e maus impossíveis",             22,  "172"),
        ("",   "4ª Lei  ·  Torne satisfatório",                                       23,  "183"),
        ("15", "A regra cardinal da mudança de comportamento",                        24,  "184"),
        ("16", "Como manter bons hábitos todos os dias",                              25,  "196"),
        ("17", "Como uma parceria de responsabilidade pode mudar tudo",               26,  "208"),
        ("",   "Táticas avançadas",                                                   27,  "215"),
        ("18", "A verdade sobre talento — quando os genes importam",                  28,  "216"),
        ("19", "A regra de Cachinhos Dourados",                                       29,  "229"),
        ("20", "A desvantagem de criar bons hábitos",                                 30,  "243"),
        ("",   "Insights profundos",                                                  31,    None),
        ("",   "Reflexão pessoal",                                                    33,    None),
        ("",   "Como mudar  ·  protocolo prático",                                    34,    None),
        ("",   "Como evoluir  ·  plano de 90 dias",                                   35,    None),
        ("",   "Exercícios e práticas",                                               36,    None),
        ("",   "Caderno de anotações",                                                37,    None),
        ("",   "Revisão trimestral",                                                  38,    None),
        ("",   "Um último lembrete",                                                  39,    None),
    ]

    # Sumário em duas colunas — divide entradas no meio
    mid = (len(sumario) + 1) // 2
    col_a = sumario[:mid]
    col_b = sumario[mid:]
    # padronizar tamanho
    while len(col_b) < len(col_a):
        col_b.append(("", "", "", None))

    col_w = (fw - 0.6*cm) / 2  # gap de 0.6cm entre colunas

    toc_title_style = ParagraphStyle(
        "toc_title", fontName="Helvetica", fontSize=7.8, leading=10,
        textColor=INK, alignment=TA_LEFT)
    toc_meta_style = ParagraphStyle(
        "toc_meta", fontName="Times-Italic", fontSize=7.8, leading=10,
        textColor=SUBINK, alignment=TA_LEFT)
    toc_sep_style = ParagraphStyle(
        "toc_sep", fontName="Helvetica-Bold", fontSize=7.8, leading=10,
        textColor=ACCENT, alignment=TA_LEFT)

    def make_col_table(entries, is_left):
        rows = [["", "TÍTULO", "RES", "LV"]]
        for cap, titulo, pg_r, pg_l in entries:
            is_sep = (cap == "" and titulo.startswith(
                ("1ª Lei", "2ª Lei", "3ª Lei", "4ª Lei", "Táticas")))
            is_meta = (cap == "" and titulo and not is_sep)
            if is_sep:
                style = toc_sep_style
            elif is_meta:
                style = toc_meta_style
            else:
                style = toc_title_style
            title_p = Paragraph(titulo, style) if titulo else ""
            rows.append([cap if cap else ("·" if titulo else ""),
                         title_p,
                         str(pg_r) if pg_r else "",
                         pg_l if pg_l else ("—" if titulo else "")])
        cw = [0.7*cm, col_w - 2.5*cm, 0.9*cm, 0.9*cm]
        tbl = Table(rows, colWidths=cw)
        cmds = [
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,0), 6.5),
            ("TEXTCOLOR", (0,0), (-1,0), MUTED),
            ("LINEBELOW", (0,0), (-1,0), 0.5, INK),
            ("BOTTOMPADDING", (0,0), (-1,0), 4),

            ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
            ("FONTSIZE", (0,1), (0,-1), 7.8),
            ("FONTSIZE", (2,1), (-1,-1), 7.8),
            ("FONTNAME", (2,1), (-1,-1), "Helvetica"),
            ("TEXTCOLOR", (0,1), (0,-1), ACCENT),
            ("ALIGN", (2,0), (3,-1), "RIGHT"),
            ("TEXTCOLOR", (2,1), (-1,-1), MUTED),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("BOTTOMPADDING", (0,1), (-1,-1), 3),
            ("TOPPADDING", (0,1), (-1,-1), 3),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (1,1), (1,-1), 2),
        ]
        for i, (cap, titulo, _, _) in enumerate(entries, start=1):
            is_sep = (cap == "" and titulo.startswith(
                ("1ª Lei", "2ª Lei", "3ª Lei", "4ª Lei", "Táticas")))
            if is_sep:
                cmds.append(("LINEABOVE", (0,i), (-1,i), 0.4, HAIRLINE))
                cmds.append(("TOPPADDING", (0,i), (-1,i), 5))
                cmds.append(("BOTTOMPADDING", (0,i), (-1,i), 3))
        tbl.setStyle(TableStyle(cmds))
        return tbl

    left = make_col_table(col_a, True)
    right = make_col_table(col_b, False)

    outer = Table([[left, right]], colWidths=[col_w, col_w])
    outer.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (0,0), 0.3*cm),
        ("LEFTPADDING", (1,0), (1,0), 0.3*cm),
    ]))
    story.append(outer)

    story.append(PageBreak())

    # =================================================
    # SOBRE O AUTOR
    # =================================================
    story.append(Paragraph("AUTOR", S["label"]))
    story.append(Paragraph("Sobre James Clear.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    story.append(Paragraph(
        "<b>James Clear</b> é um escritor norte-americano, palestrante e pesquisador "
        "independente nas áreas de comportamento humano, formação de hábitos e desempenho. "
        "Autor da newsletter semanal <i>3-2-1 Thursday</i>, lida por mais de 3 milhões "
        "de pessoas, e do best-seller <i>Atomic Habits</i> (Hábitos Atômicos), publicado "
        "em 2018, com mais de 20 milhões de exemplares vendidos em todo o mundo e "
        "tradução para mais de 50 idiomas.", S["body"]))
    story.append(Paragraph(
        "Sua proposta sintetiza ciência comportamental, biologia evolutiva e filosofia "
        "estoica em um sistema prático: <b>melhorar 1% por dia</b>. O resultado, segundo "
        "Clear, não é apenas estatístico (37× ao fim de um ano), mas estrutural — porque "
        "modifica a identidade do indivíduo, não apenas o seu comportamento.", S["body"]))

    story.append(Paragraph("Outras obras e influências", S["h2"]))
    story.append(Paragraph(
        "• Influenciado por: B. J. Fogg (<i>Tiny Habits</i>), Charles Duhigg (<i>O Poder "
        "do Hábito</i>), Carol Dweck (<i>Mindset</i>), Daniel Kahneman, Robert Cialdini, "
        "Stephen Covey, William James e os estoicos.", S["bullet"]))
    story.append(Paragraph(
        "• Linha editorial: pequenos textos densos, exemplos vividos (de Phelps a Edison), "
        "sistemas em vez de metas, ambiente em vez de força de vontade.", S["bullet"]))

    story.append(Paragraph("Por que este livro funciona", S["h2"]))
    story.append(Paragraph(
        "Porque desloca o eixo da motivação para o <b>design</b>: em vez de querer mais, "
        "o leitor aprende a projetar contextos, sinais e recompensas. É um manual de "
        "engenharia pessoal — leve, escalável e replicável em qualquer área da vida.",
        S["body"]))

    story.append(Spacer(1, 0.4*cm))
    story.append(Callout(fw,
        "Não suba o nível das suas metas; suba o nível dos seus sistemas. Você não se "
        "eleva ao nível das suas metas — você cai ao nível dos seus sistemas.",
        label="FRASE-CHAVE"))

    story.append(PageBreak())

    # =================================================
    # A GRANDE IDEIA
    # =================================================
    story.append(Paragraph("VISÃO PANORÂMICA", S["label"]))
    story.append(Paragraph("A grande ideia em uma página.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    story.append(Paragraph(
        "O livro defende uma tese simples e radical: <b>pequenas melhorias diárias, "
        "consistentes, compõem resultados extraordinários</b>. Para isso, James Clear "
        "propõe um sistema baseado em quatro leis universais para construir bons "
        "hábitos — e suas inversões para extinguir maus hábitos.", S["body"]))

    leis = [
        ["LEI",                "CONSTRUIR (BOM HÁBITO)",  "QUEBRAR (MAU HÁBITO)"],
        ["1ª  ·  Deixa",       "Torne-o claro",            "Torne-o invisível"],
        ["2ª  ·  Desejo",      "Torne-o atraente",         "Torne-o desinteressante"],
        ["3ª  ·  Resposta",    "Torne-o fácil",            "Torne-o difícil"],
        ["4ª  ·  Recompensa",  "Torne-o satisfatório",     "Torne-o insatisfatório"],
    ]
    lt = Table(leis, colWidths=[3.6*cm, (fw - 3.6*cm)/2, (fw - 3.6*cm)/2])
    lt.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 7.5),
        ("TEXTCOLOR", (0,0), (-1,0), MUTED),
        ("BOTTOMPADDING", (0,0), (-1,0), 7),
        ("LINEBELOW", (0,0), (-1,0), 0.5, INK),

        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0,1), (0,-1), ACCENT),
        ("FONTNAME", (1,1), (1,-1), "Helvetica-Bold"),
        ("FONTNAME", (2,1), (2,-1), "Helvetica"),
        ("TEXTCOLOR", (2,1), (2,-1), SUBINK),
        ("FONTSIZE", (0,1), (-1,-1), 10),
        ("BOTTOMPADDING", (0,1), (-1,-1), 10),
        ("TOPPADDING", (0,1), (-1,-1), 10),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LINEBELOW", (0,1), (-1,-1), 0.25, HAIRLINE),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(lt)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("Três camadas da mudança", S["h2"]))
    story.append(Paragraph(
        "Clear distingue três camadas hierárquicas. A mais superficial é a dos "
        "<b>resultados</b> (o que você obtém). Abaixo, está a dos <b>processos</b> "
        "(o que você faz). No fundo, a das <b>identidades</b> (em quem você acredita "
        "que é). Mudanças duradouras começam da identidade para fora: não basta "
        "querer correr, é preciso <i>tornar-se</i> alguém que corre.", S["body"]))

    story.append(Paragraph("Hábitos atômicos: a metáfora", S["h2"]))
    story.append(Paragraph(
        "“Atômico” tem dois sentidos. <b>Pequeno</b> — uma unidade mínima de "
        "comportamento. E <b>fonte de energia desproporcional</b> — porque, somado, "
        "esse pequeno gera mudança massiva. A diferença entre 1,01<sup>365</sup> "
        "(≈ 37,8) e 0,99<sup>365</sup> (≈ 0,03) é a metáfora central.", S["body"]))

    story.append(Spacer(1, 0.3*cm))
    story.append(Callout(fw,
        "Você não fracassa por preguiça nem vence por motivação. Você cai ao nível do "
        "seu sistema — projete o sistema certo e o resultado vira inevitável.",
        label="TESE CENTRAL"))

    story.append(PageBreak())

    # =================================================
    # PARTE I — FUNDAMENTOS
    # =================================================

    add_chapter(story, S, fw,
        chap_num="01", kicker="FUNDAMENTOS",
        title="O surpreendente poder dos hábitos atômicos",
        livro_pg="13",
        intro=(
            "Em 2003, a seleção britânica de ciclismo, mediana há mais de um século, "
            "contratou Dave Brailsford com uma filosofia: <b>melhorar 1% em mil pontos</b>. "
            "Em cinco anos, dominou os Jogos Olímpicos. Em dez, conquistou o Tour de "
            "France. A lição: <b>melhorias marginais compõem-se</b> de forma exponencial."
        ),
        bullets=[
            "1% melhor por dia durante 1 ano = 37,78× melhor; 1% pior = 0,03 do original.",
            "Hábitos são para a vida o que juros compostos são para o dinheiro.",
            "Você é o resultado acumulado dos seus pequenos hábitos, não dos grandes feitos.",
            "Sucesso e fracasso operam pelo mesmo princípio: o tempo amplifica o que você repete.",
            "O <b>vale da decepção</b>: bons hábitos rendem tarde, mas rendem composto.",
            "Esqueça metas, foque em <b>sistemas</b>: metas definem direção, sistemas geram progresso.",
        ],
        insights=[
            ("A ASSIMETRIA DA REPETIÇÃO",
             "Maus hábitos compõem-se enquanto você não percebe; bons hábitos compõem-se "
             "enquanto você sente que não está progredindo. Quem entende essa assimetria "
             "para de medir o resultado pelo dia e passa a medir pela trajetória."),
            ("SISTEMAS > METAS",
             "Vencedores e perdedores compartilham as mesmas metas. O que diferencia "
             "é a qualidade do sistema. Metas são úteis para definir direção; sistemas "
             "são o que cria progresso real."),
        ],
        pull_quote="Hábitos são os juros compostos do autoaperfeiçoamento.",
    )

    story.append(PageBreak())

    add_chapter(story, S, fw,
        chap_num="02", kicker="FUNDAMENTOS",
        title="Como seus hábitos moldam a sua identidade",
        livro_pg="32",
        intro=(
            "Mudanças comportamentais ocorrem em três camadas: <b>resultados</b>, "
            "<b>processos</b> e <b>identidade</b>. A maioria das pessoas tenta mudar "
            "começando pelo resultado. Clear inverte: comece pela identidade. "
            "Cada ação é um voto no tipo de pessoa que você acredita ser."
        ),
        bullets=[
            "Pergunte-se: que <b>tipo de pessoa</b> conseguiria o resultado que quero?",
            "Hábitos são votos: 1 voto não muda eleição, mas 100 votos formam uma identidade.",
            "Mudar identidade exige (1) decidir quem você quer ser e (2) provar com pequenas vitórias.",
            "Orgulho da identidade torna o hábito autossustentável: você o protege.",
            "Sua identidade é a soma das evidências que você produz sobre si.",
        ],
        insights=[
            ("DE 'EU QUERO' PARA 'EU SOU'",
             "Não diga 'eu quero parar de fumar', diga 'eu não sou fumante'. A "
             "linguagem da identidade dispensa força de vontade — você simplesmente "
             "não faz aquilo que não é seu."),
            ("VOTAR EM SI MESMO",
             "Não é preciso unanimidade: basta a maioria das ações apontar para a "
             "identidade desejada para que ela se imponha sobre as antigas."),
        ],
        pull_quote=("A meta não é ler um livro, é tornar-se um leitor. "
                    "A meta não é correr uma maratona, é tornar-se um corredor."),
    )

    story.append(PageBreak())

    add_chapter(story, S, fw,
        chap_num="03", kicker="FUNDAMENTOS",
        title="Como construir hábitos melhores em quatro passos simples",
        livro_pg="46",
        intro=(
            "Todo hábito é um <b>loop de quatro etapas</b> derivado da neurociência "
            "comportamental: <b>deixa → desejo → resposta → recompensa</b>. Reconhecer "
            "essa estrutura permite engenheirar — não apenas desejar — mudanças."
        ),
        bullets=[
            "<b>Deixa</b>: a pista que aciona o cérebro a iniciar o comportamento.",
            "<b>Desejo</b>: a motivação por trás do hábito; queremos mudar de estado.",
            "<b>Resposta</b>: o hábito em si, físico ou mental.",
            "<b>Recompensa</b>: o objetivo final; satisfaz o desejo e ensina o cérebro.",
            "Bom hábito: torne os 4 elementos óbvio/atraente/fácil/satisfatório.",
            "Mau hábito: torne-os invisível/desinteressante/difícil/insatisfatório.",
        ],
        insights=[
            ("HÁBITO É UMA SOLUÇÃO",
             "Toda repetição responde a um problema. Antes de quebrar um hábito, "
             "entenda qual problema ele resolve — caso contrário, ele voltará com "
             "outra roupagem."),
            ("AUTOMATICIDADE",
             "A definição operacional de hábito é uma resposta que se tornou "
             "automática. Avaliar a automaticidade (não o esforço) indica se o "
             "hábito está se enraizando."),
        ],
        pull_quote="Um hábito é um comportamento repetido vezes suficientes para se tornar automático.",
    )

    # =================================================
    # 1ª LEI — divisor + capítulos
    # =================================================
    story.append(NextPageTemplate("law1"))
    story.append(PageBreak())
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    add_chapter(story, S, fw,
        chap_num="04", kicker="1ª LEI · TORNE CLARO",
        title="O homem que não parecia certo",
        livro_pg="60",
        intro=(
            "A história abre com um perito que, ao olhar para uma pessoa, sente que "
            "“algo não está certo” — sem saber explicar o quê. Cérebro detecta padrões "
            "antes da consciência: maus hábitos se enraízam justamente porque param de "
            "ser vistos. <b>Tornar consciente é o primeiro ato de mudança</b>."
        ),
        bullets=[
            "Use o <b>Cartão de Pontuação de Hábitos</b>: liste o dia inteiro e marque +, − ou =.",
            "Verbalizar em voz alta reduz erros e desperta consciência (técnica japonesa <i>shisa kanko</i>).",
            "Você não muda o que não enxerga.",
            "Identifique hábitos de entrada (gatilhos) que disparam cascatas inteiras de comportamento.",
        ],
        insights=[
            ("APONTAR-E-CHAMAR",
             "Apontar para o sinal e nomear em voz alta reduz acidentes ferroviários em 85%. "
             "Aplicação pessoal: narrar a própria ação antes de executá-la."),
        ],
        pull_quote=("Até que você torne o inconsciente consciente, ele dirigirá sua vida "
                    "e você o chamará de destino."),
        pull_attr="Carl Jung",
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="05", kicker="1ª LEI · TORNE CLARO",
        title="A melhor maneira de começar um novo hábito",
        livro_pg="70",
        intro=(
            "Duas ferramentas para tornar uma deixa óbvia: <b>intenção de implementação</b> "
            "(quando + onde) e <b>empilhamento de hábitos</b> (depois de qual hábito atual)."
        ),
        bullets=[
            "<b>Fórmula 1</b>: “Eu vou [comportamento] em [horário], em [lugar].”",
            "<b>Fórmula 2</b>: “Depois de [hábito atual], eu vou [novo hábito].”",
            "Pesquisas de Peter Gollwitzer: pessoas com plano específico têm 2–3× mais probabilidade de agir.",
            "Empilhar ancora o novo comportamento em uma rede neural já existente.",
            "Encadeie hábitos para criar rotinas (manhã, trabalho, sono).",
        ],
        insights=[
            ("ELIMINAR DECISÕES",
             "O custo do hábito é, no fundo, o custo de decidir. Quando o gatilho "
             "decide por você (lugar + horário fixos), você poupa força de vontade "
             "para o que importa."),
        ],
        pull_quote="Muitas pessoas pensam que falta motivação quando, na verdade, falta clareza.",
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="06", kicker="1ª LEI · TORNE CLARO",
        title="Motivação é superestimada; ambiente importa mais",
        livro_pg="82",
        intro=(
            "Comportamento é função da pessoa e do contexto. Mudar o contexto "
            "é, quase sempre, mais barato e duradouro do que mudar a pessoa. "
            "<b>Design de ambiente</b> é o nome técnico para isso."
        ),
        bullets=[
            "Deixe pistas visíveis e fáceis para bons hábitos; remova as dos maus.",
            "Faça <b>um lugar = um propósito</b>: leitura na poltrona, trabalho na escrivaninha, sono na cama.",
            "Hospitais que põem água em destaque aumentaram o consumo em 25,8% (e refrigerante caiu 11,4%).",
            "Você não tem um problema de disciplina; tem um problema de design.",
        ],
        insights=[
            ("AMBIENTES DE MULTI-USO",
             "Quando vários hábitos disputam o mesmo lugar, vence o mais antigo. "
             "Crie nichos: separe espaço de foco do espaço de descanso, mesmo "
             "que seja por um simples tapete ou cadeira diferente."),
        ],
        pull_quote="O ambiente é a mão invisível que molda o comportamento humano.",
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="07", kicker="1ª LEI · TORNE CLARO",
        title="O segredo do autocontrole",
        livro_pg="94",
        intro=(
            "Pessoas “disciplinadas” não resistem mais à tentação — elas <b>se expõem "
            "menos</b> a ela. Em vez de treinar força de vontade, projete uma vida "
            "com menos atrito moral."
        ),
        bullets=[
            "Estudo com veteranos do Vietnã: 95% dos viciados em heroína pararam ao voltar para casa — o ambiente mudou.",
            "Maus hábitos são autorreforçados: a deixa cria o desejo, que cria a resposta, que reforça a deixa.",
            "Quebrar um hábito a partir da raiz exige tornar a deixa invisível, não combatê-la.",
            "Quem oculta o doce não o quer; quem o vê todo dia gasta energia para resistir.",
        ],
        insights=[
            ("ALÉM DA FORÇA DE VONTADE",
             "Autocontrole é estratégia de curto prazo. Mais eficaz: reduzir a "
             "exposição às deixas. Pessoas com hábitos exemplares costumam viver em "
             "ambientes que tornam o ruim incômodo e o bom inevitável."),
        ],
        pull_quote=("Você pode quebrar um hábito, mas é improvável que o esqueça. "
                    "A solução é manter os gatilhos longe da sua vista."),
    )

    # =================================================
    # 2ª LEI
    # =================================================
    story.append(NextPageTemplate("law2"))
    story.append(PageBreak())
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    add_chapter(story, S, fw,
        chap_num="08", kicker="2ª LEI · TORNE ATRAENTE",
        title="Como tornar um hábito irresistível",
        livro_pg="104",
        intro=(
            "Comida superpalatável e redes sociais entregam <b>versões exageradas</b> "
            "dos gatilhos evolutivos do prazer. Dopamina é liberada na <b>antecipação</b>, "
            "não apenas na recompensa. Use isso a seu favor com agrupamento."
        ),
        bullets=[
            "<b>Agrupamento de tentações</b>: faça o que você precisa junto com o que você gosta.",
            "Fórmula: “Depois de [necessário], eu vou [quero]; depois, [adoro].”",
            "Dopamina sobe na antecipação: criar expectativa positiva aumenta a probabilidade de execução.",
            "Não é a recompensa em si, mas o desejo da recompensa, que sustenta a repetição.",
        ],
        insights=[
            ("PRAZER É PROMESSA",
             "Quando você associa um hábito difícil a uma promessa de prazer logo "
             "à frente, o cérebro injeta o esforço primeiro — porque já está vendo "
             "a recompensa no horizonte."),
        ],
        pull_quote="É o desejo, não a obtenção, que nos faz agir.",
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="09", kicker="2ª LEI · TORNE ATRAENTE",
        title="O papel da família e dos amigos na formação de hábitos",
        livro_pg="117",
        intro=(
            "Imitamos três grupos: <b>os próximos</b> (família, amigos), <b>os muitos</b> "
            "(a tribo) e <b>os poderosos</b> (status). Escolher grupos é escolher hábitos."
        ),
        bullets=[
            "Junte-se a uma cultura em que (1) o hábito desejado é comum e (2) você já tem algo em comum.",
            "O comportamento atrativo é o que recebe aprovação social.",
            "Mude amizades como muda objetivos: as duas coisas se interpenetram.",
            "Você é o equilíbrio entre as cinco pessoas com quem mais convive.",
        ],
        insights=[
            ("PERTENCER É MAIS FORTE QUE PROVAR",
             "Hábitos sociais sobrevivem mesmo quando contradizem dados — porque "
             "estar certo perto de pessoas erradas pesa menos que estar errado perto "
             "das suas pessoas."),
        ],
        pull_quote="Um dos esforços humanos mais profundos é o de pertencer.",
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="10", kicker="2ª LEI · TORNE ATRAENTE",
        title="Como encontrar e corrigir as causas dos seus maus hábitos",
        livro_pg="129",
        intro=(
            "Por trás de um mau hábito existe sempre um <b>desejo motivador</b>: "
            "diminuir incerteza, conexão, status, poder, prazer. Maus hábitos atendem "
            "esses desejos com soluções precárias. O caminho é <b>reformular o desejo</b>."
        ),
        bullets=[
            "Liste seus maus hábitos e identifique o desejo subjacente em cada um.",
            "Substitua a resposta, não o desejo: o cigarro é um pedido de pausa — busque outra pausa.",
            "Reformulação: “Eu <b>tenho</b> que treinar” → “Eu <b>posso</b> treinar.”",
            "Atletas de elite reinterpretam o nervosismo como excitação produtiva.",
        ],
        insights=[
            ("DESEJOS SÃO ANTIGOS, MEIOS SÃO NOVOS",
             "Quase nada do que sentimos é novo. Os meios pelos quais saciamos os "
             "desejos é que mudam. Trocar de meio (mas atender o mesmo desejo) é o "
             "movimento mais barato de mudança comportamental."),
        ],
        pull_quote="A motivação é fácil quando o significado é claro.",
    )

    # =================================================
    # 3ª LEI
    # =================================================
    story.append(NextPageTemplate("law3"))
    story.append(PageBreak())
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    add_chapter(story, S, fw,
        chap_num="11", kicker="3ª LEI · TORNE FÁCIL",
        title="Caminhe devagar, mas nunca para trás",
        livro_pg="142",
        intro=(
            "Famoso experimento da escola de cerâmica: o grupo avaliado por <b>quantidade</b> "
            "produziu peças melhores que o avaliado por <b>qualidade</b>. Repetição vence "
            "perfeccionismo. Distinguir <b>estar em movimento</b> de <b>agir</b>."
        ),
        bullets=[
            "Movimento dá ilusão de progresso (planejar, pesquisar, conversar) sem produzir resultado.",
            "Ação produz resultado. Hábitos são forjados por frequência, não por tempo.",
            "A automaticidade aparece após muitas repetições, não após muito esforço.",
            "Prefira começar pequeno, terminar e repetir — sempre.",
        ],
        insights=[
            ("FREQUÊNCIA VENCE INTENSIDADE",
             "Quem fez 100 esboços ruins aprende mais do que quem planejou 1 perfeito. "
             "O número de repetições é a moeda da mestria — não o tempo investido em pensar nelas."),
        ],
        pull_quote=("Se você quer dominar um hábito, a chave é começar com a repetição, "
                    "não com a perfeição."),
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="12", kicker="3ª LEI · TORNE FÁCIL",
        title="A lei do mínimo esforço",
        livro_pg="152",
        intro=(
            "O cérebro economiza energia. Comportamentos seguem o caminho de menor "
            "resistência. Para um bom hábito, <b>diminua o atrito</b>; para um mau hábito, "
            "<b>aumente o atrito</b>."
        ),
        bullets=[
            "Prepare o ambiente na noite anterior: roupa de treino, mesa de trabalho, livros à mão.",
            "Coloque uma camada extra entre você e o mau hábito (desplug da TV, app desinstalado).",
            "Hábitos automáticos se formam quando o esforço cognitivo é mínimo.",
            "Cada segundo a mais de atrito reduz drasticamente a probabilidade de ação.",
        ],
        insights=[
            ("DESIGN INVISÍVEL",
             "A maior parte da mudança eficaz não é heroica; é silenciosa. É uma "
             "tomada deslocada, um app removido, uma fruta ao alcance da mão. "
             "Quem desenha bem o cenário quase nunca precisa atuar."),
        ],
        pull_quote="O comportamento humano segue a lei do mínimo esforço.",
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="13", kicker="3ª LEI · TORNE FÁCIL",
        title="Como parar de procrastinar usando a regra dos dois minutos",
        livro_pg="162",
        intro=(
            "Reduza qualquer novo hábito a uma versão que possa ser feita em <b>dois "
            "minutos</b>. Ler 1 página. Calçar o tênis. Abrir o caderno. O objetivo "
            "é tornar a aparição inevitável; a melhoria vem depois."
        ),
        bullets=[
            "“Ler antes de dormir” → “Ler 1 página.”",
            "“Treinar” → “Vestir a roupa de treino.”",
            "“Estudar uma hora” → “Abrir o livro na página correta.”",
            "Domine a versão fácil antes de tentar dominar a versão completa.",
            "O hábito de aparecer é mais valioso do que qualquer sessão isolada.",
        ],
        insights=[
            ("RITUAL DE ENTRADA",
             "Toda mestria precisa de uma “porta de entrada” simples. A regra dos "
             "dois minutos elimina a fricção inicial — e o início é onde quase todos os "
             "hábitos morrem."),
        ],
        pull_quote="Um hábito precisa ser estabelecido antes de ser melhorado.",
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="14", kicker="3ª LEI · TORNE FÁCIL",
        title="Como tornar bons hábitos inevitáveis e maus impossíveis",
        livro_pg="172",
        intro=(
            "<b>Dispositivos de compromisso</b>: decisões tomadas hoje para limitar "
            "comportamentos amanhã. Vão da remoção do app à automação financeira "
            "(débito automático para investimento), passando por listas, alarmes e cofres."
        ),
        bullets=[
            "Automação: pague-se primeiro; débito automático para metas financeiras.",
            "Listas únicas de compras (mais barato, sem decisão a cada item).",
            "Bloqueadores de site, modo foco, modo avião durante horas de trabalho.",
            "Restrinja-se de antemão para não depender de força de vontade no calor da hora.",
        ],
        insights=[
            ("O FUTURO 'VOCÊ' AGRADECE",
             "Quase toda decisão difícil pode ser pré-decidida. Você corta a "
             "batalha antes dela começar. O cérebro reconhece como “já resolvido” "
             "e libera energia para o que importa."),
        ],
        pull_quote="A maneira definitiva de criar bons hábitos é tornar a opção certa a mais fácil.",
    )

    # =================================================
    # 4ª LEI
    # =================================================
    story.append(NextPageTemplate("law4"))
    story.append(PageBreak())
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    add_chapter(story, S, fw,
        chap_num="15", kicker="4ª LEI · TORNE SATISFATÓRIO",
        title="A regra cardinal da mudança de comportamento",
        livro_pg="184",
        intro=(
            "Cérebros humanos priorizam o presente (preferência temporal). Hábitos "
            "saudáveis tendem a ter <b>recompensa imediata pequena</b> e <b>retorno "
            "futuro grande</b>. Solução: <b>antecipar prazer</b> e <b>postergar custo</b>."
        ),
        bullets=[
            "Adicione uma recompensa imediata pequena ao terminar o hábito (uma transferência simbólica para uma poupança de viagem, por exemplo).",
            "A recompensa não deve contradizer a identidade (não comer pizza para celebrar a dieta).",
            "Curto prazo: prazer. Longo prazo: identidade.",
            "Reforço positivo imediato fixa o circuito neuronal mais rápido.",
        ],
        insights=[
            ("MORDIDA DE FUTURO",
             "Pequenos prazeres no presente são como “mordidas” antecipadas do "
             "futuro. Eles ensinam o cérebro de que aquele caminho compensa — e o "
             "fazem voltar amanhã."),
        ],
        pull_quote="O que é recompensado é repetido. O que é punido é evitado.",
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="16", kicker="4ª LEI · TORNE SATISFATÓRIO",
        title="Como manter bons hábitos todos os dias",
        livro_pg="196",
        intro=(
            "Mensurar a sequência (<b>habit tracking</b>) torna o progresso visível, "
            "atraente e satisfatório. Marcar um X no calendário é, em si, uma "
            "recompensa imediata. A regra de ouro: <b>nunca falhe duas vezes seguidas</b>."
        ),
        bullets=[
            "Use um rastreador simples (papel ou app); cada dia executado vira evidência.",
            "Falhar uma vez é acidente; falhar duas vezes é o início de um novo (mau) hábito.",
            "Não confunda dia ruim com identidade nova: retome no dia seguinte.",
            "O que é medido melhora — mas cuidado em medir o indicador certo.",
        ],
        insights=[
            ("LEI DE GOODHART (CUIDADO)",
             "Quando uma métrica vira objetivo, deixa de ser boa métrica. Mensure "
             "para enxergar, não para se ludibriar — a régua é serva da identidade, "
             "não o contrário."),
        ],
        pull_quote="Perder uma vez é acidente. Perder duas vezes é o início de um novo hábito.",
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="17", kicker="4ª LEI · TORNE SATISFATÓRIO",
        title="Como uma parceria de responsabilidade pode mudar tudo",
        livro_pg="208",
        intro=(
            "Custos imediatos calibram comportamentos. <b>Contratos de hábito</b> "
            "tornam o preço da falha social e imediato. Ter um parceiro de "
            "responsabilidade aumenta drasticamente a aderência."
        ),
        bullets=[
            "Escreva um contrato: o que você fará, com que frequência e qual o preço de não fazer.",
            "Compartilhe metas e progresso com alguém que <b>realmente</b> cobre.",
            "Dor à vista é mais forte que dor futura — use isso pedagogicamente.",
            "Anônimo às vezes é mais eficaz que público (depende da personalidade).",
        ],
        insights=[
            ("ASSIMETRIA DA VERGONHA",
             "Não cumprir uma promessa sozinho é fácil de racionalizar; "
             "diante de outro humano, é caro. Use o capital social como aliado da sua mudança."),
        ],
        pull_quote="Sabendo que alguém está observando, você se torna seu melhor observador.",
    )

    # =================================================
    # TÁTICAS AVANÇADAS
    # =================================================
    story.append(NextPageTemplate("adv"))
    story.append(PageBreak())
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    add_chapter(story, S, fw,
        chap_num="18", kicker="TÁTICAS AVANÇADAS",
        title="A verdade sobre talento — quando os genes importam",
        livro_pg="216",
        intro=(
            "Genes não determinam o destino, mas inclinam o terreno. Maximize o "
            "retorno do esforço escolhendo arenas em que sua personalidade e biologia "
            "trabalham a seu favor."
        ),
        bullets=[
            "Encontre o jogo certo: o que parece esforço para você é diversão para outros — e vice-versa.",
            "Combine afinidade com mercado: não basta gostar, é preciso haver demanda.",
            "Hábito ótimo é o que está no limite das suas capacidades atuais (regra de Cachinhos Dourados).",
            "Compita por sua singularidade, não por uniformidade.",
        ],
        insights=[
            ("EXPLORAR ANTES DE EXPLORAR",
             "Antes de focar, faça <b>exploração</b>: experimente arenas, formatos, "
             "ferramentas. Depois, <b>aprofunde</b> o que produz energia. A maior parte do "
             "desperdício humano está em focar cedo no jogo errado."),
        ],
        pull_quote="Quando você não consegue ganhar sendo melhor, ganhe sendo diferente.",
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="19", kicker="TÁTICAS AVANÇADAS",
        title="A regra de Cachinhos Dourados",
        livro_pg="229",
        intro=(
            "Fluxo (Csikszentmihalyi) acontece em tarefas com dificuldade ≈ 4% acima "
            "da habilidade. Muito difícil: ansiedade. Muito fácil: tédio. Hábitos "
            "duráveis se sustentam no <b>ponto certo de desafio</b>."
        ),
        bullets=[
            "Aumente a dificuldade aos poucos para manter o engajamento.",
            "Variabilidade controlada: micro-mudanças mantêm o cérebro interessado.",
            "Tédio (não falha) é o maior inimigo do hábito de longo prazo.",
            "Profissionais sustentam o tédio; amadores buscam novidade.",
        ],
        insights=[
            ("AMAR ENTREDIA",
             "A diferença entre profissionais e amadores não está nos picos de "
             "inspiração, está na constância na <b>entredia</b> — quando ninguém olha "
             "e nada parece estar mudando."),
        ],
        pull_quote="Tédio talvez seja o maior obstáculo no caminho do autoaperfeiçoamento.",
    )

    story.append(PageBreak())
    add_chapter(story, S, fw,
        chap_num="20", kicker="TÁTICAS AVANÇADAS",
        title="A desvantagem de criar bons hábitos",
        livro_pg="243",
        intro=(
            "Hábitos automatizam, mas também <b>anestesiam</b>. O preço da automaticidade "
            "é a perda de atenção crítica. Por isso, combine hábito (volume) com "
            "<b>prática deliberada</b> (qualidade) e <b>revisão periódica</b>."
        ),
        bullets=[
            "Reveja o sistema mensalmente; revise a identidade anualmente.",
            "Hábito + prática deliberada = mestria. Hábito sozinho = teto rápido.",
            "Pergunte: o que está funcionando e o que está apenas confortável?",
            "Mestres não se contentam com o automático; eles questionam o automático.",
        ],
        insights=[
            ("REFLEXÃO PROGRAMADA",
             "Sem revisão, hábitos viram trilhos. Programe rituais de revisão "
             "(diário no fim do dia, retro semanal, reset anual) para que o sistema "
             "não te impeça de crescer."),
        ],
        pull_quote="O sucesso não é uma meta a alcançar, é um sistema para melhorar.",
    )

    story.append(PageBreak())

    # =================================================
    # INSIGHTS PROFUNDOS
    # =================================================
    story.append(Paragraph("PROFUNDIDADE", S["label"]))
    story.append(Paragraph("Dez insights profundos do livro.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    insights_globais = [
        ("Hábito é arquitetura, não vontade",
         "A grande inversão de Clear é deslocar a mudança da arena moral "
         "(disciplina, força de vontade) para a arena do design (ambiente, atrito, "
         "deixas). Quando você acerta a arquitetura, a vontade vira secundária."),
        ("Identidade é a alavanca mais profunda",
         "Cada hábito é um voto em uma identidade. A maioria das pessoas tenta mudar "
         "o que faz; quem muda mais profundamente muda <b>quem é</b>."),
        ("Sistema acima de meta — mas com revisão",
         "Metas mostram direção, sistemas geram progresso. Mas há um perigo: "
         "alguns sistemas viram zonas de conforto. Sistemas precisam de revisão."),
        ("Vale da Decepção",
         "A maioria dos hábitos só rende após uma fase de estagnação aparente — "
         "como um cubo de gelo que vai de −5° a 0° sem mudança visível, e então "
         "derrete a +1°."),
        ("Atrito é destino",
         "Cada segundo entre você e a ação reduz drasticamente a chance da ação. "
         "Engenharia do atrito é mais decisiva do que motivação."),
        ("Dois minutos é portal, não truque",
         "A regra dos dois minutos não busca progresso, busca <b>aparição</b>. "
         "Consistência compõe e ausência apaga."),
        ("Identidade × Evidência",
         "Identidades são frágeis quando puramente afirmadas. Tornam-se sólidas "
         "quando lastreadas por evidências (ações)."),
        ("Hábito como liberdade",
         "Quando os básicos são automáticos, sobra atenção para o criativo. "
         "Disciplina é o caminho mais curto para a liberdade."),
        ("Tempo é a moeda, não o esforço",
         "Pequenos comportamentos consistentes vencem grandes esforços esporádicos. "
         "Quem entende a aritmética do composto para de buscar atalhos."),
        ("Ambiente é o psicoterapeuta mais barato",
         "Antes de mudar a si, mude a casa. Antes de mudar a casa, mude o quarto. "
         "Camadas de design fazem trabalho silencioso."),
    ]
    for i, (titulo, texto) in enumerate(insights_globais, 1):
        story.append(Paragraph(f"{i:02d}  ·  {titulo}", S["h3"]))
        story.append(Paragraph(texto, S["body"]))
        story.append(Spacer(1, 0.12*cm))

    story.append(PageBreak())

    # caderno de anotações dos insights — DotGrid
    story.append(Paragraph("REFLEXÃO PESSOAL", S["label"]))
    story.append(Paragraph("Seus insights × sua vida.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Escolha 3 insights que mais te atravessaram. Para cada um, responda: "
        "(1) onde reconheço isso na minha vida hoje? (2) qual seria a menor "
        "experiência possível para testar isso esta semana?", S["body_small"]))
    story.append(Spacer(1, 0.4*cm))
    story.append(DotGrid(fw, fh - 5*cm, spacing=0.5*cm, label="Espaço de reflexão"))

    story.append(PageBreak())

    # =================================================
    # PROTOCOLO: COMO MUDAR
    # =================================================
    story.append(Paragraph("PROTOCOLO", S["label"]))
    story.append(Paragraph("Como mudar  ·  o método.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Mudança eficaz não é épica, é metódica. Seis movimentos para qualquer "
        "mudança comportamental concreta.", S["serif_lead"]))

    passos = [
        ("01", "Defina a identidade-alvo",
         "Antes do quê, defina o quem. Escreva: “Eu sou alguém que ____.” "
         "Frase simples, no presente, com verbo de ação no infinitivo."),
        ("02", "Escolha 1 hábito atômico",
         "Apenas um. Pequeno o suficiente para caber em dois minutos. Conectado "
         "claramente à identidade-alvo."),
        ("03", "Engenheire as 4 leis",
         "Torne claro · atraente · fácil · satisfatório o que você quer; "
         "invisível · desinteressante · difícil · insatisfatório o que atrapalha."),
        ("04", "Crie a infraestrutura",
         "Mude o ambiente físico e digital. Pré-decida o que conseguir. Anote o "
         "quando + onde. Encaixe no empilhamento."),
        ("05", "Mensure de forma simples",
         "Rastreador binário: fez/não fez. Nunca falhar duas vezes seguidas. "
         "Revisão semanal. Aceite ruído, recuse tendência."),
        ("06", "Reveja o sistema",
         "A cada 30 dias: o que funcionou? O que é apenas confortável? "
         "A cada 12 meses: revise a identidade-alvo."),
    ]
    for num, tit, txt in passos:
        # tabela com numeral grande à esquerda
        tbl = Table(
            [[num, Paragraph(f"<b>{tit}</b><br/><font color='#2B2B2B'>{txt}</font>", S["body"])]],
            colWidths=[1.6*cm, fw - 1.6*cm]
        )
        tbl.setStyle(TableStyle([
            ("FONTNAME", (0,0), (0,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (0,0), 22),
            ("TEXTCOLOR", (0,0), (0,0), ACCENT),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LINEBELOW", (0,0), (-1,0), 0.3, HAIRLINE),
            ("LEFTPADDING", (0,0), (0,0), 0),
        ]))
        story.append(tbl)

    story.append(Spacer(1, 0.4*cm))
    story.append(Callout(fw,
        "Se a mudança precisa de força de vontade no terceiro dia, o problema é "
        "de design, não de caráter. Volte ao ambiente.",
        label="REGRA DE BOLSO"))

    story.append(PageBreak())

    # =================================================
    # PROTOCOLO: COMO EVOLUIR — 90 DIAS
    # =================================================
    story.append(Paragraph("PROGRESSÃO", S["label"]))
    story.append(Paragraph("Como evoluir  ·  plano de 90 dias.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Um ciclo curto é tempo suficiente para enraizar um hábito e curto o "
        "suficiente para não pesar. Três fases, 30 dias cada.",
        S["serif_lead"]))

    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=9.5, leading=13,
                           textColor=INK, alignment=TA_LEFT)
    fases = [
        ["FASE", "DIAS", "OBJETIVO", "PRÁTICA"],
        ["Implantar",  "1–30",
            Paragraph("Tornar o hábito visível, fácil e satisfatório.", cell),
            Paragraph("Regra dos 2 min · empilhamento · tracker binário", cell)],
        ["Aprofundar", "31–60",
            Paragraph("Subir a dificuldade até Cachinhos Dourados.", cell),
            Paragraph("Aumentar duração · variabilidade · revisão semanal", cell)],
        ["Consolidar", "61–90",
            Paragraph("Internalizar como identidade e blindar contra recaída.", cell),
            Paragraph("Contrato de hábito · parceiro · revisão mensal", cell)],
    ]
    ft = Table(fases, colWidths=[2.6*cm, 1.6*cm, 5.6*cm, fw - 2.6*cm - 1.6*cm - 5.6*cm])
    ft.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 7.5),
        ("TEXTCOLOR", (0,0), (-1,0), MUTED),
        ("BOTTOMPADDING", (0,0), (-1,0), 7),
        ("LINEBELOW", (0,0), (-1,0), 0.5, INK),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0,1), (0,-1), ACCENT),
        ("FONTSIZE", (0,1), (-1,-1), 9.5),
        ("BOTTOMPADDING", (0,1), (-1,-1), 9),
        ("TOPPADDING", (0,1), (-1,-1), 9),
        ("LINEBELOW", (0,1), (-1,-1), 0.25, HAIRLINE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(ft)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("Rotina diária recomendada", S["h2"]))
    rotina = [
        "<b>Manhã (5 min)</b> · revisar identidade-alvo + relembrar o hábito do dia.",
        "<b>Bloco do hábito</b> · executar na janela e no lugar pré-definidos.",
        "<b>Final do dia (2 min)</b> · marcar tracker + uma linha de reflexão.",
        "<b>Sexta-feira (10 min)</b> · revisar a semana. O que reforço? O que ajusto?",
        "<b>Último domingo do mês</b> · revisão mensal e nova meta de dificuldade.",
    ]
    for r in rotina:
        story.append(Paragraph("·  " + r, S["bullet"]))

    story.append(Spacer(1, 0.5*cm))
    story.append(NumberedLines(fw, num_lines=5, label="Anotações sobre minha evolução"))

    story.append(PageBreak())

    # =================================================
    # EXERCÍCIOS
    # =================================================
    story.append(Paragraph("PRÁTICA", S["label"]))
    story.append(Paragraph("Exercícios para fazer agora.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Doze exercícios — alguns curtos, outros recorrentes. Marque conforme "
        "conclui. Cobrem as 4 leis e mais identidade, revisão e ambiente.",
        S["serif_lead"]))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Identidade", S["h3"]))
    story.append(CheckboxList(fw, [
        "Escreva 3 identidades-alvo (frases iniciadas com 'Eu sou alguém que…').",
        "Para cada identidade, liste 5 evidências que você poderia produzir esta semana.",
    ]))
    story.append(Paragraph("1ª Lei  ·  Tornar claro", S["h3"]))
    story.append(CheckboxList(fw, [
        "Faça o Cartão de Pontuação: liste todos os seus hábitos diários e marque +, − ou =.",
        "Escreva 1 intenção de implementação: 'Eu vou [ação] em [horário] em [lugar]'.",
        "Crie 1 empilhamento: 'Depois de [hábito atual], eu vou [novo hábito]'.",
    ]))
    story.append(Paragraph("2ª Lei  ·  Tornar atraente", S["h3"]))
    story.append(CheckboxList(fw, [
        "Aplique o agrupamento de tentações: junte algo que precisa fazer a algo que gosta de fazer.",
        "Escolha 1 grupo (presencial ou online) cujos hábitos você queira herdar.",
    ]))
    story.append(Paragraph("3ª Lei  ·  Tornar fácil", S["h3"]))
    story.append(CheckboxList(fw, [
        "Reduza 2 hábitos novos à versão de 2 minutos e teste 7 dias seguidos.",
        "Elimine 3 atritos do ambiente para os bons hábitos; adicione 3 atritos para os maus.",
    ]))
    story.append(Paragraph("4ª Lei  ·  Tornar satisfatório", S["h3"]))
    story.append(CheckboxList(fw, [
        "Crie um rastreador (papel ou app) e marque a sequência diária.",
        "Defina 1 recompensa imediata (que reforce a identidade-alvo) após o hábito.",
        "Escreva um contrato de hábito com 1 parceiro de responsabilidade.",
    ]))
    story.append(Paragraph("Revisão", S["h3"]))
    story.append(CheckboxList(fw, [
        "Agende na agenda 1 revisão semanal de 15 minutos pelas próximas 12 semanas.",
    ]))

    story.append(PageBreak())

    # =================================================
    # CADERNO DE ANOTAÇÕES
    # =================================================
    story.append(Paragraph("CADERNO", S["label"]))
    story.append(Paragraph("Anotações livres.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Use estas páginas para registrar descobertas próprias, frases que te "
        "tocaram, conexões com sua vida, perguntas e revisões mensais.",
        S["body_small"]))
    story.append(Spacer(1, 0.4*cm))

    story.append(NumberedLines(fw, num_lines=8, label="O que aprendi com este livro"))
    story.append(Spacer(1, 0.5*cm))
    story.append(NumberedLines(fw, num_lines=8, label="O que vou mudar a partir de hoje"))

    story.append(PageBreak())

    # Revisão mensal — dot grid
    story.append(Paragraph("REVISÃO TRIMESTRAL", S["label"]))
    story.append(Paragraph("Mês 1   ·   Mês 2   ·   Mês 3.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph("Mês 1 — o que funcionou? o que não funcionou?", S["h3"]))
    story.append(DotGrid(fw, 5*cm, spacing=0.45*cm))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Mês 2 — o que evoluiu?", S["h3"]))
    story.append(DotGrid(fw, 5*cm, spacing=0.45*cm))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Mês 3 — qual identidade está se consolidando?", S["h3"]))
    story.append(DotGrid(fw, 5*cm, spacing=0.45*cm))

    story.append(PageBreak())
    # Página de fechamento
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("UM ÚLTIMO LEMBRETE", S["label"]))
    story.append(Paragraph("Aparecer é a habilidade mestra.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=10))
    story.append(PullQuote(fw,
        "Você não precisa fazer muito; precisa fazer o pouco, todo dia. O resto, o tempo faz por você.",
        attribution="Síntese do leitor", size=14))

    doc.build(story)


# ─────────────────────────────────────────────────────
# HELPER — Capítulo
# ─────────────────────────────────────────────────────

def add_chapter(story, S, fw, chap_num, kicker, title, livro_pg,
                intro, bullets, insights, pull_quote, pull_attr=None):
    story.append(BigNumber(fw, chap_num, kicker=kicker, color=INK))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph(title + ".", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=3))
    story.append(Paragraph(
        f"<font color='#{MUTED.hexval()[2:]}'>EDIÇÃO BR  ·  PÁG.</font> "
        f"<b>{livro_pg}</b>", S["caption"]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(intro, S["body"]))

    story.append(Paragraph("Pontos-chave", S["h2"]))
    for b in bullets:
        story.append(Paragraph("·  " + b, S["bullet"]))

    if pull_quote:
        story.append(Spacer(1, 0.15*cm))
        story.append(PullQuote(fw, pull_quote, attribution=pull_attr, size=12))

    if insights:
        story.append(Paragraph("Insights", S["h2"]))
        for label, txt in insights:
            story.append(Callout(fw, txt, label=label))
            story.append(Spacer(1, 0.1*cm))

    story.append(Spacer(1, 0.2*cm))
    story.append(NumberedLines(fw, num_lines=3, label="Suas anotações", line_spacing=0.7*cm))


if __name__ == "__main__":
    build()
    print(f"PDF gerado: {OUTPUT}")
