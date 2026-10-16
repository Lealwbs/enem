"""
================================================================================
Simulado Coletivo • Gerador de Cartão-Resposta (Gabarito OMR) 70 Questões em PDF
Modelo oficial estilo ENEM otimizado para impressão P&B e máxima legibilidade:
- Sem código de barras, sem '* 010175BR1 *', sem '1º DIA' e sem subtítulo redundante.
- Sem CPF, sem Data de Nascimento, sem Assinatura e sem Transcrição de Frase da capa.
- Campo de Nome Completo em caixa única para escrita manual normal (sem quadradinhos).
- Instruções de preenchimento modernas e 100% em Preto e Branco com exemplos visuais.
- 4 Marcadores fiduciais nos cantos da grade de 70 questões para homografia precisa OMR.
- Painel de Avaliação da Banca no rodapé baseado no boletim de desempenho (Média,
  Linguagens 16Q, Humanas 16Q, Natureza 18Q, Matemática 20Q e Redação com 5 competências).
- Suporte para geração do Cartão em Branco e do Cartão com Gabarito Oficial preenchido.
================================================================================
"""

import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

PAGE_WIDTH, PAGE_HEIGHT = A4

FIDUCIAL_SIZE = 16.0
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

COLUMNS_DEF = [
    {"start": 1, "end": 18, "title": "QUESTÕES 01 a 18"},
    {"start": 19, "end": 36, "title": "QUESTÕES 19 a 36"},
    {"start": 37, "end": 54, "title": "QUESTÕES 37 a 54"},
    {"start": 55, "end": 70, "title": "QUESTÕES 55 a 70"},
]


def draw_clean_header(c, is_gabarito=False):
    """Desenha cabeçalho limpo, sem códigos de barras ou textos redundantes."""
    start_y = PAGE_HEIGHT - 38

    c.setFont("Helvetica-Bold", 19)
    c.setFillColor(colors.black)
    titulo = "GABARITO OFICIAL — 70 QUESTÕES" if is_gabarito else "CARTÃO-RESPOSTA"
    c.drawString(GRID_MARGIN_X, start_y, titulo)

    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor("#444444"))
    c.drawString(GRID_MARGIN_X, start_y - 12, "EXAME NACIONAL DO ENSINO MÉDIO • 2º SIMULADO PREPARATÓRIO")

    # Linha divisória preta de alto contraste
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.line(GRID_MARGIN_X, start_y - 18, GRID_MARGIN_X + GRID_W, start_y - 18)

    return start_y - 24


def draw_candidate_name_field(c, start_y, is_gabarito=False):
    """Desenha campo de nome contínuo para escrita normal sem quadradinhos."""
    box_x = GRID_MARGIN_X
    box_w = GRID_W
    box_h = 24.0
    box_y = start_y - box_h

    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.black)
    c.drawString(box_x, start_y, "NOME COMPLETO DO PARTICIPANTE:")

    # Caixa contínua de escrita
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.setFillColor(colors.white)
    c.rect(box_x, box_y, box_w, box_h, fill=1, stroke=1)

    if is_gabarito:
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(colors.black)
        c.drawString(box_x + 10, box_y + 7, "GABARITO OFICIAL DEFINITIVO — 2º SIMULADO PREPARATÓRIO ENEM")
    else:
        c.setFont("Helvetica-Oblique", 7.5)
        c.setFillColor(colors.HexColor("#777777"))
        c.drawString(box_x + 8, box_y + 8, "(Escreva seu nome legível a caneta esferográfica preta)")

    return box_y - 6


