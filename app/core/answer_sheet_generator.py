"""
Coletivo • Gerador de Cartão-Resposta (Gabarito OMR) 70 Questões em PDF.
Modelo oficial estilo ENEM otimizado para impressão P&B e máxima precisão OMR:
- Campo de Nome Completo em caixa única para escrita manual normal.
- Campo de Transcrição da Frase de Segurança conforme a capa da prova.
- Instruções de preenchimento compactas com destaque para uso exclusivo de caneta preta.
- Grid das 70 questões com múltiplos marcadores fiduciais pretos (cantos, laterais e colunas)
  para guiar a correção automática por visão computacional (OpenCV).
- Painel de Resultados posicionado no rodapé inferior da página, com espaçamento generoso
  em relação às bolhas do gabarito, layout moderno e limpo, sem textos de professor/visto/data.
"""

import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

PAGE_WIDTH, PAGE_HEIGHT = A4

FIDUCIAL_SIZE = 14.0
SMALL_FIDUCIAL = 8.0
GRID_MARGIN_X = 36.0
GRID_W = PAGE_WIDTH - 2 * GRID_MARGIN_X
GAP_COLUMNS = 10.0
COL_W = (GRID_W - 3 * GAP_COLUMNS) / 4.0

HEADER_H = 18.0
ROW_H = 18.0
MAX_ROWS = 18
BUBBLE_RADIUS = 4.8
OPT_DX = 15.6
OPTIONS = ["A", "B", "C", "D", "E"]

COLUMNS_DEF = [
    {"start": 1, "end": 18, "title": "QUESTÕES 01 a 18"},
    {"start": 19, "end": 36, "title": "QUESTÕES 19 a 36"},
    {"start": 37, "end": 54, "title": "QUESTÕES 37 a 54"},
    {"start": 55, "end": 70, "title": "QUESTÕES 55 a 70"},
]


def draw_clean_header(c, is_gabarito=False):
    """Desenha cabeçalho oficial do cartão."""
    start_y = PAGE_HEIGHT - 32

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    titulo = "GABARITO OFICIAL DEFINITIVO — 70 QUESTÕES" if is_gabarito else "CARTÃO-RESPOSTA OFICIAL"
    c.drawString(GRID_MARGIN_X, start_y, titulo)

    c.setFont("Helvetica-Bold", 7.8)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(GRID_MARGIN_X, start_y - 12, "2º SIMULADO UNIFICADO • COLETIVO VOA VOA & PREPARATÓRIO GABARITA")

    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.line(GRID_MARGIN_X, start_y - 16, GRID_MARGIN_X + GRID_W, start_y - 16)

    return start_y - 28.0


def draw_candidate_name_field(c, start_y, is_gabarito=False):
    """Desenha campo contínuo para o nome do participante (sem placeholders)."""
    box_x = GRID_MARGIN_X
    box_w = GRID_W
    box_h = 22.0
    box_y = start_y - box_h

    c.setFont("Helvetica-Bold", 7.2)
    c.setFillColor(colors.black)
    c.drawString(box_x, start_y, "NOME COMPLETO DO PARTICIPANTE:")

    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.setFillColor(colors.white)
    c.rect(box_x, box_y, box_w, box_h, fill=1, stroke=1)

    if is_gabarito:
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(colors.black)
        c.drawString(box_x + 10, box_y + 6.5, "FOLHA DE RESPOSTAS PADRÃO — GABARITO OFICIAL")

    return box_y - 12.0



