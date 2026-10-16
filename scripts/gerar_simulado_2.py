"""
================================================================================
SCRIPT MASTER DE GERAÇÃO: 2º SIMULADO ENEM (70 QUESTÕES + REDAÇÃO)
Coletivo Voa Voa & Preparatório Gabarita
================================================================================
Executa o pipeline completo:
1. Compilação do Banco de 70 Questões Autênticas e Proposta de Redação
2. Geração do Caderno de Questões (Caderno Branco estilo ENEM com Proposta no Meio)
3. Geração da Folha Unificada de Respostas (Frente: Cartão OMR / Verso: Redação)
4. Geração do Gabarito Oficial Preenchido Frente e Verso
5. Geração da Planilha Excel Oficial com Gabarito, Habilidades e Fontes
================================================================================
"""

import os
import sys
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Garante que a raiz do projeto esteja no PYTHONPATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.core.exam_generator import gerar_prova_pdf
from app.core.unified_sheet_generator import gerar_folha_unificada_pdf


def gerar_planilha_gabarito_excel(questoes_data, caminho_saida):
    """Gera a planilha Excel oficial com formatação profissional."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Gabarito Oficial"

    # Cores institucionais
    fill_header = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

    fill_areas = {
        "Linguagens, Códigos e suas Tecnologias": PatternFill(start_color="E8F1F5", end_color="E8F1F5", fill_type="solid"),
        "Ciências Humanas e suas Tecnologias": PatternFill(start_color="FDF2E9", end_color="FDF2E9", fill_type="solid"),
        "Ciências da Natureza e suas Tecnologias": PatternFill(start_color="EAF2F8", end_color="EAF2F8", fill_type="solid"),
        "Matemática e suas Tecnologias": PatternFill(start_color="EBF5FB", end_color="EBF5FB", fill_type="solid"),
    }

    fill_gab = PatternFill(start_color="27AE60", end_color="27AE60", fill_type="solid")
    font_gab = Font(name="Calibri", size=12, bold=True, color="FFFFFF")

    thin_border = Border(
        left=Side(style='thin', color='DDDDDD'),
        right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'),
        bottom=Side(style='thin', color='DDDDDD')
    )

    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")

    # Cabeçalho da Planilha
    headers = ["Questão", "Área do Conhecimento", "Disciplina", "Habilidade / Conteúdo", "Gabarito Oficial", "Fonte Oficial"]
    ws.append(headers)

    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = fill_header
        cell.font = font_header
        cell.alignment = center_align
        cell.border = thin_border
    ws.row_dimensions[1].height = 24

    for q in questoes_data.get("questoes", []):
        num = int(q["numero"])
        area = q.get("area", "")
        disc = q.get("disciplina", "")
        hab = q.get("habilidade", "")
        gab = q.get("gabarito", "").strip().upper()
        fonte = q.get("fonte", "")

        row_vals = [num, area, disc, hab, gab, fonte]
        ws.append(row_vals)
        curr_row = ws.max_row

        ws.cell(row=curr_row, column=1).alignment = center_align
        ws.cell(row=curr_row, column=2).alignment = left_align
        ws.cell(row=curr_row, column=3).alignment = left_align
        ws.cell(row=curr_row, column=4).alignment = left_align

        # Destaque na célula do gabarito
        gab_cell = ws.cell(row=curr_row, column=5)
        gab_cell.alignment = center_align
        gab_cell.fill = fill_gab
        gab_cell.font = font_gab

        ws.cell(row=curr_row, column=6).alignment = left_align

        for col_idx in range(1, len(headers) + 1):
            c = ws.cell(row=curr_row, column=col_idx)
            c.border = thin_border
            if col_idx == 2 and area in fill_areas:
                c.fill = fill_areas[area]

        ws.row_dimensions[curr_row].height = 20

    # Larguras automáticas de colunas
    larguras = {1: 10, 2: 38, 3: 20, 4: 45, 5: 18, 6: 40}
    for col_idx, w in larguras.items():
        ws.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = w

    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)
    wb.save(caminho_saida)
    print(f"[OK] Planilha Excel de Gabarito salva em: {caminho_saida}")


def main():
    print("=" * 70)
    print("INICIANDO PRODUÇÃO COMPLETA DO 2º SIMULADO ENEM")
    print("Coletivo Voa Voa & Preparatório Gabarita")
    print("=" * 70)

    # 1. Caminhos principais
    pasta_resultado = os.path.join(ROOT_DIR, "simulado_2", "resultado")
    pasta_old = os.path.join(pasta_resultado, ".old")
    os.makedirs(pasta_resultado, exist_ok=True)
    os.makedirs(pasta_old, exist_ok=True)

    caminho_json = os.path.join(ROOT_DIR, "simulado_2", "banco_questoes", "questoes.json")
    caminho_prova = os.path.join(pasta_resultado, "Caderno_Questoes_70Q.pdf")
    caminho_unificada = os.path.join(pasta_resultado, "Cartao_Resposta_e_Redacao_Frente_Verso.pdf")
    caminho_gabarito_pdf = os.path.join(pasta_resultado, "Gabarito_Oficial_Preenchido_Frente_Verso.pdf")
    caminho_gabarito_xlsx = os.path.join(pasta_resultado, "Gabarito_Oficial_Simulado_2.xlsx")

    # 2. Carrega ou compila o JSON do simulado
    if not os.path.exists(caminho_json):
        print("\n[PASSO 1] Compilando banco de questões a partir do script...")
        import scripts.build_simulado_2_json as builder
        builder.build_banco()
    else:
        print(f"\n[PASSO 1] Banco de questões verificado em: {caminho_json}")

    with open(caminho_json, "r", encoding="utf-8") as f:
        questoes_data = json.load(f)

    gabarito_map = {int(q["numero"]): q.get("gabarito", "").strip().upper() for q in questoes_data.get("questoes", [])}
    print(f"-> Total de Questões Autênticas Carregadas: {len(gabarito_map)}")

    # 3. Geração do Caderno de Questões Completo
    print("\n[PASSO 2] Gerando Caderno de Questões Completo (Caderno 1 Branco)...")
    print("-> Capa oficial formatada com detalhamento das 4 áreas e redação.")
    print("-> Proposta de redação e rascunho de 30 linhas posicionados no MEIO (após Q32).")
    print("-> Fontes TrueType e sanitização para prevenir erros de caracteres.")
    gerar_prova_pdf(caminho_questoes=caminho_json, caminho_saida=caminho_prova)

    # 4. Geração da Folha Unificada Frente e Verso (Cartão + Redação)
    print("\n[PASSO 3] Gerando Folha Unificada de Respostas (Frente e Verso)...")
    print("-> Frente: Cartão-Resposta 70Q com marcadores OMR e painel inferior espaçado.")
    print("-> Verso: Folha Oficial de Redação com 30 linhas pautadas e instruções oficiais.")
    gerar_folha_unificada_pdf(caminho_saida=caminho_unificada, gabarito_oficial=None)

    # 5. Geração do Gabarito Oficial Preenchido Frente e Verso
    print("\n[PASSO 4] Gerando Gabarito Oficial Preenchido Frente e Verso...")
    gerar_folha_unificada_pdf(caminho_saida=caminho_gabarito_pdf, gabarito_oficial=gabarito_map)

    # 6. Geração da Planilha Excel do Gabarito Oficial
    print("\n[PASSO 5] Gerando Planilha Excel do Gabarito Oficial...")
    gerar_planilha_gabarito_excel(questoes_data, caminho_gabarito_xlsx)

    print("\n" + "=" * 70)
    print("PRODUÇÃO CONCLUÍDA COM TOTAL SUCESSO!")
    print("Todos os arquivos gerados estão disponíveis em 'simulado_2/resultado/':")
    print(f"1. Caderno de Questões:   {caminho_prova}")
    print(f"2. Folha Frente e Verso:  {caminho_unificada}")
    print(f"3. Gabarito Frente/Verso: {caminho_gabarito_pdf}")
    print(f"4. Gabarito em Excel:     {caminho_gabarito_xlsx}")
    print(f"5. Arquivos Legados:      {pasta_old}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
