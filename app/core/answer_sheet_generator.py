"""
Coletivo • Gerador de Cartão-Resposta (Gabarito OMR) 70 Questões em PDF.
Modelo oficial estilo ENEM otimizado para impressão P&B e máxima precisão OMR:
- Margens seguras de impressão (40 pt) para evitar cortes em qualquer impressora.
- Campo de Nome Completo com respiro vertical entre o rótulo e a caixa.
- Instruções ampliadas e completas com destaque para caneta preta obrigatória.
- Exemplo de preenchimento com bolha 'Correto' 100% preenchida de preto (sem letra vazada).
- Quadrados pretos de alinhamento posicionados EXCLUSIVAMENTE em cima dos locais de marcar o gabarito.
- Bolinhas preenchidas do gabarito simulado 100% coloridas de preto (como marcação de caneta preta).
- Painel 'RESULTADOS' espaçoso e sem placeholders, com linhas 'Acertos' e 'Nota',
  seção de Redação com 5 competências (C1..C5) e Soma Total, e bloco TOTAL GERAL separado.
- Painel omitido no Gabarito Oficial (exibido apenas no Cartão-Resposta do participante).
- Título do gabarito ajustado para 'GABARITO OFICIAL'.
"""

import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

PAGE_WIDTH, PAGE_HEIGHT = A4

GRID_MARGIN_X = 40.0
GRID_W = PAGE_WIDTH - 2 * GRID_MARGIN_X
GAP_COLUMNS = 8.0
COL_W = (GRID_W - 3 * GAP_COLUMNS) / 4.0

HEADER_H = 17.0
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
    """Desenha cabeçalho oficial do cartão com margem segura de impressão e respiro ampliado."""
    start_y = PAGE_HEIGHT - 40.0

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    titulo = "GABARITO OFICIAL" if is_gabarito else "CARTÃO-RESPOSTA"
    c.drawString(GRID_MARGIN_X, start_y, titulo)

    c.setFont("Helvetica-Bold", 7.8)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(GRID_MARGIN_X, start_y - 12.0, "2º SIMULADO UNIFICADO • COLETIVO VOA VOA & PREPARATÓRIO GABARITA")

    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.line(GRID_MARGIN_X, start_y - 17.0, GRID_MARGIN_X + GRID_W, start_y - 17.0)

    # Espaço maior de respiro antes do campo de identificação do participante
    return start_y - 36.0


def draw_candidate_name_field(c, start_y, is_gabarito=False):
    """
    Desenha o campo de identificação com:
    - À esquerda: Nome Completo do Participante
    - À direita: Seleção de Unidade (Coletivo Voa Voa ou Preparatório Gabarita)
    """
    gap_fields = 10.0
    name_w = 320.0
    unit_w = GRID_W - name_w - gap_fields
    box_h = 24.0

    box_name_x = GRID_MARGIN_X
    box_unit_x = box_name_x + name_w + gap_fields

    # Rótulos alinhados
    c.setFont("Helvetica-Bold", 7.2)
    c.setFillColor(colors.black)
    c.drawString(box_name_x, start_y, "NOME COMPLETO DO PARTICIPANTE:")
    c.drawString(box_unit_x, start_y, "UNIDADE:")

    box_top_y = start_y - 4.5
    box_y = box_top_y - box_h

    # 1. Caixa do Nome Completo
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.setFillColor(colors.white)
    c.rect(box_name_x, box_y, name_w, box_h, fill=1, stroke=1)

    if is_gabarito:
        c.setFont("Helvetica-Bold", 9.0)
        c.setFillColor(colors.black)
        c.drawString(box_name_x + 10, box_y + 7.5, "FOLHA DE RESPOSTAS PADRÃO — GABARITO OFICIAL")

    # 2. Caixa de Seleção de Unidade
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.white)
    c.rect(box_unit_x, box_y, unit_w, box_h, fill=1, stroke=1)

    # Opções de Unidade com bolhas de marcação
    r_bubble = 3.4
    opt1_y = box_y + 15.5
    opt2_y = box_y + 6.0
    opt_x = box_unit_x + 9.0
    text_x = box_unit_x + 17.5

    # Opção 1: Coletivo Voa Voa
    c.setLineWidth(0.7)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.white)
    c.circle(opt_x, opt1_y, r_bubble, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 6.2)
    c.setFillColor(colors.black)
    c.drawString(text_x, opt1_y - 2.2, "Coletivo Voa Voa (Novo Riacho)")

    # Opção 2: Preparatório Gabarita
    c.setFillColor(colors.white)
    c.circle(opt_x, opt2_y, r_bubble, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 6.2)
    c.setFillColor(colors.black)
    c.drawString(text_x, opt2_y - 2.2, "Preparatório Gabarita (Jardim Laguna)")

    return box_y


