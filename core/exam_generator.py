"""
Gerador de Caderno de Prova Completo em PDF - Caderno Branco (Padrão ENEM 2 Colunas).
Otimizado para impressão em Preto e Branco:
- Layout obrigatório em 2 colunas com linha divisória vertical oficial.
- Capa Oficial de alto contraste (Caderno Branco) com frase de segurança e instruções 1 a 9.
- Margens seguras de impressão (36pt) para evitar corte de conteúdo.
- Cabeçalhos limpos sem códigos de barras aleatórios ou identificadores artificiais como '(Item XX)'.
- Formatação compacta para economizar folhas.
- Proposta de Redação e Folha de Rascunho posicionadas estritamente ao final das 70 questões.
"""

import os
import sys
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image as RLImage, Flowable, FrameBreak, NextPageTemplate
)
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = A4
MARGIN_LEFT = 36.0
MARGIN_RIGHT = 36.0
MARGIN_TOP = 42.0
MARGIN_BOTTOM = 38.0
GUTTER = 16.0

USABLE_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
USABLE_H = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM
COL_W = (USABLE_W - GUTTER) / 2.0


class QuestionHeaderFlowable(Flowable):
    """Desenha 'QUESTÃO XX' seguido da barra horizontal no estilo oficial do ENEM."""
    def __init__(self, q_num, width):
        super().__init__()
        self.q_num = q_num
        self.width = width
        self.height = 15

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setFont("Helvetica-Bold", 9.5)
        self.canv.setFillColor(colors.black)
        txt = f"QUESTÃO {self.q_num:02d}"
        self.canv.drawString(0, 3, txt)
        txt_w = self.canv.stringWidth(txt, "Helvetica-Bold", 9.5)

        bar_start_x = txt_w + 8
        bar_w = self.width - bar_start_x
        if bar_w > 10:
            # Barra dupla elegante em escala de cinza/preto para impressão P&B
            self.canv.setFillColor(colors.HexColor("#777777"))
            self.canv.rect(bar_start_x, bar_y := 4.5, bar_w * 0.70, 2.5, fill=1, stroke=0)
            self.canv.setFillColor(colors.black)
            self.canv.rect(bar_start_x + bar_w * 0.70, bar_y, bar_w * 0.30, 2.5, fill=1, stroke=0)
        self.canv.restoreState()


class AlternativeBadgeFlowable(Flowable):
    """Desenha a bolinha preta com a letra branca em negrito (A, B, C, D, E)."""
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
        self.canv.setFillColor(colors.black)
        self.canv.circle(cx, cy, r, fill=1, stroke=0)
        self.canv.setFont("Helvetica-Bold", 6.8)
        self.canv.setFillColor(colors.white)
        self.canv.drawCentredString(cx, cy - 2.2, self.letter)
        self.canv.restoreState()


class DraftWatermarkFlowable(Flowable):
    """Desenha as 30 linhas de rascunho com marca d'água 'RASCUNHO DA REDAÇÃO'."""
    def __init__(self, width, height=560):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()

        # Marca d'água diagonal em tom cinza muito claro
        self.canv.saveState()
        self.canv.translate(self.width / 2.0, self.height / 2.0)
        self.canv.rotate(35)
        self.canv.setFont("Helvetica-Bold", 38)
        self.canv.setFillColor(colors.HexColor("#f0f0f0"))
        self.canv.drawCentredString(0, 0, "RASCUNHO DA REDAÇÃO")
        self.canv.restoreState()

        # Grade de 30 linhas
        num_lines = 30
        line_h = self.height / float(num_lines)
        num_w = 20.0

        # Borda externa preta
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

            self.canv.setFont("Helvetica-Bold", 7.5)
            self.canv.setFillColor(colors.black)
            self.canv.drawCentredString(num_w / 2.0, y + 4.5, str(i + 1))

        self.canv.restoreState()


