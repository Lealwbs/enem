"""
Gerador da Folha Oficial de Redação em PDF.
Modelo padrão ENEM otimizado para legibilidade, conforto de escrita e impressão:
- Margens seguras de impressão (40 pt) para evitar cortes em qualquer impressora.
- Cabeçalho padronizado idêntico ao Cartão-Resposta (Título, subtítulo logo abaixo e linha divisória).
- Campo de Nome Completo com respiro vertical entre o rótulo e a caixa.
- 30 linhas pautadas com altura ampla (~22.5 pt / 7.9 mm) para escrita manual confortável.
- Marcadores fiduciais nos cantos posicionados em margens seguras.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

PAGE_WIDTH, PAGE_HEIGHT = A4

MARGIN_X = 40.0
FIDUCIAL_SIZE = 14.0
FIDUCIAL_MARGIN = 32.0


def draw_essay_fiducials(c):
    """Marcadores de alinhamento desativados para evitar sobreposição com cabeçalho e margens."""
    pass


def draw_essay_compact_header(c, start_y, is_model=False):
    """
    Desenha cabeçalho oficial da folha de redação:
    - Título: FOLHA DE REDAÇÃO
    - Subtítulo logo abaixo com linha divisória
    - Espaço de respiro antes do campo de identificação
    - À esquerda: Nome Completo do Participante
    - À direita: Seleção de Unidade (Coletivo Voa Voa ou Preparatório Gabarita)
    """
    box_x = MARGIN_X
    box_w = PAGE_WIDTH - 2 * MARGIN_X

    # 1. Título e Subtítulo
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawString(box_x, start_y, "FOLHA DE REDAÇÃO")

    c.setFont("Helvetica-Bold", 7.8)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(box_x, start_y - 12.0, "2º SIMULADO UNIFICADO • COLETIVO VOA VOA & PREPARATÓRIO GABARITA")

    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.line(box_x, start_y - 17.0, box_x + box_w, start_y - 17.0)

    # 2. Campo para Nome Completo e Unidade
    name_label_y = start_y - 36.0
    gap_fields = 10.0
    name_w = 320.0
    unit_w = box_w - name_w - gap_fields
    box_h = 24.0

    box_name_x = box_x
    box_unit_x = box_name_x + name_w + gap_fields

    # Rótulos alinhados
    c.setFont("Helvetica-Bold", 7.2)
    c.setFillColor(colors.black)
    c.drawString(box_name_x, name_label_y, "NOME COMPLETO DO PARTICIPANTE:")
    c.drawString(box_unit_x, name_label_y, "UNIDADE:")

    name_box_top = name_label_y - 4.5
    name_box_y = name_box_top - box_h

    # Caixa do Nome Completo
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.setFillColor(colors.white)
    c.rect(box_name_x, name_box_y, name_w, box_h, fill=1, stroke=1)

    if is_model:
        c.setFont("Helvetica-Bold", 9.0)
        c.setFillColor(colors.black)
        c.drawString(box_name_x + 10, name_box_y + 7.5, "FOLHA MODELO OFICIAL — VERSO DO CARTÃO-RESPOSTA")

    # Caixa de Seleção de Unidade
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.white)
    c.rect(box_unit_x, name_box_y, unit_w, box_h, fill=1, stroke=1)

    # Opções de Unidade com bolhas de marcação
    r_bubble = 3.4
    opt1_y = name_box_y + 15.5
    opt2_y = name_box_y + 6.0
    opt_x = box_unit_x + 9.0
    text_x = box_unit_x + 17.5

    # Opção 1: Coletivo Voa Voa
    c.setLineWidth(0.7)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.white)
    c.circle(opt_x, opt1_y, r_bubble, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 6.2)
    c.setFillColor(colors.black)
    c.drawString(text_x, opt1_y - 2.2, "Coletivo Voa Voa (Riacho das Pedras)")

    # Opção 2: Preparatório Gabarita
    c.setFillColor(colors.white)
    c.circle(opt_x, opt2_y, r_bubble, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 6.2)
    c.setFillColor(colors.black)
    c.drawString(text_x, opt2_y - 2.2, "Preparatório Gabarita (Jardim Laguna)")

    return name_box_y - 12.0


def draw_essay_30_lines(c, start_y):
    """Desenha a grade de 30 linhas pautadas oficiais com margens seguras (40 pt)."""
    margin_x = MARGIN_X
    box_w = PAGE_WIDTH - 2 * margin_x
    num_col_w = 24.0

    target_bottom = 40.0  # Margem segura inferior para impressão (40 pt da borda)
    available_h = start_y - target_bottom
    line_h = min(23.0, available_h / 30.0)
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
    """Renderiza a folha de redação no canvas com margem superior segura de 40 pt."""
    draw_essay_fiducials(c)
    top_y = PAGE_HEIGHT - 40.0
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
