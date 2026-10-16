"""
Gerador de Caderno de Prova Completo em PDF - Caderno Branco (Padrão ENEM 2 Colunas).
Otimizado para impressão em Preto e Branco e máxima conformidade visual com o ENEM oficial:
- Layout em 2 colunas com linha divisória vertical oficial e tipografia nítida (Arial TrueType).
- Capa Oficial de alto contraste com frase de segurança, instruções 1 a 6 detalhando as 4 áreas e redação,
  e aviso explícito de caneta preta obrigatória (proibido azul).
- Cabeçalhos de Área (Linguagens, Humanas, Natureza, Matemática) integrados no KeepTogether da primeira
  questão da área (nunca desconectam nem ficam órfãos no rodapé da página anterior).
- Proposta de Redação e Folha de Rascunho posicionadas estritamente no MEIO da prova (logo após a Q32).
- Proposta de Redação com todos os 4 textos motivadores e imagens originais extraídas do documento oficial.
- Folha de Rascunho com 30 linhas ampliadas, marca d'água e instruções oficiais completas do ENEM.
- Sanitização automática de subscritos/sobrescritos (H2O2, q0, Mg2+, etc.) para eliminar caracteres quadrados.
- Fontes/bibliografias posicionadas após imagens/ao final do texto; sem títulos de aulas e sem citações INEP em matemática.
- Rodapé padronizado como "2º SIMULADO ENEM".
"""

import os
import sys
import json
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image as RLImage, Flowable, NextPageTemplate
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Registro de fontes TrueType do Windows para renderização perfeita de caracteres Unicode
FONT_NORMAL = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"

arial_reg = "C:/Windows/Fonts/arial.ttf"
arial_bold = "C:/Windows/Fonts/arialbd.ttf"
arial_ital = "C:/Windows/Fonts/ariali.ttf"

if os.path.exists(arial_reg) and os.path.exists(arial_bold):
    try:
        pdfmetrics.registerFont(TTFont("Arial", arial_reg))
        pdfmetrics.registerFont(TTFont("Arial-Bold", arial_bold))
        if os.path.exists(arial_ital):
            pdfmetrics.registerFont(TTFont("Arial-Italic", arial_ital))
        else:
            pdfmetrics.registerFont(TTFont("Arial-Italic", arial_reg))
        FONT_NORMAL = "Arial"
        FONT_BOLD = "Arial-Bold"
        FONT_ITALIC = "Arial-Italic"
    except Exception:
        pass

PAGE_W, PAGE_H = A4
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MARGIN_LEFT = 36.0
MARGIN_RIGHT = 36.0
MARGIN_TOP = 40.0
MARGIN_BOTTOM = 38.0
GUTTER = 16.0

USABLE_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
USABLE_H = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM
COL_W = (USABLE_W - GUTTER) / 2.0


def sanitize_for_reportlab(text):
    """
    Higieniza o texto para o ReportLab:
    - Converte subscritos (H₂O₂, q₀) em <sub>...</sub>
    - Converte sobrescritos (Mg²⁺, d², 10⁻⁹) em <sup>...</sup>
    - Normaliza símbolos matemáticos, aspas curvas, travessões e marcadores de tópicos.
    """
    if not text or not isinstance(text, str):
        return ""

    # Substituição de fórmulas químicas e físicas comuns
    text = re.sub(r'H2O2\b', 'H<sub>2</sub>O<sub>2</sub>', text)
    text = re.sub(r'Mg\(OH\)2\b', 'Mg(OH)<sub>2</sub>', text)
    text = re.sub(r'Ca\(OH\)2\b', 'Ca(OH)<sub>2</sub>', text)
    text = re.sub(r'Mg2\+\b', 'Mg<sup>2+</sup>', text)
    text = re.sub(r'Ca2\+\b', 'Ca<sup>2+</sup>', text)

    # Subscritos Unicode -> <sub>
    sub_map = {
        '₀': '<sub>0</sub>', '₁': '<sub>1</sub>', '₂': '<sub>2</sub>', '₃': '<sub>3</sub>',
        '₄': '<sub>4</sub>', '₅': '<sub>5</sub>', '₆': '<sub>6</sub>', '₇': '<sub>7</sub>',
        '₈': '<sub>8</sub>', '₉': '<sub>9</sub>', 'ₐ': '<sub>a</sub>', 'ₑ': '<sub>e</sub>',
        'ₒ': '<sub>o</sub>', 'ₓ': '<sub>x</sub>'
    }
    for k, v in sub_map.items():
        text = text.replace(k, v)

    # Sobrescritos Unicode -> <sup>
    sup_map = {
        '⁰': '<sup>0</sup>', '¹': '<sup>1</sup>', '²': '<sup>2</sup>', '³': '<sup>3</sup>',
        '⁴': '<sup>4</sup>', '⁵': '<sup>5</sup>', '⁶': '<sup>6</sup>', '⁷': '<sup>7</sup>',
        '⁸': '<sup>8</sup>', '⁹': '<sup>9</sup>', '⁺': '<sup>+</sup>', '⁻': '<sup>-</sup>',
        'ⁿ': '<sup>n</sup>'
    }
    for k, v in sup_map.items():
        text = text.replace(k, v)

    # Símbolos, pontuações e setas
    sym_map = {
        '→': ' &rarr; ',
        '←': ' &larr; ',
        '•': '&bull;',
        '–': '-',       # En-dash
        '—': '--',      # Em-dash
        '“': '"',
        '”': '"',
        '’': "'",
        '‘': "'",
        '≤': '&le;',
        '≥': '&ge;',
        '≠': '&ne;',
        '×': 'x'
    }
    for k, v in sym_map.items():
        text = text.replace(k, v)

    # Converte quebras de linha em <br/> se não houver tags de parágrafo
    if "\n" in text and "<p>" not in text.lower():
        text = text.replace("\n", "<br/>")

    return text


