"""
Gerador de PDF — Resumo de "O Alquimista" (Paulo Coelho)
Design editorial moderno · paleta areia + ouro + bordô · tipografia serif-led.
"""

import math
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

OUTPUT = "/home/user/taskflow-pro/O_Alquimista_Resumo.pdf"

# ─── Patch: setCharSpace via TextObject ────────────────────────────
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
    if align == "right":  t.setTextOrigin(x - w, y)
    elif align == "center": t.setTextOrigin(x - w / 2.0, y)
    else: t.setTextOrigin(x, y)
    t.textOut(text)
    self.drawText(t)

Canvas.setCharSpace = _set_char_space
Canvas.drawString = lambda self, x, y, text: _draw_with_space(self, x, y, text, _orig_drawString, "left")
Canvas.drawRightString = lambda self, x, y, text: _draw_with_space(self, x, y, text, _orig_drawRightString, "right")
Canvas.drawCentredString = lambda self, x, y, text: _draw_with_space(self, x, y, text, _orig_drawCentredString, "center")

# ─────────────────────────────────────────────────────
# IDENTIDADE VISUAL — paleta de "manuscrito alquímico"
# ─────────────────────────────────────────────────────
PAPER       = HexColor("#F2EAD3")  # papyrus / areia clara
PAPER_DARK  = HexColor("#E5DAB7")  # tom mais profundo para o numeral fantasma
INK         = HexColor("#1A1612")  # preto quente, quase betume
SUBINK      = HexColor("#3A332A")
MUTED       = HexColor("#8C7E5D")  # ocre apagado para legendas
HAIRLINE    = HexColor("#C5BB9F")  # linha fina cor terra
ACCENT      = HexColor("#9C6B1F")  # ouro queimado
ACCENT_DEEP = HexColor("#7A2025")  # bordô — para ênfase pontual
GOLD_LIGHT  = HexColor("#D6A65A")  # ouro claro p/ detalhes
INVERSE_INK = HexColor("#1A1612")  # fundo escuro nos divisores

PAGE_W, PAGE_H = A4
MARGIN_L = 2.4*cm
MARGIN_R = 2.4*cm
MARGIN_T = 2.6*cm
MARGIN_B = 2.4*cm


# ─────────────────────────────────────────────────────
# FLOWABLES CUSTOMIZADOS
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


class JournalLines(Flowable):
    """Linhas de caderno antigo — sem numeração, suaves, evocando um diário de viagem."""
    def __init__(self, width, num_lines=8, line_spacing=0.8*cm, color=HAIRLINE, label=None):
        Flowable.__init__(self)
        self.width = width; self.num_lines = num_lines
        self.line_spacing = line_spacing; self.color = color; self.label = label
        extra = 0.85*cm if label else 0
        self.height = num_lines * line_spacing + extra + 0.2*cm
    def draw(self):
        c = self.canv
        y_top = self.height
        if self.label:
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(MUTED)
            c.setCharSpace(1.8)
            c.drawString(0, y_top - 0.35*cm, self.label.upper())
            c.setCharSpace(0)
            y_top -= 0.85*cm
        c.setStrokeColor(self.color)
        c.setLineWidth(0.3)
        for i in range(self.num_lines):
            yy = y_top - (i+1) * self.line_spacing
            c.line(0, yy, self.width, yy)


class ReflectionPrompt(Flowable):
    """Prompt reflexivo — pergunta em serif itálica + espaço para resposta com sub-linhas."""
    def __init__(self, width, prompt, num_lines=3, line_spacing=0.78*cm):
        Flowable.__init__(self)
        self.width = width; self.prompt = prompt
        self.num_lines = num_lines; self.line_spacing = line_spacing
        # Calcular altura do texto da pergunta com wrap
        from reportlab.pdfbase.pdfmetrics import stringWidth
        font, size = "Times-Italic", 11.5
        avail = width - 0.6*cm
        words = prompt.split()
        line = ""; lines = 1
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, font, size) <= avail: line = test
            else: lines += 1; line = w
        self.q_height = lines * size * 1.35 + 0.3*cm
        self.height = self.q_height + num_lines * line_spacing + 0.3*cm

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
        # marca dourada à esquerda
        c.setFillColor(ACCENT)
        c.rect(0, self.height - self.q_height + 0.1*cm, 0.05*cm, self.q_height - 0.2*cm, stroke=0, fill=1)
        # pergunta em serif itálico
        c.setFont("Times-Italic", 11.5)
        c.setFillColor(INK)
        lines = self._wrap(self.prompt, self.width - 0.6*cm, "Times-Italic", 11.5)
        y = self.height - 11.5
        for ln in lines:
            c.drawString(0.4*cm, y, ln)
            y -= 11.5 * 1.35
        # linhas de resposta abaixo
        c.setStrokeColor(HAIRLINE)
        c.setLineWidth(0.3)
        y_base = self.height - self.q_height
        for i in range(self.num_lines):
            yy = y_base - (i+1) * self.line_spacing
            c.line(0.4*cm, yy, self.width, yy)


class GildedCallout(Flowable):
    """Callout com canto dourado — uma borda L de ouro queimado, sem fundo."""
    def __init__(self, width, text, label="MENSAGEM", padding=0.55*cm):
        Flowable.__init__(self)
        self.width = width; self.text = text
        self.label = label; self.padding = padding
        from reportlab.pdfbase.pdfmetrics import stringWidth
        font, size = "Helvetica", 10
        avail = width - 2*padding - 0.4*cm
        words = text.split()
        line = ""; lines = 1
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, font, size) <= avail: line = test
            else: lines += 1; line = w
        self.height = lines * size * 1.45 + 2*padding

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
        h = self.height; w = self.width
        # cantos em "L" dourados — apenas duas marcas no canto sup. esq. e inf. dir.
        c.setStrokeColor(ACCENT)
        c.setLineWidth(1.0)
        # canto superior esquerdo
        c.line(0, h, 0, h - 0.6*cm)
        c.line(0, h, 0.6*cm, h)
        # canto inferior direito
        c.line(w, 0, w, 0.6*cm)
        c.line(w, 0, w - 0.6*cm, 0)
        # label
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(ACCENT)
        c.setCharSpace(1.8)
        c.drawString(self.padding + 0.2*cm, h - self.padding + 0.15*cm, self.label.upper())
        c.setCharSpace(0)
        # texto
        c.setFont("Helvetica", 10)
        c.setFillColor(INK)
        lines = self._wrap(self.text, w - 2*self.padding - 0.4*cm, "Helvetica", 10)
        y = h - self.padding - 0.5*cm
        for ln in lines:
            c.drawString(self.padding + 0.2*cm, y, ln)
            y -= 10 * 1.45


class CenteredQuote(Flowable):
    """Citação grande, centralizada — para a parede de citações."""
    def __init__(self, width, text, attribution=None, size=18, color=INK):
        Flowable.__init__(self)
        self.width = width; self.text = text
        self.attribution = attribution; self.size = size; self.color = color
        from reportlab.pdfbase.pdfmetrics import stringWidth
        avail = width * 0.92
        words = text.split()
        line = ""; lines = 1
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, "Times-Italic", size) <= avail: line = test
            else: lines += 1; line = w
        self.height = lines * size * 1.3 + (0.6*cm if attribution else 0) + 0.4*cm

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
        c.setFont("Times-Italic", self.size)
        c.setFillColor(self.color)
        lines = self._wrap(self.text, self.width * 0.92, "Times-Italic", self.size)
        y = self.height - self.size
        for ln in lines:
            c.drawCentredString(self.width / 2.0, y, ln)
            y -= self.size * 1.3
        if self.attribution:
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(MUTED)
            c.setCharSpace(2)
            c.drawCentredString(self.width / 2.0, y - 0.2*cm, self.attribution.upper())
            c.setCharSpace(0)


class StageNumber(Flowable):
    """Numeral display de parte — usa SERIF Times-Bold para feel literário."""
    def __init__(self, width, number, kicker=None, color=INK):
        Flowable.__init__(self)
        self.width = width; self.number = str(number)
        self.kicker = kicker; self.color = color
        self.height = 3.2*cm

    def draw(self):
        c = self.canv
        # numeral em SERIF — Times-Bold
        c.setFont("Times-Bold", 80)
        c.setFillColor(self.color)
        c.drawString(0, 0.4*cm, self.number)
        from reportlab.pdfbase.pdfmetrics import stringWidth
        w = stringWidth(self.number, "Times-Bold", 80)
        # ornamento dourado debaixo do número
        c.setStrokeColor(ACCENT)
        c.setLineWidth(1.4)
        c.line(0, 0.2*cm, w, 0.2*cm)
        # kicker do lado
        if self.kicker:
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(MUTED)
            c.setCharSpace(2.2)
            c.drawString(w + 0.5*cm, 2.55*cm, self.kicker.upper())
            c.setCharSpace(0)