def draw_instructions_bw(c, start_y):
    """
    Desenha instruções de preenchimento destacando a caneta preta obrigatória.
    Exemplos de Correto e Incorretos organizados verticalmente (um em cima do outro) à direita.
    """
    bar_x = GRID_MARGIN_X
    bar_w = GRID_W
    bar_h = 36.0
    bar_y = start_y - bar_h

    c.setStrokeColor(colors.HexColor("#333333"))
    c.setFillColor(colors.HexColor("#FAFAFA"))
    c.setLineWidth(0.7)
    c.rect(bar_x, bar_y, bar_w, bar_h, fill=1, stroke=1)

    # Texto à esquerda
    c.setFont("Helvetica-Bold", 7.4)
    c.setFillColor(colors.black)
    c.drawString(bar_x + 8, bar_y + bar_h - 9.5, "INSTRUÇÕES DE PREENCHIMENTO:")

    c.setFont("Helvetica", 6.5)
    c.setFillColor(colors.HexColor("#222222"))
    c.drawString(bar_x + 8, bar_y + bar_h - 19.0, "• Preencha a bolha por completo utilizando EXCLUSIVAMENTE caneta esferográfica de tinta PRETA (tubo transparente).")
    c.drawString(bar_x + 8, bar_y + bar_h - 28.5, "• É ESTRITAMENTE PROIBIDO O USO DE CANETA AZUL, lápis ou corretivo. Marque apenas uma opção por questão.")

    # Bloco de exemplos empilhados verticalmente à direita
    ex_block_w = 115.0
    ex_x = bar_x + bar_w - ex_block_w - 6.0

    # Linha divisória sutil vertical separando o texto dos exemplos
    c.setStrokeColor(colors.HexColor("#D8D8D8"))
    c.setLineWidth(0.6)
    c.line(ex_x - 10.0, bar_y + 4.0, ex_x - 10.0, bar_y + bar_h - 4.0)

    # 1. Linha Superior: Correto
    y_correto = bar_y + bar_h - 13.0
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.black)
    c.drawString(ex_x, y_correto - 2.2, "Correto:")

    c.setFillColor(colors.black)
    c.circle(ex_x + 48.0, y_correto, 4.2, fill=1, stroke=1)

    # 2. Linha Inferior: Incorretos
    y_incorreto = bar_y + 10.5
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.black)
    c.drawString(ex_x, y_incorreto - 2.2, "Incorretos:")

    # Incorreto 1: Com X
    c.setFillColor(colors.white)
    c.circle(ex_x + 48.0, y_incorreto, 4.2, fill=1, stroke=1)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.line(ex_x + 45.0, y_incorreto - 3, ex_x + 51.0, y_incorreto + 3)
    c.line(ex_x + 45.0, y_incorreto + 3, ex_x + 51.0, y_incorreto - 3)

    # Incorreto 2: Com traço
    c.circle(ex_x + 66.0, y_incorreto, 4.2, fill=1, stroke=1)
    c.line(ex_x + 63.0, y_incorreto - 3, ex_x + 69.0, y_incorreto + 3)

    # Incorreto 3: Ponto central
    c.circle(ex_x + 84.0, y_incorreto, 4.2, fill=1, stroke=1)
    c.setFillColor(colors.black)
    c.circle(ex_x + 84.0, y_incorreto, 1.4, fill=1, stroke=1)

    return bar_y