class QuestionHeaderFlowable(Flowable):
    """Desenha 'QUESTÃO XX' seguido da barra horizontal no estilo oficial do ENEM."""
    def __init__(self, q_num, width):
        super().__init__()
        self.q_num = q_num
        self.width = width
        self.height = 14

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setFont(FONT_BOLD, 9.2)
        self.canv.setFillColor(colors.black)
        txt = f"QUESTÃO {self.q_num:02d}"
        self.canv.drawString(0, 3, txt)
        txt_w = self.canv.stringWidth(txt, FONT_BOLD, 9.2)

        bar_start_x = txt_w + 6
        bar_w = self.width - bar_start_x
        if bar_w > 10:
            self.canv.setFillColor(colors.HexColor("#777777"))
            self.canv.rect(bar_start_x, bar_y := 4.2, bar_w * 0.70, 2.2, fill=1, stroke=0)
            self.canv.setFillColor(colors.black)
            self.canv.rect(bar_start_x + bar_w * 0.70, bar_y, bar_w * 0.30, 2.2, fill=1, stroke=0)
        self.canv.restoreState()


class AlternativeBadgeFlowable(Flowable):
    """Desenha a bolinha vazada (apenas contorno preto com letra preta), estilo oficial ENEM."""
    def __init__(self, letter):
        super().__init__()
        self.letter = letter
        self.width = 14
        self.height = 12

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        cx = 6.5
        cy = 4.5
        r = 5.2
        self.canv.setStrokeColor(colors.black)
        self.canv.setLineWidth(0.8)
        self.canv.setFillColor(colors.white)
        self.canv.circle(cx, cy, r, fill=1, stroke=1)
        self.canv.setFont(FONT_BOLD, 6.8)
        self.canv.setFillColor(colors.black)
        self.canv.drawCentredString(cx, cy - 2.2, self.letter)
        self.canv.restoreState()


class DraftWatermarkFlowable(Flowable):
    """Desenha as 30 linhas da Folha de Rascunho com marca d'água oficial centralizada."""
    def __init__(self, width, height=540):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()

        # Marca d'água diagonal em cinza sutil
        self.canv.saveState()
        self.canv.translate(self.width / 2.0, self.height / 2.0)
        self.canv.rotate(35)
        self.canv.setFont(FONT_BOLD, 36)
        self.canv.setFillColor(colors.HexColor("#f0f0f0"))
        self.canv.drawCentredString(0, 0, "RASCUNHO DA REDAÇÃO")
        self.canv.restoreState()

        # Grade de 30 linhas numeradas
        num_lines = 30
        line_h = self.height / float(num_lines)
        num_w = 20.0

        # Borda externa
        self.canv.setStrokeColor(colors.black)
        self.canv.setLineWidth(1.0)
        self.canv.rect(0, 0, self.width, self.height, fill=0, stroke=1)
        self.canv.line(num_w, 0, num_w, self.height)

        for i in range(num_lines):
            y = self.height - (i + 1) * line_h
            if i < num_lines - 1:
                self.canv.setStrokeColor(colors.HexColor("#aaaaaa"))
                self.canv.setLineWidth(0.5)
                self.canv.line(0, y, self.width, y)

            self.canv.setFont(FONT_BOLD, 7.5)
            self.canv.setFillColor(colors.black)
            self.canv.drawCentredString(num_w / 2.0, y + 4.5, str(i + 1))

        self.canv.restoreState()