class JourneyMap(Flowable):
    """Timeline horizontal — pontos numa linha central, labels alternam acima/abaixo."""
    def __init__(self, width, points, height=8*cm):
        Flowable.__init__(self)
        self.width = width; self.height = height; self.points = points

    def draw(self):
        c = self.canv
        n = len(self.points)
        margin = 0.8*cm
        usable_w = self.width - 2*margin
        step = usable_w / (n - 1) if n > 1 else 0
        # linha central da timeline
        cy = self.height / 2
        # linha contínua fina conectando todos os pontos
        c.setStrokeColor(ACCENT)
        c.setLineWidth(0.6)
        c.setDash(2, 3)
        c.line(margin, cy, margin + (n-1) * step, cy)
        c.setDash([])
        # marcadores e labels alternados (par acima, ímpar abaixo)
        for i, (label, sub) in enumerate(self.points):
            x = margin + i * step
            # marcador: círculo dourado preenchido + aro
            c.setFillColor(ACCENT)
            c.setStrokeColor(ACCENT)
            c.circle(x, cy, 0.16*cm, stroke=0, fill=1)
            c.setFillColor(PAPER)
            c.setStrokeColor(ACCENT)
            c.setLineWidth(0.6)
            c.circle(x, cy, 0.3*cm, stroke=1, fill=0)
            # texto: par (0,2,4,6) acima, ímpar (1,3,5) abaixo
            above = (i % 2 == 0)
            if above:
                # número da etapa em dourado
                c.setFont("Helvetica-Bold", 7)
                c.setFillColor(ACCENT)
                c.setCharSpace(1.5)
                c.drawCentredString(x, cy + 2.4*cm, f"ETAPA {i+1:02d}")
                c.setCharSpace(0)
                # tick vertical do ponto até o label
                c.setStrokeColor(HAIRLINE)
                c.setLineWidth(0.3)
                c.line(x, cy + 0.4*cm, x, cy + 2.0*cm)
                # label
                c.setFont("Helvetica-Bold", 9.5)
                c.setFillColor(INK)
                c.drawCentredString(x, cy + 1.7*cm, label)
                # sub
                if sub:
                    c.setFont("Times-Italic", 8.5)
                    c.setFillColor(MUTED)
                    c.drawCentredString(x, cy + 1.2*cm, sub)
            else:
                c.setFont("Helvetica-Bold", 7)
                c.setFillColor(ACCENT)
                c.setCharSpace(1.5)
                c.drawCentredString(x, cy - 2.6*cm, f"ETAPA {i+1:02d}")
                c.setCharSpace(0)
                c.setStrokeColor(HAIRLINE)
                c.setLineWidth(0.3)
                c.line(x, cy - 0.4*cm, x, cy - 1.4*cm)
                c.setFont("Helvetica-Bold", 9.5)
                c.setFillColor(INK)
                c.drawCentredString(x, cy - 1.7*cm, label)
                if sub:
                    c.setFont("Times-Italic", 8.5)
                    c.setFillColor(MUTED)
                    c.drawCentredString(x, cy - 2.2*cm, sub)


class SymbolGrid(Flowable):
    """Grade de símbolos alquímicos — geometria simples (círculo, triângulo, etc.)."""
    def __init__(self, width, symbols, cols=3, cell_h=4*cm):
        """ symbols: lista de (sym_name, title, description) """
        Flowable.__init__(self)
        self.width = width; self.symbols = symbols
        self.cols = cols; self.cell_h = cell_h
        self.rows = (len(symbols) + cols - 1) // cols
        self.height = self.rows * cell_h

    def _draw_symbol(self, c, x, y, name, size=0.9*cm):
        """Desenha o símbolo geometrico no centro de (x, y)."""
        c.setStrokeColor(ACCENT)
        c.setFillColor(ACCENT)
        c.setLineWidth(0.9)
        if name == "sol":          # círculo com ponto (ouro alquímico)
            c.circle(x, y, size, stroke=1, fill=0)
            c.circle(x, y, 0.12*cm, stroke=0, fill=1)
        elif name == "triangulo":  # triângulo equilátero
            h = size * 1.732/2
            c.line(x - size, y - h, x + size, y - h)
            c.line(x - size, y - h, x, y + h)
            c.line(x + size, y - h, x, y + h)
        elif name == "ampulheta":  # dois triângulos
            h = size
            c.line(x - size*0.8, y + h, x + size*0.8, y + h)
            c.line(x - size*0.8, y - h, x + size*0.8, y - h)
            c.line(x - size*0.8, y + h, x + size*0.8, y - h)
            c.line(x + size*0.8, y + h, x - size*0.8, y - h)
        elif name == "olho":       # círculo com olho (linha + íris)
            c.ellipse(x - size, y - size*0.5, x + size, y + size*0.5, stroke=1, fill=0)
            c.circle(x, y, size*0.3, stroke=1, fill=0)
            c.circle(x, y, size*0.1, stroke=0, fill=1)
        elif name == "ovo":        # ovo alquímico — elipse vertical
            c.ellipse(x - size*0.7, y - size, x + size*0.7, y + size, stroke=1, fill=0)
        elif name == "pirâmide":   # triângulo isóceles
            c.line(x - size, y - size*0.6, x + size, y - size*0.6)
            c.line(x - size, y - size*0.6, x, y + size)
            c.line(x + size, y - size*0.6, x, y + size)
        elif name == "circuloduplo":
            c.circle(x, y, size, stroke=1, fill=0)
            c.circle(x, y, size*0.6, stroke=1, fill=0)
        elif name == "cruz":       # cruz simples
            c.line(x - size, y, x + size, y)
            c.line(x, y - size, x, y + size)
        elif name == "lua":        # crescente
            c.circle(x, y, size, stroke=1, fill=0)
            c.setFillColor(PAPER)
            c.circle(x + size*0.4, y, size*0.85, stroke=0, fill=1)
            c.setStrokeColor(ACCENT)
            c.setFillColor(ACCENT)

    def draw(self):
        c = self.canv
        cell_w = self.width / self.cols
        for i, (sym, title, desc) in enumerate(self.symbols):
            col = i % self.cols
            row = i // self.cols
            cx = col * cell_w + cell_w / 2
            cy = self.height - (row + 1) * self.cell_h + self.cell_h * 0.65
            # símbolo
            self._draw_symbol(c, cx, cy, sym)
            # título
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(INK)
            c.drawCentredString(cx, cy - 1.6*cm, title)
            # descrição
            c.setFont("Helvetica", 8)
            c.setFillColor(MUTED)
            # wrap simples
            from reportlab.pdfbase.pdfmetrics import stringWidth
            avail = cell_w - 0.6*cm
            words = desc.split()
            line = ""; lines = []
            for w in words:
                test = (line + " " + w).strip()
                if stringWidth(test, "Helvetica", 8) <= avail: line = test
                else: lines.append(line); line = w
            if line: lines.append(line)
            dy = cy - 2.0*cm
            for ln in lines[:3]:
                c.drawCentredString(cx, dy, ln)
                dy -= 9


class CharacterCard(Flowable):
    """Cartão de personagem — barra dourada, nome em bold, papel em itálico, descrição."""
    def __init__(self, width, name, role, description, height=2.8*cm):
        Flowable.__init__(self)
        self.width = width; self.height = height
        self.name = name; self.role = role; self.description = description

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
        # barra esquerda dourada
        c.setFillColor(ACCENT)
        c.rect(0, 0, 0.08*cm, self.height, stroke=0, fill=1)
        # nome
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(INK)
        c.drawString(0.35*cm, self.height - 0.55*cm, self.name)
        # papel
        c.setFont("Times-Italic", 10)
        c.setFillColor(ACCENT)
        c.drawString(0.35*cm, self.height - 1.05*cm, self.role)
        # descrição
        c.setFont("Helvetica", 9)
        c.setFillColor(SUBINK)
        lines = self._wrap(self.description, self.width - 0.5*cm, "Helvetica", 9)
        y = self.height - 1.5*cm
        for ln in lines[:3]:
            c.drawString(0.35*cm, y, ln)
            y -= 9 * 1.4


# ─────────────────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────────────────

