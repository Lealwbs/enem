"""
================================================================================
Simulado Coletivo • Gerador de Cartão-Resposta (Gabarito OMR) 70 Questões em PDF
Modelo oficial estilo ENEM com 4 marcadores fiduciais quadrados pretos delimitando
EXCLUSIVAMENTE o bloco das 70 questões para máxima precisão de leitura óptica (OMR).
================================================================================
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib import colors

# Dimensões da página A4 em pontos (595.27 x 841.89)
PAGE_WIDTH, PAGE_HEIGHT = A4

# Configuração dos marcadores fiduciais (quadrados pretos ao redor das questões)
FIDUCIAL_SIZE = 16.0

# Dimensões e espaçamentos da grade de respostas
GRID_MARGIN_X = 36.0
GRID_W = PAGE_WIDTH - 2 * GRID_MARGIN_X
GAP_COLUMNS = 10.0
COL_W = (GRID_W - 3 * GAP_COLUMNS) / 4.0

HEADER_H = 19.0
ROW_H = 18.0
MAX_ROWS = 18
BUBBLE_RADIUS = 5.0
OPT_DX = 15.8
OPTIONS = ["A", "B", "C", "D", "E"]

# Definição das colunas de questões
COLUMNS_DEF = [
    {"start": 1, "end": 18, "title": "QUESTÕES 01 a 18"},
    {"start": 19, "end": 36, "title": "QUESTÕES 19 a 36"},
    {"start": 37, "end": 54, "title": "QUESTÕES 37 a 54"},
    {"start": 55, "end": 70, "title": "QUESTÕES 55 a 70"},
]


def draw_header(c, metadados):
    """Desenha o cabeçalho superior do cartão-resposta."""
    # Código de barras superior
    codigo_caderno = metadados.get("codigo_caderno", "010175BR1")
    barcode = code128.Code128(codigo_caderno, barWidth=1.0, barHeight=22)
    barcode.drawOn(c, (PAGE_WIDTH - barcode.width) / 2.0, PAGE_HEIGHT - 38)

    # Número do código abaixo do barcode
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.black)
    c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 48, f"* {codigo_caderno} *")

    # Título principal
    c.setFont("Helvetica-Bold", 19)
    c.setFillColor(colors.HexColor("#0c2340"))  # Azul escuro ENEM
    c.drawString(GRID_MARGIN_X, PAGE_HEIGHT - 66, "CARTÃO-RESPOSTA")

    # Linha decorativa abaixo do título
    c.setStrokeColor(colors.HexColor("#00a4e4"))
    c.setLineWidth(2.5)
    c.line(GRID_MARGIN_X, PAGE_HEIGHT - 71, GRID_MARGIN_X + 220, PAGE_HEIGHT - 71)

    # Subtítulo
    c.setFont("Helvetica", 8.2)
    c.setFillColor(colors.HexColor("#333333"))
    subtitulo = metadados.get("subtitulo", "SIMULADO COLETIVO • EXAME NACIONAL DO ENSINO MÉDIO - 70 QUESTÕES")
    c.drawString(GRID_MARGIN_X, PAGE_HEIGHT - 82, subtitulo.upper())

    # Badge do Dia (lado direito)
    dia_box_x = PAGE_WIDTH - GRID_MARGIN_X - 85
    dia_box_y = PAGE_HEIGHT - 82
    c.setStrokeColor(colors.HexColor("#0c2340"))
    c.setLineWidth(1.2)
    c.roundRect(dia_box_x, dia_box_y, 85, 28, 4, fill=0)

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#0c2340"))
    dia_texto = metadados.get("dia", "1º DIA")
    c.drawCentredString(dia_box_x + 42.5, dia_box_y + 9, dia_texto)


def draw_candidate_info(c, start_y):
    """Desenha a caixa de dados do participante (Nome, CPF, Data Nasc, Assinatura, Frase)."""
    box_x = GRID_MARGIN_X
    box_w = GRID_W
    box_h = 92
    box_y = start_y - box_h

    # Borda do painel
    c.setStrokeColor(colors.HexColor("#888888"))
    c.setLineWidth(0.7)
    c.setFillColor(colors.HexColor("#fafafa"))
    c.roundRect(box_x, box_y, box_w, box_h, 4, fill=1, stroke=1)

    # Nome Completo
    c.setFont("Helvetica-Bold", 7.8)
    c.setFillColor(colors.HexColor("#222222"))
    c.drawString(box_x + 8, box_y + box_h - 13, "Nome Completo:")

    # Quadrículas para letras do nome
    num_boxes = 33
    b_start_x = box_x + 8
    b_y = box_y + box_h - 29
    b_size = 13.5
    c.setStrokeColor(colors.HexColor("#999999"))
    c.setLineWidth(0.5)
    for i in range(num_boxes):
        c.rect(b_start_x + i * (b_size + 1.2), b_y, b_size, b_size)

    # Linha 2: CPF / Data Nasc / Assinatura
    row2_y = box_y + 36
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(box_x + 8, row2_y + 15, "CPF / Inscrição:")
    for i in range(11):
        c.rect(box_x + 8 + i * 13, row2_y, 12, 12)

    dn_x = box_x + 165
    c.drawString(dn_x, row2_y + 15, "Data de Nascimento:")
    for i in range(8):
        c.rect(dn_x + i * 13, row2_y, 12, 12)

    ass_x = box_x + 285
    ass_w = box_w - 295
    c.drawString(ass_x, row2_y + 15, "Assinatura do Participante:")
    c.setStrokeColor(colors.HexColor("#444444"))
    c.setDash([2, 2], 0)
    c.line(ass_x, row2_y + 2, ass_x + ass_w, row2_y + 2)
    c.setDash([], 0)

    # Linha 3: Frase de segurança
    row3_y = box_y + 7
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(box_x + 8, row3_y + 15, "Transcreva a frase da capa do seu caderno com caligrafia usual:")
    c.setStrokeColor(colors.HexColor("#777777"))
    c.line(box_x + 8, row3_y + 3, box_x + box_w - 8, row3_y + 3)

    return box_y


def draw_instructions_bar(c, start_y):
    """Desenha barra com instruções de preenchimento e exemplos visuais."""
    bar_x = GRID_MARGIN_X
    bar_w = GRID_W
    bar_h = 38
    bar_y = start_y - bar_h - 6

    c.setStrokeColor(colors.HexColor("#00a4e4"))
    c.setFillColor(colors.HexColor("#f0f8fd"))
    c.setLineWidth(0.7)
    c.roundRect(bar_x, bar_y, bar_w, bar_h, 3, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor("#0c2340"))
    c.drawString(bar_x + 8, bar_y + bar_h - 11, "INSTRUÇÕES DE PREENCHIMENTO:")

    c.setFont("Helvetica", 7.0)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(bar_x + 8, bar_y + bar_h - 22, "• Utilize apenas caneta esferográfica de tinta preta fabricada em material transparente.")
    c.drawString(bar_x + 8, bar_y + bar_h - 32, "• Preencha completamente o círculo da opção desejada. A correção óptica analisa apenas a área dos 4 quadrados.")

    # Exemplos visuais à direita
    ex_x = bar_x + bar_w - 150
    c.setFont("Helvetica-Bold", 7.2)
    c.drawString(ex_x, bar_y + bar_h - 13, "EXEMPLOS:")

    c.setFont("Helvetica", 6.8)
    c.drawString(ex_x, bar_y + bar_h - 26, "Correto:")
    c.setFillColor(colors.black)
    c.circle(ex_x + 40, bar_y + bar_h - 24, 4.5, fill=1, stroke=1)

    c.drawString(ex_x + 60, bar_y + bar_h - 26, "Incorreto:")
    c.setFillColor(colors.white)
    c.circle(ex_x + 105, bar_y + bar_h - 24, 4.5, fill=0, stroke=1)
    c.line(ex_x + 102, bar_y + bar_h - 27, ex_x + 108, bar_y + bar_h - 21)
    c.line(ex_x + 102, bar_y + bar_h - 21, ex_x + 108, bar_y + bar_h - 27)

    return bar_y


def draw_bubble_grid(c, start_y):
    """
    Desenha o grid de 70 questões em 4 colunas com 4 marcadores quadrados pretos
    delimitando EXCLUSIVAMENTE a área de questões para o alinhamento OMR.
    """
    cy_top = start_y - 8
    col_content_h = MAX_ROWS * ROW_H + 8
    col_content_y = cy_top - HEADER_H - col_content_h

    # 4 MARCADORES QUADRADOS PRETOS NOS CANTOS DA ÁREA DE QUESTÕES
    fid_left_x = GRID_MARGIN_X - 22.0
    fid_right_x = GRID_MARGIN_X + GRID_W + 6.0
    fid_top_y = cy_top - FIDUCIAL_SIZE
    fid_bottom_y = col_content_y

    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    # Top-Left
    c.rect(fid_left_x, fid_top_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)
    # Top-Right
    c.rect(fid_right_x, fid_top_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)
    # Bottom-Left
    c.rect(fid_left_x, fid_bottom_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)
    # Bottom-Right
    c.rect(fid_right_x, fid_bottom_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)

    # Coordenadas exatas dos centros dos marcadores para o OMR
    fiducials_centers = {
        "TL": (fid_left_x + FIDUCIAL_SIZE / 2.0, fid_top_y + FIDUCIAL_SIZE / 2.0),
        "TR": (fid_right_x + FIDUCIAL_SIZE / 2.0, fid_top_y + FIDUCIAL_SIZE / 2.0),
        "BL": (fid_left_x + FIDUCIAL_SIZE / 2.0, fid_bottom_y + FIDUCIAL_SIZE / 2.0),
        "BR": (fid_right_x + FIDUCIAL_SIZE / 2.0, fid_bottom_y + FIDUCIAL_SIZE / 2.0),
    }

    geometry = {
        "fiducials": fiducials_centers,
        "questions": {}
    }

    for col_idx, col_def in enumerate(COLUMNS_DEF):
        cx = GRID_MARGIN_X + col_idx * (COL_W + GAP_COLUMNS)

        # Cabeçalho da coluna
        c.setFillColor(colors.HexColor("#0c2340"))
        c.roundRect(cx, cy_top - HEADER_H, COL_W, HEADER_H, 2.5, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.white)
        c.drawCentredString(cx + COL_W / 2.0, cy_top - HEADER_H + 5.5, col_def["title"])

        # Fundo e borda suave da coluna
        c.setStrokeColor(colors.HexColor("#d0d7de"))
        c.setLineWidth(0.6)
        c.setFillColor(colors.white)
        c.rect(cx, col_content_y, COL_W, col_content_h, fill=1, stroke=1)

        start_q = col_def["start"]
        end_q = col_def["end"]
        num_q = end_q - start_q + 1

        for r in range(num_q):
            q_num = start_q + r
            row_y = cy_top - HEADER_H - 14 - r * ROW_H

            # Linha zebrada sutil para leitura visual confortável
            if r % 2 == 1:
                c.setFillColor(colors.HexColor("#f8fafc"))
                c.rect(cx + 1, row_y - ROW_H / 2.0 + 1, COL_W - 2, ROW_H - 2, fill=1, stroke=0)

            # Número da questão
            c.setFont("Helvetica-Bold", 8.5)
            c.setFillColor(colors.HexColor("#0c2340"))
            c.drawString(cx + 5, row_y - 3, f"{q_num:02d}")

            # Bolinhas das alternativas (A a E)
            first_opt_x = cx + 33.0
            geometry["questions"][q_num] = {}

            for opt_idx, opt_letter in enumerate(OPTIONS):
                bx = first_opt_x + opt_idx * OPT_DX
                by = row_y

                c.setStrokeColor(colors.black)
                c.setLineWidth(0.8)
                c.setFillColor(colors.white)
                c.circle(bx, by, BUBBLE_RADIUS, fill=1, stroke=1)

                c.setFont("Helvetica-Bold", 7.0)
                c.setFillColor(colors.black)
                c.drawCentredString(bx, by - 2.4, opt_letter)

                # Salva a coordenada geométrica absoluta
                geometry["questions"][q_num][opt_letter] = (bx, by, BUBBLE_RADIUS)

    return col_content_y, geometry


def draw_evaluation_box(c, start_y):
    """Desenha a caixa de resultado da banca avaliadora abaixo das questões."""
    sub_q_y = start_y - 12
    c.setFont("Helvetica-Bold", 7.2)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawCentredString(
        PAGE_WIDTH / 2.0,
        sub_q_y,
        "▲ ÁREA DE RESPOSTAS — CORREÇÃO ELETRÔNICA (OMR) EXCLUSIVA ENTRE OS 4 MARCADORES QUADRADOS ▲"
    )

    box_x = GRID_MARGIN_X
    box_w = GRID_W
    banca_box_y = sub_q_y - 74
    banca_box_h = 64

    c.setStrokeColor(colors.HexColor("#999999"))
    c.setLineWidth(0.8)
    c.setFillColor(colors.HexColor("#fafafa"))
    c.roundRect(box_x, banca_box_y, box_w, banca_box_h, 4, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 8.0)
    c.setFillColor(colors.HexColor("#0c2340"))
    c.drawString(box_x + 10, banca_box_y + banca_box_h - 14, "USO EXCLUSIVO DA BANCA AVALIADORA / RESULTADO FINAL")

    c.setStrokeColor(colors.HexColor("#cccccc"))
    c.line(box_x + 10, banca_box_y + banca_box_h - 18, box_x + box_w - 10, banca_box_y + banca_box_h - 18)

    # Campos de preenchimento de nota
    c.setFont("Helvetica-Bold", 8.0)
    c.setFillColor(colors.HexColor("#222222"))
    c.drawString(box_x + 20, banca_box_y + 24, "TOTAL DE ACERTOS:")
    c.rect(box_x + 130, banca_box_y + 14, 60, 24)
    c.setFont("Helvetica", 8.0)
    c.drawString(box_x + 196, banca_box_y + 22, "/ 70 questões")

    c.setFont("Helvetica-Bold", 8.0)
    c.drawString(box_x + 265, banca_box_y + 24, "APROVEITAMENTO:")
    c.rect(box_x + 365, banca_box_y + 14, 55, 24)
    c.drawString(box_x + 426, banca_box_y + 22, "%")

    c.setFont("Helvetica", 7.0)
    c.drawString(box_x + 10, banca_box_y + 5, "Visto do Aplicador / Responsável: _________________________________________________")


def draw_footer(c):
    """Desenha o rodapé institucional."""
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#777777"))
    c.drawString(GRID_MARGIN_X, 24, "SIMULADO COLETIVO • MODELO OFICIAL ENEM 70 QUESTÕES • LEITURA ÓPTICA AUTOMATIZADA (OMR)")
    c.drawRightString(PAGE_WIDTH - GRID_MARGIN_X, 24, "PÁGINA 1 / 1")


def gerar_cartao_resposta_pdf(caminho_saida="provas_geradas/Cartao_Resposta_70Q.pdf", metadados=None):
    """Gera o arquivo PDF completo do Cartão-Resposta de 70 questões."""
    if metadados is None:
        metadados = {
            "titulo_exame": "EXAME NACIONAL DO ENSINO MÉDIO",
            "subtitulo": "SIMULADO COLETIVO • EXAME NACIONAL DO ENSINO MÉDIO - 70 QUESTÕES",
            "dia": "1º DIA",
            "codigo_caderno": "010175BR1"
        }

    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)
    c = canvas.Canvas(caminho_saida, pagesize=A4)

    # 1. Cabeçalho
    draw_header(c, metadados)

    # 2. Painel do candidato
    y_after_cand = draw_candidate_info(c, start_y=PAGE_HEIGHT - 88)

    # 3. Barra de instruções
    y_after_inst = draw_instructions_bar(c, start_y=y_after_cand)

    # 4. Grid das 70 questões com os 4 marcadores quadrados pretos exclusivos
    bottom_grid_y, geometry = draw_bubble_grid(c, start_y=y_after_inst)

    # 5. Painel da banca avaliadora abaixo das questões
    draw_evaluation_box(c, start_y=bottom_grid_y)

    # 6. Rodapé
    draw_footer(c)

    c.save()
    print(f"Cartão-Resposta gerado com sucesso em: {caminho_saida}")
    return geometry


if __name__ == "__main__":
    gerar_cartao_resposta_pdf()