def draw_cover_background(canv, doc):
    """
    Desenha a Capa Oficial do Caderno Branco com alto padrão visual:
    - Sem cortes nas margens superiores.
    - Título refinado: 2º SIMULADO UNIFICADO COLETIVO VOA VOA & PREPARATÓRIO GABARITA.
    - Divisão das 4 áreas + Redação explicitada com exatidão nas instruções.
    - Alerta rigoroso: Uso exclusivo de caneta preta (proibido azul).
    """
    canv.saveState()
    metadados = getattr(doc, "metadados", {})

    # Moldura externa segura para impressão
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(1.4)
    canv.rect(MARGIN_LEFT - 4, MARGIN_BOTTOM - 4, USABLE_W + 8, USABLE_H + 8, fill=0, stroke=1)
    canv.setLineWidth(0.6)
    canv.rect(MARGIN_LEFT - 1, MARGIN_BOTTOM - 1, USABLE_W + 2, USABLE_H + 2, fill=0, stroke=1)

    # Topo da Capa: Identificação limpa sem cortes
    top_y = PAGE_H - MARGIN_TOP + 14
    canv.setFont(FONT_BOLD, 9.5)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT + 6, top_y, "CADERNO 1 | BRANCO")

    # Badge direito: 70 QUESTÕES
    badge_w = 90
    badge_h = 20
    badge_x = PAGE_W - MARGIN_RIGHT - badge_w - 4
    badge_y = top_y - 5
    canv.setFillColor(colors.black)
    canv.roundRect(badge_x, badge_y, badge_w, badge_h, 3, fill=1, stroke=0)
    canv.setFont(FONT_BOLD, 9.5)
    canv.setFillColor(colors.white)
    canv.drawCentredString(badge_x + badge_w / 2.0, badge_y + 6, "70 QUESTÕES")

    # Título Institucional Superior
    canv.setFont(FONT_BOLD, 15)
    canv.setFillColor(colors.black)
    canv.drawCentredString(PAGE_W / 2.0, PAGE_H - 74, "2º SIMULADO UNIFICADO")

    canv.setFont(FONT_BOLD, 11)
    canv.setFillColor(colors.HexColor("#222222"))
    canv.drawCentredString(PAGE_W / 2.0, PAGE_H - 91, "COLETIVO VOA VOA & PREPARATÓRIO GABARITA")

    canv.setFont(FONT_NORMAL, 8.5)
    canv.setFillColor(colors.HexColor("#444444"))
    canv.drawCentredString(PAGE_W / 2.0, PAGE_H - 105, "PROVA DE LINGUAGENS, CIÊNCIAS HUMANAS, NATUREZA, MATEMÁTICA E REDAÇÃO")

    # Card ENEM Central em Alto Contraste
    card_y = PAGE_H - 192
    card_h = 72
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(1.2)
    canv.setFillColor(colors.white)
    canv.roundRect(MARGIN_LEFT + 10, card_y, USABLE_W - 20, card_h, 5, fill=1, stroke=1)

    canv.setFont(FONT_BOLD, 38)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT + 36, card_y + 20, "enem")

    ano = str(metadados.get("ano", "2026"))
    canv.setFont(FONT_NORMAL, 38)
    canv.setFillColor(colors.HexColor("#444444"))
    canv.drawString(MARGIN_LEFT + 150, card_y + 20, ano)

    # Divisória vertical no card
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(1.2)
    canv.line(MARGIN_LEFT + USABLE_W - 130, card_y + 10, MARGIN_LEFT + USABLE_W - 130, card_y + card_h - 10)

    # Identificação do Caderno à direita do card
    canv.setFont(FONT_BOLD, 8.0)
    canv.setFillColor(colors.black)
    canv.drawCentredString(MARGIN_LEFT + USABLE_W - 70, card_y + 50, "CADERNO")
    canv.setFont(FONT_BOLD, 22)
    canv.drawCentredString(MARGIN_LEFT + USABLE_W - 70, card_y + 25, "1")
    canv.setFont(FONT_BOLD, 10.0)
    canv.drawCentredString(MARGIN_LEFT + USABLE_W - 70, card_y + 11, "BRANCO")

    # Caixa da Frase de Segurança
    frase_y = card_y - 78
    frase_h = 66
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(0.9)
    canv.roundRect(MARGIN_LEFT + 10, frase_y, USABLE_W - 20, frase_h, 4, fill=0, stroke=1)

    canv.setFont(FONT_BOLD, 7.8)
    canv.setFillColor(colors.black)
    canv.drawCentredString(PAGE_W / 2.0, frase_y + frase_h - 14, "ATENÇÃO: transcreva no espaço apropriado do seu CARTÃO-RESPOSTA,")
    canv.setFont(FONT_NORMAL, 7.8)
    canv.drawCentredString(PAGE_W / 2.0, frase_y + frase_h - 25, "com sua caligrafia usual, considerando as letras maiúsculas e minúsculas, a seguinte frase:")

    # Tarja preta com a frase de segurança
    frase = metadados.get("frase_seguranca", "A persistência constrói o conhecimento e abre caminhos para o futuro.")
    f_box_w = USABLE_W - 60
    f_box_h = 23
    f_box_x = MARGIN_LEFT + 30
    f_box_y = frase_y + 9
    canv.setFillColor(colors.black)
    canv.roundRect(f_box_x, f_box_y, f_box_w, f_box_h, 3, fill=1, stroke=0)
    canv.setFont(FONT_BOLD, 9.0)
    canv.setFillColor(colors.white)
    canv.drawCentredString(PAGE_W / 2.0, f_box_y + 7.0, frase)

    # Bloco das Instruções Oficiais
    inst_y = MARGIN_BOTTOM + 25
    inst_h = frase_y - inst_y - 10
    canv.setStrokeColor(colors.HexColor("#333333"))
    canv.setLineWidth(0.8)
    canv.setFillColor(colors.HexColor("#FAFAFA"))
    canv.roundRect(MARGIN_LEFT + 10, inst_y, USABLE_W - 20, inst_h, 4, fill=1, stroke=1)

    canv.setFont(FONT_BOLD, 9.5)
    canv.setFillColor(colors.black)
    canv.drawCentredString(PAGE_W / 2.0, inst_y + inst_h - 16, "LEIA ATENTAMENTE AS INSTRUÇÕES SEGUINTES:")

    instrucoes = [
        ("1. COMPOSIÇÃO DESTE CADERNO DE QUESTÕES (70 Itens + Redação):", True),
        ("   • Linguagens, Códigos e suas Tecnologias: Questões 01 a 16", False),
        ("   • Ciências Humanas e suas Tecnologias: Questões 17 a 32", False),
        ("   • Proposta de Redação e Rascunho: Localizada no MEIO do caderno (após a Questão 32)", False),
        ("   • Ciências da Natureza e suas Tecnologias: Questões 33 a 50", False),
        ("   • Matemática e suas Tecnologias: Questões 51 a 70", False),
        ("2. OBRIGATORIEDADE DE CANETA PRETA (PROIBIDO CANETA AZUL):", True),
        ("   • Preencha o CARTÃO-RESPOSTA e a FOLHA DE REDAÇÃO exclusivamente com caneta esferográfica de", False),
        ("     tinta preta (fabricada em material transparente). É ESTRITAMENTE PROIBIDO O USO DE CANETA AZUL,", False),
        ("     lápis, grafite, borracha ou qualquer tipo de corretivo líquido/fita.", False),
        ("3. DURAÇÃO E TEMPO DE PROVA:", True),
        ("   • O tempo total disponível para a realização das 70 questões e da redação é de cinco horas.", False),
        ("4. MARCAÇÃO DAS ALTERNATIVAS:", True),
        ("   • Para cada questão objetiva, são apresentadas 5 alternativas (A, B, C, D e E). Apenas uma é correta.", False),
        ("   • Preencha completamente a bolha no cartão. Marcações neste caderno NÃO serão computadas na nota.", False),
        ("5. TRANSCRIÇÃO DA REDAÇÃO:", True),
        ("   • Apenas o texto transcrito com caneta preta na FOLHA DE REDAÇÃO definitiva será corrigido.", False),
        ("6. DEVOLUÇÃO:", True),
        ("   • Ao concluir o exame, entregue ao fiscal este CADERNO, o CARTÃO-RESPOSTA e a FOLHA DE REDAÇÃO.", False),
    ]

    curr_y = inst_y + inst_h - 32
    for linha, is_title in instrucoes:
        if is_title:
            curr_y -= 4
            canv.setFont(FONT_BOLD, 7.6)
            canv.setFillColor(colors.black)
        else:
            canv.setFont(FONT_NORMAL, 7.2)
            canv.setFillColor(colors.HexColor("#222222"))
        canv.drawString(MARGIN_LEFT + 24, curr_y, linha)
        curr_y -= 11.2

    # Rodapé da Capa
    footer_y = MARGIN_BOTTOM + 7.0
    canv.setFont(FONT_BOLD, 8)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT + 6, footer_y, "COLETIVO VOA VOA • GABARITA")
    canv.drawRightString(PAGE_W - MARGIN_RIGHT - 6, footer_y, "2º SIMULADO ENEM 2026")

    canv.restoreState()