def make_styles():
    s = {}
    s["display"] = ParagraphStyle("display", fontName="Times-Bold", fontSize=58, leading=60,
                                   textColor=INK, alignment=TA_LEFT, spaceAfter=10)
    s["title_sub"] = ParagraphStyle("title_sub", fontName="Times-Italic", fontSize=16, leading=22,
                                     textColor=SUBINK, alignment=TA_LEFT, spaceAfter=6)
    s["label"] = ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=8, leading=11,
                                 textColor=ACCENT, alignment=TA_LEFT, spaceAfter=4)
    s["section"] = ParagraphStyle("section", fontName="Times-Bold", fontSize=26, leading=30,
                                   textColor=INK, alignment=TA_LEFT, spaceBefore=2, spaceAfter=4)
    s["h2"] = ParagraphStyle("h2", fontName="Times-Bold", fontSize=13, leading=16.5,
                              textColor=INK, alignment=TA_LEFT, spaceBefore=10, spaceAfter=3)
    s["h3"] = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10, leading=14,
                              textColor=ACCENT, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4)
    s["body"] = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=15.5,
                                textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)
    s["body_small"] = ParagraphStyle("body_small", fontName="Helvetica", fontSize=9, leading=13,
                                      textColor=SUBINK, alignment=TA_JUSTIFY, spaceAfter=4)
    s["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=13.5,
                                  textColor=INK, alignment=TA_LEFT, leftIndent=14, bulletIndent=2,
                                  spaceAfter=2)
    s["serif_lead"] = ParagraphStyle("serif_lead", fontName="Times-Italic", fontSize=13, leading=18,
                                      textColor=SUBINK, alignment=TA_LEFT, spaceAfter=8)
    s["caption"] = ParagraphStyle("caption", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
                                   textColor=MUTED, alignment=TA_LEFT, spaceAfter=4)
    return s


# ─────────────────────────────────────────────────────
# DESENHO DAS PÁGINAS  — capa, divisores, corpo
# ─────────────────────────────────────────────────────

def draw_paper_bg(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)


def draw_sun_symbol(c, cx, cy, r=2.6*cm, rays=12):
    """Símbolo do sol alquímico — círculo central + ponto + raios curtos."""
    c.setStrokeColor(ACCENT)
    c.setFillColor(ACCENT)
    c.setLineWidth(0.7)
    c.circle(cx, cy, r, stroke=1, fill=0)
    # raios
    for i in range(rays):
        ang = 2 * math.pi * i / rays
        x1 = cx + (r + 0.2*cm) * math.cos(ang)
        y1 = cy + (r + 0.2*cm) * math.sin(ang)
        x2 = cx + (r + 0.7*cm) * math.cos(ang)
        y2 = cy + (r + 0.7*cm) * math.sin(ang)
        c.line(x1, y1, x2, y2)
    # ponto central
    c.circle(cx, cy, 0.2*cm, stroke=0, fill=1)


def draw_cover(c, doc):
    draw_paper_bg(c)

    # rule no topo
    c.setStrokeColor(INK)
    c.setLineWidth(0.7)
    c.line(MARGIN_L, PAGE_H - 1.6*cm, PAGE_W - MARGIN_L, PAGE_H - 1.6*cm)

    # marca tipográfica topo
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(INK)
    c.setCharSpace(3)
    c.drawString(MARGIN_L, PAGE_H - 1.25*cm, "RESUMO · VOL. 02")
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.25*cm, "ED. MAIO 2026")
    c.setCharSpace(0)

    # numeral fantasma "02" em serif (Times-Bold)
    c.setFont("Times-Bold", 230)
    c.setFillColor(PAPER_DARK)
    c.drawString(MARGIN_L - 0.3*cm, PAGE_H - 10.5*cm, "02")

    # kicker categoria
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(ACCENT)
    c.setCharSpace(2.2)
    c.drawString(MARGIN_L, PAGE_H - 12.2*cm, "FÁBULA  ·  FILOSÓFICO  ·  LITERATURA BRASILEIRA")
    c.setCharSpace(0)

    # título display — SERIF, grande
    c.setFont("Times-Bold", 78)
    c.setFillColor(INK)
    c.drawString(MARGIN_L, PAGE_H - 14.8*cm, "O")
    c.drawString(MARGIN_L, PAGE_H - 17.0*cm, "Alquimista.")

    # subtítulo serif itálico
    c.setFont("Times-Italic", 14)
    c.setFillColor(SUBINK)
    c.drawString(MARGIN_L, PAGE_H - 18.3*cm, "Uma fábula sobre seguir os sonhos. A jornada")
    c.drawString(MARGIN_L, PAGE_H - 18.9*cm, "do pastor Santiago em busca de sua Lenda Pessoal.")

    # rule curta de divisão
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.4)
    c.line(MARGIN_L, PAGE_H - 19.9*cm, MARGIN_L + 2.5*cm, PAGE_H - 19.9*cm)

    # autor
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(MUTED)
    c.setCharSpace(2)
    c.drawString(MARGIN_L, PAGE_H - 20.5*cm, "AUTOR ORIGINAL")
    c.setCharSpace(0)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(INK)
    c.drawString(MARGIN_L, PAGE_H - 21.2*cm, "Paulo Coelho")

    # Sol alquímico no canto inferior direito
    draw_sun_symbol(c, PAGE_W - 5.2*cm, 7.5*cm, r=2.4*cm, rays=12)

    # Rodapé
    c.setStrokeColor(INK)
    c.setLineWidth(0.5)
    c.line(MARGIN_L, 2.3*cm, PAGE_W - MARGIN_R, 2.3*cm)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(MUTED)
    c.setCharSpace(2.5)
    c.drawString(MARGIN_L, 1.7*cm, "CADERNO DE LEITURA  ·  RESUMO · CONCEITOS · CADERNO DE JORNADA")
    c.drawRightString(PAGE_W - MARGIN_R, 1.7*cm, "FORMATO A4")
    c.setCharSpace(0)


def draw_body_chrome(c, doc):
    draw_paper_bg(c)
    # Header
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(MUTED)
    c.setCharSpace(2.5)
    c.drawString(MARGIN_L, PAGE_H - 1.3*cm, "O ALQUIMISTA")
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.3*cm, "PAULO COELHO  ·  RESUMO 02")
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
    # Número de página em destaque, com pequeno marcador dourado à esquerda
    c.setFillColor(ACCENT)
    c.circle(PAGE_W - MARGIN_R - 1.2*cm, 1.4*cm, 0.08*cm, stroke=0, fill=1)
    c.setFont("Times-Bold", 11)
    c.setFillColor(INK)
    c.drawRightString(PAGE_W - MARGIN_R, 1.25*cm, f"{page_num:02d}")


def draw_part_divider_factory(eyebrow, title_lines, subtitle):
    def _draw(c, doc):
        # fundo escuro betume
        c.setFillColor(INVERSE_INK)
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        # rule topo
        c.setStrokeColor(HexColor("#3A332A"))
        c.setLineWidth(0.3)
        c.line(MARGIN_L, PAGE_H - 1.55*cm, PAGE_W - MARGIN_R, PAGE_H - 1.55*cm)
        # header
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(HexColor("#9A8E6C"))
        c.setCharSpace(2.5)
        c.drawString(MARGIN_L, PAGE_H - 1.3*cm, "O ALQUIMISTA")
        c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.3*cm, "PAULO COELHO  ·  RESUMO 02")
        c.setCharSpace(0)

        # eyebrow em dourado
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(GOLD_LIGHT)
        c.setCharSpace(3)
        c.drawString(MARGIN_L, PAGE_H - 8.5*cm, eyebrow.upper())
        c.setCharSpace(0)

        # título em SERIF Times-Bold creme
        c.setFont("Times-Bold", 70)
        c.setFillColor(PAPER)
        y = PAGE_H - 11.5*cm
        for ln in title_lines:
            c.drawString(MARGIN_L, y, ln)
            y -= 4.4*cm

        # rule dourado
        c.setStrokeColor(ACCENT)
        c.setLineWidth(1.6)
        c.line(MARGIN_L, y + 1.6*cm, MARGIN_L + 2.8*cm, y + 1.6*cm)

        # subtítulo serif italico
        c.setFont("Times-Italic", 14)
        c.setFillColor(HexColor("#D6CCA8"))
        from reportlab.pdfbase.pdfmetrics import stringWidth
        words = subtitle.split()
        line = ""; cy = y + 0.6*cm
        avail = PAGE_W - MARGIN_L - MARGIN_R - 2*cm
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, "Times-Italic", 14) <= avail: line = test
            else: c.drawString(MARGIN_L, cy, line); cy -= 18; line = w
        if line: c.drawString(MARGIN_L, cy, line)

        # Símbolo do sol pequeno no canto inferior direito
        c.setStrokeColor(GOLD_LIGHT)
        c.setLineWidth(0.5)
        c.setFillColor(GOLD_LIGHT)
        c.circle(PAGE_W - 3.5*cm, 5*cm, 1.0*cm, stroke=1, fill=0)
        for i in range(8):
            ang = 2 * math.pi * i / 8
            cx = PAGE_W - 3.5*cm
            cy = 5*cm
            x1 = cx + 1.1*cm * math.cos(ang); y1 = cy + 1.1*cm * math.sin(ang)
            x2 = cx + 1.4*cm * math.cos(ang); y2 = cy + 1.4*cm * math.sin(ang)
            c.line(x1, y1, x2, y2)
        c.circle(PAGE_W - 3.5*cm, 5*cm, 0.12*cm, stroke=0, fill=1)

        # rodapé
        page_num = c.getPageNumber()
        c.setStrokeColor(HexColor("#3A332A"))
        c.setLineWidth(0.3)
        c.line(MARGIN_L, 1.7*cm, PAGE_W - MARGIN_R, 1.7*cm)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(HexColor("#9A8E6C"))
        c.setCharSpace(2.5)
        c.drawString(MARGIN_L, 1.3*cm, "RESUMO · LEITURA BREVE")
        c.setCharSpace(0)
        c.setFillColor(GOLD_LIGHT)
        c.circle(PAGE_W - MARGIN_R - 1.2*cm, 1.4*cm, 0.08*cm, stroke=0, fill=1)
        c.setFont("Times-Bold", 11)
        c.setFillColor(PAPER)
        c.drawRightString(PAGE_W - MARGIN_R, 1.25*cm, f"{page_num:02d}")
    return _draw