def draw_cover_background(canv, doc):
    """Desenha a Capa Oficial do Caderno Branco com alto contraste e design limpo."""
    canv.saveState()
    metadados = getattr(doc, "metadados", {})

    # Borda dupla externa oficial na folha
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(1.5)
    canv.rect(MARGIN_LEFT - 10, MARGIN_BOTTOM - 10, USABLE_W + 20, USABLE_H + 20, fill=0, stroke=1)
    canv.setLineWidth(0.6)
    canv.rect(MARGIN_LEFT - 6, MARGIN_BOTTOM - 6, USABLE_W + 12, USABLE_H + 12, fill=0, stroke=1)

    # Topo da Capa: Caderno e Dia
    canv.setFont("Helvetica-Bold", 11)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT, PAGE_H - 32, "CADERNO 1 | BRANCO")

    # Badge do Dia (lado direito)
    badge_x = PAGE_W - MARGIN_RIGHT - 80
    badge_y = PAGE_H - 36
    canv.setFillColor(colors.black)
    canv.roundRect(badge_x, badge_y, 80, 24, 4, fill=1, stroke=0)
    canv.setFont("Helvetica-Bold", 12)
    canv.setFillColor(colors.white)
    canv.drawCentredString(badge_x + 40, badge_y + 7, metadados.get("dia", "1º DIA"))

    # Título principal do exame
    canv.setFont("Helvetica-Bold", 18)
    canv.setFillColor(colors.black)
    canv.drawCentredString(PAGE_W / 2.0, PAGE_H - 72, metadados.get("titulo_exame", "EXAME NACIONAL DO ENSINO MÉDIO"))

    # Subtítulo das provas
    canv.setFont("Helvetica-Bold", 9)
    canv.setFillColor(colors.HexColor("#333333"))
    canv.drawCentredString(PAGE_W / 2.0, PAGE_H - 90, "PROVA DE LINGUAGENS, CÓDIGOS E SUAS TECNOLOGIAS E REDAÇÃO")
    canv.drawCentredString(PAGE_W / 2.0, PAGE_H - 103, "PROVA DE CIÊNCIAS HUMANAS, NATUREZA E MATEMÁTICA")

    # Card ENEM Central em Alto Contraste
    card_y = PAGE_H - 195
    card_h = 75
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(1.2)
    canv.setFillColor(colors.white)
    canv.roundRect(MARGIN_LEFT, card_y, USABLE_W, card_h, 6, fill=1, stroke=1)

    canv.setFont("Helvetica-Bold", 42)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT + 30, card_y + 20, "enem")

    ano = str(metadados.get("ano", "2026"))
    canv.setFont("Helvetica", 42)
    canv.setFillColor(colors.HexColor("#444444"))
    canv.drawString(MARGIN_LEFT + 155, card_y + 20, ano)

    # Divisória no card
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(1.5)
    canv.line(MARGIN_LEFT + USABLE_W - 120, card_y + 10, MARGIN_LEFT + USABLE_W - 120, card_y + card_h - 10)

    # Caderno Branco
    canv.setFont("Helvetica-Bold", 8.5)
    canv.setFillColor(colors.black)
    canv.drawCentredString(MARGIN_LEFT + USABLE_W - 60, card_y + 52, "CADERNO")
    canv.setFont("Helvetica-Bold", 24)
    canv.drawCentredString(MARGIN_LEFT + USABLE_W - 60, card_y + 26, "1")
    canv.setFont("Helvetica-Bold", 10.5)
    canv.drawCentredString(MARGIN_LEFT + USABLE_W - 60, card_y + 12, "BRANCO")

    # Caixa da Frase de Segurança
    frase_y = card_y - 82
    frase_h = 70
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(1.0)
    canv.roundRect(MARGIN_LEFT, frase_y, USABLE_W, frase_h, 4, fill=0, stroke=1)

    canv.setFont("Helvetica-Bold", 8)
    canv.setFillColor(colors.black)
    canv.drawCentredString(PAGE_W / 2.0, frase_y + frase_h - 15, "ATENÇÃO: transcreva no espaço apropriado do seu CARTÃO-RESPOSTA,")
    canv.drawString(MARGIN_LEFT + 25, frase_y + frase_h - 26, "com sua caligrafia usual, considerando as letras maiúsculas e minúsculas, a seguinte frase:")

    # Tarja com a frase
    frase = metadados.get("frase_seguranca", "A inclusão e a solidariedade transformam o mundo")
    f_box_w = USABLE_W - 40
    f_box_h = 24
    f_box_x = MARGIN_LEFT + 20
    f_box_y = frase_y + 10
    canv.setFillColor(colors.black)
    canv.roundRect(f_box_x, f_box_y, f_box_w, f_box_h, 3, fill=1, stroke=0)
    canv.setFont("Helvetica-Bold", 9.5)
    canv.setFillColor(colors.white)
    canv.drawCentredString(PAGE_W / 2.0, f_box_y + 7.5, frase)

    # Bloco das Instruções Oficiais
    inst_y = MARGIN_BOTTOM + 35
    inst_h = frase_y - inst_y - 12
    canv.setStrokeColor(colors.HexColor("#333333"))
    canv.setLineWidth(0.8)
    canv.setFillColor(colors.HexColor("#fafafa"))
    canv.roundRect(MARGIN_LEFT, inst_y, USABLE_W, inst_h, 4, fill=1, stroke=1)

    canv.setFont("Helvetica-Bold", 10)
    canv.setFillColor(colors.black)
    canv.drawCentredString(PAGE_W / 2.0, inst_y + inst_h - 18, "LEIA ATENTAMENTE AS INSTRUÇÕES SEGUINTES:")

    instrucoes = [
        "1. Este CADERNO DE QUESTÕES contém 70 questões objetivas e a Proposta de Redação ao final.",
        "2. As questões estão numeradas de 01 a 70 e divididas entre as grandes áreas do conhecimento.",
        "3. Para cada questão objetiva, são apresentadas 5 alternativas (A, B, C, D e E). Apenas uma é correta.",
        f"4. O tempo total disponível para a realização desta prova é de {metadados.get('tempo_prova', 'cinco horas')}.",
        "5. Reserve os minutos finais para preencher com caneta preta o CARTÃO-RESPOSTA e a FOLHA DE REDAÇÃO.",
        "6. Marcações ou anotações feitas neste caderno de questões NÃO serão consideradas na nota oficial.",
        "7. Somente serão corrigidas as redações transcritas na FOLHA DE REDAÇÃO definitiva.",
        "8. Ao terminar a prova, entregue ao aplicador este CADERNO, o CARTÃO-RESPOSTA e a FOLHA DE REDAÇÃO.",
        "9. A folha de rascunho da redação encontra-se após a proposta de redação no término deste caderno."
    ]

    curr_y = inst_y + inst_h - 36
    canv.setFont("Helvetica", 7.8)
    canv.setFillColor(colors.black)
    for linha in instrucoes:
        is_bold = linha.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9."))
        if is_bold:
            canv.setFont("Helvetica-Bold", 8.0)
            curr_y -= 4
        else:
            canv.setFont("Helvetica", 7.6)
        canv.drawString(MARGIN_LEFT + 14, curr_y, linha)
        curr_y -= 15.0

    # Rodapé da Capa
    footer_y = MARGIN_BOTTOM - 2
    canv.setFont("Helvetica-Bold", 8)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT, footer_y, "SIMULADO COLETIVO • CADERNO BRANCO")
    canv.drawRightString(PAGE_W - MARGIN_RIGHT, footer_y, "MODELO OFICIAL ENEM • 70 QUESTÕES")

    canv.restoreState()