def draw_two_column_decorations(canv, doc):
    """
    Desenha o cabeçalho superior e o rodapé limpo das páginas de questões em 2 colunas.
    """
    canv.saveState()
    page_num = canv.getPageNumber()

    # Linha vertical divisória entre as 2 colunas
    x_sep = MARGIN_LEFT + COL_W + (GUTTER / 2.0)
    canv.setStrokeColor(colors.HexColor("#bbbbbb"))
    canv.setLineWidth(0.6)
    canv.line(x_sep, MARGIN_BOTTOM, x_sep, PAGE_H - MARGIN_TOP)

    # Cabeçalho Superior
    header_y = PAGE_H - MARGIN_TOP + 8
    canv.setFont(FONT_BOLD, 11)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT, header_y + 2, "enem")
    canv.setFont(FONT_NORMAL, 11)
    canv.setFillColor(colors.HexColor("#555555"))
    canv.drawString(MARGIN_LEFT + 32, header_y + 2, "2026")

    canv.setFont(FONT_BOLD, 8)
    canv.setFillColor(colors.black)
    canv.drawRightString(PAGE_W - MARGIN_RIGHT, header_y + 2, "CADERNO 1 | BRANCO")

    canv.setStrokeColor(colors.black)
    canv.setLineWidth(0.8)
    canv.line(MARGIN_LEFT, header_y - 4, PAGE_W - MARGIN_RIGHT, header_y - 4)

    # Rodapé Padronizado
    footer_y = MARGIN_BOTTOM - 16
    canv.setStrokeColor(colors.HexColor("#cccccc"))
    canv.setLineWidth(0.5)
    canv.line(MARGIN_LEFT, footer_y + 12, PAGE_W - MARGIN_RIGHT, footer_y + 12)

    # Número da página à esquerda
    canv.setFont(FONT_BOLD, 9)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT, footer_y + 1, str(page_num))

    # Identificador oficial à direita
    canv.setFont(FONT_BOLD, 8.0)
    canv.setFillColor(colors.black)
    canv.drawRightString(PAGE_W - MARGIN_RIGHT, footer_y + 1, "2º SIMULADO ENEM")

    canv.restoreState()


