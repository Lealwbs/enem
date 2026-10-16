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
    PageBreak, KeepTogether, Image as RLImage, Flowable, NextPageTemplate, FrameBreak
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
        from reportlab.pdfbase.pdfmetrics import registerFontFamily
        registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-Bold")
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
    """Desenha a bolinha vazada alinhada exatamente com a caixa alta da primeira linha de texto."""
    def __init__(self, letter):
        super().__init__()
        self.letter = letter
        self.width = 12.6
        self.height = 9.5

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        cx = 4.6
        cy = 4.8
        r = 4.4
        self.canv.setStrokeColor(colors.black)
        self.canv.setLineWidth(0.7)
        self.canv.setFillColor(colors.white)
        self.canv.circle(cx, cy, r, fill=1, stroke=1)
        self.canv.setFont(FONT_BOLD, 6.0)
        self.canv.setFillColor(colors.black)
        self.canv.drawCentredString(cx, cy - 2.1, self.letter)
        self.canv.restoreState()


class HRFlowable(Flowable):
    """Linha horizontal divisória com largura e espessura configuráveis."""
    def __init__(self, width, thickness=0.8, color=colors.black):
        super().__init__()
        self.width = width
        self.thickness = thickness
        self.color = color
        self.height = thickness + 4

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 2, self.width, 2)
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
    - Topo com código de barras simulado |||||| | |||||||| |||| | ||||| 01 centralizado
    - CADERNO 1 | BRANCO à esquerda e SIMULADO UNIFICADO à direita
    - Título refinado: 2º SIMULADO UNIFICADO COLETIVO VOA VOA & PREPARATÓRIO GABARITA
    - 4 linhas de subtítulo oficiais completas
    - Instruções oficiais completas com o aviso explícito de caneta preta obrigatória
    """
    canv.saveState()
    metadados = getattr(doc, "metadados", {})

    # Moldura externa segura para impressão
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(1.4)
    canv.rect(MARGIN_LEFT - 4, MARGIN_BOTTOM - 4, USABLE_W + 8, USABLE_H + 8, fill=0, stroke=1)
    canv.setLineWidth(0.6)
    canv.rect(MARGIN_LEFT - 1, MARGIN_BOTTOM - 1, USABLE_W + 2, USABLE_H + 2, fill=0, stroke=1)

    # Topo da Capa: Identificação limpa com código de barras simulado
    top_y = PAGE_H - MARGIN_TOP + 12
    canv.setFont(FONT_BOLD, 8.8)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT + 6, top_y, "CADERNO 1 | BRANCO")

    canv.setFont("Courier-Bold", 10.0)
    canv.drawCentredString(PAGE_W / 2.0, top_y, "|||||| | |||||||| |||| | ||||| 01")

    canv.setFont(FONT_BOLD, 8.8)
    canv.drawRightString(PAGE_W - MARGIN_RIGHT - 6, top_y, "SIMULADO UNIFICADO")

    canv.setStrokeColor(colors.black)
    canv.setLineWidth(0.8)
    canv.line(MARGIN_LEFT + 4, top_y - 6, PAGE_W - MARGIN_RIGHT - 4, top_y - 6)

    # Título Institucional Superior
    canv.setFont(FONT_BOLD, 15)
    canv.setFillColor(colors.black)
    canv.drawCentredString(PAGE_W / 2.0, PAGE_H - 58, "2º SIMULADO UNIFICADO")

    canv.setFont(FONT_BOLD, 10.8)
    canv.setFillColor(colors.HexColor("#222222"))
    canv.drawCentredString(PAGE_W / 2.0, PAGE_H - 74, "COLETIVO VOA VOA & PREPARATÓRIO GABARITA")

    # 4 Linhas de Subtítulo Oficiais com maior respiro e fonte ampliada
    subtitles = [
        "PROVA DE LINGUAGENS, CÓDIGOS E SUAS TECNOLOGIAS E REDAÇÃO",
        "PROVA DE CIÊNCIAS DA NATUREZA E SUAS TECNOLOGIAS",
        "PROVA DE CIÊNCIAS HUMANAS E SUAS TECNOLOGIAS",
        "PROVA DE MATEMÁTICA E SUAS TECNOLOGIAS",
    ]
    canv.setFont(FONT_BOLD, 8.4)
    canv.setFillColor(colors.HexColor("#2b2b2b"))
    y_sub = PAGE_H - 95
    for s in subtitles:
        canv.drawCentredString(PAGE_W / 2.0, y_sub, s)
        y_sub -= 13.0

    # Espaço ampliado de respiro após "PROVA DE MATEMÁTICA E SUAS TECNOLOGIAS"
    card_h = 66
    card_y = y_sub - 18 - card_h
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(1.2)
    canv.setFillColor(colors.white)
    canv.roundRect(MARGIN_LEFT + 10, card_y, USABLE_W - 20, card_h, 5, fill=1, stroke=1)

    # Marca "enem 2026" com proximidade refinada (formando um bloco único)
    enem_x = MARGIN_LEFT + 36
    canv.setFont(FONT_BOLD, 36)
    canv.setFillColor(colors.black)
    canv.drawString(enem_x, card_y + 18, "enem")
    w_enem = canv.stringWidth("enem", FONT_BOLD, 36)

    ano = str(metadados.get("ano", "2026"))
    canv.setFont(FONT_NORMAL, 36)
    canv.setFillColor(colors.HexColor("#444444"))
    canv.drawString(enem_x + w_enem + 6, card_y + 18, ano)

    # Divisória vertical no card
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(1.2)
    canv.line(MARGIN_LEFT + USABLE_W - 130, card_y + 8, MARGIN_LEFT + USABLE_W - 130, card_y + card_h - 8)

    # Identificação do Caderno à direita do card
    canv.setFont(FONT_BOLD, 8.0)
    canv.setFillColor(colors.black)
    canv.drawCentredString(MARGIN_LEFT + USABLE_W - 70, card_y + 45, "CADERNO")
    canv.setFont(FONT_BOLD, 22)
    canv.drawCentredString(MARGIN_LEFT + USABLE_W - 70, card_y + 22, "1")
    canv.setFont(FONT_BOLD, 9.5)
    canv.drawCentredString(MARGIN_LEFT + USABLE_W - 70, card_y + 9, "BRANCO")

    # Caixa da Frase de Segurança
    frase_y = card_y - 68
    frase_h = 58
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(0.9)
    canv.roundRect(MARGIN_LEFT + 10, frase_y, USABLE_W - 20, frase_h, 4, fill=0, stroke=1)

    canv.setFont(FONT_BOLD, 7.8)
    canv.setFillColor(colors.black)
    canv.drawCentredString(PAGE_W / 2.0, frase_y + frase_h - 13, "ATENÇÃO: transcreva no espaço apropriado do seu CARTÃO-RESPOSTA,")
    canv.setFont(FONT_NORMAL, 7.8)
    canv.drawCentredString(PAGE_W / 2.0, frase_y + frase_h - 24, "com sua caligrafia usual, considerando as letras maiúsculas e minúsculas, a seguinte frase:")

    # Tarja preta com a frase de segurança
    frase = metadados.get("frase_seguranca", "A persistência constrói o conhecimento e abre caminhos para o futuro.")
    f_box_w = USABLE_W - 60
    f_box_h = 22
    f_box_x = MARGIN_LEFT + 30
    f_box_y = frase_y + 7
    canv.setFillColor(colors.black)
    canv.roundRect(f_box_x, f_box_y, f_box_w, f_box_h, 3, fill=1, stroke=0)
    canv.setFont(FONT_BOLD, 9.0)
    canv.setFillColor(colors.white)
    canv.drawCentredString(PAGE_W / 2.0, f_box_y + 6.5, frase)

    # Bloco das Instruções Oficiais Ampliado e Confortável
    inst_y = MARGIN_BOTTOM + 20
    inst_h = frase_y - inst_y - 10
    canv.setStrokeColor(colors.HexColor("#333333"))
    canv.setLineWidth(0.8)
    canv.setFillColor(colors.HexColor("#FAFAFA"))
    canv.roundRect(MARGIN_LEFT + 10, inst_y, USABLE_W - 20, inst_h, 4, fill=1, stroke=1)

    canv.setFont(FONT_BOLD, 9.8)
    canv.setFillColor(colors.black)
    canv.drawCentredString(PAGE_W / 2.0, inst_y + inst_h - 18, "LEIA ATENTAMENTE AS INSTRUÇÕES SEGUINTES:")

    instrucoes = [
        ("1. Este CADERNO DE QUESTÕES contém 70 questões numeradas de 01 a 70 e a Proposta de Redação,", True),
        ("   dispostas da seguinte maneira:", True),
        ("   a) questões de número 01 a 16, relativas à área de Linguagens, Códigos e suas Tecnologias;", False),
        ("      ATENÇÃO: as questões de 01 a 05 são relativas à Língua Inglesa.", False),
        ("   b) questões de número 17 a 32, relativas à área de Ciências Humanas e suas Tecnologias;", False),
        ("   c) questões de número 33 a 50, relativas à área de Ciências da Natureza e suas Tecnologias;", False),
        ("   d) questões de número 51 a 70, relativas à área de Matemática e suas Tecnologias;", False),
        ("   e) Proposta de Redação e Folha de Rascunho da Redação ao final deste caderno,", False),
        ("      e Folha de Redação Definitiva e Cartão-Resposta em folhas avulsas.", False),
        ("2. Confira se a quantidade e a ordem das questões deste caderno estão de acordo com as instruções.", True),
        ("3. Preencha o CARTÃO-RESPOSTA e a FOLHA DE REDAÇÃO exclusivamente com caneta esferográfica de", True),
        ("   tinta PRETA (tubo transparente). É ESTRITAMENTE PROIBIDO O USO DE CANETA AZUL,", False),
        ("   lápis, borracha ou corretivo líquido/fita.", False),
        ("4. Para cada uma das questões objetivas, são apresentadas 5 alternativas. Apenas uma responde corretamente.", True),
        ("5. O tempo disponível para a realização das 70 questões e da proposta de redação é de cinco horas.", True),
        ("6. Reserve tempo suficiente para preencher o CARTÃO-RESPOSTA e a FOLHA DE REDAÇÃO definitiva.", True),
        ("   Os rascunhos e marcações neste caderno NÃO serão considerados na avaliação.", False),
        ("7. Quando terminar as provas, entregue ao aplicador o CARTÃO-RESPOSTA e a FOLHA DE REDAÇÃO.", True),
        ("   Você poderá levar este CADERNO DE QUESTÕES para casa ao término da prova.", False),
    ]

    curr_y = inst_y + inst_h - 35
    for linha, is_title in instrucoes:
        if is_title:
            curr_y -= 5.5
            canv.setFont(FONT_BOLD, 7.8)
            canv.setFillColor(colors.black)
        else:
            canv.setFont(FONT_NORMAL, 7.5)
            canv.setFillColor(colors.HexColor("#222222"))
        canv.drawString(MARGIN_LEFT + 20, curr_y, linha)
        curr_y -= 12.2

    # Rodapé da Capa
    footer_y = MARGIN_BOTTOM + 5.0
    canv.setFont(FONT_BOLD, 7.8)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT + 6, footer_y, "COLETIVO VOA VOA • PREPARATÓRIO GABARITA")
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
    """Decorações da folha de rascunho de redação (coluna única)."""
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
    canv.drawRightString(PAGE_W - MARGIN_RIGHT, header_y + 2, "CADERNO 1 | BRANCO")

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


def draw_redacao_page_decorations(canv, doc):
    """Decorações da página oficial de Proposta de Redação (estilo ENEM oficial)."""
    canv.saveState()
    page_num = canv.getPageNumber()

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
    canv.drawRightString(PAGE_W - MARGIN_RIGHT, header_y + 2, "PROPOSTA DE REDAÇÃO • CADERNO BRANCO")

    canv.setStrokeColor(colors.black)
    canv.setLineWidth(0.8)
    canv.line(MARGIN_LEFT, header_y - 4, PAGE_W - MARGIN_RIGHT, header_y - 4)

    # Linha divisória vertical apenas entre as duas colunas inferiores (abaixo da área de cabeçalho da proposta)
    x_sep = MARGIN_LEFT + COL_W + (GUTTER / 2.0)
    canv.setStrokeColor(colors.HexColor("#bbbbbb"))
    canv.setLineWidth(0.6)
    canv.line(x_sep, MARGIN_BOTTOM, x_sep, PAGE_H - MARGIN_TOP - 74)

    # Rodapé Padronizado
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
            fontSize=8.2,
            leading=10.8,
            textColor=colors.black,
            backColor=colors.HexColor("#EEEEEE"),
            borderPadding=(4, 6, 4, 6),
            spaceAfter=5,
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
        "EnglishBody": ParagraphStyle(
            "EnglishBody",
            fontName=FONT_NORMAL,
            fontSize=7.2,
            leading=8.8,
            textColor=colors.HexColor("#111111"),
            alignment=4,
            spaceAfter=2,
        ),
        "EnglishPrompt": ParagraphStyle(
            "EnglishPrompt",
            fontName=FONT_NORMAL,
            fontSize=7.4,
            leading=9.2,
            textColor=colors.black,
            alignment=4,
            spaceAfter=2,
            spaceBefore=1,
        ),
        "EnglishAlt": ParagraphStyle(
            "EnglishAlt",
            fontName=FONT_NORMAL,
            fontSize=7.2,
            leading=8.8,
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
        "EssayHeaderTitle": ParagraphStyle(
            "EssayHeaderTitle",
            fontName=FONT_BOLD,
            fontSize=11.5,
            leading=14.0,
            textColor=colors.black,
            alignment=1,
            spaceAfter=3,
        ),
        "EssayHeaderInst": ParagraphStyle(
            "EssayHeaderInst",
            fontName=FONT_NORMAL,
            fontSize=7.4,
            leading=9.8,
            textColor=colors.black,
            alignment=4,
            spaceAfter=4,
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
            fontSize=8.8,
            leading=11.2,
            textColor=colors.black,
            spaceAfter=2,
        ),
        "MotivatingBody": ParagraphStyle(
            "MotivatingBody",
            fontName=FONT_NORMAL,
            fontSize=8.0,
            leading=10.5,
            textColor=colors.HexColor("#111111"),
            alignment=4,
            spaceAfter=3,
        ),
    }
    return styles


def format_question_support_content(conteudo_raw, body_style, col_width):
    """
    Processa o texto de apoio da questão:
    - Se houver dados tabulares delimitados por '|', gera uma Table formatada padrão ENEM
      (com cabeçalho sombreado, bordas e alinhamento centralizado).
    - Para textos normais, gera parágrafos limpos.
    """
    if not conteudo_raw:
        return []

    if "|" not in conteudo_raw:
        conteudo_san = sanitize_for_reportlab(conteudo_raw)
        return [Paragraph(conteudo_san, body_style)]

    lines = [l.strip() for l in conteudo_raw.split("\n")]
    elements = []
    text_chunk = []
    table_lines = []

    def flush_text():
        if text_chunk:
            full_txt = "\n".join(text_chunk).strip()
            if full_txt:
                elements.append(Paragraph(sanitize_for_reportlab(full_txt), body_style))
                elements.append(Spacer(1, 2))
            text_chunk.clear()

    def flush_table():
        if table_lines:
            rows = []
            for r in table_lines:
                clean_r = r.strip()
                if clean_r.startswith("|"):
                    clean_r = clean_r[1:]
                if clean_r.endswith("|"):
                    clean_r = clean_r[:-1]
                cols = [c.strip() for c in clean_r.split("|")]
                # Ignora divisórias markdown tipo ---|---
                if all(set(c).issubset({"-", ":", " "}) for c in cols):
                    continue
                rows.append(cols)

            if rows:
                num_cols = max(len(r) for r in rows)
                for r in rows:
                    while len(r) < num_cols:
                        r.append("")

                hdr_style = ParagraphStyle(
                    "TblHdr",
                    fontName=FONT_BOLD,
                    fontSize=6.8,
                    leading=8.2,
                    textColor=colors.black,
                    alignment=1
                )
                cell_style = ParagraphStyle(
                    "TblCell",
                    fontName=FONT_NORMAL,
                    fontSize=6.5,
                    leading=8.0,
                    textColor=colors.HexColor("#111111"),
                    alignment=1
                )

                table_data = []
                for row_idx, r in enumerate(rows):
                    row_cells = []
                    style = hdr_style if row_idx == 0 else cell_style
                    for cell_txt in r:
                        row_cells.append(Paragraph(sanitize_for_reportlab(cell_txt), style))
                    table_data.append(row_cells)

                col_lens = []
                for c_idx in range(num_cols):
                    lens = [len(r[c_idx]) for r in rows]
                    col_lens.append(max(lens) + 6)
                total_len = max(sum(col_lens), 1)

                tbl_w = min(col_width * 0.94, 235.0)
                col_widths = [(l / total_len) * tbl_w for l in col_lens]

                t = Table(table_data, colWidths=col_widths, hAlign='CENTER')
                t.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.6, colors.HexColor("#333333")),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EEEEEE")),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 1.5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
                    ('LEFTPADDING', (0, 0), (-1, -1), 3),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                ]))
                elements.append(Spacer(1, 2))
                elements.append(t)
                elements.append(Spacer(1, 4))
            table_lines.clear()

    for line in lines:
        if "|" in line:
            flush_text()
            table_lines.append(line)
        else:
            if table_lines:
                flush_table()
            if line:
                text_chunk.append(line)

    flush_text()
    flush_table()
    return elements


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
    is_english = q.get("numero") in [1, 2, 3, 4, 5]

    body_style = styles["EnglishBody"] if is_english else styles["TextSupportBody"]
    prompt_style = styles["EnglishPrompt"] if is_english else styles["QuestionPrompt"]
    alt_style = styles["EnglishAlt"] if is_english else styles["AlternativeText"]

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
            content_flowables = format_question_support_content(
                texto_apoio["conteudo"], body_style, col_width
            )
            elements.extend(content_flowables)

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
                draw_w = max_w
                draw_h = draw_w * aspect
                # Limite de altura para a Q02 (ampliado com excelente legibilidade) ou limite geral amplo
                if q.get("numero") == 2:
                    if draw_h > 155:
                        draw_h = 155
                        draw_w = draw_h / aspect
                elif draw_h > 210:
                    draw_h = 210
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
    elements.append(Paragraph(enun_san, prompt_style))
    elements.append(Spacer(1, 2))

    # 7. Alternativas de A a E com micro-espaço refinado
    alts = q.get("alternativas") or q.get("alts") or {}
    table_data = []
    badge_w = 12.6
    text_w = col_width - badge_w

    for letter in ["A", "B", "C", "D", "E"]:
        alt_raw = alts.get(letter, "")
        alt_san = sanitize_for_reportlab(alt_raw)
        badge = AlternativeBadgeFlowable(letter)
        para = Paragraph(alt_san, alt_style)
        table_data.append([badge, para])

    t = Table(table_data, colWidths=[badge_w, text_w])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.4 if is_english else 3.8),
    ]))
    elements.append(t)
    # Espaçador compacto para as 5 de inglês caberem na pág 2
    spacer_h = 2.5 if is_english else 6.0
    elements.append(Spacer(1, spacer_h))

    return KeepTogether(elements)


def build_essay_proposal_page(redacao, styles, col_width, usable_w):
    """
    Constrói os elementos da Proposta de Redação para a página dedicada:
    1. Top Frame: Cabeçalho 'PROPOSTA DE REDAÇÃO' + instrução oficial com tema em negrito + divisória.
    2. Coluna 1: Texto I e Texto II (imagem em destaque ampliada). Sem retângulos cinzas!
    3. Coluna 2: Texto III e Texto IV (imagem ampliada). Sem retângulos cinzas!
    """
    elements = []
    tema = redacao.get("tema", "A urgência para a inclusão de pessoas neurodiversas no Brasil")

    # --- 1. TOPO DA PÁGINA (LARGURA TOTAL) ---
    elements.append(Paragraph("PROPOSTA DE REDAÇÃO", styles["EssayHeaderTitle"]))
    instrucao_com_tema = (
        "A partir da leitura dos textos motivadores e com base nos conhecimentos construídos ao longo de sua formação, "
        "redija um texto dissertativo-argumentativo em modalidade escrita formal da língua portuguesa sobre o tema "
        f"<b>&ldquo;{tema}&rdquo;</b>, apresentando proposta de intervenção que respeite os direitos humanos. "
        "Selecione, organize e relacione, de forma coerente e coesa, argumentos e fatos para a defesa de seu ponto de vista."
    )
    elements.append(Paragraph(instrucao_com_tema, styles["EssayHeaderInst"]))
    elements.append(HRFlowable(usable_w, thickness=0.8, color=colors.black))
    elements.append(FrameBreak())

    textos = redacao.get("textos_motivadores", [])

    # --- 2. COLUNA 1: TEXTO I e TEXTO II (sem retângulos cinzas) ---
    if len(textos) > 0:
        t1 = textos[0]
        elements.append(Paragraph(f"<b>{t1.get('titulo', 'TEXTO I')}</b>", styles["MotivatingTitle"]))
        if t1.get("conteudo"):
            elements.append(Paragraph(sanitize_for_reportlab(t1["conteudo"]), styles["MotivatingBody"]))
        if t1.get("fonte"):
            elements.append(Paragraph(sanitize_for_reportlab(t1["fonte"]), styles["TextSupportSource"]))
        elements.append(Spacer(1, 8))

    if len(textos) > 1:
        t2 = textos[1]
        elements.append(Paragraph(f"<b>{t2.get('titulo', 'TEXTO II')}</b>", styles["MotivatingTitle"]))
        t2_img = t2.get("imagem")
        if t2_img:
            cand = [t2_img, os.path.join(ROOT_DIR, t2_img)]
            p = next((x for x in cand if os.path.exists(x)), None)
            if p:
                try:
                    img = RLImage(p)
                    aspect = img.imageHeight / float(img.imageWidth)
                    img.drawWidth = col_width - 8
                    img.drawHeight = img.drawWidth * aspect
                    if img.drawHeight > 340:
                        img.drawHeight = 340
                        img.drawWidth = 340 / aspect
                    elements.append(img)
                    elements.append(Spacer(1, 2))
                except Exception:
                    pass
        if t2.get("fonte"):
            elements.append(Paragraph(sanitize_for_reportlab(t2["fonte"]), styles["TextSupportSource"]))

    elements.append(FrameBreak())

    # --- 3. COLUNA 2: TEXTO III e TEXTO IV (sem retângulos cinzas) ---
    if len(textos) > 2:
        t3 = textos[2]
        elements.append(Paragraph(f"<b>{t3.get('titulo', 'TEXTO III')}</b>", styles["MotivatingTitle"]))
        if t3.get("conteudo"):
            elements.append(Paragraph(sanitize_for_reportlab(t3["conteudo"]), styles["MotivatingBody"]))
        if t3.get("fonte"):
            elements.append(Paragraph(sanitize_for_reportlab(t3["fonte"]), styles["TextSupportSource"]))
        elements.append(Spacer(1, 8))

    if len(textos) > 3:
        t4 = textos[3]
        elements.append(Paragraph(f"<b>{t4.get('titulo', 'TEXTO IV')}</b>", styles["MotivatingTitle"]))
        t4_img = t4.get("imagem")
        if t4_img:
            cand = [t4_img, os.path.join(ROOT_DIR, t4_img)]
            p = next((x for x in cand if os.path.exists(x)), None)
            if p:
                try:
                    img = RLImage(p)
                    aspect = img.imageHeight / float(img.imageWidth)
                    img.drawWidth = col_width - 8
                    img.drawHeight = img.drawWidth * aspect
                    if img.drawHeight > 165:
                        img.drawHeight = 165
                        img.drawWidth = 165 / aspect
                    elements.append(img)
                    elements.append(Spacer(1, 2))
                except Exception:
                    pass
        if t4.get("conteudo"):
            elements.append(Paragraph(sanitize_for_reportlab(t4["conteudo"]), styles["MotivatingBody"]))
        if t4.get("fonte"):
            elements.append(Paragraph(sanitize_for_reportlab(t4["fonte"]), styles["TextSupportSource"]))

    return elements


def gerar_prova_pdf(caminho_questoes="simulado_2/banco_questoes/questoes.json", caminho_saida="simulado_2/resultado/Caderno_Questoes.pdf"):
    """
    Gera o Caderno de Questões Oficial do 2º Simulado em PDF:
    - Capa oficial elegante com alto contraste e instruções padronizadas.
    - Linguagens (Q01 a Q16), Humanas (Q17 a Q32), Natureza (Q33 a Q50) e Matemática (Q51 a Q70) em 2 colunas.
    - PROPOSTA DE REDAÇÃO logo antes da Folha de Rascunho.
    - FOLHA DE RASCUNHO DA REDAÇÃO no final do caderno (última página).
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

    # Frames para a Página de Proposta de Redação (Topo de largura total + 2 colunas)
    red_top_h = 70.0
    frame_red_top = Frame(
        MARGIN_LEFT, PAGE_H - MARGIN_TOP - red_top_h, USABLE_W, red_top_h,
        id='red_top', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )
    frame_red_col1 = Frame(
        MARGIN_LEFT, MARGIN_BOTTOM, COL_W, USABLE_H - red_top_h - 6,
        id='red_col1', leftPadding=0, rightPadding=5, topPadding=4, bottomPadding=0
    )
    frame_red_col2 = Frame(
        MARGIN_LEFT + COL_W + GUTTER, MARGIN_BOTTOM, COL_W, USABLE_H - red_top_h - 6,
        id='red_col2', leftPadding=5, rightPadding=0, topPadding=4, bottomPadding=0
    )

    # Frame amplo de coluna única para a Folha de Rascunho
    frame_single = Frame(
        MARGIN_LEFT, MARGIN_BOTTOM, USABLE_W, USABLE_H,
        id='single_frame', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )

    template_cover = PageTemplate(id='Cover', frames=frame_cover, onPage=draw_cover_background)
    template_two_col = PageTemplate(id='TwoCol', frames=[frame_col1, frame_col2], onPage=draw_two_column_decorations)
    template_redacao = PageTemplate(id='RedacaoProposal', frames=[frame_red_top, frame_red_col1, frame_red_col2], onPage=draw_redacao_page_decorations)
    template_single = PageTemplate(id='Single', frames=frame_single, onPage=draw_single_column_decorations)

    doc.addPageTemplates([template_cover, template_two_col, template_redacao, template_single])

    styles = get_two_column_styles()
    story = []

    # 1. Página 1: Capa Oficial
    story.append(NextPageTemplate('TwoCol'))
    story.append(PageBreak())

    # Mapas de cabeçalhos de área por questão inicial (2 linhas: nome da área em cima, questões embaixo)
    area_headers = {
        1: "<b>LINGUAGENS, CÓDIGOS E SUAS TECNOLOGIAS</b><br/><font size=6.8 color='#333333'><b>QUESTÕES DE 01 A 16</b> (01 a 05: Língua Inglesa)</font>",
        17: "<b>CIÊNCIAS HUMANAS E SUAS TECNOLOGIAS</b><br/><font size=6.8 color='#333333'><b>QUESTÕES DE 17 A 32</b></font>",
        33: "<b>CIÊNCIAS DA NATUREZA E SUAS TECNOLOGIAS</b><br/><font size=6.8 color='#333333'><b>QUESTÕES DE 33 A 50</b></font>",
        51: "<b>MATEMÁTICA E SUAS TECNOLOGIAS</b><br/><font size=6.8 color='#333333'><b>QUESTÕES DE 51 A 70</b></font>",
    }

    # 2. Questões de 1 a 70
    for q in questoes:
        q_num = q["numero"]
        header_text = area_headers.get(q_num)

        # Adiciona a questão em 2 colunas
        story.append(build_two_column_question(q, styles, COL_W, area_header=header_text))

        # As primeiras 5 questões (Inglês) ficam na Página 2; Q06 inicia na Página 3
        if q_num == 5:
            story.append(PageBreak())

    # 3. PROPOSTA DE REDAÇÃO logo antes da Folha de Rascunho da Redação
    if redacao:
        story.append(NextPageTemplate('RedacaoProposal'))
        story.append(PageBreak())
        story.extend(build_essay_proposal_page(redacao, styles, COL_W, USABLE_W))

    # 4. FOLHA DE RASCUNHO DA REDAÇÃO no FINAL da prova, estilo ENEM oficial!
    if redacao:
        story.append(NextPageTemplate('Single'))
        story.append(PageBreak())
        story.append(Paragraph("FOLHA DE RASCUNHO DA REDAÇÃO", styles["EssayMainTitle"]))

        inst_rascunho = (
            "<b>INSTRUÇÕES PARA O RASCUNHO DA REDAÇÃO:</b><br/>"
            "1. O rascunho da redação deve ser feito exclusivamente no espaço pautado a seguir.<br/>"
            "2. O texto definitivo DEVE ser transcrito a caneta preta na FOLHA DE REDAÇÃO oficial (até 30 linhas).<br/>"
            "3. A redação que apresentar cópia dos textos da Proposta terá o número de linhas copiadas desconsiderado.<br/>"
            "4. <b>Receberá nota zero a redação que:</b> tiver até 7 linhas escritas; fugir ao tema proposto ou não atender "
            "ao padrão dissertativo-argumentativo; apresentar parte deliberadamente desconectada do tema; ou contiver "
            "qualquer identificação fora do campo oficial."
        )
        story.append(Paragraph(inst_rascunho, styles["EssayInst"]))
        story.append(Spacer(1, 4))
        story.append(DraftWatermarkFlowable(USABLE_W, height=530))

    doc.build(story)
    print(f"[OK] Caderno de Prova Oficial gerado em: {caminho_saida}")


if __name__ == "__main__":
    gerar_prova_pdf()
