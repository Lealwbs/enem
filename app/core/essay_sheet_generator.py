"""
Gerador da Folha Oficial de Redação em PDF.
Modelo padrão ENEM otimizado para legibilidade, conforto de escrita e impressão:
- Campo de Nome Completo em caixa única para escrita manual normal.
- Instruções oficiais compactas padronizadas do ENEM com alerta de caneta preta.
- 30 linhas pautadas com altura confortável (~21.6 pt / 7.6 mm) para escrita manual.
- Marcadores fiduciais nos cantos extremos para alinhamento e digitalização.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

PAGE_WIDTH, PAGE_HEIGHT = A4

FIDUCIAL_SIZE = 16.0
FIDUCIAL_MARGIN = 24.0


def draw_essay_fiducials(c):
    """Desenha 4 marcadores nos cantos extremos para alinhamento OMR."""
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    c.rect(FIDUCIAL_MARGIN, PAGE_HEIGHT - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    c.rect(PAGE_WIDTH - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, PAGE_HEIGHT - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    c.rect(FIDUCIAL_MARGIN, FIDUCIAL_MARGIN, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    c.rect(PAGE_WIDTH - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_MARGIN, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)


def draw_essay_compact_header(c, start_y, is_model=False):
    """Desenha cabeçalho oficial da folha de redação."""
    box_x = FIDUCIAL_MARGIN + 20
    box_w = PAGE_WIDTH - 2 * (FIDUCIAL_MARGIN + 20)

    # 1. Título e Subtítulo
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.black)
    c.drawString(box_x, start_y, "FOLHA DE REDAÇÃO DEFINITIVA")

    c.setFont("Helvetica-Bold", 7.6)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawRightString(box_x + box_w, start_y + 1, "2º SIMULADO UNIFICADO • COLETIVO VOA VOA & GABARITA")

    # 2. Campo para Nome Completo do Participante
    name_label_y = start_y - 18
    c.setFont("Helvetica-Bold", 7.0)
    c.setFillColor(colors.black)
    c.drawString(box_x, name_label_y, "NOME COMPLETO DO PARTICIPANTE:")

    name_box_y = name_label_y - 18
    name_box_h = 18.0
    c.setStrokeColor(colors.HexColor("#333333"))
    c.setLineWidth(0.8)
    c.setFillColor(colors.white)
    c.rect(box_x, name_box_y, box_w, name_box_h, fill=1, stroke=1)

    if is_model:
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(colors.black)
        c.drawString(box_x + 8, name_box_y + 5, "FOLHA MODELO OFICIAL — VERSO DO CARTÃO-RESPOSTA")
    else:
        c.setFont("Helvetica-Oblique", 7.0)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(box_x + 8, name_box_y + 5, "(Escreva seu nome legível exclusivamente a caneta esferográfica preta)")

    # 3. Caixa de Instruções Oficiais da Redação
    inst_box_y = name_box_y - 42
    inst_box_h = 36.0

    c.setStrokeColor(colors.HexColor("#555555"))
    c.setLineWidth(0.6)
    c.setFillColor(colors.HexColor("#F9F9F9"))
    c.rect(box_x, inst_box_y, box_w, inst_box_h, fill=1, stroke=1)

    # Faixa lateral "INSTRUÇÕES"
    c.saveState()
    c.translate(box_x + 9, inst_box_y + 4)
    c.rotate(90)
    c.setFont("Helvetica-Bold", 6.2)
    c.setFillColor(colors.black)
    c.drawString(0, 0, "INSTRUÇÕES")
    c.restoreState()

    c.setStrokeColor(colors.HexColor("#777777"))
    c.setLineWidth(0.5)
    c.line(box_x + 13, inst_box_y, box_x + 13, inst_box_y + inst_box_h)

    # Textos oficiais do ENEM em 2 colunas
    col1_x = box_x + 18
    col2_x = box_x + 258

    c.setFont("Helvetica", 6.0)
    c.setFillColor(colors.HexColor("#222222"))

    c.drawString(col1_x, inst_box_y + 25, "• Escreva sua redação com caneta esferográfica de tinta preta transparente.")
    c.drawString(col1_x, inst_box_y + 15, "• Não utilize corretivo ou borracha. Em caso de erro, risque com um traço simples.")
    c.drawString(col1_x, inst_box_y + 5, "• Escreva com letra legível. Não será avaliado texto escrito fora das 30 linhas.")

    c.drawString(col2_x, inst_box_y + 25, "• Respeite os direitos humanos e não se identifique no espaço do texto.")
    c.drawString(col2_x, inst_box_y + 15, "• Redação com até 7 linhas será considerada 'em branco' (nota zero).")
    c.drawString(col2_x, inst_box_y + 5, "• Textos que fujam ao tema ou desobedeçam ao padrão dissertativo serão zerados.")

    return inst_box_y - 10


def draw_essay_30_lines(c, start_y):
    """Desenha a grade de 30 linhas pautadas oficiais."""
    margin_x = FIDUCIAL_MARGIN + 20
    box_w = PAGE_WIDTH - 2 * margin_x
    num_col_w = 24.0

    target_bottom = FIDUCIAL_MARGIN + 12
    available_h = start_y - target_bottom
    line_h = min(22.0, available_h / 30.0)
    total_grid_h = 30 * line_h
    grid_y = start_y - total_grid_h

    # Moldura externa da grade
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.setFillColor(colors.white)
    c.rect(margin_x, grid_y, box_w, total_grid_h, fill=1, stroke=1)

    # Linha vertical separando a coluna dos números das linhas
    c.setLineWidth(0.8)
    c.line(margin_x + num_col_w, grid_y, margin_x + num_col_w, start_y)

    # Linhas pautadas horizontais
    for i in range(30):
        y_pos = start_y - (i + 1) * line_h

        # Linha horizontal divisória
        if i < 29:
            c.setStrokeColor(colors.HexColor("#BBBBBB"))
            c.setLineWidth(0.5)
            c.line(margin_x + num_col_w, y_pos, margin_x + box_w, y_pos)

        # Número da linha
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#333333"))
        c.drawCentredString(margin_x + (num_col_w / 2.0), y_pos + (line_h / 2.0) - 2.8, str(i + 1))


def render_essay_sheet_on_canvas(c, is_model=False):
    """Renderiza a folha de redação no canvas."""
    draw_essay_fiducials(c)
    top_y = PAGE_HEIGHT - (FIDUCIAL_MARGIN + 10)
    start_lines_y = draw_essay_compact_header(c, top_y, is_model=is_model)
    draw_essay_30_lines(c, start_lines_y)


def gerar_folha_redacao_pdf(caminho_saida="simulado_2/resultado/Folha_Redacao_Oficial.pdf"):
    """Gera a Folha de Redação avulsa em PDF."""
    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)
    c = canvas.Canvas(caminho_saida, pagesize=A4)

    render_essay_sheet_on_canvas(c, is_model=False)

    c.save()
    print(f"[OK] Folha de Redação gerada em: {caminho_saida}")


if __name__ == "__main__":
    gerar_folha_redacao_pdf()