def draw_single_column_decorations(canv, doc):
    """Decorações da página de redação e rascunho (coluna única)."""
    canv.saveState()
    page_num = canv.getPageNumber()

    header_y = PAGE_H - MARGIN_TOP + 8
    canv.setFont(FONT_BOLD, 11)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT, header_y + 2, "enem")
    canv.setFont(FONT_NORMAL, 11)
    canv.setFillColor(colors.HexColor("#555555"))
    canv.drawString(MARGIN_LEFT + 32, header_y + 2, "2026")

    canv.setFont(FONT_BOLD, 8)
    canv.setFillColor(colors.black)
    canv.drawRightString(PAGE_W - MARGIN_RIGHT, header_y + 2, "PROPOSTA DE REDAÇÃO • CADERNO BRANCO")

    canv.setStrokeColor(colors.black)
    canv.setLineWidth(0.8)
    canv.line(MARGIN_LEFT, header_y - 4, PAGE_W - MARGIN_RIGHT, header_y - 4)

    footer_y = MARGIN_BOTTOM - 16
    canv.setStrokeColor(colors.HexColor("#cccccc"))
    canv.setLineWidth(0.5)
    canv.line(MARGIN_LEFT, footer_y + 12, PAGE_W - MARGIN_RIGHT, footer_y + 12)

    canv.setFont(FONT_BOLD, 9)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT, footer_y + 1, str(page_num))

    canv.setFont(FONT_BOLD, 8.0)
    canv.setFillColor(colors.black)
    canv.drawRightString(PAGE_W - MARGIN_RIGHT, footer_y + 1, "2º SIMULADO ENEM")

    canv.restoreState()