def draw_instructions_bw(c, start_y):
    """Desenha instruções de preenchimento destacando a caneta preta obrigatória."""
    bar_x = GRID_MARGIN_X
    bar_w = GRID_W
    bar_h = 24.0
    bar_y = start_y - bar_h

    c.setStrokeColor(colors.HexColor("#444444"))
    c.setFillColor(colors.HexColor("#F8F8F8"))
    c.setLineWidth(0.6)
    c.rect(bar_x, bar_y, bar_w, bar_h, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.black)
    c.drawString(bar_x + 6, bar_y + bar_h - 8.5, "INSTRUÇÕES:")

    c.setFont("Helvetica", 6.0)
    c.setFillColor(colors.HexColor("#222222"))
    c.drawString(bar_x + 6, bar_y + bar_h - 15.5, "• Preencha integralmente a bolha correspondente utilizando EXCLUSIVAMENTE caneta esferográfica de tinta preta.")
    c.drawString(bar_x + 6, bar_y + bar_h - 22.0, "• É ESTRITAMENTE PROIBIDO O USO DE CANETA AZUL, lápis ou corretivo. Não dobre nem rasure os marcadores pretos.")

    # Exemplos visuais P&B
    ex_x = bar_x + bar_w - 130
    c.setFont("Helvetica-Bold", 6.0)
    c.drawString(ex_x, bar_y + bar_h - 10, "Correto:")
    c.setFillColor(colors.black)
    c.circle(ex_x + 34, bar_y + bar_h - 9, 3.8, fill=1, stroke=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 5.2)
    c.drawCentredString(ex_x + 34, bar_y + bar_h - 11, "A")

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 6.0)
    c.drawString(ex_x + 52, bar_y + bar_h - 10, "Incorretos:")
    c.circle(ex_x + 90, bar_y + bar_h - 9, 3.8, fill=0, stroke=1)
    c.line(ex_x + 86, bar_y + bar_h - 13, ex_x + 94, bar_y + bar_h - 5)
    c.circle(ex_x + 106, bar_y + bar_h - 9, 3.8, fill=0, stroke=1)
    c.circle(ex_x + 106, bar_y + bar_h - 9, 1.2, fill=1, stroke=1)

    return bar_y - 8