def draw_instructions_bw(c, start_y):
    """Desenha barra de instruções elegante, compacta e 100% em Preto e Branco."""
    bar_x = GRID_MARGIN_X
    bar_w = GRID_W
    bar_h = 32.0
    bar_y = start_y - bar_h

    # Borda fina preta e fundo cinza muito suave
    c.setStrokeColor(colors.HexColor("#444444"))
    c.setFillColor(colors.HexColor("#F8F8F8"))
    c.setLineWidth(0.7)
    c.rect(bar_x, bar_y, bar_w, bar_h, fill=1, stroke=1)

    # Título das instruções
    c.setFont("Helvetica-Bold", 7.2)
    c.setFillColor(colors.black)
    c.drawString(bar_x + 8, bar_y + bar_h - 10, "INSTRUÇÕES DE PREENCHIMENTO:")

    # Texto das instruções
    c.setFont("Helvetica", 6.3)
    c.setFillColor(colors.HexColor("#222222"))
    c.drawString(bar_x + 8, bar_y + bar_h - 19, "• Preencha completamente a bolha da opção escolhida utilizando caneta esferográfica de tinta preta transparente.")
    c.drawString(bar_x + 8, bar_y + bar_h - 27, "• Não utilize corretivo nem amasse esta folha. A leitura óptica analisa exclusivamente o espaço entre os 4 marcadores.")

    # Exemplos visuais P&B à direita
    ex_x = bar_x + bar_w - 145
    c.setFont("Helvetica-Bold", 6.8)
    c.drawString(ex_x, bar_y + bar_h - 11, "EXEMPLOS:")

    # Correto
    c.setFont("Helvetica", 6.3)
    c.drawString(ex_x, bar_y + bar_h - 23, "Correto:")
    c.setFillColor(colors.black)
    c.circle(ex_x + 36, bar_y + bar_h - 21, 4.2, fill=1, stroke=1)

    # Incorreto
    c.drawString(ex_x + 55, bar_y + bar_h - 23, "Incorreto:")
    c.setFillColor(colors.white)
    c.circle(ex_x + 95, bar_y + bar_h - 21, 4.2, fill=0, stroke=1)
    c.line(ex_x + 92, bar_y + bar_h - 24, ex_x + 98, bar_y + bar_h - 18)
    c.line(ex_x + 92, bar_y + bar_h - 18, ex_x + 98, bar_y + bar_h - 24)

    c.circle(ex_x + 115, bar_y + bar_h - 21, 4.2, fill=0, stroke=1)
    c.circle(ex_x + 115, bar_y + bar_h - 21, 1.8, fill=1, stroke=1)

    return bar_y - 6


def draw_bubble_grid(c, start_y, gabarito_oficial=None):
    """
    Desenha o grid de 70 questões com 4 marcadores fiduciais pretos nos cantos.
    Se gabarito_oficial for fornecido, preenche as bolhas corretas de preto com letra branca.
    """
    cy_top = start_y
    col_content_h = MAX_ROWS * ROW_H + 8
    col_content_y = cy_top - HEADER_H - col_content_h

    # 4 MARCADORES QUADRADOS PRETOS NOS CANTOS DA ÁREA DE QUESTÕES (OMR)
    fid_left_x = GRID_MARGIN_X - 22.0
    fid_right_x = GRID_MARGIN_X + GRID_W + 6.0
    fid_top_y = cy_top - FIDUCIAL_SIZE
    fid_bottom_y = col_content_y

    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    c.rect(fid_left_x, fid_top_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)
    c.rect(fid_right_x, fid_top_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)
    c.rect(fid_left_x, fid_bottom_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)
    c.rect(fid_right_x, fid_bottom_y, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1, stroke=0)

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

        # Cabeçalho da coluna (P&B alto contraste)
        c.setFillColor(colors.black)
        c.rect(cx, cy_top - HEADER_H, COL_W, HEADER_H, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.white)
        c.drawCentredString(cx + COL_W / 2.0, cy_top - HEADER_H + 5.5, col_def["title"])

        # Fundo e borda suave da coluna
        c.setStrokeColor(colors.HexColor("#555555"))
        c.setLineWidth(0.6)
        c.setFillColor(colors.white)
        c.rect(cx, col_content_y, COL_W, col_content_h, fill=1, stroke=1)

        start_q = col_def["start"]
        end_q = col_def["end"]
        num_q = end_q - start_q + 1

        for r in range(num_q):
            q_num = start_q + r
            row_y = cy_top - HEADER_H - 14 - r * ROW_H

            # Linha zebrada sutil para facilitar visualização
            if r % 2 == 1:
                c.setFillColor(colors.HexColor("#F6F6F6"))
                c.rect(cx + 1, row_y - ROW_H / 2.0 + 1, COL_W - 2, ROW_H - 2, fill=1, stroke=0)

            # Número da questão
            c.setFont("Helvetica-Bold", 8.5)
            c.setFillColor(colors.black)
            c.drawString(cx + 5, row_y - 3, f"{q_num:02d}")

            # Bolinhas das alternativas (A a E)
            first_opt_x = cx + 33.0
            geometry["questions"][q_num] = {}

            resp_correta = (gabarito_oficial.get(q_num, "") or "").strip().upper() if gabarito_oficial else ""

            for opt_idx, opt_letter in enumerate(OPTIONS):
                bx = first_opt_x + opt_idx * OPT_DX
                by = row_y

                is_correct_opt = (opt_letter == resp_correta)

                c.setStrokeColor(colors.black)
                c.setLineWidth(0.8)

                if is_correct_opt:
                    # Gabarito: bolha totalmente preenchida de preto com letra branca
                    c.setFillColor(colors.black)
                    c.circle(bx, by, BUBBLE_RADIUS, fill=1, stroke=1)
                    c.setFont("Helvetica-Bold", 7.0)
                    c.setFillColor(colors.white)
                    c.drawCentredString(bx, by - 2.4, opt_letter)
                else:
                    # Cartão normal: bolha branca com borda preta e letra preta
                    c.setFillColor(colors.white)
                    c.circle(bx, by, BUBBLE_RADIUS, fill=1, stroke=1)
                    c.setFont("Helvetica-Bold", 7.0)
                    c.setFillColor(colors.black)
                    c.drawCentredString(bx, by - 2.4, opt_letter)

                geometry["questions"][q_num][opt_letter] = (bx, by, BUBBLE_RADIUS)

    return col_content_y, geometry