def draw_bubble_grid(c, start_y, gabarito_oficial=None):
    """
    Desenha o grid das 70 questões:
    - Quadrados pretos de alinhamento em volta do espaço de marcar as respostas (topo, rodapé e cantos laterais).
    - Bolinhas preenchidas do gabarito 100% pretas (como preenchimento real de caneta).
    """
    grid_top_y = start_y
    grid_h = HEADER_H + MAX_ROWS * ROW_H
    grid_bottom_y = grid_top_y - grid_h

    marker_s = 8.0
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)

    # 1. Marcadores pretos em cima de cada uma das 4 colunas
    for col_idx in range(4):
        cx = GRID_MARGIN_X + col_idx * (COL_W + GAP_COLUMNS)
        c.rect(cx + (COL_W - marker_s) / 2.0, grid_top_y + 4.0, marker_s, marker_s, fill=1, stroke=0)

    # 2. Marcadores pretos embaixo de cada uma das 4 colunas
    for col_idx in range(4):
        cx = GRID_MARGIN_X + col_idx * (COL_W + GAP_COLUMNS)
        c.rect(cx + (COL_W - marker_s) / 2.0, grid_bottom_y - 12.0, marker_s, marker_s, fill=1, stroke=0)

    # 3. Marcadores pretos fiduciais nas laterais delimitando o bloco de questões
    f_size = 9.0
    # Canto superior esquerdo e direito (alinhados com a primeira linha de respostas)
    c.rect(GRID_MARGIN_X - 16.0, grid_top_y - HEADER_H - 2.0, f_size, f_size, fill=1, stroke=0)
    c.rect(GRID_MARGIN_X + GRID_W + 7.0, grid_top_y - HEADER_H - 2.0, f_size, f_size, fill=1, stroke=0)
    # Canto inferior esquerdo e direito (alinhados com a última linha de respostas)
    c.rect(GRID_MARGIN_X - 16.0, grid_bottom_y + 4.0, f_size, f_size, fill=1, stroke=0)
    c.rect(GRID_MARGIN_X + GRID_W + 7.0, grid_bottom_y + 4.0, f_size, f_size, fill=1, stroke=0)

    geometry = {
        "questions": {}
    }

    # Desenha as 4 Colunas com cabeçalhos e bolhas
    col_content_y = grid_top_y

    for col_idx, col_def in enumerate(COLUMNS_DEF):
        cx = GRID_MARGIN_X + col_idx * (COL_W + GAP_COLUMNS)
        cy = col_content_y

        c.setFillColor(colors.HexColor("#222222"))
        c.rect(cx, cy - HEADER_H, COL_W, HEADER_H, fill=1, stroke=0)

        c.setFont("Helvetica-Bold", 7.2)
        c.setFillColor(colors.white)
        c.drawCentredString(cx + COL_W / 2.0, cy - 12.0, col_def["title"])

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

            c.setFont("Helvetica-Bold", 8.0)
            c.setFillColor(colors.black)
            c.drawString(cx + 4, row_y - 2.8, f"{q_num:02d}")

            first_opt_x = cx + 30.0
            geometry["questions"][q_num] = {}
            resp_correta = (gabarito_oficial.get(q_num, "") or "").strip().upper() if gabarito_oficial else ""

            for opt_idx, opt_letter in enumerate(OPTIONS):
                bx = first_opt_x + opt_idx * OPT_DX
                by = row_y

                is_correct = (opt_letter == resp_correta)

                c.setStrokeColor(colors.black)
                c.setLineWidth(0.7)

                if is_correct:
                    # Totalmente colorida de preto (como estudante marcando com caneta preta)
                    c.setFillColor(colors.black)
                    c.circle(bx, by, BUBBLE_RADIUS, fill=1, stroke=1)
                else:
                    c.setFillColor(colors.white)
                    c.circle(bx, by, BUBBLE_RADIUS, fill=1, stroke=1)
                    c.setFont("Helvetica-Bold", 6.8)
                    c.setFillColor(colors.black)
                    c.drawCentredString(bx, by - 2.2, opt_letter)

                geometry["questions"][q_num][opt_letter] = (bx, by, BUBBLE_RADIUS)

    return grid_bottom_y, geometry