def draw_two_column_decorations(canv, doc):
    """
    Desenha o cabeçalho, rodapé e a linha divisória vertical entre as duas colunas,
    exatamente como na diagramação oficial do ENEM.
    """
    canv.saveState()
    page_num = canv.getPageNumber()

    # Linha vertical divisória entre as 2 colunas
    x_sep = MARGIN_LEFT + COL_W + (GUTTER / 2.0)
    canv.setStrokeColor(colors.HexColor("#bbbbbb"))
    canv.setLineWidth(0.6)
    canv.line(x_sep, MARGIN_BOTTOM, x_sep, PAGE_H - MARGIN_TOP)

    # Cabeçalho Superior Limpo (sem códigos aleatórios de barras)
    header_y = PAGE_H - MARGIN_TOP + 8

    # Logo ENEM estilizado à esquerda
    canv.setFont("Helvetica-Bold", 11)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT, header_y + 2, "enem")
    canv.setFont("Helvetica", 11)
    canv.setFillColor(colors.HexColor("#555555"))
    canv.drawString(MARGIN_LEFT + 32, header_y + 2, "2026")

    # Identificação do caderno à direita
    canv.setFont("Helvetica-Bold", 8)
    canv.setFillColor(colors.black)
    canv.drawRightString(PAGE_W - MARGIN_RIGHT, header_y + 2, "CADERNO 1 | BRANCO")

    # Linha horizontal sob o cabeçalho
    canv.setStrokeColor(colors.black)
    canv.setLineWidth(0.8)
    canv.line(MARGIN_LEFT, header_y - 4, PAGE_W - MARGIN_RIGHT, header_y - 4)

    # Rodapé Limpo
    footer_y = MARGIN_BOTTOM - 16
    canv.setStrokeColor(colors.HexColor("#cccccc"))
    canv.setLineWidth(0.5)
    canv.line(MARGIN_LEFT, footer_y + 12, PAGE_W - MARGIN_RIGHT, footer_y + 12)

    # Número da página à esquerda
    canv.setFont("Helvetica-Bold", 9)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT, footer_y + 1, str(page_num))

    # Identificador à direita
    canv.setFont("Helvetica", 7.5)
    canv.setFillColor(colors.HexColor("#555555"))
    canv.drawRightString(PAGE_W - MARGIN_RIGHT, footer_y + 1, "SIMULADO COLETIVO • 1º DIA • CADERNO 1 BRANCO")

    canv.restoreState()