def draw_bubble_grid(c, start_y, gabarito_oficial=None):
    """
    Desenha o grid das 70 questões com marcadores fiduciais pretos nos 4 cantos
    e marcadores auxiliares laterais para ancoragem OMR.
    """
    grid_top_y = start_y
    grid_h = HEADER_H + MAX_ROWS * ROW_H
    grid_bottom_y = grid_top_y - grid_h

    # 1. Marcadores Fiduciais nos 4 cantos
    fid_pad = 1.0
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)

    tl_x = GRID_MARGIN_X - FIDUCIAL_SIZE - fid_pad
    tl_y = grid_top_y - FIDUCIAL_SIZE
    c.rect(tl_x, tl_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)

    tr_x = GRID_MARGIN_X + GRID_W + fid_pad
    tr_y = grid_top_y - FIDUCIAL_SIZE
    c.rect(tr_x, tr_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)

    bl_x = GRID_MARGIN_X - FIDUCIAL_SIZE - fid_pad
    bl_y = grid_bottom_y
    c.rect(bl_x, bl_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)

    br_x = GRID_MARGIN_X + GRID_W + fid_pad
    br_y = grid_bottom_y
    c.rect(br_x, br_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)

    # 2. Marcadores auxiliares laterais em posições percentuais (25%, 50%, 75%)
    for frac in [0.25, 0.50, 0.75]:
        aux_y = grid_bottom_y + frac * grid_h - SMALL_FIDUCIAL / 2.0
        c.rect(tl_x + (FIDUCIAL_SIZE - SMALL_FIDUCIAL) / 2.0, aux_y, SMALL_FIDUCIAL, SMALL_FIDUCIAL, fill=1, stroke=0)
        c.rect(tr_x + (FIDUCIAL_SIZE - SMALL_FIDUCIAL) / 2.0, aux_y, SMALL_FIDUCIAL, SMALL_FIDUCIAL, fill=1, stroke=0)

    # 3. Marcadores de alinhamento nas bases e topos das colunas
    marker_s = 6.0
    for col_idx in range(4):
        cx = GRID_MARGIN_X + col_idx * (COL_W + GAP_COLUMNS)
        c.rect(cx + COL_W / 2.0 - marker_s / 2.0, grid_top_y + 2, marker_s, marker_s, fill=1, stroke=0)
        c.rect(cx + COL_W / 2.0 - marker_s / 2.0, grid_bottom_y - 8, marker_s, marker_s, fill=1, stroke=0)

    geometry = {
        "fiducials": {
            "top_left": (tl_x + FIDUCIAL_SIZE / 2.0, tl_y + FIDUCIAL_SIZE / 2.0),
            "top_right": (tr_x + FIDUCIAL_SIZE / 2.0, tr_y + FIDUCIAL_SIZE / 2.0),
            "bottom_left": (bl_x + FIDUCIAL_SIZE / 2.0, bl_y + FIDUCIAL_SIZE / 2.0),
            "bottom_right": (br_x + FIDUCIAL_SIZE / 2.0, br_y + FIDUCIAL_SIZE / 2.0),
        },
        "questions": {}
    }

    # 4. Desenha as 4 Colunas com cabeçalhos e bolhas
    col_content_y = grid_top_y

    for col_idx, col_def in enumerate(COLUMNS_DEF):
        cx = GRID_MARGIN_X + col_idx * (COL_W + GAP_COLUMNS)
        cy = col_content_y

        c.setFillColor(colors.HexColor("#222222"))
        c.rect(cx, cy - HEADER_H, COL_W, HEADER_H, fill=1, stroke=0)

        c.setFont("Helvetica-Bold", 7.2)
        c.setFillColor(colors.white)
        c.drawCentredString(cx + COL_W / 2.0, cy - 12.5, col_def["title"])

        start_q = col_def["start"]
        end_q = col_def["end"]
        num_rows = end_q - start_q + 1

        for r in range(MAX_ROWS):
            row_y = cy - HEADER_H - (r * ROW_H) - (ROW_H / 2.0)

            if r >= num_rows:
                c.setStrokeColor(colors.HexColor("#EAEAEA"))
                c.rect(cx, row_y - ROW_H / 2.0 + 1, COL_W, ROW_H - 2, fill=0, stroke=1)
                continue

            q_num = start_q + r

            if r % 2 == 1:
                c.setFillColor(colors.HexColor("#F6F6F6"))
                c.rect(cx + 1, row_y - ROW_H / 2.0 + 1, COL_W - 2, ROW_H - 2, fill=1, stroke=0)

            c.setFont("Helvetica-Bold", 8.2)
            c.setFillColor(colors.black)
            c.drawString(cx + 4, row_y - 2.8, f"{q_num:02d}")

            first_opt_x = cx + 32.0
            geometry["questions"][q_num] = {}
            resp_correta = (gabarito_oficial.get(q_num, "") or "").strip().upper() if gabarito_oficial else ""

            for opt_idx, opt_letter in enumerate(OPTIONS):
                bx = first_opt_x + opt_idx * OPT_DX
                by = row_y

                is_correct = (opt_letter == resp_correta)

                c.setStrokeColor(colors.black)
                c.setLineWidth(0.7)

                if is_correct:
                    c.setFillColor(colors.black)
                    c.circle(bx, by, BUBBLE_RADIUS, fill=1, stroke=1)
                    c.setFont("Helvetica-Bold", 6.8)
                    c.setFillColor(colors.white)
                    c.drawCentredString(bx, by - 2.2, opt_letter)
                else:
                    c.setFillColor(colors.white)
                    c.circle(bx, by, BUBBLE_RADIUS, fill=1, stroke=1)
                    c.setFont("Helvetica-Bold", 6.8)
                    c.setFillColor(colors.black)
                    c.drawCentredString(bx, by - 2.2, opt_letter)

                geometry["questions"][q_num][opt_letter] = (bx, by, BUBBLE_RADIUS)

    return grid_bottom_y, geometry