def draw_clean_evaluator_panel(c):
    """
    Desenha o painel 'RESULTADOS' no rodapé inferior da folha do aluno:
    - Rótulos das linhas: 'Acertos' e 'Nota'
    - 4 colunas para as áreas objetivas (Linguagens, Humanas, Natureza, Matemática)
    - Seção de REDAÇÃO com 5 competências (C1 a C5) e Soma Total abaixo
    - Bloco TOTAL GERAL / MÉDIA destacado e separado
    - Espaçamento amplo e sem placeholders intrusivos
    """
    panel_x = GRID_MARGIN_X
    panel_w = GRID_W
    panel_h = 84.0
    panel_y = 40.0  # Margem segura para não cortar na impressão (40 pt da borda inferior)

    # Moldura externa do painel
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.setFillColor(colors.white)
    c.rect(panel_x, panel_y, panel_w, panel_h, fill=1, stroke=1)

    # Faixa de título: RESULTADOS + AVISO DE USO EXCLUSIVO
    header_h = 16.0
    c.setFillColor(colors.black)
    c.rect(panel_x, panel_y + panel_h - header_h, panel_w, header_h, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 8.8)
    c.setFillColor(colors.white)
    c.drawString(panel_x + 10.0, panel_y + panel_h - 11.5, "RESULTADOS")

    # Aviso explícito para o aluno não preencher este painel
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.HexColor("#FFCCCC"))
    c.drawRightString(panel_x + panel_w - 10.0, panel_y + panel_h - 11.5, "USO EXCLUSIVO DOS AVALIADORES • NÃO PREENCHER")

    # Dimensões da tabela
    table_top_y = panel_y + panel_h - header_h
    row_h_title = 18.0
    row_h_data = 25.0

    w_lbl = 54.0
    w_area = 58.0
    w_red = 145.0
    w_tot = panel_w - (w_lbl + 4 * w_area + w_red)

    # 1. Coluna de Rótulos das Linhas (Acertos e Nota)
    c.setFillColor(colors.HexColor("#F0F0F0"))
    c.rect(panel_x, table_top_y - row_h_title, w_lbl, row_h_title, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.HexColor("#444444"))
    c.drawCentredString(panel_x + w_lbl / 2.0, table_top_y - 11.5, "AVALIAÇÃO")

    # Linha Acertos
    c.setFillColor(colors.HexColor("#F8F8F8"))
    c.rect(panel_x, table_top_y - row_h_title - row_h_data, w_lbl, row_h_data, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.black)
    c.drawCentredString(panel_x + w_lbl / 2.0, table_top_y - row_h_title - row_h_data + 9.5, "Acertos")

    # Linha Nota
    c.setFillColor(colors.HexColor("#F8F8F8"))
    c.rect(panel_x, table_top_y - row_h_title - 2 * row_h_data, w_lbl, row_h_data, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.black)
    c.drawCentredString(panel_x + w_lbl / 2.0, table_top_y - row_h_title - 2 * row_h_data + 9.5, "Nota")

    # 2. As 4 Áreas do Conhecimento
    areas = [
        {"title": "LINGUAGENS", "sub": "16 Questões"},
        {"title": "C. HUMANAS", "sub": "16 Questões"},
        {"title": "C. NATUREZA", "sub": "18 Questões"},
        {"title": "MATEMÁTICA", "sub": "20 Questões"},
    ]

    curr_x = panel_x + w_lbl
    for area in areas:
        # Cabeçalho da área
        c.setFillColor(colors.HexColor("#F0F0F0"))
        c.rect(curr_x, table_top_y - row_h_title, w_area, row_h_title, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 6.8)
        c.setFillColor(colors.black)
        c.drawCentredString(curr_x + w_area / 2.0, table_top_y - 8.5, area["title"])
        c.setFont("Helvetica", 5.2)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawCentredString(curr_x + w_area / 2.0, table_top_y - 14.5, area["sub"])

        # Célula Acertos (sem placeholders)
        box_y1 = table_top_y - row_h_title - row_h_data
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#777777"))
        c.rect(curr_x, box_y1, w_area, row_h_data, fill=1, stroke=1)

        # Célula Nota (sem placeholders)
        box_y2 = table_top_y - row_h_title - 2 * row_h_data
        c.rect(curr_x, box_y2, w_area, row_h_data, fill=1, stroke=1)

        curr_x += w_area

    # 3. Seção REDAÇÃO (C1 a C5 + Soma Total)
    red_x = curr_x
    c.setFillColor(colors.HexColor("#F0F0F0"))
    c.rect(red_x, table_top_y - row_h_title, w_red, row_h_title, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 7.2)
    c.setFillColor(colors.black)
    c.drawCentredString(red_x + w_red / 2.0, table_top_y - 8.5, "REDAÇÃO")
    c.setFont("Helvetica", 5.2)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawCentredString(red_x + w_red / 2.0, table_top_y - 14.5, "5 Competências (0 a 200 pts)")

    # Linha 1 de Redação: 5 Competências
    sub_w = w_red / 5.0
    for i in range(5):
        cx_comp = red_x + i * sub_w
        # Mini rótulo da competência
        c.setFillColor(colors.HexColor("#EAEAEA"))
        c.setStrokeColor(colors.HexColor("#888888"))
        c.rect(cx_comp, table_top_y - row_h_title - 7.5, sub_w, 7.5, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 5.8)
        c.setFillColor(colors.black)
        c.drawCentredString(cx_comp + sub_w / 2.0, table_top_y - row_h_title - 6.0, f"C{i+1}")

        # Espaço para nota da competência (sem placeholder)
        c.setFillColor(colors.white)
        c.rect(cx_comp, table_top_y - row_h_title - row_h_data, sub_w, row_h_data - 7.5, fill=1, stroke=1)

    # Linha 2 de Redação: Soma Total
    box_soma_y = table_top_y - row_h_title - 2 * row_h_data
    lbl_soma_w = 55.0
    c.setFillColor(colors.HexColor("#F0F0F0"))
    c.setStrokeColor(colors.HexColor("#777777"))
    c.rect(red_x, box_soma_y, lbl_soma_w, row_h_data, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.black)
    c.drawCentredString(red_x + lbl_soma_w / 2.0, box_soma_y + 9.5, "Soma Total:")

    c.setFillColor(colors.white)
    c.rect(red_x + lbl_soma_w, box_soma_y, w_red - lbl_soma_w, row_h_data, fill=1, stroke=1)

    curr_x += w_red

    # 4. Coluna TOTAL GERAL / MÉDIA (adjacente com divisória padrão da tabela)
    tot_x = curr_x
    c.setFillColor(colors.HexColor("#222222"))
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.rect(tot_x, table_top_y - row_h_title, w_tot, row_h_title, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.white)
    c.drawCentredString(tot_x + w_tot / 2.0, table_top_y - 8.5, "TOTAL GERAL")
    c.setFont("Helvetica", 5.0)
    c.setFillColor(colors.HexColor("#DDDDDD"))
    c.drawCentredString(tot_x + w_tot / 2.0, table_top_y - 14.5, "Desempenho Global")

    # Célula Superior: Soma Total de Acertos (com fundo levemente sombreado mas ótimo para caneta)
    box_tot_y1 = table_top_y - row_h_title - row_h_data
    c.setFillColor(colors.HexColor("#EAEAEA"))
    c.setStrokeColor(colors.HexColor("#777777"))
    c.rect(tot_x, box_tot_y1, w_tot, row_h_data, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 5.8)
    c.setFillColor(colors.HexColor("#444444"))
    c.drawCentredString(tot_x + w_tot / 2.0, box_tot_y1 + row_h_data - 7.5, "TOTAL ACERTOS")

    # Célula Inferior: Média Geral / Nota Final
    box_tot_y2 = table_top_y - row_h_title - 2 * row_h_data
    c.setFillColor(colors.HexColor("#EAEAEA"))
    c.rect(tot_x, box_tot_y2, w_tot, row_h_data, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 5.8)
    c.setFillColor(colors.HexColor("#444444"))
    c.drawCentredString(tot_x + w_tot / 2.0, box_tot_y2 + row_h_data - 7.5, "MÉDIA GERAL")


def render_answer_sheet_on_canvas(c, is_gabarito=False, gabarito_oficial=None):
    """Renderiza a página completa do Cartão-Resposta com espaçamento e margens seguras."""
    y_head = draw_clean_header(c, is_gabarito=is_gabarito)
    y_cand = draw_candidate_name_field(c, start_y=y_head, is_gabarito=is_gabarito)

    # Espaço antes das instruções
    y_inst = draw_instructions_bw(c, start_y=y_cand - 8.0)

    # Centralização vertical precisa da grade de questões (incluindo marcadores ao redor)
    panel_top = 124.0
    grid_start_y = (y_inst + panel_top + 340.0) / 2.0
    bottom_grid_y, geometry = draw_bubble_grid(c, start_y=grid_start_y, gabarito_oficial=gabarito_oficial)

    # Painel de Resultados desenhado SOMENTE no cartão-resposta do estudante (removido no gabarito oficial)
    if not is_gabarito:
        draw_clean_evaluator_panel(c)

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
