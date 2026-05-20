"""
Gerador de PDF — Resumo profundo de "Hábitos Atômicos" (James Clear)
Design minimalista e moderno.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, Table, TableStyle, KeepTogether, FrameBreak, NextPageTemplate
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus.flowables import HRFlowable, Flowable

OUTPUT = "/home/user/taskflow-pro/Habitos_Atomicos_Resumo.pdf"

# Paleta — minimalista moderna
INK       = HexColor("#111418")  # tinta principal
SUBINK    = HexColor("#3A3F47")  # tinta secundária
MUTED     = HexColor("#7A828D")  # texto suave
HAIRLINE  = HexColor("#D9DEE4")  # linhas finas
ACCENT    = HexColor("#1F6F4A")  # verde profundo (acento)
ACCENT_SOFT = HexColor("#E8F1EC")
PAPER     = HexColor("#FAFAF7")  # off-white

PAGE_W, PAGE_H = A4
MARGIN_L = 2.2 * cm
MARGIN_R = 2.2 * cm
MARGIN_T = 2.4 * cm
MARGIN_B = 2.2 * cm

# =====================================================
# Flowables customizados
# =====================================================

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
        y = self.space_after
        self.canv.line(0, y, self.width, y)


class NoteLines(Flowable):
    """Bloco de linhas para anotações manuais."""
    def __init__(self, width, num_lines=8, line_spacing=0.7*cm, color=HAIRLINE, label=None):
        Flowable.__init__(self)
        self.width = width
        self.num_lines = num_lines
        self.line_spacing = line_spacing
        self.color = color
        self.label = label
        extra = 0.8*cm if label else 0
        self.height = num_lines * line_spacing + extra + 0.4*cm

    def draw(self):
        c = self.canv
        y = self.height
        if self.label:
            c.setFont("Helvetica-Oblique", 8.5)
            c.setFillColor(MUTED)
            c.drawString(0, y - 0.45*cm, self.label.upper())
            y -= 0.85*cm
        c.setStrokeColor(self.color)
        c.setLineWidth(0.35)
        for i in range(self.num_lines):
            yy = y - (i+1) * self.line_spacing
            c.line(0, yy, self.width, yy)


class CheckboxList(Flowable):
    """Lista de exercícios com caixas para marcar."""
    def __init__(self, width, items, box_size=0.32*cm, line_height=0.62*cm):
        Flowable.__init__(self)
        self.width = width
        self.items = items
        self.box_size = box_size
        self.line_height = line_height
        # estimar altura — cada item pode quebrar em 2 linhas
        self.height = len(items) * (line_height + 0.18*cm) + 0.3*cm

    def draw(self):
        c = self.canv
        y = self.height - 0.2*cm
        max_chars = 95
        for item in self.items:
            # caixa
            c.setStrokeColor(INK)
            c.setLineWidth(0.55)
            c.rect(0, y - self.box_size + 0.05*cm, self.box_size, self.box_size, stroke=1, fill=0)
            # texto (com quebra simples)
            c.setFont("Helvetica", 9.5)
            c.setFillColor(INK)
            tx = self.box_size + 0.25*cm
            # quebrar texto manualmente em duas linhas se necessário
            words = item.split()
            line1 = ""
            line2 = ""
            for w in words:
                test = (line1 + " " + w).strip()
                if c.stringWidth(test, "Helvetica", 9.5) <= self.width - tx:
                    line1 = test
                else:
                    line2 = (line2 + " " + w).strip()
            c.drawString(tx, y, line1)
            if line2:
                c.drawString(tx, y - 0.42*cm, line2)
                y -= self.line_height + 0.22*cm
            else:
                y -= self.line_height


class CalloutBox(Flowable):
    """Caixa de destaque para insights."""
    def __init__(self, width, text, label="INSIGHT", bg=ACCENT_SOFT, border=ACCENT, padding=0.45*cm):
        Flowable.__init__(self)
        self.width = width
        self.text = text
        self.label = label
        self.bg = bg
        self.border = border
        self.padding = padding
        # estimar altura
        from reportlab.pdfbase.pdfmetrics import stringWidth
        font = "Helvetica"
        size = 9.7
        avail = width - 2*padding
        words = text.split()
        line = ""
        lines = 1
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, font, size) <= avail:
                line = test
            else:
                lines += 1
                line = w
        self.height = lines * (size * 1.35) + 2*padding + 0.5*cm

    def wrap_text(self, text, width, font, size):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        words = text.split()
        lines = []
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, font, size) <= width:
                line = test
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        return lines

    def draw(self):
        c = self.canv
        h = self.height
        # fundo arredondado
        c.setFillColor(self.bg)
        c.setStrokeColor(self.border)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, self.width, h, 6, stroke=0, fill=1)
        # barra lateral de acento
        c.setFillColor(self.border)
        c.rect(0, 0, 0.12*cm, h, stroke=0, fill=1)
        # label
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(self.border)
        c.drawString(self.padding + 0.15*cm, h - self.padding - 0.05*cm, self.label.upper())
        # texto
        c.setFont("Helvetica", 9.7)
        c.setFillColor(INK)
        lines = self.wrap_text(self.text, self.width - 2*self.padding - 0.15*cm, "Helvetica", 9.7)
        y = h - self.padding - 0.5*cm
        for ln in lines:
            c.drawString(self.padding + 0.15*cm, y, ln)
            y -= 9.7 * 1.35


# =====================================================
# Estilos
# =====================================================

def make_styles():
    s = {}
    s["title_huge"] = ParagraphStyle(
        "title_huge", fontName="Helvetica-Bold", fontSize=42, leading=46,
        textColor=INK, alignment=TA_LEFT, spaceAfter=12
    )
    s["title_sub"] = ParagraphStyle(
        "title_sub", fontName="Helvetica", fontSize=14, leading=20,
        textColor=SUBINK, alignment=TA_LEFT, spaceAfter=8
    )
    s["meta"] = ParagraphStyle(
        "meta", fontName="Helvetica", fontSize=9, leading=13,
        textColor=MUTED, alignment=TA_LEFT, spaceAfter=4
    )
    s["section"] = ParagraphStyle(
        "section", fontName="Helvetica-Bold", fontSize=20, leading=24,
        textColor=INK, alignment=TA_LEFT, spaceBefore=4, spaceAfter=4
    )
    s["section_kicker"] = ParagraphStyle(
        "section_kicker", fontName="Helvetica-Bold", fontSize=8, leading=10,
        textColor=ACCENT, alignment=TA_LEFT, spaceAfter=4
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=13, leading=17,
        textColor=INK, alignment=TA_LEFT, spaceBefore=12, spaceAfter=4
    )
    s["h3"] = ParagraphStyle(
        "h3", fontName="Helvetica-Bold", fontSize=10.5, leading=14,
        textColor=ACCENT, alignment=TA_LEFT, spaceBefore=8, spaceAfter=2
    )
    s["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=10, leading=15,
        textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6
    )
    s["body_small"] = ParagraphStyle(
        "body_small", fontName="Helvetica", fontSize=9, leading=13,
        textColor=SUBINK, alignment=TA_JUSTIFY, spaceAfter=4
    )
    s["bullet"] = ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=10, leading=14.5,
        textColor=INK, alignment=TA_LEFT, leftIndent=14, bulletIndent=2,
        spaceAfter=3
    )
    s["quote"] = ParagraphStyle(
        "quote", fontName="Helvetica-Oblique", fontSize=11, leading=16,
        textColor=SUBINK, alignment=TA_LEFT, leftIndent=14, rightIndent=14,
        spaceBefore=6, spaceAfter=6
    )
    s["toc_item"] = ParagraphStyle(
        "toc_item", fontName="Helvetica", fontSize=10.5, leading=18,
        textColor=INK, alignment=TA_LEFT
    )
    s["toc_dotted"] = ParagraphStyle(
        "toc_dotted", fontName="Helvetica", fontSize=10.5, leading=18,
        textColor=MUTED, alignment=TA_LEFT
    )
    s["caption"] = ParagraphStyle(
        "caption", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
        textColor=MUTED, alignment=TA_LEFT, spaceAfter=4
    )
    s["cover_label"] = ParagraphStyle(
        "cover_label", fontName="Helvetica-Bold", fontSize=9, leading=12,
        textColor=ACCENT, alignment=TA_LEFT, spaceAfter=6
    )
    return s


# =====================================================
# Page templates: capa e conteúdo (com header/footer)
# =====================================================

# anchor para registrar páginas de seções (page numbers reais no índice)
section_pages = {}

def header_footer(canvas_obj, doc):
    canvas_obj.saveState()
    # fundo off-white sutil
    canvas_obj.setFillColor(PAPER)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # header
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawString(MARGIN_L, PAGE_H - 1.3*cm, "HÁBITOS ATÔMICOS  ·  RESUMO DETALHADO")
    canvas_obj.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.3*cm, "JAMES CLEAR")

    # linha fina sob o header
    canvas_obj.setStrokeColor(HAIRLINE)
    canvas_obj.setLineWidth(0.4)
    canvas_obj.line(MARGIN_L, PAGE_H - 1.55*cm, PAGE_W - MARGIN_R, PAGE_H - 1.55*cm)

    # footer
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(MUTED)
    page_num = canvas_obj.getPageNumber()
    canvas_obj.drawString(MARGIN_L, 1.3*cm, "Resumo · 2026")
    canvas_obj.drawRightString(PAGE_W - MARGIN_R, 1.3*cm, f"— {page_num} —")

    canvas_obj.restoreState()


def cover_decoration(canvas_obj, doc):
    canvas_obj.saveState()
    # fundo
    canvas_obj.setFillColor(PAPER)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # bloco geométrico minimalista no canto superior
    canvas_obj.setFillColor(ACCENT)
    canvas_obj.rect(0, PAGE_H - 1.2*cm, PAGE_W, 1.2*cm, stroke=0, fill=1)

    # círculos sutis (motivo "átomo")
    canvas_obj.setStrokeColor(HAIRLINE)
    canvas_obj.setLineWidth(0.6)
    cx, cy = PAGE_W - 5.5*cm, 8*cm
    canvas_obj.circle(cx, cy, 3.5*cm, stroke=1, fill=0)
    canvas_obj.circle(cx, cy, 2.2*cm, stroke=1, fill=0)
    canvas_obj.circle(cx, cy, 1.1*cm, stroke=1, fill=0)
    canvas_obj.setFillColor(ACCENT)
    canvas_obj.circle(cx, cy, 0.18*cm, stroke=0, fill=1)
    # núcleo orbital
    canvas_obj.circle(cx + 3.5*cm, cy, 0.13*cm, stroke=0, fill=1)
    canvas_obj.circle(cx - 2.2*cm, cy, 0.13*cm, stroke=0, fill=1)

    # rodapé da capa
    canvas_obj.setStrokeColor(INK)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(MARGIN_L, 2.2*cm, PAGE_W - MARGIN_R, 2.2*cm)
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawString(MARGIN_L, 1.7*cm, "RESUMO DETALHADO  ·  EDIÇÃO LEITOR")
    canvas_obj.drawRightString(PAGE_W - MARGIN_R, 1.7*cm, "MAIO · 2026")

    canvas_obj.restoreState()


# =====================================================
# Documento
# =====================================================

def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title="Hábitos Atômicos — Resumo Detalhado",
        author="Resumo a partir da obra de James Clear",
    )

    cover_frame = Frame(MARGIN_L, MARGIN_B, PAGE_W - MARGIN_L - MARGIN_R,
                        PAGE_H - MARGIN_T - MARGIN_B, id="cover", showBoundary=0)
    body_frame = Frame(MARGIN_L, MARGIN_B, PAGE_W - MARGIN_L - MARGIN_R,
                       PAGE_H - MARGIN_T - MARGIN_B - 0.4*cm, id="body", showBoundary=0)

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=cover_decoration),
        PageTemplate(id="body",  frames=[body_frame],  onPage=header_footer),
    ])

    S = make_styles()
    story = []

    frame_w = PAGE_W - MARGIN_L - MARGIN_R

    # ---------- CAPA ----------
    story.append(Spacer(1, 1.3*cm))
    story.append(Paragraph("RESUMO DETALHADO", S["cover_label"]))
    story.append(HLine(2.2*cm, thickness=1.2, color=INK, space_after=4))
    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph("Hábitos<br/>Atômicos", S["title_huge"]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Um método fácil e comprovado de criar bons hábitos e<br/>"
        "se livrar dos maus.", S["title_sub"]))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("DO AUTOR", S["cover_label"]))
    story.append(Paragraph("<b>James Clear</b><br/>"
                           "Escritor, palestrante e pesquisador de comportamento humano.<br/>"
                           "Edição original: <i>Atomic Habits</i> (2018) — Avery / Penguin.<br/>"
                           "Edição brasileira: Sextante.", S["body_small"]))
    story.append(Spacer(1, 1.1*cm))
    story.append(Paragraph("ORGANIZADO POR", S["cover_label"]))
    story.append(Paragraph("Leitor — caderno de resumo, anotações, exercícios e insights.",
                           S["body_small"]))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # ---------- FICHA + BESTSELLERS ----------
    story.append(Paragraph("FICHA TÉCNICA", S["section_kicker"]))
    story.append(Paragraph("Sobre esta edição de resumo", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=8))
    story.append(Spacer(1, 0.2*cm))

    ficha_data = [
        ["Título original", "Atomic Habits"],
        ["Título no Brasil", "Hábitos Atômicos"],
        ["Autor", "James Clear"],
        ["Editora (BR)", "Editora Sextante"],
        ["Ano de publicação", "2018 (orig.) · 2019 (BR)"],
        ["Páginas (edição BR)", "Aproximadamente 320 páginas"],
        ["Gênero", "Desenvolvimento pessoal · Comportamento"],
        ["Tema central", "Pequenas mudanças, resultados notáveis"],
    ]
    t = Table(ficha_data, colWidths=[4.5*cm, frame_w - 4.5*cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9.5),
        ("TEXTCOLOR", (0,0), (0,-1), MUTED),
        ("TEXTCOLOR", (1,0), (1,-1), INK),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("LINEBELOW", (0,0), (-1,-1), 0.3, HAIRLINE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.8*cm))

    story.append(Paragraph("CONTEXTO DE MERCADO", S["section_kicker"]))
    story.append(Paragraph("15 títulos mais vendidos no Brasil", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=8))
    story.append(Paragraph(
        "Lista organizada por popularidade histórica e desempenho consistente nas "
        "principais livrarias brasileiras (Amazon BR, Saraiva, Cultura, PublishNews). "
        "O <b>nº 1</b> é o livro detalhado a partir da próxima página.", S["body"]))
    story.append(Spacer(1, 0.3*cm))

    bestsellers = [
        ("1",  "Hábitos Atômicos",                                 "James Clear"),
        ("2",  "A Sutil Arte de Ligar o F*da-se",                  "Mark Manson"),
        ("3",  "O Poder do Hábito",                                "Charles Duhigg"),
        ("4",  "Mindset: A Nova Psicologia do Sucesso",            "Carol S. Dweck"),
        ("5",  "O Milagre da Manhã",                               "Hal Elrod"),
        ("6",  "Pai Rico, Pai Pobre",                              "Robert T. Kiyosaki"),
        ("7",  "Os 7 Hábitos das Pessoas Altamente Eficazes",      "Stephen R. Covey"),
        ("8",  "Como Fazer Amigos e Influenciar Pessoas",          "Dale Carnegie"),
        ("9",  "O Homem Mais Rico da Babilônia",                   "George S. Clason"),
        ("10", "O Monge e o Executivo",                            "James C. Hunter"),
        ("11", "O Alquimista",                                     "Paulo Coelho"),
        ("12", "Inteligência Emocional",                           "Daniel Goleman"),
        ("13", "Rápido e Devagar: Duas Formas de Pensar",          "Daniel Kahneman"),
        ("14", "Trabalhe 4 Horas por Semana",                      "Timothy Ferriss"),
        ("15", "Os Segredos da Mente Milionária",                  "T. Harv Eker"),
    ]
    rows = [["#", "TÍTULO", "AUTOR"]] + [list(b) for b in bestsellers]
    bt = Table(rows, colWidths=[1.1*cm, 9.5*cm, frame_w - 10.6*cm])
    bt.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 8),
        ("TEXTCOLOR", (0,0), (-1,0), MUTED),
        ("LINEBELOW", (0,0), (-1,0), 0.5, INK),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
        ("TOPPADDING", (0,0), (-1,0), 4),

        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,1), (-1,-1), 9.5),
        ("TEXTCOLOR", (0,1), (0,-1), ACCENT),
        ("TEXTCOLOR", (1,1), (-1,-1), INK),
        ("BOTTOMPADDING", (0,1), (-1,-1), 6),
        ("TOPPADDING", (0,1), (-1,-1), 6),
        ("LINEBELOW", (0,1), (-1,-1), 0.25, HAIRLINE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

        # destaque do nº 1
        ("BACKGROUND", (0,1), (-1,1), ACCENT_SOFT),
        ("FONTNAME", (1,1), (1,1), "Helvetica-Bold"),
    ]))
    story.append(bt)

    story.append(PageBreak())

    # ---------- SUMÁRIO / ÍNDICE ----------
    story.append(Paragraph("NAVEGAÇÃO", S["section_kicker"]))
    story.append(Paragraph("Sumário", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=10))
    story.append(Paragraph(
        "As páginas referem-se a este caderno de resumo. Para a paginação da "
        "edição original brasileira (Sextante, ~320 p.), veja a coluna <i>Livro</i>.",
        S["body_small"]))
    story.append(Spacer(1, 0.4*cm))

    sumario = [
        # (capítulo, título, pg resumo, pg livro)
        ("",  "Capa",                                                                 1,   None),
        ("",  "Ficha técnica e lista dos 15 mais vendidos",                            2,   None),
        ("",  "Sumário",                                                               3,   None),
        ("",  "Sobre o autor",                                                         4,   None),
        ("",  "A grande ideia em uma página",                                          5,   None),
        ("1", "O surpreendente poder dos hábitos atômicos",                            6,   "13"),
        ("2", "Como seus hábitos moldam a sua identidade (e vice-versa)",              7,   "32"),
        ("3", "Como construir hábitos melhores em quatro passos simples",              8,   "46"),
        ("",  "1ª LEI · Torne claro",                                                  9,   "59"),
        ("4", "O homem que não parecia certo",                                         9,   "60"),
        ("5", "A melhor maneira de começar um novo hábito",                           10,   "70"),
        ("6", "Motivação é superestimada; ambiente importa mais",                     11,   "82"),
        ("7", "O segredo do autocontrole",                                            12,   "94"),
        ("",  "2ª LEI · Torne atraente",                                              13,  "103"),
        ("8", "Como tornar um hábito irresistível",                                   13,  "104"),
        ("9", "O papel da família e dos amigos na formação de hábitos",               14,  "117"),
        ("10","Como encontrar e corrigir as causas de seus maus hábitos",             15,  "129"),
        ("",  "3ª LEI · Torne fácil",                                                 16,  "141"),
        ("11","Caminhe devagar, mas nunca para trás",                                 16,  "142"),
        ("12","A lei do mínimo esforço",                                              17,  "152"),
        ("13","Como parar de procrastinar usando a regra dos dois minutos",           18,  "162"),
        ("14","Como tornar os bons hábitos inevitáveis e os maus impossíveis",        19,  "172"),
        ("",  "4ª LEI · Torne satisfatório",                                          20,  "183"),
        ("15","A regra cardinal da mudança de comportamento",                         20,  "184"),
        ("16","Como manter bons hábitos todos os dias",                               21,  "196"),
        ("17","Como uma parceria de responsabilidade pode mudar tudo",                22,  "208"),
        ("",  "TÁTICAS AVANÇADAS",                                                    23,  "215"),
        ("18","A verdade sobre talento (quando os genes importam)",                   23,  "216"),
        ("19","A regra de Cachinhos Dourados",                                        24,  "229"),
        ("20","A desvantagem de criar bons hábitos",                                  25,  "243"),
        ("",  "INSIGHTS PROFUNDOS",                                                   26,  None),
        ("",  "Como mudar — protocolo prático",                                       28,  None),
        ("",  "Como evoluir — plano de 90 dias",                                      29,  None),
        ("",  "Exercícios e práticas",                                                30,  None),
        ("",  "Caderno de anotações",                                                 32,  None),
    ]

    # tabela do sumário
    sum_rows = [["", "TÍTULO", "RESUMO", "LIVRO"]]
    for cap, titulo, pg_r, pg_l in sumario:
        cap_str = cap if cap else "·"
        title_str = titulo
        if cap == "" and titulo.startswith(("1ª LEI", "2ª LEI", "3ª LEI", "4ª LEI", "TÁTICAS", "INSIGHTS", "Como mudar", "Como evoluir", "Exercícios", "Caderno", "Capa", "Ficha", "Sumário", "Sobre", "A grande")):
            title_str = titulo  # já estilizado pelo conteúdo
        sum_rows.append([cap_str, title_str, str(pg_r), pg_l if pg_l else "—"])

    st = Table(sum_rows, colWidths=[1.0*cm, frame_w - 4.0*cm, 1.5*cm, 1.5*cm])
    style_cmds = [
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 7.5),
        ("TEXTCOLOR", (0,0), (-1,0), MUTED),
        ("LINEBELOW", (0,0), (-1,0), 0.5, INK),
        ("BOTTOMPADDING", (0,0), (-1,0), 5),

        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 9.3),
        ("TEXTCOLOR", (0,1), (0,-1), ACCENT),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("ALIGN", (2,0), (3,-1), "RIGHT"),
        ("TEXTCOLOR", (2,1), (-1,-1), MUTED),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BOTTOMPADDING", (0,1), (-1,-1), 4),
        ("TOPPADDING", (0,1), (-1,-1), 4),
    ]
    # destacar separadores
    for i, row in enumerate(sumario, start=1):
        cap, titulo, _, _ = row
        if cap == "" and (titulo.startswith(("1ª LEI", "2ª LEI", "3ª LEI", "4ª LEI", "TÁTICAS", "INSIGHTS"))):
            style_cmds.append(("FONTNAME", (1,i), (1,i), "Helvetica-Bold"))
            style_cmds.append(("TEXTCOLOR", (1,i), (1,i), ACCENT))
            style_cmds.append(("LINEABOVE", (0,i), (-1,i), 0.4, HAIRLINE))
            style_cmds.append(("TOPPADDING", (0,i), (-1,i), 8))
    st.setStyle(TableStyle(style_cmds))
    story.append(st)

    story.append(PageBreak())

    # ---------- SOBRE O AUTOR ----------
    story.append(Paragraph("AUTOR", S["section_kicker"]))
    story.append(Paragraph("Sobre James Clear", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=10))

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
        "Stephen Covey, William James e os estoicos (Marco Aurélio, Epicteto).", S["bullet"]))
    story.append(Paragraph(
        "• Linha editorial: pequenos textos densos, exemplos vividos (de Phelps a Edison), "
        "sistemas em vez de metas, ambiente em vez de força de vontade.", S["bullet"]))

    story.append(Paragraph("Por que este livro funciona", S["h2"]))
    story.append(Paragraph(
        "Porque desloca o eixo da motivação para o <b>design</b>: em vez de querer mais, "
        "o leitor aprende a projetar contextos, sinais e recompensas. É um manual de "
        "engenharia pessoal — leve, escalável e replicável em qualquer área da vida.",
        S["body"]))

    story.append(CalloutBox(
        frame_w,
        "Não suba o nível das suas metas, suba o nível dos seus sistemas. "
        "Você não se eleva ao nível das suas metas; você cai ao nível dos seus sistemas.",
        label="FRASE-CHAVE"))

    story.append(PageBreak())

    # ---------- A GRANDE IDEIA ----------
    story.append(Paragraph("VISÃO PANORÂMICA", S["section_kicker"]))
    story.append(Paragraph("A grande ideia em uma página", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=10))

    story.append(Paragraph(
        "O livro defende uma tese simples e radical: <b>pequenas melhorias diárias, "
        "consistentes, compõem resultados extraordinários</b>. Para isso, James Clear "
        "propõe um sistema baseado em quatro leis universais para construir bons "
        "hábitos — e suas inversões para extinguir maus hábitos.", S["body"]))

    # 4 leis em tabela
    leis = [
        ["LEI", "CONSTRUIR (BOM HÁBITO)", "QUEBRAR (MAU HÁBITO)"],
        ["1ª  ·  DEIXA",         "Torne-o claro",       "Torne-o invisível"],
        ["2ª  ·  DESEJO",        "Torne-o atraente",    "Torne-o desinteressante"],
        ["3ª  ·  RESPOSTA",      "Torne-o fácil",       "Torne-o difícil"],
        ["4ª  ·  RECOMPENSA",    "Torne-o satisfatório","Torne-o insatisfatório"],
    ]
    lt = Table(leis, colWidths=[3.6*cm, (frame_w - 3.6*cm)/2, (frame_w - 3.6*cm)/2])
    lt.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 8),
        ("TEXTCOLOR", (0,0), (-1,0), MUTED),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
        ("LINEBELOW", (0,0), (-1,0), 0.5, INK),

        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0,1), (0,-1), ACCENT),
        ("FONTNAME", (1,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 10),
        ("BACKGROUND", (1,1), (1,-1), ACCENT_SOFT),
        ("BOTTOMPADDING", (0,1), (-1,-1), 9),
        ("TOPPADDING", (0,1), (-1,-1), 9),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LINEBELOW", (0,1), (-1,-1), 0.3, HAIRLINE),
    ]))
    story.append(lt)
    story.append(Spacer(1, 0.4*cm))

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
        "esse pequeno gera mudança massiva. A diferença entre 1,01 elevado a 365 "
        "(≈ 37,8) e 0,99 elevado a 365 (≈ 0,03) é a metáfora central.", S["body"]))

    story.append(CalloutBox(
        frame_w,
        "Você não fracassa por preguiça nem vence por motivação. Você cai ao nível "
        "do seu sistema — projete o sistema certo e o resultado vira inevitável.",
        label="TESE CENTRAL"))

    story.append(PageBreak())

    # =====================================================
    # PARTE I — FUNDAMENTOS
    # =====================================================

    # --- CAP 1 ---
    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 1",
        title="O surpreendente poder dos hábitos atômicos",
        livro_pg="13",
        intro=(
            "Em 2003, a seleção britânica de ciclismo, mediana há mais de um século, "
            "contratou Dave Brailsford com uma filosofia: <b>melhorar 1% em mil pontos</b>. "
            "Em cinco anos, dominou os Jogos Olímpicos. Em dez, conquistou o Tour de "
            "France. A lição: <b>melhorias marginais compõem-se</b> de forma exponencial."
        ),
        bullets=[
            "1% melhor por dia durante 1 ano = 37,78× melhor; 1% pior por dia = 0,03 do original.",
            "Hábitos são para a vida o que juros compostos são para o dinheiro.",
            "Você é o resultado acumulado dos seus pequenos hábitos, não dos seus grandes feitos.",
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
        key_quotes=[
            "Você não se eleva ao nível das suas metas; você cai ao nível dos seus sistemas.",
            "Hábitos são os juros compostos do autoaperfeiçoamento.",
        ]
    )

    story.append(PageBreak())

    # --- CAP 2 ---
    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 2",
        title="Como seus hábitos moldam a sua identidade (e vice-versa)",
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
        key_quotes=[
            "A meta não é ler um livro, é tornar-se um leitor. A meta não é correr uma maratona, é tornar-se um corredor.",
            "A forma mais eficaz de mudar seus hábitos é focar não no que você quer alcançar, mas em quem você deseja se tornar.",
        ]
    )

    story.append(PageBreak())

    # --- CAP 3 ---
    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 3",
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
            "Mau hábito: torne os 4 elementos invisível/desinteressante/difícil/insatisfatório.",
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
        key_quotes=[
            "Um hábito é um comportamento que foi repetido vezes suficientes para se tornar automático.",
        ]
    )

    story.append(PageBreak())

    # =====================================================
    # 1ª LEI — TORNE CLARO
    # =====================================================
    add_law_separator(story, S, frame_w, "1ª LEI",
                      "Torne claro",
                      "Tornar o que você quer fazer óbvio, e o que não quer, invisível.")

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 4",
        title="O homem que não parecia certo",
        livro_pg="60",
        intro=(
            "A história abre com um perito que, ao olhar para uma pessoa, sente que "
            "“algo não está certo” — sem saber explicar o quê. Cérebro detecta padrões "
            "antes da consciência: maus hábitos se enraízam justamente porque param de "
            "ser vistos. <b>Tornar consciente é o primeiro ato de mudança</b>."
        ),
        bullets=[
            "Use o <b>Cartão de Pontuação de Hábitos</b>: liste tudo que faz num dia e marque +, − ou =.",
            "Verbalizar (em voz alta, p.ex. em supermercados japoneses) reduz erros e desperta consciência.",
            "Você não muda o que não enxerga.",
            "Identifique hábitos de entrada (gatilhos) que disparam cascatas inteiras de comportamento.",
        ],
        insights=[
            ("APONTAR-E-CHAMAR",
             "Técnica japonesa do <i>shisa kanko</i>: apontar para o sinal e nomear "
             "em voz alta. Reduz acidentes ferroviários em 85%. Aplicação pessoal: "
             "narrar a própria ação antes de executá-la."),
        ],
        key_quotes=[
            "Até que você torne o inconsciente consciente, ele dirigirá sua vida e você o chamará de destino.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 5",
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
            "Empilhar funciona porque ancora o novo comportamento em uma rede neural já existente.",
            "Encadeie hábitos para criar rotinas (manhã, trabalho, sono).",
        ],
        insights=[
            ("ELIMINAR DECISÕES",
             "O custo do hábito é, no fundo, o custo de decidir. Quando o gatilho "
             "decide por você (lugar + horário fixos), você poupa força de vontade "
             "para o que importa."),
        ],
        key_quotes=[
            "Muitas pessoas pensam que faltam motivação quando, na verdade, lhes falta clareza.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 6",
        title="Motivação é superestimada; ambiente importa mais",
        livro_pg="82",
        intro=(
            "Comportamento é uma função da pessoa e do contexto. Mudar o contexto "
            "é, quase sempre, mais barato e duradouro do que mudar a pessoa. "
            "<b>Design de ambiente</b> é o nome técnico para isso."
        ),
        bullets=[
            "Deixe pistas visíveis e fáceis para bons hábitos; remova as dos maus.",
            "Faça <b>um lugar = um propósito</b>: leitura na poltrona, trabalho na escrivaninha, sono na cama.",
            "Hospitais que põem água em destaque aumentaram consumo em 25,8% (e refrigerante caiu 11,4%).",
            "Você não tem um problema de disciplina; tem um problema de design.",
        ],
        insights=[
            ("AMBIENTES DE MULTI-USO",
             "Quando vários hábitos disputam o mesmo lugar, vence o mais antigo. "
             "Crie nichos: separe espaço de foco do espaço de descanso, mesmo "
             "que seja por um simples tapete ou cadeira diferente."),
        ],
        key_quotes=[
            "O ambiente é a mão invisível que molda o comportamento humano.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 7",
        title="O segredo do autocontrole",
        livro_pg="94",
        intro=(
            "Pessoas “disciplinadas” não resistem mais à tentação — elas <b>se expõem "
            "menos</b> a ela. Em vez de treinar força de vontade, projete uma vida "
            "com menos atrito moral."
        ),
        bullets=[
            "Estudo com veteranos do Vietnã: 95% dos viciados em heroína pararam ao voltar para casa — o ambiente havia mudado.",
            "Maus hábitos são autorreforçados: a deixa cria o desejo, que cria a resposta, que reforça a deixa.",
            "Quebrar um hábito a partir da raiz exige tornar a deixa invisível, não combatê-la.",
            "Quem oculta o doce não o quer; quem o vê o todo dia gasta energia para resistir.",
        ],
        insights=[
            ("ALÉM DA FORÇA DE VONTADE",
             "Autocontrole é uma estratégia de curto prazo. Mais eficaz: reduzir a "
             "exposição às deixas. Pessoas com hábitos exemplares costumam viver em "
             "ambientes que tornam o ruim incômodo e o bom inevitável."),
        ],
        key_quotes=[
            "Você pode quebrar um hábito, mas é improvável que o esqueça. A solução é manter os gatilhos longe da sua vista.",
        ]
    )

    story.append(PageBreak())

    # =====================================================
    # 2ª LEI — TORNE ATRAENTE
    # =====================================================
    add_law_separator(story, S, frame_w, "2ª LEI",
                      "Torne atraente",
                      "O desejo move a ação; engenheirar o desejo aumenta a probabilidade do hábito.")

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 8",
        title="Como tornar um hábito irresistível",
        livro_pg="104",
        intro=(
            "Comida superpalatável e redes sociais entregam <b>versões exageradas</b> "
            "dos gatilhos evolutivos do prazer. Dopamina é liberada na <b>antecipação</b>, "
            "não apenas na recompensa. Use isso a seu favor com agrupamento."
        ),
        bullets=[
            "<b>Agrupamento de tentações</b>: faça o que você precisa fazer junto com o que você gosta de fazer.",
            "Fórmula: “Depois de [hábito necessário], eu vou [hábito que quero]; depois, [hábito que adoro].”",
            "Dopamina sobe na antecipação: criar expectativa positiva aumenta a probabilidade de execução.",
            "Não é a recompensa em si, mas o desejo da recompensa, que sustenta a repetição.",
        ],
        insights=[
            ("PRAZER É PROMESSA",
             "Quando você associa um hábito difícil a uma promessa de prazer logo "
             "à frente, o cérebro injeta o esforço primeiro — porque já está vendo a "
             "recompensa no horizonte."),
        ],
        key_quotes=[
            "É o desejo, não a obtenção, que nos faz agir.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 9",
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
             "das suas pessoas. Pertencimento move comportamento mais do que a razão."),
        ],
        key_quotes=[
            "Um dos esforços humanos mais profundos é o de pertencer.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 10",
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
            "Reformulação: “Eu <b>tenho</b> que treinar” → “Eu <b>posso</b> treinar; meu corpo me permite.”",
            "Atletas de elite reinterpretam o nervosismo como excitação produtiva.",
        ],
        insights=[
            ("DESEJOS SÃO ANTIGOS, MEIOS SÃO NOVOS",
             "Quase nada do que sentimos é novo. Os meios pelos quais saciamos os "
             "desejos é que mudam. Trocar de meio (mas atender o mesmo desejo) é o "
             "movimento mais barato de mudança comportamental."),
        ],
        key_quotes=[
            "A motivação é fácil quando significado é claro.",
        ]
    )

    story.append(PageBreak())

    # =====================================================
    # 3ª LEI — TORNE FÁCIL
    # =====================================================
    add_law_separator(story, S, frame_w, "3ª LEI",
                      "Torne fácil",
                      "Reduza o atrito; remova obstáculos; menos passos, mais ação.")

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 11",
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
        key_quotes=[
            "Se você quer dominar um hábito, a chave é começar com a repetição, não com a perfeição.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 12",
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
        key_quotes=[
            "O comportamento humano segue a lei do mínimo esforço.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 13",
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
        key_quotes=[
            "Um hábito precisa ser estabelecido antes de ser melhorado.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 14",
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
        key_quotes=[
            "A maneira definitiva de criar bons hábitos é tornar a opção certa a mais fácil.",
        ]
    )

    story.append(PageBreak())

    # =====================================================
    # 4ª LEI — TORNE SATISFATÓRIO
    # =====================================================
    add_law_separator(story, S, frame_w, "4ª LEI",
                      "Torne satisfatório",
                      "O que é recompensado é repetido. Sem prazer no presente, o hábito não se fixa.")

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 15",
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
        key_quotes=[
            "O que é recompensado é repetido. O que é punido é evitado.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 16",
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
            "O que é medido melhora — mas cuidado em medir o indicador certo (entrada × resultado).",
        ],
        insights=[
            ("LEI DE GOODHART (CUIDADO)",
             "Quando uma métrica vira objetivo, deixa de ser boa métrica. Mensure "
             "para enxergar, não para se ludibriar — a régua é serva da identidade, "
             "não o contrário."),
        ],
        key_quotes=[
            "Perder uma vez é acidente. Perder duas vezes é o início de um novo hábito.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 17",
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
            "Dor à vista é mais forte que dor futura — use isso pedagogicamente, não punitivamente.",
            "Anônimo às vezes é mais eficaz que público (depende da personalidade).",
        ],
        insights=[
            ("ASSIMETRIA DA VERGONHA",
             "Não cumprir uma promessa sozinho é fácil de racionalizar; "
             "diante de outro humano, é caro. Use o capital social como aliado da sua mudança."),
        ],
        key_quotes=[
            "Sabendo que alguém está observando, você se torna seu melhor observador.",
        ]
    )

    story.append(PageBreak())

    # =====================================================
    # TÁTICAS AVANÇADAS
    # =====================================================

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 18",
        title="A verdade sobre talento (quando os genes importam)",
        livro_pg="216",
        intro=(
            "Genes não determinam o destino, mas inclinam o terreno. Maximize o "
            "retorno do esforço escolhendo arenas em que sua personalidade e biologia "
            "trabalham a seu favor. Os Big Five (abertura, conscienciosidade, "
            "extroversão, amabilidade, neuroticismo) sugerem para onde focar."
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
             "ferramentas. Depois, <b>explore</b> (em sentido de aprofundar) o que produz "
             "energia. A maior parte do desperdício humano está em focar cedo no jogo errado."),
        ],
        key_quotes=[
            "Quando você não consegue ganhar sendo melhor, ganhe sendo diferente.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 19",
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
        key_quotes=[
            "Tédio talvez seja o maior obstáculo no caminho do autoaperfeiçoamento.",
        ]
    )

    story.append(PageBreak())

    add_chapter(story, S, frame_w,
        cap_num="CAPÍTULO 20",
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
        key_quotes=[
            "O sucesso não é uma meta a alcançar, é um sistema para melhorar.",
        ]
    )

    story.append(PageBreak())

    # =====================================================
    # INSIGHTS PROFUNDOS
    # =====================================================
    story.append(Paragraph("PROFUNDIDADE", S["section_kicker"]))
    story.append(Paragraph("Insights profundos do livro", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=10))

    insights_globais = [
        ("Hábito é arquitetura, não vontade",
         "A grande inversão de James Clear é deslocar a mudança da arena moral "
         "(disciplina, força de vontade) para a arena do design (ambiente, atrito, "
         "deixas). Quando você acerta a arquitetura, a vontade vira secundária."),
        ("Identidade é a alavanca mais profunda",
         "Cada hábito é um voto em uma identidade. A maioria das pessoas tenta mudar "
         "o que faz; quem muda mais profundamente muda <b>quem é</b>. A pergunta-mestra "
         "é: que tipo de pessoa precisaria ser para esse resultado se tornar inevitável?"),
        ("Sistema > Meta (mas nem sempre)",
         "Metas mostram direção, sistemas geram progresso. Mas há um perigo: "
         "alguns sistemas viram zonas de conforto. Por isso, sistemas precisam de "
         "revisão — caso contrário, automaticidade se torna estagnação."),
        ("Vale da Decepção",
         "A maioria dos hábitos só rende após uma fase de estagnação aparente — "
         "como um cubo de gelo que vai de −5° a 0° sem mudança visível, e então "
         "derrete a +1°. Continuar nessa zona é, talvez, a habilidade mais subestimada."),
        ("Atrito é destino",
         "Cada segundo entre você e a ação reduz drasticamente a chance da ação. "
         "Engenharia do atrito é mais decisiva do que motivação. Você pode "
         "literalmente prever seu comportamento futuro pelo design do seu lar."),
        ("Dois minutos não é truque, é portal",
         "A regra dos dois minutos não busca progresso, busca <b>aparição</b>. "
         "Aparecer é a habilidade mestra do longo prazo — porque consistência "
         "compõe e ausência apaga."),
        ("Identidade × Evidência",
         "Identidades são frágeis quando puramente afirmadas. Tornam-se sólidas "
         "quando lastreadas por evidências (ações). Auto-narrativa sem prova "
         "vira síndrome do impostor; prova sem narrativa vira esforço estéril."),
        ("Hábito como liberdade, não prisão",
         "Quando os básicos são automáticos, sobra atenção para o criativo. "
         "Disciplina, paradoxalmente, é o caminho mais curto para a liberdade. "
         "Quem não automatiza o trivial, gasta o melhor de si com o irrelevante."),
        ("Tempo, não esforço, é a moeda",
         "Pequenos comportamentos consistentes vencem grandes esforços esporádicos. "
         "Quem entende a aritmética do composto para de buscar atalhos e passa a "
         "buscar regularidade."),
        ("Ambiente é o psicoterapeuta mais barato",
         "Antes de mudar a si, mude a casa. Antes de mudar a casa, mude o quarto. "
         "Antes de mudar o quarto, mude a mesa de cabeceira. Camadas de design fazem "
         "trabalho silencioso que a terapia explícita levaria meses."),
    ]
    for titulo, texto in insights_globais:
        story.append(Paragraph(titulo, S["h3"]))
        story.append(Paragraph(texto, S["body"]))
        story.append(Spacer(1, 0.15*cm))

    story.append(PageBreak())

    # caderno de anotações da seção de insights
    story.append(Paragraph("REFLEXÃO PESSOAL", S["section_kicker"]))
    story.append(Paragraph("Suas anotações sobre os insights", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=10))
    story.append(Paragraph(
        "Escolha 3 insights desta seção que mais te atravessaram. Para cada um, "
        "responda: (1) onde reconheço isso na minha vida hoje? (2) qual seria "
        "a menor experiência possível para testar isso esta semana?", S["body_small"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(NoteLines(frame_w, num_lines=18, label="Insights × minha vida"))

    story.append(PageBreak())

    # =====================================================
    # COMO MUDAR
    # =====================================================
    story.append(Paragraph("PROTOCOLO", S["section_kicker"]))
    story.append(Paragraph("Como mudar — protocolo prático", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=10))

    story.append(Paragraph(
        "Mudança eficaz não é épica, é metódica. Siga este protocolo de "
        "<b>seis movimentos</b> para qualquer mudança comportamental concreta.",
        S["body"]))

    passos = [
        ("01 · Defina a identidade-alvo",
         "Antes do quê, defina o quem. Escreva: “Eu sou alguém que ____.” "
         "Use uma frase simples, no presente, com verbo de ação no infinitivo."),
        ("02 · Escolha 1 hábito atômico",
         "Apenas um. Pequeno o suficiente para caber em dois minutos. Conectado "
         "claramente à identidade-alvo. Mais de um hábito por ciclo dispersa o foco."),
        ("03 · Engenheire as 4 leis",
         "Para o hábito desejado: torne-o claro (deixa visível), atraente "
         "(agrupamento), fácil (atrito baixo) e satisfatório (recompensa imediata). "
         "Para qualquer hábito que atrapalhe: torne-o invisível, desinteressante, "
         "difícil e insatisfatório."),
        ("04 · Crie a infraestrutura",
         "Mude o ambiente físico e digital. Pré-decida tudo o que conseguir. "
         "Anote o quando + onde (intenção de implementação). Encaixe no empilhamento."),
        ("05 · Mensure de forma simples",
         "Rastreador binário: fez/não fez. Regra: nunca falhar duas vezes seguidas. "
         "Reveja semanalmente; aceite ruído, recuse tendência."),
        ("06 · Reveja o sistema",
         "A cada 30 dias: o que está funcionando? O que está só confortável? "
         "Ajuste a dificuldade (regra de Cachinhos Dourados). A cada 12 meses: "
         "revise a identidade-alvo."),
    ]
    for tit, txt in passos:
        story.append(Paragraph(tit, S["h3"]))
        story.append(Paragraph(txt, S["body"]))
    story.append(Spacer(1, 0.3*cm))

    story.append(CalloutBox(
        frame_w,
        "Regra de bolso: se a mudança precisa de força de vontade no terceiro dia, "
        "o problema é de design, não de caráter. Volte ao ambiente.",
        label="REGRA DE BOLSO"))

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("Suas anotações", S["h3"]))
    story.append(NoteLines(frame_w, num_lines=6))

    story.append(PageBreak())

    # =====================================================
    # COMO EVOLUIR — PLANO 90 DIAS
    # =====================================================
    story.append(Paragraph("PROGRESSÃO", S["section_kicker"]))
    story.append(Paragraph("Como evoluir — plano de 90 dias", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=10))

    story.append(Paragraph(
        "Um ciclo curto é tempo suficiente para enraizar um hábito e curto o suficiente "
        "para não pesar. Use este molde de 90 dias divididos em três fases.",
        S["body"]))

    fases = [
        ["FASE", "DIAS", "OBJETIVO", "PRÁTICA"],
        ["Implantar", "1–30", "Tornar o hábito visível, fácil e satisfatório.",
            "Regra dos 2 minutos · empilhamento · tracker binário"],
        ["Aprofundar", "31–60", "Subir a dificuldade até o ponto de Cachinhos Dourados.",
            "Aumentar duração/intensidade · variabilidade controlada · revisão semanal"],
        ["Consolidar", "61–90", "Internalizar como identidade e blindar contra recaída.",
            "Contrato de hábito · parceiro de responsabilidade · revisão mensal"],
    ]
    ft = Table(fases, colWidths=[2.6*cm, 1.6*cm, 5.2*cm, frame_w - 2.6*cm - 1.6*cm - 5.2*cm])
    ft.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 8),
        ("TEXTCOLOR", (0,0), (-1,0), MUTED),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
        ("LINEBELOW", (0,0), (-1,0), 0.5, INK),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0,1), (0,-1), ACCENT),
        ("FONTSIZE", (0,1), (-1,-1), 9.5),
        ("BOTTOMPADDING", (0,1), (-1,-1), 8),
        ("TOPPADDING", (0,1), (-1,-1), 8),
        ("LINEBELOW", (0,1), (-1,-1), 0.3, HAIRLINE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(ft)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("Rotina diária recomendada", S["h2"]))
    rotina = [
        "<b>Manhã (5 min)</b>: revisar identidade-alvo + relembrar o hábito do dia.",
        "<b>Bloco do hábito</b>: executar na janela e no lugar pré-definidos.",
        "<b>Final do dia (2 min)</b>: marcar tracker + uma linha de reflexão.",
        "<b>Sexta-feira (10 min)</b>: revisar semana. O que reforço? O que ajusto?",
        "<b>Último domingo do mês</b>: revisão mensal e nova meta de dificuldade.",
    ]
    for r in rotina:
        story.append(Paragraph("•  " + r, S["bullet"]))

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("Anotações sobre minha evolução", S["h3"]))
    story.append(NoteLines(frame_w, num_lines=6))

    story.append(PageBreak())

    # =====================================================
    # EXERCÍCIOS
    # =====================================================
    story.append(Paragraph("PRÁTICA", S["section_kicker"]))
    story.append(Paragraph("Exercícios para fazer agora", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=10))
    story.append(Paragraph(
        "Lista de 12 exercícios — alguns curtos, outros recorrentes. Marque "
        "conforme conclui. Eles cobrem as 4 leis e mais identidade, revisão e "
        "ambiente.", S["body"]))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("Identidade", S["h3"]))
    story.append(CheckboxList(frame_w, [
        "Escreva 3 identidades-alvo (frases iniciadas com 'Eu sou alguém que…').",
        "Para cada identidade, liste 5 evidências que você poderia produzir esta semana.",
    ]))
    story.append(Paragraph("1ª Lei · Tornar claro", S["h3"]))
    story.append(CheckboxList(frame_w, [
        "Faça o Cartão de Pontuação: liste todos os seus hábitos diários e marque +, − ou =.",
        "Escreva 1 intenção de implementação: 'Eu vou [ação] em [horário] em [lugar]'.",
        "Crie 1 empilhamento: 'Depois de [hábito atual], eu vou [novo hábito]'.",
    ]))
    story.append(Paragraph("2ª Lei · Tornar atraente", S["h3"]))
    story.append(CheckboxList(frame_w, [
        "Aplique o agrupamento de tentações: junte algo que precisa fazer a algo que gosta de fazer.",
        "Escolha 1 grupo (presencial ou online) cujos hábitos você queira herdar.",
    ]))
    story.append(Paragraph("3ª Lei · Tornar fácil", S["h3"]))
    story.append(CheckboxList(frame_w, [
        "Reduza 2 hábitos novos à versão de 2 minutos e teste 7 dias seguidos.",
        "Elimine 3 atritos do ambiente para os bons hábitos; adicione 3 atritos para os maus.",
    ]))
    story.append(Paragraph("4ª Lei · Tornar satisfatório", S["h3"]))
    story.append(CheckboxList(frame_w, [
        "Crie um rastreador (papel ou app) e marque a sequência diária.",
        "Defina 1 recompensa imediata (que reforce a identidade-alvo) após o hábito.",
        "Escreva um contrato de hábito com 1 parceiro de responsabilidade.",
    ]))
    story.append(Paragraph("Revisão", S["h3"]))
    story.append(CheckboxList(frame_w, [
        "Agende na agenda 1 revisão semanal de 15 minutos pelas próximas 12 semanas.",
    ]))

    story.append(PageBreak())

    # ----- Caderno de anotações (final) -----
    story.append(Paragraph("CADERNO", S["section_kicker"]))
    story.append(Paragraph("Anotações livres", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=10))
    story.append(Paragraph(
        "Use estas páginas para registrar descobertas próprias, frases que te "
        "tocaram, conexões com sua vida, perguntas e revisões mensais.",
        S["body_small"]))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("O que aprendi com este livro", S["h3"]))
    story.append(NoteLines(frame_w, num_lines=10))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("O que vou mudar a partir de hoje", S["h3"]))
    story.append(NoteLines(frame_w, num_lines=10))

    story.append(PageBreak())

    story.append(Paragraph("REVISÃO MENSAL", S["section_kicker"]))
    story.append(Paragraph("Mês 1   ·   Mês 2   ·   Mês 3", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=10))

    story.append(Paragraph("Mês 1 — o que funcionou? o que não funcionou?", S["h3"]))
    story.append(NoteLines(frame_w, num_lines=6))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("Mês 2 — o que evoluiu?", S["h3"]))
    story.append(NoteLines(frame_w, num_lines=6))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("Mês 3 — qual identidade está se consolidando?", S["h3"]))
    story.append(NoteLines(frame_w, num_lines=6))

    story.append(PageBreak())

    # --- Página de fechamento ---
    story.append(Spacer(1, 5*cm))
    story.append(Paragraph("UM ÚLTIMO LEMBRETE", S["section_kicker"]))
    story.append(Paragraph("Aparecer é a habilidade mestra.", S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=14))
    story.append(Paragraph(
        "Você não precisa fazer muito; precisa fazer o pouco, todo dia. O resto, "
        "o tempo faz por você.", S["body"]))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("— Resumo organizado a partir de <i>Hábitos Atômicos</i>, de James Clear.",
                           S["caption"]))

    doc.build(story)


# =====================================================
# Helpers
# =====================================================

def add_chapter(story, S, frame_w, cap_num, title, livro_pg, intro, bullets, insights, key_quotes):
    story.append(Paragraph(f"{cap_num}  ·  PÁGINA NO LIVRO: {livro_pg}", S["section_kicker"]))
    story.append(Paragraph(title, S["section"]))
    story.append(HLine(frame_w, thickness=0.6, color=INK, space_after=10))

    story.append(Paragraph(intro, S["body"]))

    story.append(Paragraph("Pontos-chave", S["h2"]))
    for b in bullets:
        story.append(Paragraph("•  " + b, S["bullet"]))

    if key_quotes:
        story.append(Paragraph("Frases para guardar", S["h2"]))
        for q in key_quotes:
            story.append(Paragraph(f"“{q}”", S["quote"]))

    if insights:
        story.append(Paragraph("Insights", S["h2"]))
        for label, txt in insights:
            story.append(CalloutBox(frame_w, txt, label=label))
            story.append(Spacer(1, 0.15*cm))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Suas anotações", S["h3"]))
    story.append(NoteLines(frame_w, num_lines=5))


def add_law_separator(story, S, frame_w, lei, titulo, subt):
    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph(lei, S["section_kicker"]))
    story.append(Paragraph(titulo, S["section"]))
    story.append(HLine(frame_w, thickness=1.2, color=ACCENT, space_after=8))
    story.append(Paragraph(subt, S["body"]))
    story.append(Spacer(1, 0.4*cm))


if __name__ == "__main__":
    build()
    print(f"PDF gerado: {OUTPUT}")
