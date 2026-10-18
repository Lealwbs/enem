"""
Gera a planilha oficial do 2º Simulado ENEM 2026 com as respostas dos alunos
extraídas via OMR (Optical Mark Recognition) a partir dos cartões escaneados.

Estrutura idêntica à planilha do 1º Simulado:
- Aba 'Respostas': Grade horizontal completa (Totais, Linguagens Q1-16, Humanas Q17-32, Natureza Q33-50, Matemática Q51-70) com fórmulas TCT e Gabarito
- Aba 'Respostas_Por_ID': Todas as 71 linhas ordenadas por ID (1 a 71) para cópia direta no Google Sheets
- Aba 'Apenas_Presentes': Tabela limpa com os 14 alunos presentes e seus acertos por área
- Aba 'Dashboard': Painel geral de notas consolidadas (Linguagens, Humanas, Natureza, Matemática, Redação, Média)
- Aba 'TCT': Metodologia Teoria Clássica dos Testes Ponderada (TRI Adaptada)
- Aba 'Gabarito_Oficial': Gabarito oficial de 1 a 70 com disciplinas e estatísticas de acerto da turma
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# 1. Carrega dados dos alunos
CSV_ALUNOS = "simulado_2/lista_alunos_detalhada.csv"
XLSX_GABARITO = "simulado_2/prova/Gabarito_Simulado_2.xlsx"

df_alunos = pd.read_csv(CSV_ALUNOS)

# 2. Carrega Gabarito Oficial
wb_gab = openpyxl.load_workbook(XLSX_GABARITO, data_only=True)
s_gab = wb_gab.active
gabarito_oficial = {}
disciplinas = {}
areas_conhecimento = {}

for r in range(2, 72):
    q = int(s_gab.cell(r, 1).value)
    area = str(s_gab.cell(r, 2).value).strip()
    disc = str(s_gab.cell(r, 3).value).strip() if s_gab.cell(r, 3).value else ""
    gab = str(s_gab.cell(r, 5).value).strip().upper()
    gabarito_oficial[q] = gab
    disciplinas[q] = disc
    areas_conhecimento[q] = area

# 3. Respostas verificadas dos 14 alunos presentes (Ordem das páginas do PDF escaneado)
# Cada string contém exatamente 70 respostas (Q1 a Q70)
RESPOSTAS_OMR = {
    1:  "ACCBDACECBCECBBDCBEDCCDABDBDBBABDCBADCDCCBCDBADACCCAEDDACBCDEDCDBABDDB",
    4:  "BBCCADCDBACABEBDCACDACABDABCCDACBDABECEDBCAECBCADADEABCABECAACCEBABDAE",
    11: "BDABCACBAACECECEDACDCCABEACCDBAADEABCCADBDCBEDDCDABADBCDACDBCCDEBCEBBD",
    12: "ABACBABDABCECDECDACDCCABCADCBDECBEBCEBCCDCABDBDDDABECDABCDCAADDCDDBDAC",
    15: "EDCCABCBAECEBCADCEADCCAEBABDEBCABDEAADCEBBADCEABCBCDAEBECDABCEDBACEDBA",
    17: "CDBAEECDCCCAABDCCAABCCAACACEDBCCACCDDCCCACBCCEBEDECBABAECCCDCECEDBDCAC",
    28: "CBACBBDAABEEBDDBDCADCABCAABDCDABBCBADAADCBECBAACECDABBCBDEBABCADCAACDD",
    30: "EBCCDACBBECACBEBACADCBABDADCCBBCCEDDADDCECBACAADABCDEDBDCEDAABDCANULADADBBED",
    38: "EBBCDACBBBCECBCBACABCCABBACCDACDADBAADDABCBEDBAADABAABDCBBCCBDACDBBEAD",
    48: "DBACDCCBBACEBABDDCCDCCABBACCDBCDBCECCBDCCDBAACBEDAABCDCBAABCCBDEBBBDCA",
    56: "BEADCBDBBBCEBAEBDCCDCCABBACCEBEDACEBACCCCDBEACBADABADBDCBBCCBDDCDBBEAD",
    57: "DBACDCBAADCABADBDACDCCABCDCCBEAABAACADDCBEBACDBCEACACDABABCCABCADABCED",
    58: "BBACDDCBBACBDABCABCEBCABDBECECCDAABCEDDAEDCDBADADDCACDCCBCDEDCDBABB-BB",
    62: "DDACDDEDABCEBDAEDCDBCBABCACCEBABCCADCDCCBDCEEBACDACBCEDACBBCDCCDCEEADE"
}

# Converter strings em lista de 70 respostas
respostas_por_aluno = {}
for sid, raw in RESPOSTAS_OMR.items():
    if "ANULADA" in raw:
        # Substitui ANULADA por token para split correto
        parts = []
        i = 0
        while i < len(raw):
            if raw[i:i+7] == "ANULADA":
                parts.append("ANULADA")
                i += 7
            else:
                parts.append(raw[i])
                i += 1
        respostas_por_aluno[sid] = parts
    else:
        respostas_por_aluno[sid] = list(raw)

assert all(len(respostas_por_aluno[sid]) == 70 for sid in respostas_por_aluno), "Erro: Nem todos os alunos tem 70 respostas!"

# Criação do Workbook
wb = openpyxl.Workbook()
# Remove sheet padrão
wb.remove(wb.active)

# Estilos Visuais
font_header = Font(name="Arial", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Arial", size=10, bold=True)
font_regular = Font(name="Arial", size=9)
font_title = Font(name="Arial", size=12, bold=True, color="FFFFFF")

fill_ling = PatternFill(start_color="CC0000", end_color="CC0000", fill_type="solid")       # Vermelho
fill_hum = PatternFill(start_color="E69138", end_color="E69138", fill_type="solid")        # Laranja / Ouro
fill_nat = PatternFill(start_color="3C78D8", end_color="3C78D8", fill_type="solid")        # Azul
fill_mat = PatternFill(start_color="674EA7", end_color="674EA7", fill_type="solid")        # Roxo
fill_tot = PatternFill(start_color="356854", end_color="356854", fill_type="solid")        # Verde Escuro
fill_gab = PatternFill(start_color="274E13", end_color="274E13", fill_type="solid")        # Verde Gabarito
fill_sub = PatternFill(start_color="F3F3F3", end_color="F3F3F3", fill_type="solid")
fill_meta = PatternFill(start_color="EFEFEF", end_color="EFEFEF", fill_type="solid")
fill_presente = PatternFill(start_color="D9EAD3", end_color="D9EAD3", fill_type="solid")
fill_ausente = PatternFill(start_color="F4CCCC", end_color="F4CCCC", fill_type="solid")

align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")

thin_border = Border(
    left=Side(style="thin", color="D3D3D3"),
    right=Side(style="thin", color="D3D3D3"),
    top=Side(style="thin", color="D3D3D3"),
    bottom=Side(style="thin", color="D3D3D3")
)
header_border = Border(
    left=Side(style="thin", color="808080"),
    right=Side(style="thin", color="808080"),
    top=Side(style="thin", color="808080"),
    bottom=Side(style="thin", color="808080")
)

# ==============================================================================
# 1. ABA 'TCT' (Metodologia e Parâmetros)
# ==============================================================================
ws_tct = wb.create_sheet(title="TCT")
ws_tct.views.sheetView[0].showGridLines = True

ws_tct["A1"] = "Quantidade de alunos presentes no dia da prova:"
ws_tct["F1"] = 14
ws_tct["A1"].font = font_bold
ws_tct["F1"].font = font_bold
ws_tct["F1"].alignment = align_center

headers_tct = ["Área", "Qtde Acertos", "Nota Máxima", "Nota Mínima", "Diferença", "Pontuação da questão por acerto"]
for col_idx, h in enumerate(headers_tct, 1):
    cell = ws_tct.cell(2, col_idx, h)
    cell.font = font_header
    cell.fill = fill_tot
    cell.alignment = align_center

tct_data = [
    ("Linguagens", "=SUM(Respostas!$L$4:$AA$4)", 798.01, 302.56, "=C3-D3", "=E3/B3"),
    ("Humanas",    "=SUM(Respostas!$AB$4:$AQ$4)", 852.41, 311.69, "=C4-D4", "=E4/B4"),
    ("Natureza",   "=SUM(Respostas!$AR$4:$BI$4)", 906.82, 351.11, "=C5-D5", "=E5/B5"),
    ("Matemática", "=SUM(Respostas!$BJ$4:$CC$4)", 998.07, 362.43, "=C6-D6", "=E6/B6"),
]

for r_idx, row in enumerate(tct_data, 3):
    ws_tct.cell(r_idx, 1, row[0]).font = font_bold
    ws_tct.cell(r_idx, 2, row[1]).number_format = "#,##0"
    ws_tct.cell(r_idx, 3, row[2]).number_format = "#,##0.00"
    ws_tct.cell(r_idx, 4, row[3]).number_format = "#,##0.00"
    ws_tct.cell(r_idx, 5, row[4]).number_format = "#,##0.00"
    ws_tct.cell(r_idx, 6, row[5]).number_format = "#,##0.0000"
    for c in range(1, 7):
        ws_tct.cell(r_idx, c).border = thin_border
        if c > 1:
            ws_tct.cell(r_idx, c).alignment = align_center

ws_tct["A8"] = "Metodologia de Correção: Teoria Clássica dos Testes Ponderada (TCT)"
ws_tct["A8"].font = font_bold

tct_desc = (
    "Esta metodologia utiliza uma TRI Adaptada, onde a nota de cada área parte de um piso mínimo fixo "
    "e o valor de cada questão é calculado com base no desempenho geral da turma. Quanto mais alunos acertam "
    "uma questão, maior é o peso dela no simulado. Isso garante que o acerto nos conteúdos fundamentais e de "
    "domínio geral seja mais valorizado na composição da nota.\n\n"
    "Para calcular o resultado final, soma-se esse piso base da área à pontuação das questões que o aluno acertou. "
    "A média geral do aluno no simulado é obtida calculando a média simples entre as notas das quatro áreas "
    "do conhecimento e a nota da Redação."
)
ws_tct["A9"] = tct_desc
ws_tct["A9"].alignment = Alignment(wrap_text=True, vertical="top")
ws_tct.merge_cells("A9:F14")

# ==============================================================================
# 2. ABA 'Respostas' (Formato padrão Simulado 1 com fórmulas e gabarito)
# ==============================================================================
ws_resp = wb.create_sheet(title="Respostas")
ws_resp.views.sheetView[0].showGridLines = True

# Linha 1: Cabeçalhos Principais de Área
ws_resp["A1"] = "ID"
ws_resp["B1"] = "Nome do Aluno"
ws_resp["D1"] = "Totais"
ws_resp["L1"] = "Linguagens"
ws_resp["AB1"] = "Humanas"
ws_resp["AR1"] = "Natureza"
ws_resp["BJ1"] = "Matemática"

# Cores e merges da Linha 1
ws_resp["A1"].font = font_header
ws_resp["A1"].fill = fill_tot
ws_resp["A1"].alignment = align_center

ws_resp["B1"].font = font_header
ws_resp["B1"].fill = fill_tot
ws_resp["B1"].alignment = align_center

ws_resp.merge_cells("D1:K1")
for col in range(4, 12):
    cell = ws_resp.cell(1, col)
    cell.fill = fill_tot
    cell.font = font_header
    cell.alignment = align_center

ws_resp.merge_cells("L1:AA1")
for col in range(12, 28):
    cell = ws_resp.cell(1, col)
    cell.fill = fill_ling
    cell.font = font_header
    cell.alignment = align_center

ws_resp.merge_cells("AB1:AQ1")
for col in range(28, 44):
    cell = ws_resp.cell(1, col)
    cell.fill = fill_hum
    cell.font = font_header
    cell.alignment = align_center

ws_resp.merge_cells("AR1:BI1")
for col in range(44, 62):
    cell = ws_resp.cell(1, col)
    cell.fill = fill_nat
    cell.font = font_header
    cell.alignment = align_center

ws_resp.merge_cells("BJ1:CC1")
for col in range(62, 82):
    cell = ws_resp.cell(1, col)
    cell.fill = fill_mat
    cell.font = font_header
    cell.alignment = align_center

# Linha 2: Sub-cabeçalhos
ws_resp["C2"] = "Total Acertos"
ws_resp["D2"] = "Ling"
ws_resp["F2"] = "Hum"
ws_resp["H2"] = "Nat"
ws_resp["J2"] = "Mat"

for q in range(1, 71):
    col = 11 + q
    ws_resp.cell(2, col, f"Q{q}").font = font_bold
    ws_resp.cell(2, col).alignment = align_center

for c in range(1, 82):
    cell = ws_resp.cell(2, c)
    cell.font = font_bold
    cell.fill = fill_sub
    cell.alignment = align_center
    cell.border = thin_border

# Linha 3: PONTUAÇÃO DA QUESTÃO
ws_resp["A3"] = "PONTUAÇÃO DA QUESTÃO"
ws_resp["A3"].font = font_bold
ws_resp["D3"] = "Média"
ws_resp["F3"] = "Média"
ws_resp["H3"] = "Média"
ws_resp["J3"] = "Média"

for q in range(1, 71):
    col = 11 + q
    col_let = get_column_letter(col)
    if q <= 16:
        ws_resp[f"{col_let}3"] = f"=TCT!$E$3*{col_let}4/TCT!$B$3"
    elif q <= 32:
        ws_resp[f"{col_let}3"] = f"=TCT!$E$4*{col_let}4/TCT!$B$4"
    elif q <= 50:
        ws_resp[f"{col_let}3"] = f"=TCT!$E$5*{col_let}4/TCT!$B$5"
    else:
        ws_resp[f"{col_let}3"] = f"=TCT!$E$6*{col_let}4/TCT!$B$6"
    ws_resp[f"{col_let}3"].number_format = "#,##0.00"
    ws_resp[f"{col_let}3"].font = font_regular
    ws_resp[f"{col_let}3"].alignment = align_center

# Linha 4: ACERTOS DA QUESTÃO
ws_resp["A4"] = "ACERTOS DA QUESTÃO"
ws_resp["A4"].font = font_bold
ws_resp["D4"] = "=AVERAGE(D6:D19)"
ws_resp["F4"] = "=AVERAGE(F6:F19)"
ws_resp["H4"] = "=AVERAGE(H6:H19)"
ws_resp["J4"] = "=AVERAGE(J6:J19)"

for col_idx in [4, 6, 8, 10]:
    ws_resp.cell(4, col_idx).number_format = "#,##0.00"
    ws_resp.cell(4, col_idx).font = font_bold
    ws_resp.cell(4, col_idx).alignment = align_center

for q in range(1, 71):
    col = 11 + q
    col_let = get_column_letter(col)
    ws_resp[f"{col_let}4"] = f"=COUNTIF({col_let}6:{col_let}76, {col_let}$5)"
    ws_resp[f"{col_let}4"].number_format = "#,##0"
    ws_resp[f"{col_let}4"].font = font_bold
    ws_resp[f"{col_let}4"].alignment = align_center

# Linha 5: GABARITO
ws_resp["A5"] = "GABARITO"
ws_resp["B5"] = "GABARITO"
ws_resp["D5"] = "Nota"
ws_resp["E5"] = "Acertos"
ws_resp["F5"] = "Nota"
ws_resp["G5"] = "Acertos"
ws_resp["H5"] = "Nota"
ws_resp["I5"] = "Acertos"
ws_resp["J5"] = "Nota"
ws_resp["K5"] = "Acertos"

for c in range(1, 12):
    cell = ws_resp.cell(5, c)
    cell.font = font_header
    cell.fill = fill_gab
    cell.alignment = align_center

for q in range(1, 71):
    col = 11 + q
    col_let = get_column_letter(col)
    cell = ws_resp[f"{col_let}5"]
    cell.value = gabarito_oficial[q]
    cell.font = font_header
    cell.fill = fill_gab
    cell.alignment = align_center

# Ordenação dos alunos: Presentes primeiro (14 alunos), seguidos dos ausentes (57 alunos)
presentes_ids = [1, 4, 11, 12, 15, 17, 28, 30, 38, 48, 56, 57, 58, 62]
ausentes_ids = [int(sid) for sid in df_alunos["ID"].tolist() if sid not in presentes_ids]
ordem_ids = presentes_ids + ausentes_ids

row_num = 6
for sid in ordem_ids:
    row_aluno = df_alunos[df_alunos["ID"] == sid].iloc[0]
    nome = row_aluno["Nome do Aluno"]
    is_presente = (sid in presentes_ids)

    ws_resp.cell(row_num, 1, sid).alignment = align_center
    ws_resp.cell(row_num, 2, nome).alignment = align_left

    r_str = str(row_num)
    ws_resp.cell(row_num, 3, f"=SUM(E{r_str},G{r_str},I{r_str},K{r_str})").alignment = align_center

    if is_presente:
        # Fórmulas de notas e acertos
        ws_resp.cell(row_num, 4, f"=SUMPRODUCT(--($L{r_str}:$AA{r_str} = $L$5:$AA$5), $L$3:$AA$3) + TCT!$D$3").number_format = "#,##0.00"
        ws_resp.cell(row_num, 5, f"=SUMPRODUCT(--($L$5:$AA$5=L{r_str}:AA{r_str}))").number_format = "#,##0"

        ws_resp.cell(row_num, 6, f"=SUMPRODUCT(--($AB{r_str}:$AQ{r_str} = $AB$5:$AQ$5), $AB$3:$AQ$3) + TCT!$D$4").number_format = "#,##0.00"
        ws_resp.cell(row_num, 7, f"=SUMPRODUCT(--($AB$5:$AQ$5=AB{r_str}:AQ{r_str}))").number_format = "#,##0"

        ws_resp.cell(row_num, 8, f"=SUMPRODUCT(--($AR{r_str}:$BI{r_str} = $AR$5:$BI$5), $AR$3:$BI$3) + TCT!$D$5").number_format = "#,##0.00"
        ws_resp.cell(row_num, 9, f"=SUMPRODUCT(--($AR$5:$BI$5=AR{r_str}:BI{r_str}))").number_format = "#,##0"

        ws_resp.cell(row_num, 10, f"=SUMPRODUCT(--($BJ{r_str}:$CC{r_str} = $BJ$5:$CC$5), $BJ$3:$CC$3) + TCT!$D$6").number_format = "#,##0.00"
        ws_resp.cell(row_num, 11, f"=SUMPRODUCT(--($BJ$5:$CC$5=BJ{r_str}:CC{r_str}))").number_format = "#,##0"

        # Respostas do aluno
        resps = respostas_por_aluno[sid]
        for q_idx in range(70):
            col = 12 + q_idx
            ans = resps[q_idx]
            cell = ws_resp.cell(row_num, col, ans)
            cell.alignment = align_center
            if ans == gabarito_oficial[q_idx + 1]:
                cell.font = font_bold
            elif ans == "ANULADA":
                cell.font = Font(name="Arial", size=9, bold=True, color="FF9900")
    else:
        # Ausente: 0 e '-'
        for c_idx in range(4, 12):
            cell = ws_resp.cell(row_num, c_idx, 0)
            cell.alignment = align_center
        for q_idx in range(70):
            col = 12 + q_idx
            cell = ws_resp.cell(row_num, col, "-")
            cell.alignment = align_center

    for c in range(1, 82):
        ws_resp.cell(row_num, c).border = thin_border

    row_num += 1


# ==============================================================================
# 3. ABA 'Respostas_Por_ID' (Ordenada numericamente 1 a 71 - Pronta para Google Sheets)
# ==============================================================================
ws_id = wb.create_sheet(title="Respostas_Por_ID")
ws_id.views.sheetView[0].showGridLines = True

headers_id = ["ID", "Nome do Aluno", "Unidade", "Presente", "Total Acertos", "Ling Acertos", "Hum Acertos", "Nat Acertos", "Mat Acertos"]
for q in range(1, 71):
    headers_id.append(f"Q{q}")

for c_idx, h in enumerate(headers_id, 1):
    cell = ws_id.cell(1, c_idx, h)
    cell.font = font_header
    if c_idx <= 4:
        cell.fill = fill_tot
    elif c_idx <= 9:
        cell.fill = fill_sub
        cell.font = font_bold
    elif c_idx <= 25:
        cell.fill = fill_ling
    elif c_idx <= 41:
        cell.fill = fill_hum
    elif c_idx <= 59:
        cell.fill = fill_nat
    else:
        cell.fill = fill_mat
    cell.alignment = align_center
    cell.border = thin_border

# Gabarito na Linha 2
ws_id.cell(2, 1, "GABARITO").font = font_bold
ws_id.cell(2, 2, "GABARITO OFICIAL").font = font_bold
ws_id.cell(2, 3, "-").alignment = align_center
ws_id.cell(2, 4, "-").alignment = align_center
ws_id.cell(2, 5, 70).alignment = align_center
ws_id.cell(2, 6, 16).alignment = align_center
ws_id.cell(2, 7, 16).alignment = align_center
ws_id.cell(2, 8, 18).alignment = align_center
ws_id.cell(2, 9, 20).alignment = align_center
for q in range(1, 71):
    cell = ws_id.cell(2, 9 + q, gabarito_oficial[q])
    cell.alignment = align_center
    cell.font = font_header
    cell.fill = fill_gab

for c in range(1, len(headers_id) + 1):
    ws_id.cell(2, c).border = thin_border

# Alunos de 1 a 71
for idx, r_aluno in df_alunos.iterrows():
    sid = int(r_aluno["ID"])
    nome = r_aluno["Nome do Aluno"]
    unidade = r_aluno["Unidade"]
    is_presente = (sid in presentes_ids)
    r_idx = idx + 3

    ws_id.cell(r_idx, 1, sid).alignment = align_center
    ws_id.cell(r_idx, 2, nome).alignment = align_left
    ws_id.cell(r_idx, 3, unidade).alignment = align_left
    pres_cell = ws_id.cell(r_idx, 4, "SIM" if is_presente else "NÃO")
    pres_cell.alignment = align_center
    pres_cell.fill = fill_presente if is_presente else fill_ausente

    if is_presente:
        resps = respostas_por_aluno[sid]
        # Calcula acertos por área
        ac_ling = sum(1 for q in range(16) if resps[q] == gabarito_oficial[q+1])
        ac_hum = sum(1 for q in range(16, 32) if resps[q] == gabarito_oficial[q+1])
        ac_nat = sum(1 for q in range(32, 50) if resps[q] == gabarito_oficial[q+1])
        ac_mat = sum(1 for q in range(50, 70) if resps[q] == gabarito_oficial[q+1])
        tot = ac_ling + ac_hum + ac_nat + ac_mat

        ws_id.cell(r_idx, 5, tot).alignment = align_center
        ws_id.cell(r_idx, 6, ac_ling).alignment = align_center
        ws_id.cell(r_idx, 7, ac_hum).alignment = align_center
        ws_id.cell(r_idx, 8, ac_nat).alignment = align_center
        ws_id.cell(r_idx, 9, ac_mat).alignment = align_center

        for q_idx in range(70):
            ans = resps[q_idx]
            cell = ws_id.cell(r_idx, 10 + q_idx, ans)
            cell.alignment = align_center
            if ans == gabarito_oficial[q_idx + 1]:
                cell.font = font_bold
            elif ans == "ANULADA":
                cell.font = Font(name="Arial", size=9, bold=True, color="FF9900")
    else:
        for c in range(5, 10):
            ws_id.cell(r_idx, c, 0).alignment = align_center
        for q_idx in range(70):
            cell = ws_id.cell(r_idx, 10 + q_idx, "-")
            cell.alignment = align_center

    for c in range(1, len(headers_id) + 1):
        ws_id.cell(r_idx, c).border = thin_border


# ==============================================================================
# 4. ABA 'Apenas_Presentes' (14 alunos com respostas e acertos)
# ==============================================================================
ws_pres = wb.create_sheet(title="Apenas_Presentes")
ws_pres.views.sheetView[0].showGridLines = True

headers_pres = ["ID", "Nome do Aluno", "Unidade", "Total Acertos", "Ling (16)", "Hum (16)", "Nat (18)", "Mat (20)"]
for q in range(1, 71):
    headers_pres.append(f"Q{q}")

for c_idx, h in enumerate(headers_pres, 1):
    cell = ws_pres.cell(1, c_idx, h)
    cell.font = font_header
    if c_idx <= 3:
        cell.fill = fill_tot
    elif c_idx <= 8:
        cell.fill = fill_sub
        cell.font = font_bold
    elif c_idx <= 24:
        cell.fill = fill_ling
    elif c_idx <= 40:
        cell.fill = fill_hum
    elif c_idx <= 58:
        cell.fill = fill_nat
    else:
        cell.fill = fill_mat
    cell.alignment = align_center
    cell.border = thin_border

# Gabarito na Linha 2
ws_pres.cell(2, 1, "GABARITO").font = font_bold
ws_pres.cell(2, 2, "GABARITO OFICIAL").font = font_bold
ws_pres.cell(2, 3, "-").alignment = align_center
ws_pres.cell(2, 4, 70).alignment = align_center
ws_pres.cell(2, 5, 16).alignment = align_center
ws_pres.cell(2, 6, 16).alignment = align_center
ws_pres.cell(2, 7, 18).alignment = align_center
ws_pres.cell(2, 8, 20).alignment = align_center
for q in range(1, 71):
    cell = ws_pres.cell(2, 8 + q, gabarito_oficial[q])
    cell.alignment = align_center
    cell.font = font_header
    cell.fill = fill_gab

for c in range(1, len(headers_pres) + 1):
    ws_pres.cell(2, c).border = thin_border

for p_idx, sid in enumerate(presentes_ids, 3):
    r_aluno = df_alunos[df_alunos["ID"] == sid].iloc[0]
    nome = r_aluno["Nome do Aluno"]
    unidade = r_aluno["Unidade"]
    resps = respostas_por_aluno[sid]

    ac_ling = sum(1 for q in range(16) if resps[q] == gabarito_oficial[q+1])
    ac_hum = sum(1 for q in range(16, 32) if resps[q] == gabarito_oficial[q+1])
    ac_nat = sum(1 for q in range(32, 50) if resps[q] == gabarito_oficial[q+1])
    ac_mat = sum(1 for q in range(50, 70) if resps[q] == gabarito_oficial[q+1])
    tot = ac_ling + ac_hum + ac_nat + ac_mat

    ws_pres.cell(p_idx, 1, sid).alignment = align_center
    ws_pres.cell(p_idx, 2, nome).alignment = align_left
    ws_pres.cell(p_idx, 3, unidade).alignment = align_left
    ws_pres.cell(p_idx, 4, tot).alignment = align_center
    ws_pres.cell(p_idx, 4).font = font_bold
    ws_pres.cell(p_idx, 5, ac_ling).alignment = align_center
    ws_pres.cell(p_idx, 6, ac_hum).alignment = align_center
    ws_pres.cell(p_idx, 7, ac_nat).alignment = align_center
    ws_pres.cell(p_idx, 8, ac_mat).alignment = align_center

    for q_idx in range(70):
        ans = resps[q_idx]
        cell = ws_pres.cell(p_idx, 9 + q_idx, ans)
        cell.alignment = align_center
        if ans == gabarito_oficial[q_idx + 1]:
            cell.font = font_bold
            cell.fill = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
        elif ans == "ANULADA":
            cell.font = Font(name="Arial", size=9, bold=True, color="FF9900")

    for c in range(1, len(headers_pres) + 1):
        ws_pres.cell(p_idx, c).border = thin_border


# ==============================================================================
# 5. ABA 'Dashboard' (Painel Geral de Notas)
# ==============================================================================
ws_dash = wb.create_sheet(title="Dashboard")
ws_dash.views.sheetView[0].showGridLines = True

headers_dash = ["ID", "Nome do Aluno", "Unidade", "Presente", "Linguagens", "Humanas", "Natureza", "Matemática", "Redação", "Média"]
for c_idx, h in enumerate(headers_dash, 1):
    cell = ws_dash.cell(1, c_idx, h)
    cell.font = font_header
    cell.fill = fill_tot
    cell.alignment = align_center
    cell.border = thin_border

for idx, r_aluno in df_alunos.iterrows():
    sid = int(r_aluno["ID"])
    nome = r_aluno["Nome do Aluno"]
    unidade = r_aluno["Unidade"]
    is_presente = (sid in presentes_ids)
    r_idx = idx + 2
    r_str = str(r_idx)

    ws_dash.cell(r_idx, 1, sid).alignment = align_center
    ws_dash.cell(r_idx, 2, nome).alignment = align_left
    ws_dash.cell(r_idx, 3, unidade).alignment = align_left
    
    p_cell = ws_dash.cell(r_idx, 4, "SIM" if is_presente else "NÃO")
    p_cell.alignment = align_center
    p_cell.fill = fill_presente if is_presente else fill_ausente

    # VLOOKUP no Respostas
    ws_dash.cell(r_idx, 5, f"=VLOOKUP($A{r_str},Respostas!$A:$K,4,FALSE)").number_format = "#,##0.00"
    ws_dash.cell(r_idx, 6, f"=VLOOKUP($A{r_str},Respostas!$A:$K,6,FALSE)").number_format = "#,##0.00"
    ws_dash.cell(r_idx, 7, f"=VLOOKUP($A{r_str},Respostas!$A:$K,8,FALSE)").number_format = "#,##0.00"
    ws_dash.cell(r_idx, 8, f"=VLOOKUP($A{r_str},Respostas!$A:$K,10,FALSE)").number_format = "#,##0.00"
    ws_dash.cell(r_idx, 9, f"=IF($D{r_str}=\"NÃO\", \"-\", \"Pendente\")").alignment = align_center
    ws_dash.cell(r_idx, 10, f"=IFERROR(AVERAGE(E{r_str}:H{r_str}),\"-\")").number_format = "#,##0.00"

    for c in range(5, 11):
        ws_dash.cell(r_idx, c).alignment = align_center
    for c in range(1, 11):
        ws_dash.cell(r_idx, c).border = thin_border


# ==============================================================================
# 6. ABA 'Gabarito_Oficial' (Estatísticas por questão)
# ==============================================================================
ws_gab_sheet = wb.create_sheet(title="Gabarito_Oficial")
ws_gab_sheet.views.sheetView[0].showGridLines = True

headers_gab_stat = ["Questão", "Área do Conhecimento", "Disciplina", "Gabarito Oficial", "Acertos na Turma (14)", "% de Acerto", "Classificação"]
for c_idx, h in enumerate(headers_gab_stat, 1):
    cell = ws_gab_sheet.cell(1, c_idx, h)
    cell.font = font_header
    cell.fill = fill_tot
    cell.alignment = align_center
    cell.border = thin_border

for q in range(1, 71):
    r_idx = q + 1
    gab = gabarito_oficial[q]
    area = areas_conhecimento[q]
    disc = disciplinas[q]

    # Contagem real de acertos
    acertos = sum(1 for sid in presentes_ids if respostas_por_aluno[sid][q-1] == gab)
    pct = (acertos / 14.0) * 100.0

    if pct >= 70.0:
        classif = "Fácil"
    elif pct >= 35.0:
        classif = "Média"
    else:
        classif = "Difícil"

    ws_gab_sheet.cell(r_idx, 1, q).alignment = align_center
    ws_gab_sheet.cell(r_idx, 2, area).alignment = align_left
    ws_gab_sheet.cell(r_idx, 3, disc).alignment = align_left
    ws_gab_sheet.cell(r_idx, 4, gab).alignment = align_center
    ws_gab_sheet.cell(r_idx, 4).font = font_bold
    ws_gab_sheet.cell(r_idx, 5, acertos).alignment = align_center
    ws_gab_sheet.cell(r_idx, 6, f"{pct:.1f}%").alignment = align_center
    ws_gab_sheet.cell(r_idx, 7, classif).alignment = align_center

    for c in range(1, 8):
        ws_gab_sheet.cell(r_idx, c).border = thin_border


# Ajuste inteligente de largura de colunas em todas as abas
for sheet in wb.worksheets:
    for col in sheet.columns:
        col_letter = get_column_letter(col[0].column)
        if sheet.title in ["Respostas", "Respostas_Por_ID", "Apenas_Presentes"] and col[0].column >= 10:
            sheet.column_dimensions[col_letter].width = 5.0
        else:
            max_len = 0
            for cell in col[:15]:
                val = str(cell.value or "")
                if len(val) > max_len and not str(val).startswith("="):
                    max_len = len(val)
            sheet.column_dimensions[col_letter].width = max(max_len + 3, 10)

# Salvar a planilha nos caminhos de interesse
paths = [
    "simulado_2/2º Simulado ENEM 2026.xlsx",
    "simulado_2/correcao/2º Simulado ENEM 2026.xlsx",
    "simulado_2/correcao/respostas_alunos.xlsx"
]

for p in paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    wb.save(p)
    print(f"[OK] Planilha gerada com sucesso em: {p}")
