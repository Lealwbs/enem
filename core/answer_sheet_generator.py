"""
Gerador de Cartão-Resposta (Gabarito OMR) de 70 Questões em PDF.
Modelo oficial estilo ENEM com 4 marcadores fiduciais nos cantos para alinhamento geométrico perfeito.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib import colors

# Dimensões da página A4 em pontos (595.27 x 841.89)
PAGE_WIDTH, PAGE_HEIGHT = A4

# Configuração dos marcadores fiduciais (quadrados pretos nos 4 cantos)
FIDUCIAL_SIZE = 18.0
FIDUCIAL_MARGIN = 20.0

# Definição das colunas de questões
COLUMNS_DEF = [
    {"start": 1, "end": 18, "title": "QUESTÕES 01 a 18"},
    {"start": 19, "end": 36, "title": "QUESTÕES 19 a 36"},
    {"start": 37, "end": 54, "title": "QUESTÕES 37 a 54"},
    {"start": 55, "end": 70, "title": "QUESTÕES 55 a 70"},
]


def draw_fiducials(c):
    """Desenha 4 quadrados pretos nos cantos extremos para calibração por visão computacional."""
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)

    # Canto superior esquerdo
    c.rect(FIDUCIAL_MARGIN, PAGE_HEIGHT - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    # Canto superior direito
    c.rect(PAGE_WIDTH - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, PAGE_HEIGHT - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    # Canto inferior esquerdo
    c.rect(FIDUCIAL_MARGIN, FIDUCIAL_MARGIN, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)
    # Canto inferior direito
    c.rect(PAGE_WIDTH - FIDUCIAL_MARGIN - FIDUCIAL_SIZE, FIDUCIAL_MARGIN, FIDUCIAL_SIZE, FIDUCIAL_SIZE, fill=1)


def draw_header(c, metadados):
    """Desenha o cabeçalho superior do cartão-resposta."""
    # Código de barras superior
    codigo_caderno = metadados.get("codigo_caderno", "010175AZ1")
    barcode = code128.Code128(codigo_caderno, barWidth=1.0, barHeight=22)
    barcode.drawOn(c, (PAGE_WIDTH - barcode.width) / 2.0, PAGE_HEIGHT - FIDUCIAL_MARGIN - 24)

    # Número do código abaixo do barcode
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - FIDUCIAL_MARGIN - 33, f"* {codigo_caderno} *")

    # Título principal
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor("#0c2340"))  # Azul escuro ENEM
    c.drawString(FIDUCIAL_MARGIN + 28, PAGE_HEIGHT - 65, "CARTÃO-RESPOSTA")

    # Linha decorativa abaixo do título
    c.setStrokeColor(colors.HexColor("#00a4e4"))
    c.setLineWidth(3)
    c.line(FIDUCIAL_MARGIN + 28, PAGE_HEIGHT - 70, FIDUCIAL_MARGIN + 250, PAGE_HEIGHT - 70)

    # Subtítulo
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor("#333333"))
    subtitulo = metadados.get("subtitulo", "SIMULADO DO EXAME NACIONAL DO ENSINO MÉDIO - 70 QUESTÕES")
    c.drawString(FIDUCIAL_MARGIN + 28, PAGE_HEIGHT - 82, subtitulo.upper())

    # Badge do Dia (lado direito)
    dia_box_x = PAGE_WIDTH - FIDUCIAL_MARGIN - 110
    dia_box_y = PAGE_HEIGHT - 85
    c.setStrokeColor(colors.HexColor("#0c2340"))
    c.setLineWidth(1.5)
    c.roundRect(dia_box_x, dia_box_y, 80, 32, 6, fill=0)

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#0c2340"))
    dia_texto = metadados.get("dia", "1º DIA")
    c.drawCentredString(dia_box_x + 40, dia_box_y + 11, dia_texto)


def draw_candidate_info(c, start_y):
    """Desenha a caixa de dados do participante (Nome, CPF, Data Nasc, Assinatura, Frase)."""
    box_x = FIDUCIAL_MARGIN + 20
    box_w = PAGE_WIDTH - 2 * (FIDUCIAL_MARGIN + 20)
    box_h = 100
    box_y = start_y - box_h

    # Borda do painel
    c.setStrokeColor(colors.HexColor("#777777"))
    c.setLineWidth(0.8)
    c.setFillColor(colors.HexColor("#fafafa"))
    c.roundRect(box_x, box_y, box_w, box_h, 4, fill=1, stroke=1)

    # Nome Completo
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#222222"))
    c.drawString(box_x + 8, box_y + box_h - 14, "Nome Completo:")

    # Quadrículas para letras do nome
    num_boxes = 32
    b_start_x = box_x + 8
    b_y = box_y + box_h - 32
    b_size = 14
    c.setStrokeColor(colors.HexColor("#999999"))
    c.setLineWidth(0.5)
    for i in range(num_boxes):
        c.rect(b_start_x + i * (b_size + 1.2), b_y, b_size, b_size)

    # Linha 2: CPF / Data Nasc / Assinatura
    row2_y = box_y + 40
    # CPF
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(box_x + 8, row2_y + 16, "CPF / Inscrição:")
    cpf_boxes = 11
    cpf_size = 12
    for i in range(cpf_boxes):
        c.rect(box_x + 8 + i * (cpf_size + 1), row2_y, cpf_size, cpf_size)

    # Data Nasc
    dn_x = box_x + 160
    c.drawString(dn_x, row2_y + 16, "Data de Nascimento:")
    for i in range(8):
        c.rect(dn_x + i * (cpf_size + 1), row2_y, cpf_size, cpf_size)

    # Assinatura
    ass_x = box_x + 280
    ass_w = box_w - 290
    c.drawString(ass_x, row2_y + 16, "Assinatura do Participante:")
    c.setStrokeColor(colors.HexColor("#444444"))
    c.setDash([2, 2], 0)
    c.line(ass_x, row2_y + 2, ass_x + ass_w, row2_y + 2)
    c.setDash([], 0)

    # Linha 3: Frase de segurança
    row3_y = box_y + 8
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(box_x + 8, row3_y + 16, "Transcreva a frase da capa do seu caderno com caligrafia usual:")
    c.setStrokeColor(colors.HexColor("#777777"))
    c.line(box_x + 8, row3_y + 4, box_x + box_w - 8, row3_y + 4)

    return box_y


def draw_instructions_bar(c, start_y):
    """Desenha barra com instruções de preenchimento e exemplos visuais."""
    bar_x = FIDUCIAL_MARGIN + 20
    bar_w = PAGE_WIDTH - 2 * (FIDUCIAL_MARGIN + 20)
    bar_h = 44
    bar_y = start_y - bar_h - 8

    c.setStrokeColor(colors.HexColor("#00a4e4"))
    c.setFillColor(colors.HexColor("#f0f8fd"))
    c.setLineWidth(0.8)
    c.roundRect(bar_x, bar_y, bar_w, bar_h, 4, fill=1, stroke=1)

    # Texto de instrução à esquerda
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#0c2340"))
    c.drawString(bar_x + 10, bar_y + bar_h - 13, "INSTRUÇÕES DE PREENCHIMENTO:")

    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(bar_x + 10, bar_y + bar_h - 25, "• Utilize apenas caneta esferográfica de tinta preta fabricada em material transparente.")
    c.drawString(bar_x + 10, bar_y + bar_h - 36, "• Preencha completamente o círculo da opção escolhida. Respostas em branco ou rasuradas serão anuladas.")

    # Exemplos visuais à direita
    ex_x = bar_x + bar_w - 170
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(ex_x, bar_y + bar_h - 15, "EXEMPLOS:")

    # Correto
    c.setFont("Helvetica", 7)
    c.drawString(ex_x, bar_y + bar_h - 28, "Correto:")
    c.setFillColor(colors.black)
    c.circle(ex_x + 45, bar_y + bar_h - 26, 4.5, fill=1, stroke=1)

    # Incorreto
    c.drawString(ex_x + 65, bar_y + bar_h - 28, "Incorreto:")
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.black)
    c.circle(ex_x + 115, bar_y + bar_h - 26, 4.5, fill=0, stroke=1)
    # desenha um X sobre a bolinha
    c.line(ex_x + 112, bar_y + bar_h - 29, ex_x + 118, bar_y + bar_h - 23)
    c.line(ex_x + 112, bar_y + bar_h - 23, ex_x + 118, bar_y + bar_h - 29)

    c.circle(ex_x + 135, bar_y + bar_h - 26, 4.5, fill=0, stroke=1)
    # desenha um traço simples
    c.line(ex_x + 132, bar_y + bar_h - 26, ex_x + 138, bar_y + bar_h - 26)

    return bar_y


def draw_bubble_grid(c, start_y):
    """
    Desenha o grid de 70 questões divididas em 4 blocos/colunas:
    - Coluna 1: Q01 a Q18
    - Coluna 2: Q19 a Q36
    - Coluna 3: Q37 a Q54
    - Coluna 4: Q55 a Q70

    Retorna o dicionário de geometria teórica com as coordenadas de cada bolinha.
    """
    grid_x = FIDUCIAL_MARGIN + 20
    grid_w = PAGE_WIDTH - 2 * (FIDUCIAL_MARGIN + 20)
    col_w = (grid_w - 3 * 10) / 4.0  # 4 colunas com gap de 10pt

    row_h = 16.5  # altura por linha de questão
    max_rows = 18
    bubble_radius = 4.8
    options = ["A", "B", "C", "D", "E"]
    opt_dx = 15.0  # distância entre alternativas

    geometry = {"columns": [], "questions": {}}

    for col_idx, col_def in enumerate(COLUMNS_DEF):
        cx = grid_x + col_idx * (col_w + 10)
        cy_top = start_y - 12

        # Cabeçalho da coluna
        header_h = 18
        c.setFillColor(colors.HexColor("#0c2340"))
        c.setStrokeColor(colors.HexColor("#0c2340"))
        c.roundRect(cx, cy_top - header_h, col_w, header_h, 3, fill=1, stroke=1)

        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.white)
        c.drawCentredString(cx + col_w / 2.0, cy_top - header_h + 5, col_def["title"])

        # Fundo suave da coluna com borda sutil
        col_content_h = max_rows * row_h + 10
        col_content_y = cy_top - header_h - col_content_h
        c.setStrokeColor(colors.HexColor("#d0d7de"))
        c.setLineWidth(0.6)
        c.setFillColor(colors.HexColor("#ffffff"))
        c.rect(cx, col_content_y, col_w, col_content_h, fill=1, stroke=1)

        # Desenho das linhas de questões
        start_q = col_def["start"]
        end_q = col_def["end"]
        num_q = end_q - start_q + 1

        for r in range(num_q):
            q_num = start_q + r
            row_y = cy_top - header_h - 14 - r * row_h

            # Linha zebrada sutil para facilitar visualização
            if r % 2 == 1:
                c.setFillColor(colors.HexColor("#f8fafc"))
                c.rect(cx + 1, row_y - row_h / 2.0 + 1, col_w - 2, row_h - 2, fill=1, stroke=0)

            # Número da questão
            c.setFont("Helvetica-Bold", 8.5)
            c.setFillColor(colors.HexColor("#0c2340"))
            c.drawString(cx + 6, row_y - 3, f"{q_num:02d}")

            # Bolinhas A, B, C, D, E
            first_opt_x = cx + 33.0
            geometry["questions"][q_num] = {}

            for opt_idx, opt_letter in enumerate(options):
                bx = first_opt_x + opt_idx * opt_dx
                by = row_y

                # Desenha círculo com borda preta
                c.setStrokeColor(colors.black)
                c.setLineWidth(0.8)
                c.setFillColor(colors.white)
                c.circle(bx, by, bubble_radius, fill=1, stroke=1)

                # Desenha a letra no centro
                c.setFont("Helvetica-Bold", 6.5)
                c.setFillColor(colors.black)
                c.drawCentredString(bx, by - 2.2, opt_letter)

                # Salva coordenada teórica
                geometry["questions"][q_num][opt_letter] = (bx, by, bubble_radius)

    return geometry


def draw_footer(c):
    """Desenha o rodapé com código de barras inferior, aviso e logos."""
    footer_y = FIDUCIAL_MARGIN + 20

    # Linha divisória
    c.setStrokeColor(colors.HexColor("#cccccc"))
    c.setLineWidth(0.5)
    c.line(FIDUCIAL_MARGIN + 20, footer_y + 14, PAGE_WIDTH - FIDUCIAL_MARGIN - 20, footer_y + 14)

    # Texto de identificação
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(FIDUCIAL_MARGIN + 20, footer_y + 3, "CARTÃO-RESPOSTA OFICIAL • MODELO PADRÃO ENEM 70 QUESTÕES • LEITURA ÓPTICA AUTOMATIZADA (OMR)")

    c.drawRightString(PAGE_WIDTH - FIDUCIAL_MARGIN - 20, footer_y + 3, "PÁGINA 1 / 1")


def gerar_cartao_resposta_pdf(caminho_saida="provas_geradas/Cartao_Resposta_70Q.pdf", metadados=None):
    """Gera o arquivo PDF completo do Cartão-Resposta de 70 questões."""
    if metadados is None:
        metadados = {
            "titulo_exame": "EXAME NACIONAL DO ENSINO MÉDIO",
            "subtitulo": "SIMULADO DO EXAME NACIONAL DO ENSINO MÉDIO - 70 QUESTÕES",
            "dia": "1º DIA",
            "codigo_caderno": "010175AZ1"
        }

    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)
    c = canvas.Canvas(caminho_saida, pagesize=A4)

    # 1. Marcadores fiduciais nos 4 cantos
    draw_fiducials(c)

    # 2. Cabeçalho
    draw_header(c, metadados)

    # 3. Painel do candidato
    y_after_cand = draw_candidate_info(c, start_y=PAGE_HEIGHT - 95)

    # 4. Barra de instruções
    y_after_inst = draw_instructions_bar(c, start_y=y_after_cand)

    # 5. Grid das 70 questões (4 blocos)
    geometry = draw_bubble_grid(c, start_y=y_after_inst)

    # 6. Rodapé
    draw_footer(c)

    c.save()
    print(f"Cartão-Resposta gerado com sucesso em: {caminho_saida}")
    return geometry


if __name__ == "__main__":
    gerar_cartao_resposta_pdf()