def get_two_column_styles():
    """Tipografia de alta legibilidade para diagramação em 2 colunas."""
    styles = {
        "AreaBanner": ParagraphStyle(
            "AreaBanner",
            fontName=FONT_BOLD,
            fontSize=8.6,
            leading=11.0,
            textColor=colors.black,
            backColor=colors.HexColor("#EAEAEA"),
            borderPadding=(4, 6, 4, 6),
            spaceAfter=6,
            spaceBefore=2,
            alignment=0,
            keepWithNext=True
        ),
        "TextSupportTitle": ParagraphStyle(
            "TextSupportTitle",
            fontName=FONT_BOLD,
            fontSize=8.0,
            leading=10.2,
            textColor=colors.black,
            alignment=1,
            spaceAfter=2,
            spaceBefore=2,
        ),
        "TextSupportBody": ParagraphStyle(
            "TextSupportBody",
            fontName=FONT_NORMAL,
            fontSize=7.6,
            leading=9.8,
            textColor=colors.HexColor("#111111"),
            alignment=4,  # Justificado
            spaceAfter=3,
        ),
        "TextSupportSource": ParagraphStyle(
            "TextSupportSource",
            fontName=FONT_ITALIC,
            fontSize=6.4,
            leading=8.2,
            textColor=colors.HexColor("#444444"),
            alignment=2,  # Direita
            spaceAfter=4,
            spaceBefore=2,
        ),
        "QuestionPrompt": ParagraphStyle(
            "QuestionPrompt",
            fontName=FONT_NORMAL,
            fontSize=7.8,
            leading=10.0,
            textColor=colors.black,
            alignment=4,
            spaceAfter=4,
            spaceBefore=1,
        ),
        "AlternativeText": ParagraphStyle(
            "AlternativeText",
            fontName=FONT_NORMAL,
            fontSize=7.4,
            leading=9.5,
            textColor=colors.HexColor("#111111"),
            alignment=4,
        ),
        "EssayMainTitle": ParagraphStyle(
            "EssayMainTitle",
            fontName=FONT_BOLD,
            fontSize=13,
            leading=16,
            textColor=colors.black,
            alignment=1,
            spaceAfter=6,
        ),
        "EssayInst": ParagraphStyle(
            "EssayInst",
            fontName=FONT_NORMAL,
            fontSize=7.8,
            leading=10.5,
            textColor=colors.black,
            alignment=4,
            spaceAfter=6,
        ),
        "ThemeBox": ParagraphStyle(
            "ThemeBox",
            fontName=FONT_BOLD,
            fontSize=9.2,
            leading=12.0,
            textColor=colors.black,
            alignment=1,
        ),
        "MotivatingTitle": ParagraphStyle(
            "MotivatingTitle",
            fontName=FONT_BOLD,
            fontSize=8.2,
            leading=10.5,
            textColor=colors.black,
            spaceAfter=2,
        ),
        "MotivatingBody": ParagraphStyle(
            "MotivatingBody",
            fontName=FONT_NORMAL,
            fontSize=7.4,
            leading=9.6,
            textColor=colors.HexColor("#111111"),
            alignment=4,
            spaceAfter=2,
        ),
    }
    return styles


def build_two_column_question(q, styles, col_width, area_header=None):
    """
    Constrói os flowables de uma questão em 2 colunas:
    - Se houver area_header, adiciona o banner no topo e EMBUTE dentro do KeepTogether,
      garantindo que o banner e a questão NUNCA se separem.
    - Suporta imagem com posicionamento antes da fonte (imagem -> fonte).
    - Oculta títulos de aula e citações genéricas do INEP em matemática.
    """
    elements = []

    # 1. Faixa de Área (se for o primeiro item da matéria)
    if area_header:
        elements.append(Paragraph(area_header, styles["AreaBanner"]))
        elements.append(Spacer(1, 2))

    # 2. Cabeçalho oficial: QUESTÃO XX + barra
    elements.append(QuestionHeaderFlowable(q["numero"], col_width))
    elements.append(Spacer(1, 3))

    # 3. Texto de Apoio
    texto_apoio = q.get("texto_apoio")
    is_matematica = (q.get("area", "").lower().startswith("matem") or q.get("disciplina", "").lower().startswith("matem"))

    titulo_limpo = None
    if texto_apoio and isinstance(texto_apoio, dict):
        titulo_raw = texto_apoio.get("titulo", "")
        # Em matemática, não exibe títulos de aula ou conteúdo
        if titulo_raw and not (is_matematica and any(k in titulo_raw.lower() for k in ["aula", "introdução", "conjunto", "fração", "porcentagem"])):
            if not titulo_raw.lower().startswith("item"):
                titulo_limpo = sanitize_for_reportlab(titulo_raw)

        if titulo_limpo:
            elements.append(Paragraph(titulo_limpo, styles["TextSupportTitle"]))

        if texto_apoio.get("conteudo"):
            conteudo_san = sanitize_for_reportlab(texto_apoio["conteudo"])
            elements.append(Paragraph(conteudo_san, styles["TextSupportBody"]))

    # 4. Imagem de Apoio (se houver, vem ANTES da fonte)
    img_path = q.get("imagem")
    if img_path:
        candidatos = [
            img_path,
            os.path.join(ROOT_DIR, img_path),
            os.path.join(ROOT_DIR, "simulado_2", "banco_questoes", "imagens", os.path.basename(img_path)),
            os.path.join(ROOT_DIR, "simulado_2", img_path),
        ]
        real_img_path = next((p for p in candidatos if p and os.path.exists(p)), None)
        if real_img_path:
            try:
                rl_img = RLImage(real_img_path)
                max_w = col_width * 0.96
                aspect = rl_img.imageHeight / float(rl_img.imageWidth)
                draw_w = min(max_w, rl_img.imageWidth * 0.70)
                draw_h = draw_w * aspect
                # Limite de altura máxima para não estourar a coluna
                if draw_h > 120:
                    draw_h = 120
                    draw_w = draw_h / aspect
                rl_img.drawWidth = draw_w
                rl_img.drawHeight = draw_h
                elements.append(rl_img)
                elements.append(Spacer(1, 2))
            except Exception:
                pass

    # 5. Fonte / Citação (fica DEPOIS da imagem ou ao final do texto)
    if texto_apoio and isinstance(texto_apoio, dict) and texto_apoio.get("fonte"):
        fonte_raw = texto_apoio["fonte"].strip()
        # Não exibe citações artificiais ao INEP em matemática
        is_artificial_inep = ("instituto nacional de estudos" in fonte_raw.lower() or "inep" in fonte_raw.lower()) and is_matematica
        if not is_artificial_inep and len(fonte_raw) > 2:
            fonte_san = sanitize_for_reportlab(fonte_raw)
            elements.append(Paragraph(fonte_san, styles["TextSupportSource"]))

    # 6. Enunciado (Prompt)
    enun_san = sanitize_for_reportlab(q.get("enunciado", ""))
    elements.append(Paragraph(enun_san, styles["QuestionPrompt"]))
    elements.append(Spacer(1, 2))

    # 7. Alternativas de A a E
    alts = q.get("alternativas") or q.get("alts") or {}
    table_data = []
    badge_w = 16.0
    text_w = col_width - badge_w

    for letter in ["A", "B", "C", "D", "E"]:
        alt_raw = alts.get(letter, "")
        alt_san = sanitize_for_reportlab(alt_raw)
        badge = AlternativeBadgeFlowable(letter)
        para = Paragraph(alt_san, styles["AlternativeText"])
        table_data.append([badge, para])

    t = Table(table_data, colWidths=[badge_w, text_w])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 7))

    return KeepTogether(elements)