def draw_evaluator_panel(c, start_y, is_gabarito=False):
    """
    Desenha o Painel de Correção / Avaliação da Banca no rodapé,
    baseado na estrutura do boletim de desempenho (Média, Linguagens 16Q,
    Humanas 16Q, Natureza 18Q, Matemática 20Q e Redação com as 5 Competências).
    Espaço vazio para preenchimento manual pelo corretor ou preenchido no gabarito oficial.
    """
    panel_x = GRID_MARGIN_X
    panel_w = GRID_W
    panel_h = 88.0
    panel_y = start_y - panel_h - 4

    # 1. Borda externa e fundo
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.setFillColor(colors.white)
    c.rect(panel_x, panel_y, panel_w, panel_h, fill=1, stroke=1)

    # 2. Faixa superior do painel: Título + Alerta ao estudante
    header_h = 16.0
    c.setFillColor(colors.black)
    c.rect(panel_x, panel_y + panel_h - header_h, panel_w, header_h, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.white)
    c.drawString(panel_x + 8, panel_y + panel_h - 11.5, "PAINEL DE CORREÇÃO — USO EXCLUSIVO DO PROFESSOR / AVALIADOR")

    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.HexColor("#EEEEEE"))
    c.drawRightString(panel_x + panel_w - 8, panel_y + panel_h - 11.5, "⚠️ ATENÇÃO: NÃO PREENCHER ESTE CAMPO (RESERVADO À CORREÇÃO)")

    # 3. Divisão em 2 colunas principais:
    # Esquerda: Prova Objetiva (Média, Linguagens, Humanas, Natureza, Matemática) -> largura 355pt
    # Direita: Redação (Nota Total e 5 Competências) -> largura 168pt
    obj_w = 355.0
    red_x = panel_x + obj_w
    red_w = panel_w - obj_w

    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.line(red_x, panel_y, red_x, panel_y + panel_h - header_h)

    # ==========================
    # LADO ESQUERDO: OBJETIVA
    # ==========================
    cols_obj = [
        {"title": "Média / Geral", "qtd": "70", "w": 75.0},
        {"title": "Linguagens",    "qtd": "16", "w": 70.0},
        {"title": "Humanas",       "qtd": "16", "w": 70.0},
        {"title": "Natureza",      "qtd": "18", "w": 70.0},
        {"title": "Matemática",    "qtd": "20", "w": 70.0},
    ]

    table_top_y = panel_y + panel_h - header_h
    row_title_h = 16.0
    row_data_h = 18.0

    # Cabeçalho das matérias objetivas
    curr_x = panel_x
    for col in cols_obj:
        w_c = col["w"]
        # Fundo do cabeçalho
        c.setFillColor(colors.HexColor("#EAEAEA"))
        c.rect(curr_x, table_top_y - row_title_h, w_c, row_title_h, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 7.2)
        c.setFillColor(colors.black)
        c.drawCentredString(curr_x + w_c / 2.0, table_top_y - 11.5, col["title"])
        curr_x += w_c

    # Linha: Nota / Escore
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.black)
    c.drawString(panel_x + 4, table_top_y - row_title_h - 12, "Nota:")

    # Linha: Acertos
    c.drawString(panel_x + 4, table_top_y - row_title_h - row_data_h - 12, "Acertos:")

    # Linha: Qtde. Questões
    c.drawString(panel_x + 4, table_top_y - row_title_h - 2 * row_data_h - 11, "Questões:")

    curr_x = panel_x
    for col in cols_obj:
        w_c = col["w"]
        # Caixas da linha Nota
        c.setStrokeColor(colors.HexColor("#888888"))
        c.rect(curr_x + 3, table_top_y - row_title_h - row_data_h + 2, w_c - 6, row_data_h - 4, fill=0)

        # Caixas da linha Acertos
        c.rect(curr_x + 3, table_top_y - row_title_h - 2 * row_data_h + 2, w_c - 6, row_data_h - 4, fill=0)

        # Texto da linha Qtde. de Questões
        c.setFont("Helvetica", 7.0)
        c.setFillColor(colors.black)
        c.drawCentredString(curr_x + w_c / 2.0, table_top_y - row_title_h - 2 * row_data_h - 11, col["qtd"])

        if is_gabarito:
            c.setFont("Helvetica-Bold", 8.0)
            c.drawCentredString(curr_x + w_c / 2.0, table_top_y - row_title_h - row_data_h + 6, "1000")
            c.drawCentredString(curr_x + w_c / 2.0, table_top_y - row_title_h - 2 * row_data_h + 6, col["qtd"])

        curr_x += w_c

    # ==========================
    # LADO DIREITO: REDAÇÃO
    # ==========================
    # Cabeçalho da Redação
    c.setFillColor(colors.HexColor("#EAEAEA"))
    c.rect(red_x, table_top_y - row_title_h, red_w, row_title_h, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.black)
    c.drawCentredString(red_x + red_w / 2.0, table_top_y - 11.5, "Nota Total Redação: [        / 1000]")

    if is_gabarito:
        c.drawCentredString(red_x + red_w / 2.0, table_top_y - 11.5, "Nota Total Redação: [ 1000 / 1000 ]")

    # 5 Competências da Redação em 2 colunas
    comp_start_y = table_top_y - row_title_h - 11
    comps = [
        ("Comp. 1 (Norma Culta):", 0, 0),
        ("Comp. 2 (Tema/Estrutura):", 0, 12),
        ("Comp. 3 (Argumentação):", 0, 24),
        ("Comp. 4 (Coesão Língua):", 85, 0),
        ("Comp. 5 (Intervenção):", 85, 12),
    ]

    c.setFont("Helvetica", 6.0)
    c.setFillColor(colors.black)
    for lbl, dx, dy in comps:
        cy_pos = comp_start_y - dy
        c.drawString(red_x + 6 + dx, cy_pos, lbl)
        c.setStrokeColor(colors.HexColor("#777777"))
        c.rect(red_x + 6 + dx + 54, cy_pos - 2, 22, 9, fill=0)
        if is_gabarito:
            c.drawCentredString(red_x + 6 + dx + 65, cy_pos, "200")

    # Linha para Visto do Corretor
    visto_y = panel_y + 4
    c.setFont("Helvetica", 6.2)
    c.setFillColor(colors.black)
    c.drawString(panel_x + 8, visto_y, "Visto do Corretor / Avaliador: _______________________________________________")
    c.drawString(red_x + 8, visto_y, "Data da Correção: _____ / _____ / 2026")


