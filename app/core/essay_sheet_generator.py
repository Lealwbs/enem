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
    - Título principal
    - Subtítulo logo abaixo
    - Linha divisória horizontal
    - Campo de nome completo com espaço de respiro após o rótulo
    """
    box_x = MARGIN_X
    box_w = PAGE_WIDTH - 2 * MARGIN_X

    # 1. Título e Subtítulo (semelhante ao Cartão-Resposta Oficial)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawString(box_x, start_y, "FOLHA DE REDAÇÃO DEFINITIVA")

    c.setFont("Helvetica-Bold", 7.8)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(box_x, start_y - 12, "2º SIMULADO UNIFICADO • COLETIVO VOA VOA & PREPARATÓRIO GABARITA")

    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.line(box_x, start_y - 16, box_x + box_w, start_y - 16)

    # 2. Campo para Nome Completo do Participante
    name_label_y = start_y - 28.0
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.black)
    c.drawString(box_x, name_label_y, "NOME COMPLETO DO PARTICIPANTE:")

    # Espaço pequeno (respiro) após o texto antes da caixa
    name_box_top = name_label_y - 4.5
    name_box_h = 22.0
    name_box_y = name_box_top - name_box_h

    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.setFillColor(colors.white)
    c.rect(box_x, name_box_y, box_w, name_box_h, fill=1, stroke=1)

    if is_model:
        c.setFont("Helvetica-Bold", 9.0)
        c.setFillColor(colors.black)
        c.drawString(box_x + 10, name_box_y + 6.5, "FOLHA MODELO OFICIAL — VERSO DO CARTÃO-RESPOSTA")

    return name_box_y - 12.0


def draw_essay_30_lines(c, start_y):
    """Desenha a grade de 30 linhas pautadas oficiais com margens seguras."""
    margin_x = MARGIN_X
    box_w = PAGE_WIDTH - 2 * margin_x
    num_col_w = 24.0

    target_bottom = 32.0  # Margem segura inferior para impressão
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
    """Renderiza a folha de redação no canvas."""
    draw_essay_fiducials(c)
    top_y = PAGE_HEIGHT - 34.0
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