def draw_single_column_decorations(canv, doc):
    """Decorações para a página de redação e folha de rascunho (coluna única)."""
    canv.saveState()
    page_num = canv.getPageNumber()

    header_y = PAGE_H - MARGIN_TOP + 8
    canv.setFont("Helvetica-Bold", 11)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT, header_y + 2, "enem")
    canv.setFont("Helvetica", 11)
    canv.setFillColor(colors.HexColor("#555555"))
    canv.drawString(MARGIN_LEFT + 32, header_y + 2, "2026")

    canv.setFont("Helvetica-Bold", 8)
    canv.setFillColor(colors.black)
    canv.drawRightString(PAGE_W - MARGIN_RIGHT, header_y + 2, "PROPOSTA DE REDAÇÃO • CADERNO BRANCO")

    canv.setStrokeColor(colors.black)
    canv.setLineWidth(0.8)
    canv.line(MARGIN_LEFT, header_y - 4, PAGE_W - MARGIN_RIGHT, header_y - 4)

    footer_y = MARGIN_BOTTOM - 16
    canv.setStrokeColor(colors.HexColor("#cccccc"))
    canv.setLineWidth(0.5)
    canv.line(MARGIN_LEFT, footer_y + 12, PAGE_W - MARGIN_RIGHT, footer_y + 12)

    canv.setFont("Helvetica-Bold", 9)
    canv.setFillColor(colors.black)
    canv.drawString(MARGIN_LEFT, footer_y + 1, str(page_num))

    canv.restoreState()