def gerar_cartao_resposta_pdf(caminho_saida="provas_geradas/Cartao_Resposta_70Q.pdf", gabarito_oficial=None):
    """
    Gera o arquivo PDF do Cartão-Resposta OMR oficial (70 questões).
    Se gabarito_oficial for passado, gera o Cartão com o Gabarito Oficial preenchido.
    """
    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)
    c = canvas.Canvas(caminho_saida, pagesize=A4)

    is_gabarito = (gabarito_oficial is not None and len(gabarito_oficial) > 0)

    # 1. Cabeçalho limpo sem código de barras nem textos redundantes
    y_after_head = draw_clean_header(c, is_gabarito=is_gabarito)

    # 2. Campo de Nome contínuo (sem quadradinhos)
    y_after_cand = draw_candidate_name_field(c, start_y=y_after_head, is_gabarito=is_gabarito)

    # 3. Barra de instruções elegante e 100% P&B com exemplos visuais
    y_after_inst = draw_instructions_bw(c, start_y=y_after_cand)

    # 4. Grid das 70 questões delimitado exclusivamente pelos 4 marcadores quadrados pretos
    bottom_grid_y, geometry = draw_bubble_grid(c, start_y=y_after_inst, gabarito_oficial=gabarito_oficial)

    # 5. Painel de Correção / Avaliação da Banca no rodapé
    draw_evaluator_panel(c, start_y=bottom_grid_y, is_gabarito=is_gabarito)

    c.save()
    tipo = "GABARITO OFICIAL" if is_gabarito else "CARTÃO EM BRANCO"
    print(f"[OK] {tipo} gerado em: {caminho_saida}")
    return geometry


if __name__ == "__main__":
    gerar_cartao_resposta_pdf()
