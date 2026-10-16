"""
Gerador da Folha de Redação Oficial em PDF.
Modelo padrão ENEM otimizado para legibilidade, conforto de escrita e impressão:
- Nome completo em campo contínuo para escrita manual normal (sem quadradinhos).
- Sem CPF, sem Data de Nascimento e sem campo de Assinatura.
- Sem títulos e rodapés redundantes ("CADERNO 1 | BRANCO", "FOLHA DEFINITIVA", "enem INEP MINISTÉRIO DA EDUCAÇÃO").
- Instruções oficiais completas padronizadas do ENEM em formato compacto.
- 30 linhas pautadas com altura ampliada (~21.6 pt / 7.6 mm) para máxima legibilidade e conforto.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

PAGE_WIDTH, PAGE_HEIGHT = A4

FIDUCIAL_SIZE = 16.0
FIDUCIAL_MARGIN = 24.0


def draw_essay_fiducials(c):
    """Desenha 4 marcadores nos cantos extremos para alinhamento e escaneamento OMR."""
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    c.rect(FIDUCIAL_MARGIN, PAGE_HEIGHT - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    c.rect(PAGE_WIDTH - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, PAGE_HEIGHT - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    c.rect(FIDUCIAL_MARGIN, FIDUCIAL_MARGIN, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    c.rect(PAGE_WIDTH - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_MARGIN, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)


def draw_essay_compact_header(c, start_y):
    """
    Desenha cabeçalho compacto, campo de nome contínuo e instruções oficiais do ENEM.
    Retorna o valor de 'y' onde a grade de 30 linhas deve iniciar.
    """
    box_x = FIDUCIAL_MARGIN + 20
    box_w = PAGE_WIDTH - 2 * (FIDUCIAL_MARGIN + 20)

    # 1. Título e subtítulo elegantes e compactos
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(colors.black)
    c.drawString(box_x, start_y, "FOLHA DE REDAÇÃO")

    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#444444"))
    c.drawString(box_x + 180, start_y + 1, "EXAME NACIONAL DO ENSINO MÉDIO")

    # 2. Campo para Nome Completo do Participante (escrita manual normal em caixa única)
    name_label_y = start_y - 18
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.black)
    c.drawString(box_x, name_label_y, "NOME COMPLETO DO PARTICIPANTE:")

    name_box_y = name_label_y - 20
    name_box_h = 18.0
    c.setStrokeColor(colors.HexColor("#333333"))
    c.setLineWidth(0.8)
    c.setFillColor(colors.white)
    c.rect(box_x, name_box_y, box_w, name_box_h, fill=1, stroke=1)

    # Dica sutil em cinza claro para o participante
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawString(box_x + 8, name_box_y + 5, "(Escreva seu nome legível a caneta preta)")

    # 3. Caixa de Instruções Oficiais da Redação (Compacta em 2 Colunas)
    inst_box_y = name_box_y - 48
    inst_box_h = 42.0

    c.setStrokeColor(colors.HexColor("#555555"))
    c.setLineWidth(0.6)
    c.setFillColor(colors.HexColor("#F9F9F9"))
    c.rect(box_x, inst_box_y, box_w, inst_box_h, fill=1, stroke=1)

    # Faixa lateral "INSTRUÇÕES"
    c.saveState()
    c.translate(box_x + 9, inst_box_y + 4)
    c.rotate(90)
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.black)
    c.drawString(0, 0, "INSTRUÇÕES")
    c.restoreState()

    c.setStrokeColor(colors.HexColor("#777777"))
    c.setLineWidth(0.5)
    c.line(box_x + 13, inst_box_y, box_x + 13, inst_box_y + inst_box_h)

    # Textos oficiais do ENEM distribuídos em 2 colunas
    col1_x = box_x + 18
    col2_x = box_x + 258

    c.setFont("Helvetica", 5.8)
    c.setFillColor(colors.HexColor("#222222"))

    # Coluna 1
    c.drawString(col1_x, inst_box_y + 31, "• Escreva sua redação com caneta esferográfica de tinta preta transparente.")
    c.drawString(col1_x, inst_box_y + 19, "• Não utilize corretivo ou borracha. Em caso de erro, risque com um traço simples.")
    c.drawString(col1_x, inst_box_y + 7, "• Escreva com letra legível. Não será avaliado texto escrito fora das 30 linhas.")

    # Coluna 2
    c.drawString(col2_x, inst_box_y + 31, "• A redação com até 7 linhas escritas será considerada insuficiente (nota zero).")
    c.drawString(col2_x, inst_box_y + 19, "• Não assine nem faça qualquer marca identificadora no espaço do texto.")
    c.drawString(col2_x, inst_box_y + 7, "• Não haverá substituição desta folha de redação por erro de preenchimento.")

    return inst_box_y - 8


def draw_essay_lines_grid(c, start_y):
    """
    Desenha as 30 linhas pautadas com ESPAÇAMENTO AMPLIADO (~21.6 pt / 7.6 mm).
    Proporciona máximo espaço vertical e conforto caligráfico para o candidato.
    """
    grid_x = FIDUCIAL_MARGIN + 20
    grid_w = PAGE_WIDTH - 2 * (FIDUCIAL_MARGIN + 20)

    num_lines = 30
    line_h = 21.6  # Altura confortável (7.62 mm)
    num_col_w = 22.0

    grid_h = num_lines * line_h
    grid_y = start_y - grid_h

    # Borda externa do bloco de linhas (linha preta nítida 1.2pt)
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.rect(grid_x, grid_y, grid_w, grid_h, fill=0, stroke=1)

    # Linha vertical separando a coluna dos números do espaço de escrita
    c.setLineWidth(0.8)
    c.line(grid_x + num_col_w, grid_y, grid_x + num_col_w, grid_y + grid_h)

    # Linhas horizontais e números de 1 a 30
    for i in range(num_lines):
        line_num = i + 1
        curr_y = grid_y + (num_lines - i) * line_h

        # Linha horizontal divisória
        if i > 0:
            c.setStrokeColor(colors.HexColor("#555555"))
            c.setLineWidth(0.6)
            c.line(grid_x, curr_y, grid_x + grid_w, curr_y)

        # Número da linha (1 a 30)
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(colors.black)
        c.drawCentredString(grid_x + num_col_w / 2.0, curr_y - 15.0, str(line_num))

    return grid_y


def gerar_folha_redacao_pdf(caminho_saida="provas_geradas/Folha_Redacao_Oficial.pdf", metadados=None):
    """
    Gera a Folha Oficial de Redação com cabeçalho compacto,
    sem campos desnecessários (CPF, data de nascimento, assinatura, logos de rodapé)
    e com espaço máximo dedicado às 30 linhas pautadas.
    """
    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)
    c = canvas.Canvas(caminho_saida, pagesize=A4)

    # 1. Marcadores nos 4 cantos
    draw_essay_fiducials(c)

    # 2. Cabeçalho compacto, nome em caixa única e instruções oficiais
    y_start_grid = draw_essay_compact_header(c, start_y=PAGE_HEIGHT - 48)

    # 3. Grade de 30 linhas pautadas com altura ampliada
    draw_essay_lines_grid(c, start_y=y_start_grid)

    c.save()
    print(f"Folha de Redação gerada com sucesso em: {caminho_saida}")


if __name__ == "__main__":
    gerar_folha_redacao_pdf()