def get_two_column_styles():
    """Tipografia ultra compacta e de alta legibilidade para diagramação em 2 colunas."""
    styles = {
        "AreaBanner": ParagraphStyle(
            "AreaBanner",
            fontName="Helvetica-Bold",
            fontSize=9.0,
            leading=11.5,
            textColor=colors.black,
            backColor=colors.HexColor("#eeeeee"),
            borderPadding=(4, 6, 4, 6),
            spaceAfter=6,
            spaceBefore=4,
            alignment=0,
        ),
        "TextSupportTitle": ParagraphStyle(
            "TextSupportTitle",
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10.5,
            textColor=colors.black,
            alignment=1,
            spaceAfter=2,
            spaceBefore=2,
        ),
        "TextSupportBody": ParagraphStyle(
            "TextSupportBody",
            fontName="Helvetica",
            fontSize=7.8,
            leading=10.2,
            textColor=colors.HexColor("#111111"),
            alignment=4,  # Justificado
            spaceAfter=2,
        ),
        "TextSupportSource": ParagraphStyle(
            "TextSupportSource",
            fontName="Helvetica-Oblique",
            fontSize=6.5,
            leading=8.5,
            textColor=colors.HexColor("#444444"),
            alignment=2,  # Direita
            spaceAfter=4,
        ),
        "QuestionPrompt": ParagraphStyle(
            "QuestionPrompt",
            fontName="Helvetica",
            fontSize=8.0,
            leading=10.5,
            textColor=colors.black,
            alignment=4,
            spaceAfter=4,
            spaceBefore=1,
        ),
        "AlternativeText": ParagraphStyle(
            "AlternativeText",
            fontName="Helvetica",
            fontSize=7.6,
            leading=9.8,
            textColor=colors.HexColor("#111111"),
            alignment=4,
        ),
        "EssayTitle": ParagraphStyle(
            "EssayTitle",
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.black,
            alignment=1,
            spaceAfter=8,
        ),
        "EssayInst": ParagraphStyle(
            "EssayInst",
            fontName="Helvetica",
            fontSize=8.2,
            leading=11.5,
            textColor=colors.black,
            alignment=4,
            spaceAfter=8,
        ),
        "MotivatingTitle": ParagraphStyle(
            "MotivatingTitle",
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11.0,
            textColor=colors.black,
            spaceAfter=2,
        ),
        "MotivatingBody": ParagraphStyle(
            "MotivatingBody",
            fontName="Helvetica",
            fontSize=7.8,
            leading=10.2,
            textColor=colors.HexColor("#111111"),
            alignment=4,
            spaceAfter=2,
        ),
    }
    return styles


def build_two_column_question(q, styles, col_width):
    """Constrói uma questão formatada especificamente para caber na coluna estreita do ENEM."""
    elements = []

    # Cabeçalho: QUESTÃO XX + barra
    elements.append(QuestionHeaderFlowable(q["numero"], col_width))
    elements.append(Spacer(1, 3))

    # Texto de apoio (apenas se existir título real, sem '(Item XX)')
    texto_apoio = q.get("texto_apoio")
    if texto_apoio:
        titulo = texto_apoio.get("titulo")
        # Filtra títulos artificiais
        if titulo and not titulo.lower().startswith("item"):
            elements.append(Paragraph(titulo, styles["TextSupportTitle"]))
        if texto_apoio.get("conteudo"):
            elements.append(Paragraph(texto_apoio["conteudo"], styles["TextSupportBody"]))
        if texto_apoio.get("fonte"):
            elements.append(Paragraph(texto_apoio["fonte"], styles["TextSupportSource"]))

    # Imagem de apoio (se houver)
    img_path = q.get("imagem")
    if img_path and os.path.exists(img_path):
        try:
            rl_img = RLImage(img_path)
            max_w = col_width * 0.90
            aspect = rl_img.imageHeight / float(rl_img.imageWidth)
            rl_img.drawWidth = max_w
            rl_img.drawHeight = max_w * aspect
            elements.append(rl_img)
            elements.append(Spacer(1, 3))
        except Exception:
            pass

    # Enunciado
    elements.append(Paragraph(q["enunciado"], styles["QuestionPrompt"]))
    elements.append(Spacer(1, 2))

    # Tabela de alternativas (A a E)
    alts = q.get("alternativas") or q.get("alts") or {}
    table_data = []
    badge_w = 16.0
    text_w = col_width - badge_w

    for letter in ["A", "B", "C", "D", "E"]:
        alt_text = alts.get(letter, "")
        badge = AlternativeBadgeFlowable(letter)
        para = Paragraph(alt_text, styles["AlternativeText"])
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
    elements.append(Spacer(1, 8))

    return KeepTogether(elements)