def gerar_prova_pdf(caminho_questoes="simulado_2/banco_questoes/questoes.json", caminho_saida="simulado_2/resultado/Caderno_Questoes_70Q.pdf"):
    """
    Gera o Caderno de Questões Oficial do 2º Simulado em PDF:
    - Capa oficial elegante com alto contraste.
    - Linguagens (Q01 a Q16) e Humanas (Q17 a Q32) em 2 colunas.
    - PROPOSTA DE REDAÇÃO + FOLHA DE RASCUNHO posicionadas estritamente no MEIO da prova.
    - Natureza (Q33 a Q50) e Matemática (Q51 a Q70) em 2 colunas.
    """
    with open(caminho_questoes, "r", encoding="utf-8") as f:
        dados = json.load(f)

    metadados = dados.get("metadados", {})
    redacao = dados.get("redacao", {})
    questoes = dados.get("questoes", [])

    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)

    doc = BaseDocTemplate(
        caminho_saida,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM
    )
    doc.metadados = metadados

    # Frame para a Capa (Página 1)
    frame_cover = Frame(MARGIN_LEFT, MARGIN_BOTTOM, USABLE_W, USABLE_H, id='cover_frame')

    # Frames para as 2 Colunas das Questões
    frame_col1 = Frame(
        MARGIN_LEFT, MARGIN_BOTTOM, COL_W, USABLE_H,
        id='col1', leftPadding=0, rightPadding=5, topPadding=0, bottomPadding=0
    )
    frame_col2 = Frame(
        MARGIN_LEFT + COL_W + GUTTER, MARGIN_BOTTOM, COL_W, USABLE_H,
        id='col2', leftPadding=5, rightPadding=0, topPadding=0, bottomPadding=0
    )

    # Frame amplo de coluna única para a Proposta de Redação e Rascunho
    frame_single = Frame(
        MARGIN_LEFT, MARGIN_BOTTOM, USABLE_W, USABLE_H,
        id='single_frame', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )

    template_cover = PageTemplate(id='Cover', frames=frame_cover, onPage=draw_cover_background)
    template_two_col = PageTemplate(id='TwoCol', frames=[frame_col1, frame_col2], onPage=draw_two_column_decorations)
    template_single = PageTemplate(id='Single', frames=frame_single, onPage=draw_single_column_decorations)

    doc.addPageTemplates([template_cover, template_two_col, template_single])

    styles = get_two_column_styles()
    story = []

    # 1. Página 1: Capa Oficial
    story.append(NextPageTemplate('TwoCol'))
    story.append(PageBreak())

    # Mapas de cabeçalhos de área por questão inicial
    area_headers = {
        1: "LINGUAGENS, CÓDIGOS E SUAS TECNOLOGIAS • QUESTÕES DE 01 A 16",
        17: "CIÊNCIAS HUMANAS E SUAS TECNOLOGIAS • QUESTÕES DE 17 A 32",
        33: "CIÊNCIAS DA NATUREZA E SUAS TECNOLOGIAS • QUESTÕES DE 33 A 50",
        51: "MATEMÁTICA E SUAS TECNOLOGIAS • QUESTÕES DE 51 A 70",
    }

    # 2. Questões de 1 a 70 intercalando a Redação após a Questão 32
    for q in questoes:
        q_num = q["numero"]
        header_text = area_headers.get(q_num)

        # Adiciona a questão em 2 colunas (com o banner incorporado se for a 1ª da área)
        story.append(build_two_column_question(q, styles, COL_W, area_header=header_text))

        # Quando termina Ciências Humanas (Q32), insere a PROPOSTA DE REDAÇÃO e RASCUNHO no meio da prova!
        if q_num == 32 and redacao:
            story.append(NextPageTemplate('Single'))
            story.append(PageBreak())

            # --- PÁGINA DA PROPOSTA DE REDAÇÃO ---
            story.append(Paragraph("PROPOSTA DE REDAÇÃO", styles["EssayMainTitle"]))

            tema = redacao.get("tema", "A urgência para a inclusão de pessoas neurodiversas no Brasil")
            inst_geral = redacao.get("instrucoes", "")
            texto_inst_full = (
                f"{sanitize_for_reportlab(inst_geral)}<br/><br/>"
                f"<b>PROPOSTA DE REDAÇÃO: &ldquo;{tema.upper()}&rdquo;</b>"
            )
            story.append(Paragraph(texto_inst_full, styles["EssayInst"]))
            story.append(Spacer(1, 4))

            # Caixa destacada do Tema
            theme_table = Table([[Paragraph(f"TEMA: <b>{tema.upper()}</b>", styles["ThemeBox"])]], colWidths=[USABLE_W])
            theme_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EEEEEE")),
                ('BOX', (0, 0), (-1, -1), 1.0, colors.black),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(theme_table)
            story.append(Spacer(1, 6))

            # Textos Motivadores (I a IV)
            for t in redacao.get("textos_motivadores", []):
                card_content = []
                card_content.append(Paragraph(sanitize_for_reportlab(t.get("titulo", "TEXTO")), styles["MotivatingTitle"]))

                # Imagem do motivador (se houver)
                t_img = t.get("imagem")
                if t_img:
                    cand_paths = [t_img, os.path.join(ROOT_DIR, t_img)]
                    real_t_img = next((p for p in cand_paths if os.path.exists(p)), None)
                    if real_t_img:
                        try:
                            rl_mot_img = RLImage(real_t_img)
                            aspect_mot = rl_mot_img.imageHeight / float(rl_mot_img.imageWidth)
                            max_mot_w = min(USABLE_W - 30, 240.0)
                            rl_mot_img.drawWidth = max_mot_w
                            rl_mot_img.drawHeight = max_mot_w * aspect_mot
                            if rl_mot_img.drawHeight > 130:
                                rl_mot_img.drawHeight = 130
                                rl_mot_img.drawWidth = 130 / aspect_mot
                            card_content.append(rl_mot_img)
                            card_content.append(Spacer(1, 2))
                        except Exception:
                            pass

                if t.get("conteudo"):
                    card_content.append(Paragraph(sanitize_for_reportlab(t["conteudo"]), styles["MotivatingBody"]))

                if t.get("fonte"):
                    card_content.append(Paragraph(sanitize_for_reportlab(t["fonte"]), styles["TextSupportSource"]))

                card_table = Table([[card_content]], colWidths=[USABLE_W])
                card_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FAFAFA")),
                    ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor("#CCCCCC")),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))
                story.append(card_table)
                story.append(Spacer(1, 4))

            # --- PÁGINA DA FOLHA DE RASCUNHO DA REDAÇÃO ---
            story.append(PageBreak())
            story.append(Paragraph("FOLHA DE RASCUNHO DA REDAÇÃO", styles["EssayMainTitle"]))

            inst_rascunho_completa = (
                "<b>INSTRUÇÕES PARA O RASCUNHO DA REDAÇÃO:</b><br/>"
                "1. O rascunho da redação deve ser feito exclusivamente no espaço pautado a seguir.<br/>"
                "2. O texto definitivo DEVE ser transcrito a caneta preta na FOLHA DE REDAÇÃO oficial (até 30 linhas).<br/>"
                "3. A redação que apresentar cópia dos textos da Proposta terá o número de linhas copiadas desconsiderado.<br/>"
                "4. <b>Receberá nota zero a redação que:</b> tiver até 7 linhas escritas; fugir ao tema proposto ou não atender "
                "ao padrão dissertativo-argumentativo; apresentar parte deliberadamente desconectada do tema; ou contiver "
                "qualquer identificação (nome, assinatura ou rubrica) fora do campo oficial."
            )
            story.append(Paragraph(inst_rascunho_completa, styles["EssayInst"]))
            story.append(Spacer(1, 4))
            story.append(DraftWatermarkFlowable(USABLE_W, height=520))

            # Retorna para o template de 2 colunas para continuar com Natureza e Matemática
            story.append(NextPageTemplate('TwoCol'))
            story.append(PageBreak())

    doc.build(story)
    print(f"[OK] Caderno de Prova Oficial (70Q + Redacao no meio) gerado em: {caminho_saida}")


if __name__ == "__main__":
    gerar_prova_pdf()