# ─────────────────────────────────────────────────────
# CONSTRUÇÃO DO DOCUMENTO
# ─────────────────────────────────────────────────────

def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title="O Alquimista — Resumo",
        author="Resumo a partir da obra de Paulo Coelho",
    )

    fw = PAGE_W - MARGIN_L - MARGIN_R
    fh = PAGE_H - MARGIN_T - MARGIN_B

    cover_frame = Frame(MARGIN_L, MARGIN_B, fw, fh, id="cover", showBoundary=0)
    body_frame  = Frame(MARGIN_L, MARGIN_B, fw, fh - 0.4*cm, id="body", showBoundary=0)

    templates = [
        PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover),
        PageTemplate(id="body",  frames=[body_frame],  onPage=draw_body_chrome),
    ]

    partes = [
        ("p1", "Parte I",  ["Andaluzia."],
         "Onde o pastor Santiago tem um sonho e encontra o velho Rei de Salém."),
        ("p2", "Parte II", ["Tânger."],
         "Onde tudo se perde, e a loja de cristais ensina que perder e renascer caminham juntos."),
        ("p3", "Parte III",["O deserto."],
         "Onde a caravana atravessa o tempo, e o silêncio começa a falar."),
        ("p4", "Parte IV", ["O oásis."],
         "Onde Santiago conhece Fátima, o Alquimista, e aprende a Linguagem do Mundo."),
        ("p5", "Parte V",  ["O tesouro."],
         "Onde o caminho retorna ao ponto de partida — e revela o sentido inteiro."),
    ]
    for tid, eyebrow, title_lines, subt in partes:
        templates.append(
            PageTemplate(id=tid,
                frames=[Frame(MARGIN_L, MARGIN_B, fw, fh, id=tid, showBoundary=0)],
                onPage=draw_part_divider_factory(eyebrow, title_lines, subt))
        )

    doc.addPageTemplates(templates)

    S = make_styles()
    story = []

    # ============== CAPA ==============
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # ============== FICHA TÉCNICA ==============
    story.append(Paragraph("FICHA TÉCNICA", S["label"]))
    story.append(Paragraph("Sobre esta edição.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    story.append(Paragraph(
        "Caderno de leitura de <b>O Alquimista</b>, romance-fábula de Paulo Coelho. "
        "Reúne sinopse, mapa da jornada, conceitos-chave, resumo por partes, "
        "símbolos, mensagens profundas, citações em destaque e espaço próprio para "
        "anotar a sua jornada de leitor.", S["serif_lead"]))
    story.append(Spacer(1, 0.3*cm))

    ficha = [
        ["Título original",   "O Alquimista"],
        ["Edição em inglês",  "The Alchemist"],
        ["Autor",             "Paulo Coelho"],
        ["Editora original",  "Rocco (1988); Sextante (edições contemporâneas)"],
        ["Primeira publicação","1988 (Brasil)"],
        ["Páginas (edição BR)","Aproximadamente 184 páginas"],
        ["Gênero",            "Romance · Fábula filosófica"],
        ["Idiomas",           "Traduzido em mais de 80 idiomas"],
        ["Vendas globais",    "Acima de 65 milhões de exemplares"],
        ["Status no Brasil",  "Maior bestseller brasileiro de todos os tempos"],
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

    story.append(CenteredQuote(fw,
        "Quando você quer alguma coisa, todo o universo conspira para que você realize o seu desejo.",
        attribution="Paulo Coelho · O Alquimista", size=15))

    story.append(PageBreak())

    # ============== SUMÁRIO ==============
    story.append(Paragraph("NAVEGAÇÃO", S["label"]))
    story.append(Paragraph("Sumário.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    story.append(Paragraph(
        "Paginação deste caderno. A jornada está dividida em cinco partes, "
        "precedidas pelos pilares conceituais e seguidas por símbolos, "
        "mensagens, citações e o seu próprio caderno de jornada.",
        S["body_small"]))
    story.append(Spacer(1, 0.5*cm))

    # Sumário com paginação real (apurada após primeira renderização)
    sumario = [
        ("",   "Capa",                                         "1"),
        ("",   "Ficha técnica",                                "2"),
        ("",   "Sumário",                                      "3"),
        ("",   "Sobre o autor",                                "4"),
        ("",   "Sinopse em uma página",                        "5"),
        ("",   "Personagens da jornada",                       "6"),
        ("",   "Pilares conceituais",                          "7"),
        ("",   "Mapa da jornada",                              "8"),
        ("I",  "Andaluzia — o pastor e o sonho",               "9"),
        ("·",  "Santiago, o sonho recorrente e a cigana",     "10"),
        ("·",  "Tarifa: o encontro com Melquisedeque",        "11"),
        ("II", "Tânger — a perda e a loja de cristais",       "12"),
        ("·",  "O roubo e a primeira morte",                  "13"),
        ("·",  "Onze meses entre os cristais",                "14"),
        ("III","O deserto — a caravana atravessa o tempo",    "15"),
        ("·",  "O inglês e a leitura do mundo",               "16"),
        ("·",  "Sinais, guerras e silêncio",                  "17"),
        ("IV", "O oásis — Fátima e o Alquimista",             "18"),
        ("·",  "Os falcões, a visão e a salvação do oásis",  "19"),
        ("·",  "O Alquimista o aceita como discípulo",        "20"),
        ("V",  "O tesouro — a travessia final",               "21"),
        ("·",  "As provas: tornar-se vento",                  "22"),
        ("·",  "As pirâmides e o retorno",                    "23"),
        ("",   "Símbolos da obra",                            "24"),
        ("",   "Mensagens profundas",                         "25"),
        ("",   "A linguagem do mundo",                        "26"),
        ("",   "Citações em destaque",                        "27"),
        ("",   "Reflexões para a sua jornada",                "28"),
        ("",   "Caderno de jornada",                          "29"),
        ("",   "Última palavra",                              "30"),
    ]
    toc_style = ParagraphStyle("toc", fontName="Helvetica", fontSize=9, leading=12,
                                textColor=INK, alignment=TA_LEFT)
    toc_meta = ParagraphStyle("toc_m", fontName="Times-Italic", fontSize=9, leading=12,
                               textColor=SUBINK, alignment=TA_LEFT)
    toc_part = ParagraphStyle("toc_p", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
                               textColor=ACCENT, alignment=TA_LEFT)
    rows = []
    for tag, title, pg in sumario:
        is_part = tag in ("I", "II", "III", "IV", "V")
        is_meta = (tag == "" and title not in ("Capa","Ficha técnica","Sumário",
                                                "Sobre o autor","Sinopse em uma página",
                                                "Personagens da jornada","Pilares conceituais",
                                                "Mapa da jornada","Símbolos da obra",
                                                "Mensagens profundas","A linguagem do mundo",
                                                "Citações em destaque","Reflexões para a sua jornada",
                                                "Caderno de jornada","Última palavra"))
        if is_part:
            style = toc_part
        elif tag == "·":
            style = toc_meta
        else:
            style = toc_style
        rows.append([tag if tag else "·",
                     Paragraph(title, style),
                     pg])

    tbl = Table(rows, colWidths=[1.0*cm, fw - 3.0*cm, 1.5*cm])
    cmds = [
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (0,-1), 8.5),
        ("TEXTCOLOR", (0,0), (0,-1), ACCENT),
        ("FONTNAME", (2,0), (2,-1), "Helvetica"),
        ("FONTSIZE", (2,0), (2,-1), 8.5),
        ("TEXTCOLOR", (2,0), (2,-1), MUTED),
        ("ALIGN", (2,0), (2,-1), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]
    for i, (tag, _, _) in enumerate(sumario):
        if tag in ("I", "II", "III", "IV", "V"):
            cmds.append(("LINEABOVE", (0,i), (-1,i), 0.4, HAIRLINE))
            cmds.append(("TOPPADDING", (0,i), (-1,i), 5))
            cmds.append(("BOTTOMPADDING", (0,i), (-1,i), 3))
    tbl.setStyle(TableStyle(cmds))
    story.append(tbl)

    story.append(PageBreak())

    # ============== SOBRE O AUTOR ==============
    story.append(Paragraph("AUTOR", S["label"]))
    story.append(Paragraph("Sobre Paulo Coelho.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    story.append(Paragraph(
        "<b>Paulo Coelho de Souza</b> nasceu no Rio de Janeiro em 24 de agosto de 1947. "
        "Letrista de Raul Seixas no início dos anos 1970, dramaturgo, jornalista e "
        "viajante incansável, encontrou na escrita o seu próprio caminho a partir do "
        "fim dos anos 1980 — depois de uma travessia pessoal de Saint-Jean-Pied-de-Port "
        "a Santiago de Compostela.", S["body"]))
    story.append(Paragraph(
        "<i>O Diário de um Mago</i> (1987), publicado a partir dessa caminhada, foi o "
        "primeiro de uma sucessão de livros que se tornariam bestsellers em mais de 80 "
        "idiomas. Em 1988 publica <b>O Alquimista</b>, sua obra mais reconhecida, "
        "vendendo, ao longo das décadas, mais de 65 milhões de exemplares no mundo todo.",
        S["body"]))

    story.append(Paragraph("Linha temática", S["h2"]))
    story.append(Paragraph(
        "Coelho costura, em seus livros, três fios: a <b>busca pessoal</b> (o caminho "
        "como personagem), o <b>simbolismo</b> herdado do esoterismo cristão e da "
        "alquimia ocidental, e a <b>simplicidade narrativa</b> de quem prefere a parábola "
        "à demonstração. <i>O Alquimista</i> sintetiza os três.", S["body"]))

    story.append(Paragraph("Outras obras essenciais", S["h2"]))
    livros = [
        "<b>O Diário de um Mago</b> (1987) — A caminhada de Compostela.",
        "<b>Brida</b> (1990) — A escola da Lua e a tradição feminina.",
        "<b>Na Margem do Rio Piedra Eu Sentei e Chorei</b> (1994) — Amor e devoção.",
        "<b>Veronika Decide Morrer</b> (1998) — Liberdade e loucura.",
        "<b>O Demônio e a Senhorita Prym</b> (2000) — A natureza do bem e do mal.",
        "<b>Onze Minutos</b> (2003) — O sagrado no profano.",
        "<b>O Zahir</b> (2005) — Obsessão e busca pela alma do outro.",
    ]
    for l in livros:
        story.append(Paragraph("·  " + l, S["bullet"]))

    story.append(Spacer(1, 0.4*cm))
    story.append(GildedCallout(fw,
        "Antes de ser um livro sobre tesouros, O Alquimista é um livro sobre escutar. "
        "Os sinais, o coração, o silêncio do deserto, o som do próprio nome no idioma do mundo.",
        label="CHAVE DE LEITURA"))

    story.append(PageBreak())

    # ============== SINOPSE EM UMA PÁGINA ==============
    story.append(Paragraph("VISÃO PANORÂMICA", S["label"]))
    story.append(Paragraph("Sinopse em uma página.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    story.append(Paragraph(
        "<b>Santiago</b>, um jovem pastor andaluz, sonha repetidamente com um tesouro "
        "escondido próximo às pirâmides do Egito. Uma cigana e o misterioso "
        "<b>Melquisedeque</b>, Rei de Salém, interpretam o sonho como sua <i>Lenda "
        "Pessoal</i> — aquilo que ele veio cumprir na vida. Vende suas ovelhas e "
        "atravessa o estreito de Gibraltar.", S["body"]))
    story.append(Paragraph(
        "Em <b>Tânger</b>, é roubado no mesmo dia em que chega. Sem dinheiro, decide "
        "trabalhar em uma <b>loja de cristais</b> aos pés do monte, e ali passa quase "
        "um ano. Aprende sobre o conformismo, ajuda o cristaleiro a expandir o negócio "
        "e, ao fim, decide retomar a jornada com mais dinheiro do que tinha começado.",
        S["body"]))
    story.append(Paragraph(
        "Atravessa o <b>deserto do Saara</b> em uma caravana. Conhece o <b>Inglês</b>, "
        "estudioso de alquimia em busca do mesmo mestre — o <b>Alquimista</b> de "
        "Al-Fayoum. Aprende, na lentidão da caravana, a ler os sinais. No oásis, "
        "encontra <b>Fátima</b> e se apaixona. Vê uma visão de cavalaria atacando o "
        "oásis e a transmite aos chefes tribais, salvando o lugar.", S["body"]))
    story.append(Paragraph(
        "O <b>Alquimista</b> o reconhece e o leva pelo deserto. Quando uma tribo "
        "guerreira o intima a provar seu poder, Santiago precisa transformar-se em "
        "vento. Em diálogo com o sol, o vento e a Mão que escreveu tudo, consegue. "
        "Chega às pirâmides, começa a cavar — e é assaltado por bandidos. Um deles, "
        "rindo, conta-lhe que sonhou repetidamente com um tesouro enterrado em uma "
        "igreja em ruínas, sob um sicômoro, na Espanha.", S["body"]))
    story.append(Paragraph(
        "Santiago volta. <b>O tesouro estava em casa</b>, no exato lugar onde "
        "tudo começou. Mas só se conhece a casa depois da viagem.", S["body"]))

    story.append(Spacer(1, 0.3*cm))
    story.append(CenteredQuote(fw,
        "Maktub.   Está escrito.",
        attribution="repetido pelo Mercador e pelo Alquimista", size=16))

    story.append(PageBreak())

    # ============== PERSONAGENS ==============
    story.append(Paragraph("PERSONAGENS", S["label"]))
    story.append(Paragraph("A caravana de figuras.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Não há, em <i>O Alquimista</i>, personagens secundários. Cada figura "
        "que aparece carrega uma função simbólica precisa. Conhecê-las é metade do "
        "trabalho de leitura.", S["serif_lead"]))
    story.append(Spacer(1, 0.3*cm))

    personagens = [
        ("Santiago",
         "O pastor andaluz",
         "Jovem de cerca de 18 anos. Lê livros, conversa com as ovelhas e está em "
         "movimento. É a alma de qualquer buscador — você."),
        ("Melquisedeque",
         "O Rei de Salém",
         "Surge na praça de Tarifa. Carrega Urim e Tumim, duas pedras (sim/não) que "
         "ajudam quando os sinais ficam confusos. Representa o chamado inicial."),
        ("A Cigana",
         "A leitora dos sonhos",
         "Interpreta o sonho do tesouro em troca de um décimo dele. Encarna a "
         "intuição feminina e a sabedoria popular."),
        ("O Mercador de Cristais",
         "O homem que adiou a Meca",
         "O homem que sustentou a vida inteira o sonho de ir a Meca — e que nunca foi. "
         "Personificação do conforto que substitui a missão."),
        ("O Inglês",
         "O alquimista de livro",
         "Estudioso meticuloso da Grande Obra. Carrega livros pelo deserto. Mostra o "
         "limite da teoria sem prática — o saber sem entrega."),
        ("Fátima",
         "A mulher do deserto",
         "Filha do oásis. Não pede que Santiago fique. Ensina que o verdadeiro amor "
         "não impede a Lenda Pessoal — ele a sustenta."),
        ("O Alquimista",
         "O guia",
         "Vive em Al-Fayoum. Conhece a Linguagem do Mundo e a Grande Obra. Acompanha "
         "Santiago não para entregar respostas, mas para arrancar dele as próprias."),
        ("Os Bandidos do Deserto",
         "O instrumento do destino",
         "Aparecem nas pirâmides como uma derrota final. Um deles, rindo, conta o "
         "sonho que envia Santiago de volta à Espanha. O destino fala pela boca de quem ele quer."),
    ]
    # Em duas colunas — 4 e 4
    half = len(personagens) // 2
    cards_l = [CharacterCard(fw/2 - 0.3*cm, n, r, d) for (n, r, d) in personagens[:half]]
    cards_r = [CharacterCard(fw/2 - 0.3*cm, n, r, d) for (n, r, d) in personagens[half:]]
    # alinhar pares
    rows_p = []
    for i in range(max(len(cards_l), len(cards_r))):
        l = cards_l[i] if i < len(cards_l) else Spacer(1, 0)
        r = cards_r[i] if i < len(cards_r) else Spacer(1, 0)
        rows_p.append([l, r])
    pt = Table(rows_p, colWidths=[fw/2 - 0.3*cm, fw/2 - 0.3*cm])
    pt.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (0,0), 0.3*cm),
        ("LEFTPADDING", (1,0), (1,0), 0.3*cm),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(pt)

    story.append(PageBreak())

    # ============== PILARES CONCEITUAIS ==============
    story.append(Paragraph("CONCEITOS-CHAVE", S["label"]))
    story.append(Paragraph("Os pilares da fábula.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Seis ideias atravessam <i>O Alquimista</i>. Compreendê-las é abrir a porta "
        "para os símbolos e mensagens que vêm a seguir.", S["serif_lead"]))
    story.append(Spacer(1, 0.2*cm))

    conceitos = [
        ("Lenda Pessoal",
         "Aquilo que você sempre quis fazer no fundo do coração — sua missão na Terra. "
         "Quando jovem, todos a conhecem; com o tempo, uma força misteriosa tenta convencê-lo "
         "de que ela é impossível. Quem cumpre, vive."),
        ("Alma do Mundo",
         "A fonte de onde tudo provém e à qual tudo retorna. Tudo no Universo está conectado, "
         "e quem entende uma coisa profundamente entende todas — porque tocou essa Alma."),
        ("Linguagem do Mundo",
         "A linguagem universal, sem palavras, que pode ser entendida pelo coração atento. "
         "Sinais, omens, coincidências significativas. Aprender a lê-la é o trabalho do buscador."),
        ("Princípio Favorável",
         "Também chamado de “sorte do iniciante”. Quando você dá o primeiro passo na direção "
         "da Lenda Pessoal, o Universo é generoso para encorajá-lo a continuar."),
        ("Maktub",
         "Em árabe, “está escrito”. Não é fatalismo: é confiança. O que precisa acontecer "
         "acontecerá; cabe a você responder com presença."),
        ("A Grande Obra",
         "O coração da alquimia: transformar chumbo em ouro. Metaforicamente, transmutar o "
         "próprio chumbo (medo, conformismo) no ouro de uma vida verdadeiramente vivida."),
    ]
    for tit, txt in conceitos:
        story.append(Paragraph(tit, S["h3"]))
        story.append(Paragraph(txt, S["body"]))
        story.append(Spacer(1, 0.1*cm))

    story.append(PageBreak())

    # ============== MAPA DA JORNADA ==============
    story.append(Paragraph("CARTOGRAFIA", S["label"]))
    story.append(Paragraph("Mapa da jornada.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Sete paradas, da Espanha ao Egito. O caminho não é reto — e é justamente nas "
        "curvas que o pastor aprende.", S["serif_lead"]))
    story.append(Spacer(1, 0.3*cm))

    pontos = [
        ("Andaluzia",  "O sonho"),
        ("Tarifa",     "Melquisedeque"),
        ("Tânger",     "A perda"),
        ("Loja",       "11 meses"),
        ("Saara",      "A caravana"),
        ("Al-Fayoum",  "Fátima"),
        ("Pirâmides",  "O retorno"),
    ]
    story.append(JourneyMap(fw, pontos, height=9*cm))

    story.append(Spacer(1, 0.5*cm))
    story.append(GildedCallout(fw,
        "A jornada vai de uma igrejinha em ruínas até as pirâmides do Egito — e volta. "
        "O tesouro estava no mesmo lugar do início. Mas só se reconhece o ponto de "
        "partida depois de tê-lo deixado.",
        label="LEITURA DO MAPA"))

    story.append(NextPageTemplate("p1"))
    story.append(PageBreak())

    # ============== PARTE I ==============
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    add_stage(story, S, fw,
        num="I", kicker="Parte I · Andaluzia",
        title="Santiago, o sonho e a cigana",
        intro=(
            "Santiago dorme sob um sicômoro nas ruínas de uma antiga igreja na Andaluzia. "
            "Pela segunda vez sonha o mesmo sonho: uma criança o leva pelas patas das "
            "pirâmides e mostra um tesouro escondido. Ele acorda inquieto."
        ),
        beats=[
            "Estudou para ser padre, abandonou o seminário, virou pastor para conhecer o mundo.",
            "Há dois anos atravessa a Andaluzia com seu rebanho; conversa com as ovelhas e lê livros.",
            "Em uma cidade próxima, procura uma <b>cigana</b> para interpretar o sonho.",
            "Ela cobra um décimo do tesouro que ele encontrar. Santiago aceita e ri por dentro.",
        ],
        insight=("O SONHO REPETIDO",
                 "Sonhos que se repetem não são acidentes do sono — são pedidos da alma. "
                 "Cabe a quem sonha decidir se vai escutar."),
        quote="As pessoas aprendem cedo demais a sua razão de viver. Talvez por isso desistam tão cedo também.",
    )

    story.append(PageBreak())

    add_stage(story, S, fw,
        num="I", kicker="Parte I · Andaluzia",
        title="Melquisedeque, o Rei de Salém",
        intro=(
            "Na praça de Tarifa, um velho desconhecido se aproxima de Santiago. "
            "Diz-se Melquisedeque, Rei de Salém. Mostra que sabe exatamente o que se passa com ele — "
            "e introduz, em poucas frases, três ideias que mudarão a vida do pastor."
        ),
        beats=[
            "O velho fala da <b>Lenda Pessoal</b>: o que cada um veio cumprir.",
            "Dá a Santiago duas pedras, <b>Urim e Tumim</b>: branca = sim, preta = não.",
            "Cobra um décimo do rebanho como pagamento; o resto, o vento leva.",
            "Santiago vende as ovelhas, atravessa Gibraltar e desembarca em Tânger.",
        ],
        insight=("PRINCÍPIO FAVORÁVEL",
                 "“Quando se quer alguma coisa, todo o universo conspira para que se realize.” "
                 "É a lei do primeiro passo: o universo é generoso com quem ousa começar."),
        quote="Quando se quer alguma coisa, todo o universo conspira para que se realize o desejo.",
    )

    story.append(NextPageTemplate("p2"))
    story.append(PageBreak())

    # ============== PARTE II ==============
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    add_stage(story, S, fw,
        num="II", kicker="Parte II · Tânger",
        title="A primeira morte: o roubo",
        intro=(
            "Santiago chega a Tânger sem falar árabe. Confia em um rapaz que se "
            "oferece para levá-lo ao Egito. No mercado, é roubado de todo o dinheiro. "
            "Em uma única tarde, perde idioma, dinheiro, ovelhas, plano e direção."
        ),
        beats=[
            "Sente-se vítima — mas, ao recuperar a calma, percebe que continua vivo e em viagem.",
            "Sobe ao monte e encontra uma <b>loja de cristais</b> empoeirada, descendo o turismo.",
            "Lava todas as peças em troca de comida. O <b>Mercador</b> oferece um trabalho.",
            "A escolha é íntima: voltar como pastor, com o dinheiro de poucos cristais, ou continuar.",
        ],
        insight=("O MEDO DO SOFRIMENTO É MAIOR QUE O PRÓPRIO",
                 "Quando algo dá errado, o trauma não é o evento — é o medo paralisante de "
                 "que ele se repita. O caminho é seguir, com olhos abertos."),
        quote="Toda a busca começa com a sorte de principiante. E toda busca termina com a prova severa do conquistador.",
    )

    story.append(PageBreak())

    add_stage(story, S, fw,
        num="II", kicker="Parte II · Tânger",
        title="Onze meses entre os cristais",
        intro=(
            "Santiago trabalha quase um ano na loja. Sugere ideias — uma estante na "
            "subida, chá em copos de cristal, vitrines voltadas à rua. A loja "
            "prospera. Ele economiza. Aos poucos, reconhece-se mais rico do que antes "
            "de partir."
        ),
        beats=[
            "O Mercador é um homem bom — mas paralisado pelo sonho não cumprido de ir a Meca.",
            "Santiago percebe duas opções: voltar à Andaluzia e ser pastor maior, ou cruzar o Saara.",
            "Pega o saco de moedas, agradece, e ouve do Mercador: “sigo a sua jornada e a minha pela sua”.",
            "Compra uma travessia em uma caravana rumo ao Egito.",
        ],
        insight=("A LOJA É UM ESPELHO",
                 "Cada um carrega uma “loja de cristais” por dentro: o sonho que se sustenta "
                 "como pintura na parede para não ser cumprido. O Alquimista pergunta: "
                 "qual é a sua?"),
        quote="Sempre, antes de realizar um sonho, a Alma do Mundo resolve testar tudo aquilo que foi aprendido durante a caminhada.",
    )

    story.append(NextPageTemplate("p3"))
    story.append(PageBreak())

    # ============== PARTE III ==============
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    add_stage(story, S, fw,
        num="III", kicker="Parte III · O deserto",
        title="A caravana e o Inglês",
        intro=(
            "Santiago entra na grande caravana que cruzará o Saara em dois meses. "
            "Conhece o <b>Inglês</b>, que carrega malas pesadas de livros. O Inglês "
            "busca o Alquimista de Al-Fayoum, capaz de transformar metal em ouro. "
            "Vão para o mesmo lugar — com mapas diferentes."
        ),
        beats=[
            "O Inglês fala da <b>pedra filosofal</b> e do <b>elixir da longa vida</b>.",
            "Estuda alquimia há dez anos a partir de livros, mas nunca soprou um forno.",
            "O <b>chefe da caravana</b> ensina: no deserto, obedece-se sem perguntas — sobreviver é coletivo.",
            "Santiago tenta ler o Inglês; o Inglês tenta ensinar Santiago. Cada um lê do seu jeito.",
        ],
        insight=("DUAS MANEIRAS DE APRENDER",
                 "Há dois jeitos de saber: pelos livros (Inglês) e pela <b>experiência</b> "
                 "(Santiago). O melhor caminho costuma usar ambos — primeiro o livro, "
                 "depois o forno; primeiro o forno, depois o livro."),
        quote="Tudo na vida são sinais. Existe uma língua universal, compreendida por todos.",
    )

    story.append(PageBreak())

    add_stage(story, S, fw,
        num="III", kicker="Parte III · O deserto",
        title="Sinais, guerras e silêncio",
        intro=(
            "Sinais cruzam o deserto: dois falcões que se atacam no oásis, "
            "exércitos invisíveis ao horizonte, palavras sussurradas no silêncio. "
            "Santiago descobre que tudo no deserto fala — mas só ao coração paciente."
        ),
        beats=[
            "O Inglês permanece no camelo lendo; Santiago observa o céu, o vento, as outras pessoas.",
            "Cada noite a caravana acampa em silêncio — mais que um descanso, é um ritual.",
            "A guerra entre tribos ronda a caravana. O destino acelera as decisões.",
            "Santiago intui sinais de morte; aprende a confiar mesmo sem entendimento.",
        ],
        insight=("DESERTO É PROFESSOR",
                 "O deserto subtrai tudo o que distrai — paisagens, ruído, opções. "
                 "Sobra o essencial. Não é por acaso que místicos de todas as tradições "
                 "preferem as areias."),
        quote="O segredo está em saber esperar.",
    )

    story.append(NextPageTemplate("p4"))
    story.append(PageBreak())

    # ============== PARTE IV ==============
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    add_stage(story, S, fw,
        num="IV", kicker="Parte IV · O oásis",
        title="O oásis, Fátima e a visão",
        intro=(
            "A caravana entra em <b>Al-Fayoum</b>, oásis neutro entre tribos. Santiago "
            "encontra <b>Fátima</b> em um poço — e reconhece, antes de qualquer palavra, "
            "a Linguagem do Mundo entre eles. Ainda assim, é o oásis em perigo que vira "
            "o eixo da página."
        ),
        beats=[
            "Santiago vê <b>falcões caçando</b> no céu como prenúncio de um ataque.",
            "Avisa os anciãos; eles ouvem a contragosto. Se errar, será morto.",
            "Os guerreiros chegam, são repelidos. O oásis sobrevive; Santiago é poupado.",
            "Um homem vestido de preto, com falcão no ombro, surge no horizonte: o Alquimista.",
        ],
        insight=("AMOR NÃO IMPEDE A LENDA",
                 "Fátima não pede que Santiago fique. “Mulher do deserto sabe esperar”. "
                 "O verdadeiro amor não interrompe a Lenda do outro — sustenta-a."),
        quote="O amor é uma força que transforma e melhora a Alma do Mundo.",
    )

    story.append(PageBreak())

    add_stage(story, S, fw,
        num="IV", kicker="Parte IV · O oásis",
        title="O Alquimista o aceita",
        intro=(
            "O Alquimista convida Santiago para um chá em sua tenda. Bebem em silêncio. "
            "Ele diz, ao fim, que o aguardava há tempos. Promete acompanhá-lo até "
            "as pirâmides, ainda atravessando território de guerra. Em troca, exige "
            "que Santiago deixe parte do dinheiro com Fátima e continue."
        ),
        beats=[
            "O Alquimista demonstra a Grande Obra: <b>transforma chumbo em ouro</b> com um sopro.",
            "Diverte-se ensinando Santiago a ouvir o próprio coração — “medroso e leal”.",
            "Quando perguntado por que escolheu Santiago, responde: “Para que você ensine os outros depois”.",
            "Fátima aceita a partida em silêncio. Maktub.",
        ],
        insight=("ENCONTRAR O MESTRE É RECONHECÊ-LO",
                 "Mestres aparecem o tempo todo. O trabalho do discípulo é desenvolver "
                 "olhos para reconhecê-los — quase sempre eles são mais simples do que "
                 "imaginamos."),
        quote="A coisa mais importante para todos os homens é fazer aquilo que o coração manda.",
    )

    story.append(NextPageTemplate("p5"))
    story.append(PageBreak())

    # ============== PARTE V ==============
    story.append(Spacer(1, 0.1*cm))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    add_stage(story, S, fw,
        num="V", kicker="Parte V · O tesouro",
        title="As provas: tornar-se vento",
        intro=(
            "Quase nas pirâmides, são capturados por uma tribo guerreira. O Alquimista, "
            "para salvar a vida de ambos, anuncia que Santiago é um mágico capaz de "
            "transformar-se em vento. Os guerreiros lhe dão três dias para provar."
        ),
        beats=[
            "Dia 1: Santiago observa o deserto. Sente medo. O Alquimista o consola: “Não tenha medo de errar”.",
            "Dia 2: conversa com o vento. O vento pede ajuda ao sol. O sol pede à Mão que escreveu tudo.",
            "Dia 3: na presença da Mão que escreveu tudo, Santiago descobre que ele e tudo são uma só coisa.",
            "O vento sopra forte. Santiago se transforma. A tribo guerreira o liberta.",
        ],
        insight=("DESCOBRIR-SE INSEPARÁVEL",
                 "A prova final não é mágica — é mística. Tornar-se vento exige "
                 "reconhecer que entre você e o vento não existe muro. O verdadeiro poder "
                 "vem de saber-se parte da Alma do Mundo."),
        quote="Quando se ama, as coisas fazem ainda mais sentido.",
    )

    story.append(PageBreak())

    add_stage(story, S, fw,
        num="V", kicker="Parte V · O tesouro",
        title="As pirâmides e o retorno",
        intro=(
            "O Alquimista deixa Santiago a poucos dias das pirâmides. Lá, finalmente, "
            "o pastor as vê. Curva-se, beija a areia. Começa a cavar. Aparecem "
            "<b>refugiados</b>; ele é espancado. Um deles, rindo, conta-lhe um sonho."
        ),
        beats=[
            "“Sonhei duas vezes com um tesouro enterrado numa igrejinha em ruínas na Espanha, sob um sicômoro. Mas só um tolo persegue sonhos.”",
            "Santiago entende: o tesouro estava onde ele já dormiu uma noite — na origem.",
            "Volta à Andaluzia. Cava. Encontra moedas, joias, máscaras de ouro.",
            "Lembra-se de Fátima. O vento sopra do oriente. Diz: “estou indo, Fátima”.",
        ],
        insight=("VOLTAR É O FIM DA JORNADA",
                 "O caminho heróico só se conclui no retorno. O tesouro é objetivo, "
                 "mas o sentido é a transformação que o trajeto operou no buscador. "
                 "É a casa, depois da viagem, que é finalmente vista."),
        quote="O tesouro está onde o coração esquece de olhar.",
        is_attribution_synth=True,
    )

    story.append(PageBreak())

    # ============== SÍMBOLOS ==============
    story.append(Paragraph("SIMBOLOGIA", S["label"]))
    story.append(Paragraph("Símbolos da obra.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "<i>O Alquimista</i> é, antes de tudo, um livro de símbolos. Reconhecê-los é "
        "ler o livro duas vezes — uma com os olhos, outra com o coração.", S["serif_lead"]))
    story.append(Spacer(1, 0.3*cm))

    simbolos = [
        ("sol",         "O Sol",          "Símbolo alquímico do ouro e da consciência. A inteligência que dá sentido."),
        ("triangulo",   "O Triângulo",    "Símbolo do fogo, da elevação e da Trindade. Apontando para cima: aspiração."),
        ("ampulheta",   "A Ampulheta",    "O tempo do deserto. Lento, mas tudo passa por ele. Maktub."),
        ("ovo",         "O Ovo Alquímico","O recipiente da transmutação. O nascimento contido no fechamento."),
        ("circuloduplo","Os Dois Círculos","Urim e Tumim. Sim e Não. A bússola das decisões quando os sinais somem."),
        ("pirâmide",    "A Pirâmide",     "O destino visível, mas só atingível depois da travessia. O ouro do destino."),
        ("olho",        "O Olho",         "Ver a Linguagem do Mundo. Falcões e visões — atenção como faculdade."),
        ("lua",         "A Lua",          "A intuição feminina, Fátima, o silêncio que ensina. O complemento do sol."),
        ("cruz",        "A Cruz",         "Encruzilhada das escolhas. Cada cruz é também uma soma — quatro direções, um centro."),
    ]
    story.append(SymbolGrid(fw, simbolos, cols=3, cell_h=4*cm))

    story.append(PageBreak())

    # ============== MENSAGENS PROFUNDAS ==============
    story.append(Paragraph("PROFUNDIDADE", S["label"]))
    story.append(Paragraph("Mensagens profundas.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    mensagens = [
        ("01", "Sonho repetido pede coragem",
         "O sonho recorrente não é repetição: é insistência. A alma chama duas, três, "
         "dez vezes — até que se atenda."),
        ("02", "O conformismo é mais perigoso que o erro",
         "O Mercador prefere sonhar Meca a viver Meca. Quem nunca tenta, nunca falha — "
         "e nunca vive. O verdadeiro fracasso é a vida adiada."),
        ("03", "Tudo é a mesma coisa",
         "A grande revelação alquímica é a unidade. O deserto, o vento, a tribo, o "
         "coração: tudo está escrito na mesma Alma do Mundo."),
        ("04", "Sinais existem porque a vida quer conversar",
         "Os sinais não são truques místicos — são a maneira como a realidade fala "
         "com quem desenvolveu escuta."),
        ("05", "O medo do sofrimento é maior que o próprio sofrimento",
         "Quando o pior acontece, percebemos que somos mais resistentes do que "
         "achávamos. O sofrimento real é frequentemente menor que o sofrimento imaginado."),
        ("06", "O amor não impede; sustenta",
         "Fátima não retém Santiago — não porque seja indiferente, mas porque ama. "
         "O amor que retém é prisão; o que liberta é apoio."),
        ("07", "Sorte de iniciante e prova do conquistador",
         "O começo é generoso; o meio é duro. A vida testa duas vezes — quando você "
         "começa (com presentes) e quando você quase chega (com dúvidas)."),
        ("08", "Maktub é confiança, não passividade",
         "“Está escrito” não significa “espere”. Significa “aja sem medo: o resultado "
         "já está cuidado por algo maior”."),
        ("09", "O tesouro estava em casa — depois da viagem",
         "Sem a viagem, a casa é só uma casa. Depois da viagem, é também tudo o que "
         "se atravessou. O ponto de chegada é o ponto de partida revisitado."),
        ("10", "O coração mente, mas também pede para ser ouvido",
         "Santiago aprende a escutar o coração com paciência — sabendo que ele às "
         "vezes mente por medo, mas que vale mais ouvi-lo do que silenciá-lo."),
    ]
    for num, tit, txt in mensagens:
        story.append(Paragraph(f"{num}  ·  {tit}", S["h3"]))
        story.append(Paragraph(txt, S["body"]))

    story.append(PageBreak())

    # ============== A LINGUAGEM DO MUNDO ==============
    story.append(Paragraph("ENSINAMENTO", S["label"]))
    story.append(Paragraph("A Linguagem do Mundo.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))

    story.append(Paragraph(
        "Como o livro ensina a perceber sinais? Cinco práticas se desenham, em segundo "
        "plano, no texto de Coelho. Não são técnicas — são posturas.",
        S["serif_lead"]))

    praticas = [
        ("Silenciar antes de interpretar",
         "Santiago aprende, no deserto, a esperar sem nomear. A leitura dos sinais "
         "começa pela suspensão dos rótulos prontos."),
        ("Olhar para o que se repete",
         "Sonhos repetidos, encontros repetidos, perguntas repetidas. O Mundo "
         "convoca por repetição."),
        ("Observar a sincronia",
         "Quando uma intuição interna coincide com um sinal externo, há ali uma "
         "abertura. Não decida só pela intuição nem só pelo sinal; decida quando os dois se encontram."),
        ("Aceitar mensageiros improváveis",
         "O Rei aparece como velho de rua. O Alquimista aparece como guerreiro de "
         "preto. O bandido conta-lhe o sonho. O Mundo fala pela boca menos esperada."),
        ("Agir com o pouco que se entende",
         "Não espere clareza total. Aja com o sinal mínimo, e a próxima parte do "
         "caminho aparece. O todo não se mostra antes do passo."),
    ]
    for tit, txt in praticas:
        story.append(Paragraph(tit, S["h3"]))
        story.append(Paragraph(txt, S["body"]))

    story.append(Spacer(1, 0.3*cm))
    story.append(GildedCallout(fw,
        "Sinais não vêm para serem decifrados pela mente — vêm para serem reconhecidos "
        "pelo coração. Aceite que entender venha depois de obedecer.",
        label="RESUMO DA ESCUTA"))

    story.append(PageBreak())

    # ============== CITAÇÕES EM DESTAQUE ==============
    story.append(Paragraph("PAREDE DE CITAÇÕES", S["label"]))
    story.append(Paragraph("As frases que ficam.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=14))

    # Citações em sizes diferentes para feel tipográfico
    story.append(Spacer(1, 0.3*cm))
    story.append(CenteredQuote(fw,
        "Quando você quer alguma coisa, todo o universo conspira para que você realize o seu desejo.",
        size=15, attribution="O Velho Rei de Salém"))
    story.append(Spacer(1, 0.4*cm))
    story.append(CenteredQuote(fw,
        "Maktub.",
        size=44, color=ACCENT))
    story.append(Spacer(1, 0.2*cm))
    story.append(CenteredQuote(fw,
        "É a possibilidade de realizar um sonho que torna a vida interessante.",
        size=14, attribution="O Velho Rei de Salém"))
    story.append(Spacer(1, 0.4*cm))
    story.append(CenteredQuote(fw,
        "Onde está o seu tesouro, ali estará também o seu coração.",
        size=15, color=ACCENT_DEEP))
    story.append(Spacer(1, 0.3*cm))
    story.append(CenteredQuote(fw,
        "A vida atrai a vida.",
        size=22))
    story.append(Spacer(1, 0.3*cm))
    story.append(CenteredQuote(fw,
        "Não tenha medo. Mas sobretudo, não tenha medo de errar.",
        size=14, attribution="O Alquimista, antes da prova do vento"))

    story.append(PageBreak())

    # ============== REFLEXÕES PESSOAIS ==============
    story.append(Paragraph("REFLEXÃO PESSOAL", S["label"]))
    story.append(Paragraph("Sua jornada — em perguntas.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Em vez de exercícios, perguntas. Reserve um café e o caderno; responda em voz "
        "calma. Algumas exigirão dias.", S["serif_lead"]))
    story.append(Spacer(1, 0.2*cm))

    perguntas = [
        "Qual é a sua Lenda Pessoal — aquilo que, no fundo, você sempre quis fazer?",
        "Que sonho recorrente sua vida lhe apresenta há mais tempo? E o que ainda não fez sobre ele?",
        "Qual é a sua “loja de cristais”: o lugar confortável que substituiu a missão?",
        "Quem é o seu Melquisedeque hoje — a pessoa, livro ou sinal que apareceu como chamado?",
        "Quais sinais o Mundo tem te enviado nas últimas semanas? Liste, sem julgar.",
        "Se um bandido contasse, rindo, onde está o seu tesouro real — o que ele diria?",
    ]
    for p in perguntas:
        story.append(ReflectionPrompt(fw, p, num_lines=2, line_spacing=0.65*cm))
        story.append(Spacer(1, 0.1*cm))

    story.append(PageBreak())

    # ============== CADERNO DE JORNADA ==============
    story.append(Paragraph("CADERNO", S["label"]))
    story.append(Paragraph("Caderno de jornada.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=12))
    story.append(Paragraph(
        "Use estas páginas para registrar suas próprias travessias, frases que "
        "ficaram, conexões com a sua vida.",
        S["body_small"]))
    story.append(Spacer(1, 0.4*cm))

    story.append(JournalLines(fw, num_lines=9, line_spacing=0.78*cm,
                              label="O que aprendi com este livro"))
    story.append(Spacer(1, 0.5*cm))
    story.append(JournalLines(fw, num_lines=9, line_spacing=0.78*cm,
                              label="Os sinais que tenho recebido"))

    story.append(PageBreak())

    # ============== ÚLTIMA PALAVRA ==============
    story.append(Spacer(1, 3.5*cm))
    story.append(Paragraph("ÚLTIMA PALAVRA", S["label"]))
    story.append(Paragraph("Ande.", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=14))
    story.append(CenteredQuote(fw,
        "O tesouro estava onde tudo começou. Mas só se vê depois de partir.",
        attribution="Síntese do leitor", size=15))

    doc.build(story)


# ─────────────────────────────────────────────────────
# HELPER — Estágio
# ─────────────────────────────────────────────────────

def add_stage(story, S, fw, num, kicker, title, intro, beats, insight, quote,
              is_attribution_synth=False):
    story.append(StageNumber(fw, num, kicker=kicker))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph(title + ".", S["section"]))
    story.append(HLine(fw, thickness=0.6, color=INK, space_after=8))

    story.append(Paragraph(intro, S["body"]))

    story.append(Paragraph("Momentos da cena", S["h2"]))
    for b in beats:
        story.append(Paragraph("·  " + b, S["bullet"]))

    if quote:
        story.append(Spacer(1, 0.25*cm))
        attr = "Síntese" if is_attribution_synth else "Paulo Coelho · O Alquimista"
        story.append(CenteredQuote(fw, quote, attribution=attr, size=14))

    if insight:
        label, txt = insight
        story.append(Spacer(1, 0.2*cm))
        story.append(GildedCallout(fw, txt, label=label))

    story.append(Spacer(1, 0.25*cm))
    story.append(JournalLines(fw, num_lines=3, line_spacing=0.7*cm,
                              label="Notas desta cena"))


if __name__ == "__main__":
    build()
    print(f"PDF gerado: {OUTPUT}")