def draw_extra_fiducials(c, bottom_grid_y, panel_top_y):
    """Desenha marcadores pretos adicionais para máxima precisão de correção OMR."""
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    
    # 1. Marcadores nas laterais intermediárias entre o gabarito e o painel
    mid_gap_y = (bottom_grid_y + panel_top_y) / 2.0 - SMALL_FIDUCIAL / 2.0
    c.rect(GRID_MARGIN_X - FIDUCIAL_SIZE - 1.0, mid_gap_y, SMALL_FIDUCIAL, SMALL_FIDUCIAL, fill=1, stroke=0)
    c.rect(GRID_MARGIN_X + GRID_W + 1.0, mid_gap_y, SMALL_FIDUCIAL, SMALL_FIDUCIAL, fill=1, stroke=0)

    # 2. Marcadores inferiores nos cantos extremos da página
    bot_y = 10.0
    c.rect(GRID_MARGIN_X - FIDUCIAL_SIZE - 1.0, bot_y, SMALL_FIDUCIAL, SMALL_FIDUCIAL, fill=1, stroke=0)
    c.rect(GRID_MARGIN_X + GRID_W + 1.0, bot_y, SMALL_FIDUCIAL, SMALL_FIDUCIAL, fill=1, stroke=0)

    # 3. Marcadores de referência horizontal na margem inferior
    marker_w = 6.0
    for col_idx in range(4):
        cx = GRID_MARGIN_X + col_idx * (COL_W + GAP_COLUMNS) + COL_W / 2.0 - marker_w / 2.0
        c.rect(cx, bot_y, marker_w, marker_w, fill=1, stroke=0)


def draw_clean_evaluator_panel(c, is_gabarito=False):
    """
    Desenha o Painel de Desempenho no rodapé inferior da folha,
    com amplo espaçamento em relação ao gabarito, layout moderno e limpo,
    sem textos de 'USO EXCLUSIVO', sem vistos e sem datas.
    """
    panel_x = GRID_MARGIN_X
    panel_w = GRID_W
    panel_h = 62.0
    panel_y = 18.0  # Ancorado no rodapé inferior da página

    # Marcadores fiduciais laterais no painel
    c.setFillColor(colors.black)
    c.rect(panel_x - FIDUCIAL_SIZE - 1.0, panel_y + (panel_h - SMALL_FIDUCIAL) / 2.0, SMALL_FIDUCIAL, SMALL_FIDUCIAL, fill=1, stroke=0)
    c.rect(panel_x + panel_w + 1.0, panel_y + (panel_h - SMALL_FIDUCIAL) / 2.0, SMALL_FIDUCIAL, SMALL_FIDUCIAL, fill=1, stroke=0)

    # Moldura externa do painel
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.9)
    c.setFillColor(colors.white)
    c.rect(panel_x, panel_y, panel_w, panel_h, fill=1, stroke=1)

    # Faixa superior limpa
    header_h = 15.0
    c.setFillColor(colors.black)
    c.rect(panel_x, panel_y + panel_h - header_h, panel_w, header_h, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.white)
    c.drawString(panel_x + 8, panel_y + panel_h - 11.0, "PAINEL DE DESEMPENHO DO ESTUDANTE")

    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.HexColor("#DDDDDD"))
    c.drawRightString(panel_x + panel_w - 8, panel_y + panel_h - 11.0, "4 ÁREAS DO CONHECIMENTO • 70 QUESTÕES + REDAÇÃO")

    # Colunas com larguras que somam exatamente GRID_W (523.27 pt)
    cols = [
        {"title": "LINGUAGENS", "sub": "Questões 01 a 16", "total": "16", "w": 84.0},
        {"title": "C. HUMANAS", "sub": "Questões 17 a 32", "total": "16", "w": 84.0},
        {"title": "C. NATUREZA", "sub": "Questões 33 a 50", "total": "18", "w": 84.0},
        {"title": "MATEMÁTICA", "sub": "Questões 51 a 70", "total": "20", "w": 84.0},
        {"title": "REDAÇÃO", "sub": "Tema Inclusão", "total": "1000", "w": 93.0},
        {"title": "TOTAL GERAL", "sub": "70 Itens + Redação", "total": "70", "w": panel_w - (84.0 * 4 + 93.0)},
    ]

    table_top_y = panel_y + panel_h - header_h
    row_h_title = 15.0
    row_h_data = 15.0

    curr_x = panel_x
    for col in cols:
        w = col["w"]

        # Cabeçalho da coluna
        c.setFillColor(colors.HexColor("#F0F0F0"))
        c.rect(curr_x, table_top_y - row_h_title, w, row_h_title, fill=1, stroke=1)

        c.setFont("Helvetica-Bold", 6.8)
        c.setFillColor(colors.black)
        c.drawCentredString(curr_x + w / 2.0, table_top_y - 8.5, col["title"])
        c.setFont("Helvetica", 5.6)
        c.setFillColor(colors.HexColor("#444444"))
        c.drawCentredString(curr_x + w / 2.0, table_top_y - 13.5, col["sub"])

        # Linha 1 de pontuação
        c.setStrokeColor(colors.HexColor("#777777"))
        c.setFillColor(colors.white)
        c.rect(curr_x + 2, table_top_y - row_h_title - row_h_data + 2, w - 4, row_h_data - 3, fill=1, stroke=1)

        # Linha 2 de pontuação
        c.rect(curr_x + 2, table_top_y - row_h_title - 2 * row_h_data + 3, w - 4, row_h_data - 3, fill=1, stroke=1)

        if is_gabarito:
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(colors.black)
            if col["title"] == "REDAÇÃO":
                c.drawCentredString(curr_x + w / 2.0, table_top_y - row_h_title - row_h_data + 5.0, "1000 pts")
                c.drawCentredString(curr_x + w / 2.0, table_top_y - row_h_title - 2 * row_h_data + 6.0, "Nota Máxima")
            else:
                c.drawCentredString(curr_x + w / 2.0, table_top_y - row_h_title - row_h_data + 5.0, f"{col['total']} / {col['total']}")
                c.drawCentredString(curr_x + w / 2.0, table_top_y - row_h_title - 2 * row_h_data + 6.0, "100% Acerto")
        else:
            c.setFont("Helvetica", 6.0)
            c.setFillColor(colors.HexColor("#888888"))
            if col["title"] == "REDAÇÃO":
                c.drawCentredString(curr_x + w / 2.0, table_top_y - row_h_title - row_h_data + 5.0, "Nota: _____ / 1000")
                c.drawCentredString(curr_x + w / 2.0, table_top_y - row_h_title - 2 * row_h_data + 6.0, "Faixa: ___________")
            else:
                c.drawCentredString(curr_x + w / 2.0, table_top_y - row_h_title - row_h_data + 5.0, f"Acertos: ___ / {col['total']}")
                c.drawCentredString(curr_x + w / 2.0, table_top_y - row_h_title - 2 * row_h_data + 6.0, "%: _____________")

        curr_x += w


