"""
Gerador da Folha de Redação Oficial em PDF.
Modelo padrão ENEM otimizado para impressão P&B / Caderno Branco:
- 30 linhas pautadas com espaçamento ampliado para escrita confortável.
- Sem número de série '029' e sem códigos redundantes.
- Identificação do participante, instruções oficiais e marcadores de enquadramento.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

PAGE_WIDTH, PAGE_HEIGHT = A4

FIDUCIAL_SIZE = 16.0
FIDUCIAL_MARGIN = 24.0


def draw_essay_fiducials(c):
    """Desenha 4 quadrados pretos nos cantos extremos para alinhamento."""
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    c.rect(FIDUCIAL_MARGIN, PAGE_HEIGHT - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    c.rect(PAGE_WIDTH - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, PAGE_HEIGHT - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    c.rect(FIDUCIAL_MARGIN, FIDUCIAL_MARGIN, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    c.rect(PAGE_WIDTH - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_MARGIN, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)


def draw_essay_header(c, metadados):
    """Desenha o cabeçalho superior limpo, sem número '029' nem códigos redundantes."""
    # Título principal
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.black)
    c.drawString(FIDUCIAL_MARGIN + 22, PAGE_HEIGHT - 46, "FOLHA DE REDAÇÃO")

    # Subtítulo oficial
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(FIDUCIAL_MARGIN + 22, PAGE_HEIGHT - 58, "EXAME NACIONAL DO ENSINO MÉDIO – ENEM")

    # Indicação do Caderno Branco no topo direito
    caderno_info = f"{metadados.get('caderno_nome', 'CADERNO 1')} | {metadados.get('cor_caderno', 'BRANCO')}"
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.black)
    c.drawRightString(PAGE_WIDTH - FIDUCIAL_MARGIN - 22, PAGE_HEIGHT - 48, caderno_info)


def draw_essay_participant_info(c, start_y):
    """Desenha a seção de identificação do participante e instruções oficiais."""
    box_x = FIDUCIAL_MARGIN + 20
    box_w = PAGE_WIDTH - 2 * (FIDUCIAL_MARGIN + 20)

    # 1. Nome completo do participante
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.black)
    c.drawString(box_x, start_y, "Nome completo do Participante:")

    nome_y = start_y - 18
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.black)
    c.drawString(box_x + 4, nome_y + 4, "NOME ➔")

    num_boxes = 30
    b_size = 14
    b_start = box_x + 55
    c.setStrokeColor(colors.HexColor("#666666"))
    c.setLineWidth(0.6)
    c.setFillColor(colors.white)
    for i in range(num_boxes):
        c.rect(b_start + i * (b_size + 1), nome_y, b_size, b_size, fill=1, stroke=1)

    # 2. CPF e Data de Nascimento (lado esquerdo)
    cpf_y = nome_y - 26
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.black)
    c.drawString(box_x, cpf_y + 13, "CPF / Inscrição:")
    c.drawString(box_x + 4, cpf_y + 2, "CPF ➔")
    c.setFillColor(colors.white)
    for i in range(11):
        c.rect(box_x + 42 + i * 13, cpf_y, 12, 12, fill=1, stroke=1)

    dn_y = cpf_y - 22
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.black)
    c.drawString(box_x, dn_y + 13, "Data de nascimento:")
    c.drawString(box_x + 4, dn_y + 2, "DATA ➔")
    c.setFillColor(colors.white)
    for i in range(8):
        c.rect(box_x + 46 + i * 13, dn_y, 12, 12, fill=1, stroke=1)

    # 3. Assinatura e Caixa de Instruções (lado direito)
    col_right_x = box_x + 215
    col_right_w = box_w - 215

    # Assinatura do Participante
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.black)
    c.drawCentredString(col_right_x + col_right_w / 2.0, cpf_y + 16, "-----------------  Assinatura do Participante  -----------------")

    c.setStrokeColor(colors.HexColor("#777777"))
    c.setDash([2, 2], 0)
    c.line(col_right_x + 10, cpf_y + 3, col_right_x + col_right_w - 10, cpf_y + 3)
    c.setDash([], 0)

    # Caixa de Instruções oficiais
    inst_box_y = dn_y - 4
    inst_box_h = 36
    c.setStrokeColor(colors.HexColor("#444444"))
    c.setLineWidth(0.7)
    c.setFillColor(colors.HexColor("#f8f8f8"))
    c.rect(col_right_x, inst_box_y, col_right_w, inst_box_h, fill=1, stroke=1)

    # Rótulo vertical "INSTRUÇÕES"
    c.saveState()
    c.translate(col_right_x + 8, inst_box_y + 4)
    c.rotate(90)
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.black)
    c.drawString(0, 0, "INSTRUÇÕES")
    c.restoreState()

    c.line(col_right_x + 12, inst_box_y, col_right_x + 12, inst_box_y + inst_box_h)

    # Textos de instrução
    c.setFont("Helvetica", 5.5)
    c.setFillColor(colors.HexColor("#222222"))
    inst_x = col_right_x + 16
    c.drawString(inst_x, inst_box_y + 27, "1. Verifique se seu CPF, nome e data de nascimento estão corretos e preencha-os.")
    c.drawString(inst_x, inst_box_y + 20, "2. Transcreva a sua redação com caneta esferográfica de tinta preta transparente.")
    c.drawString(inst_x, inst_box_y + 13, "3. Não haverá substituição desta FOLHA DE REDAÇÃO por erro de preenchimento.")
    c.drawString(inst_x, inst_box_y + 6, "4. Escreva com letra legível. Em caso de erro, risque com um traço simples.")
    c.drawString(inst_x, inst_box_y - 1, "5. Não será avaliado texto fora das 30 linhas. Respeite rigorosamente as margens.")

    return dn_y - 10


def draw_essay_lines_grid(c, start_y):
    """
    Desenha as 30 linhas pautadas com ESPAÇAMENTO AMPLIADO para escrita confortável.
    Altura aumentada para preencher a folha proporcionalmente e dar mais espaço para a caneta.
    """
    grid_x = FIDUCIAL_MARGIN + 20
    grid_w = PAGE_WIDTH - 2 * (FIDUCIAL_MARGIN + 20)

    num_lines = 30
    line_h = 21.0  # Ampliado para 21pt por linha (escrita muito mais confortável)
    num_col_w = 22.0

    grid_h = num_lines * line_h
    grid_y = start_y - grid_h

    # Borda externa do bloco de linhas (linha preta nítida 1.2pt)
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.rect(grid_x, grid_y, grid_w, grid_h, fill=0, stroke=1)

    # Linha vertical separando a coluna dos números do texto
    c.setLineWidth(0.8)
    c.line(grid_x + num_col_w, grid_y, grid_x + num_col_w, grid_y + grid_h)

    # Linhas horizontais e números
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
        c.drawCentredString(grid_x + num_col_w / 2.0, curr_y - 14.5, str(line_num))

    return grid_y


def draw_essay_footer(c, start_y):
    """Desenha o rodapé limpo com identificação do exame e logos institucionais."""
    footer_y = FIDUCIAL_MARGIN + 10

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.black)
    c.drawString(FIDUCIAL_MARGIN + 22, footer_y + 8, "enem")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(FIDUCIAL_MARGIN + 95, footer_y + 10, "INEP")
    c.setFont("Helvetica", 6.5)
    c.drawString(FIDUCIAL_MARGIN + 125, footer_y + 14, "MINISTÉRIO DA")
    c.drawString(FIDUCIAL_MARGIN + 125, footer_y + 6, "EDUCAÇÃO")

    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#444444"))
    c.drawRightString(PAGE_WIDTH - FIDUCIAL_MARGIN - 22, footer_y + 8, "FOLHA DEFINITIVA • MODELO OFICIAL")


def gerar_folha_redacao_pdf(caminho_saida="provas_geradas/Folha_Redacao_Oficial.pdf", metadados=None):
    """Gera o arquivo PDF oficial da Folha de Redação ampliada."""
    if metadados is None:
        metadados = {
            "titulo_exame": "EXAME NACIONAL DO ENSINO MÉDIO",
            "ano": "2026",
            "caderno_nome": "CADERNO 1",
            "cor_caderno": "BRANCO"
        }

    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)
    c = canvas.Canvas(caminho_saida, pagesize=A4)

    # 1. Marcadores nos 4 cantos
    draw_essay_fiducials(c)

    # 2. Cabeçalho limpo
    draw_essay_header(c, metadados)

    # 3. Painel do participante
    y_after_part = draw_essay_participant_info(c, start_y=PAGE_HEIGHT - 72)

    # 4. Grade de 30 linhas pautadas com altura ampliada (21pt)
    y_after_grid = draw_essay_lines_grid(c, start_y=y_after_part)

    # 5. Rodapé limpo
    draw_essay_footer(c, start_y=y_after_grid)

    c.save()
    print(f"Folha de Redação gerada com sucesso em: {caminho_saida}")


if __name__ == "__main__":
    gerar_folha_redacao_pdf()