def gerar_prova_pdf(caminho_questoes="banco_questoes/questoes.json", caminho_saida="provas_geradas/Prova_Completa.pdf"):
    """Gera o Caderno de Prova Completo em 2 colunas estilo ENEM no Caderno Branco."""
    with open(caminho_questoes, "r", encoding="utf-8") as f:
        dados = json.load(f)

    metadados = dados.get("metadados", {})
    redacao = dados.get("redacao", {})
    questoes = dados.get("questoes", [])

    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)

    # Documento com suporte a múltiplos templates (Capa, 2 Colunas e Redação)
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
        id='col1', leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0
    )
    frame_col2 = Frame(
        MARGIN_LEFT + COL_W + GUTTER, MARGIN_BOTTOM, COL_W, USABLE_H,
        id='col2', leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0
    )

    # Frame para a Redação e Rascunho (Coluna única ampla)
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

    # 1. Capa
    # Muda o template da próxima página para TwoCol e faz PageBreak
    story.append(NextPageTemplate('TwoCol'))
    story.append(PageBreak())

    # 2. Questões de 1 a 70 (em 2 Colunas contínuas)
    current_area = None

    for q in questoes:
        q_num = q["numero"]
        q_area = q.get("area", "Linguagens e Códigos")

        # Faixa de área quando muda
        if q_area != current_area:
            current_area = q_area
            story.append(Paragraph(current_area.upper(), styles["AreaBanner"]))

        # Questão formatada em 2 colunas
        story.append(build_two_column_question(q, styles, COL_W))

    # 3. Proposta de Redação ao final de todas as 70 questões
    if redacao:
        story.append(NextPageTemplate('Single'))
        story.append(PageBreak())

        story.append(Paragraph("PROPOSTA DE REDAÇÃO", styles["EssayTitle"]))

        tema = redacao.get("tema", "A inclusão de pessoas neurodiversas no Brasil")
        inst = redacao.get("instrucoes", "")
        texto_inst = f"{inst}<br/><br/><b>TEMA: &ldquo;{tema.upper()}&rdquo;</b>"
        story.append(Paragraph(texto_inst, styles["EssayInst"]))
        story.append(Spacer(1, 6))

        for t in redacao.get("textos_motivadores", []):
            card_content = [
                Paragraph(t.get("titulo", "TEXTO"), styles["MotivatingTitle"]),
                Paragraph(t.get("conteudo", ""), styles["MotivatingBody"])
            ]
            if t.get("fonte"):
                card_content.append(Paragraph(t["fonte"], styles["TextSupportSource"]))

            card_table = Table([[card_content]], colWidths=[USABLE_W])
            card_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8f8f8")),
                ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor("#cccccc")),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(card_table)
            story.append(Spacer(1, 6))

        # 4. Folha de Rascunho da Redação (imediatamente após a proposta)
        story.append(PageBreak())
        inst_rascunho = (
            "<b>INSTRUÇÕES PARA O RASCUNHO DA REDAÇÃO:</b><br/>"
            "1. Utilize o espaço abaixo para estruturar sua tese, argumentos e proposta de intervenção.<br/>"
            "2. O texto definitivo DEVE ser transcrito a caneta preta na FOLHA DE REDAÇÃO oficial (até 30 linhas)."
        )
        story.append(Paragraph(inst_rascunho, styles["EssayInst"]))
        story.append(Spacer(1, 6))
        story.append(DraftWatermarkFlowable(USABLE_W, height=540))

    doc.build(story)
    print(f"Caderno de Prova (2 Colunas, Caderno Branco) gerado em: {caminho_saida}")


if __name__ == "__main__":
    gerar_prova_pdf()