def render_answer_sheet_on_canvas(c, is_gabarito=False, gabarito_oficial=None):
    """Renderiza a página completa do Cartão-Resposta com espaçamento e sem assinatura/frase."""
    y_head = draw_clean_header(c, is_gabarito=is_gabarito)
    y_cand = draw_candidate_name_field(c, start_y=y_head, is_gabarito=is_gabarito)
    
    # Espaço generoso antes das instruções
    y_inst = draw_instructions_bw(c, start_y=y_cand - 6.0)

    # Espaço de respiro antes de começar a grade de questões
    grid_start_y = y_inst - 16.0
    bottom_grid_y, geometry = draw_bubble_grid(c, start_y=grid_start_y, gabarito_oficial=gabarito_oficial)

    # Painel de desempenho no rodapé e fiduciais adicionais
    panel_top_y = 18.0 + 62.0
    draw_extra_fiducials(c, bottom_grid_y=bottom_grid_y, panel_top_y=panel_top_y)
    draw_clean_evaluator_panel(c, is_gabarito=is_gabarito)

    return geometry


def gerar_cartao_resposta_pdf(caminho_saida="simulado_2/resultado/Cartao_Resposta_70Q.pdf", gabarito_oficial=None):
    """Gera o Cartão-Resposta avulso em PDF."""
    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)
    c = canvas.Canvas(caminho_saida, pagesize=A4)

    is_gabarito = (gabarito_oficial is not None and len(gabarito_oficial) > 0)
    geometry = render_answer_sheet_on_canvas(c, is_gabarito=is_gabarito, gabarito_oficial=gabarito_oficial)

    c.save()
    tipo = "GABARITO OFICIAL" if is_gabarito else "CARTÃO EM BRANCO"
    print(f"[OK] {tipo} gerado em: {caminho_saida}")
    return geometry


if __name__ == "__main__":
    gerar_cartao_resposta_pdf()
