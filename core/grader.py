"""
Avaliador e Corretor Automático de Exames.
Compara as respostas lidas pelo motor OMR com o gabarito oficial das 70 questões,
calcula total de acertos, aproveitamento percentual e consolida os resultados em planilha Excel formatada.
"""

import os
import sys

# Garante que a raiz do projeto esteja no PYTHONPATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import glob
import json
import re
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from core.omr_engine import processar_cartao


def ordenacao_natural(texto):
    """Ordenação natural para arquivos como 1.jpg, 2.jpg, 10.jpg."""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', texto)]


def carregar_gabarito_oficial(caminho_questoes="banco_questoes/questoes.json"):
    """Extrai o gabarito oficial das 70 questões do banco de dados da prova."""
    if not os.path.exists(caminho_questoes):
        raise FileNotFoundError(f"Arquivo de questões não encontrado em '{caminho_questoes}'")

    with open(caminho_questoes, "r", encoding="utf-8") as f:
        dados = json.load(f)

    gabarito = {}
    for q in dados.get("questoes", []):
        q_num = int(q["numero"])
        gab_letra = q.get("gabarito", "").strip().upper()
        gabarito[q_num] = gab_letra

    return gabarito


def avaliar_aluno(df_respostas, gabarito_oficial):
    """
    Compara respostas do aluno com o gabarito oficial.
    Retorna métricas de acertos, erros, brancos e anuladas.
    """
    acertos = 0
    erros = 0
    brancos = 0
    anuladas = 0

    detalhes = {}
    for _, row in df_respostas.iterrows():
        q_num = int(row["Questao"])
        resp = row["Resposta"]
        gab = gabarito_oficial.get(q_num, "")

        if resp == "EM_BRANCO":
            status = "EM_BRANCO"
            brancos += 1
        elif resp == "ANULADA":
            status = "ANULADA"
            anuladas += 1
        elif resp == gab:
            status = "CORRETA"
            acertos += 1
        else:
            status = "INCORRETA"
            erros += 1

        detalhes[q_num] = {
            "resposta": resp,
            "gabarito": gab,
            "status": status
        }

    total_questoes = len(gabarito_oficial) if gabarito_oficial else len(df_respostas)
    porcentagem = round((acertos / float(total_questoes)) * 100.0, 1) if total_questoes > 0 else 0.0

    return {
        "acertos": acertos,
        "erros": erros,
        "brancos": brancos,
        "anuladas": anuladas,
        "total": total_questoes,
        "porcentagem": porcentagem,
        "detalhes": detalhes
    }


def formatar_excel(caminho_excel):
    """Aplica formatação profissional na planilha Excel gerada."""
    import openpyxl

    wb = openpyxl.load_workbook(caminho_excel)
    ws = wb.active

    # Estilos
    header_fill = PatternFill(start_color="0C2340", end_color="0C2340", fill_type="solid")
    header_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    kpi_fill = PatternFill(start_color="00A4E4", end_color="00A4E4", fill_type="solid")
    kpi_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")

    thin_border = Border(
        left=Side(style='thin', color='DDDDDD'),
        right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'),
        bottom=Side(style='thin', color='DDDDDD')
    )

    center_align = Alignment(horizontal="center", vertical="center")

    # Formata cabeçalho
    for col_idx in range(1, ws.max_column + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.alignment = center_align
        cell.border = thin_border
        col_name = str(cell.value)
        if col_name in ["Acertos", "% Acerto", "Nota / 70"]:
            cell.fill = kpi_fill
            cell.font = kpi_font
        else:
            cell.fill = header_fill
            cell.font = header_font

    # Formata células de dados
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            cell.alignment = center_align
            cell.border = thin_border

    # Ajusta largura das colunas
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = col[0].column_letter
        ws.column_dimensions[col_letter].width = max(max_len + 3, 5)

    wb.save(caminho_excel)


def corrigir_pasta_cartoes(pasta_cartoes="cartoes", caminho_questoes="banco_questoes/questoes.json", caminho_saida="resultado.xlsx"):
    """
    Processa todos os cartões da pasta, corrige contra o gabarito oficial e salva a planilha consolidada.
    """
    if pasta_cartoes == "cartoes" and not os.path.exists("cartoes"):
        if os.path.exists("simulado_2/cartoes"):
            pasta_cartoes = "simulado_2/cartoes"
        elif os.path.exists("simulado_1/cartoes_digitalizados"):
            pasta_cartoes = "simulado_1/cartoes_digitalizados"

    gabarito = carregar_gabarito_oficial(caminho_questoes)

    padroes = [os.path.join(pasta_cartoes, f"*{ext}") for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]]
    arquivos = []
    for p in padroes:
        arquivos.extend(glob.glob(p))

    arquivos = sorted(set(arquivos), key=ordenacao_natural)

    if not arquivos:
        print(f"Nenhuma imagem encontrada na pasta '{pasta_cartoes}'.")
        return None

    print(f"\n=======================================================")
    print(f"CORRETOR AUTOMÁTICO OMR • {len(arquivos)} CARTÕES ENCONTRADOS")
    print(f"Gabarito Oficial carregado: {len(gabarito)} questões.")
    print(f"=======================================================\n")

    if "simulado_1" in pasta_cartoes:
        pasta_debug = os.path.join("simulado_1", "debug_omr")
    elif "simulado_2" in pasta_cartoes:
        pasta_debug = os.path.join("simulado_2", "debug_omr")
    else:
        pasta_debug = "debug"
    os.makedirs(pasta_debug, exist_ok=True)

    for idx, caminho in enumerate(arquivos):
        nome_cartao = os.path.splitext(os.path.basename(caminho))[0]
        try:
            df_resp, metodo = processar_cartao(caminho, salvar_debug=True, pasta_debug=pasta_debug)
            metricas = avaliar_aluno(df_resp, gabarito)

            registro = {
                "Cartao": nome_cartao,
                "Acertos": metricas["acertos"],
                "% Acerto": f"{metricas['porcentagem']}%",
            }

            # Adiciona cada questão de 1 a 70
            for q_num in range(1, 71):
                resp_info = metricas["detalhes"].get(q_num, {})
                registro[str(q_num)] = resp_info.get("resposta", "EM_BRANCO")

            linhas_tabela.append(registro)
            totais_acertos.append(metricas["acertos"])

            print(f"[{idx+1:02d}/{len(arquivos):02d}] Cartão {nome_cartao}: {metricas['acertos']}/70 acertos ({metricas['porcentagem']}%) - Método: {metodo}")

        except Exception as e:
            print(f"[{idx+1:02d}/{len(arquivos):02d}] Cartão {nome_cartao}: Erro ao processar ({e})")

    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    if linhas_tabela:
        df_resultado = pd.DataFrame(linhas_tabela)
        df_resultado.to_excel(caminho_saida, index=False)
        formatar_excel(caminho_saida)

        media_acertos = round(sum(totais_acertos) / float(len(totais_acertos)), 1)
        print(f"\n[OK] Concluido! Planilha consolidada salva em: '{caminho_saida}'")
        print(f"[ESTATISTICA] Media de acertos da turma: {media_acertos}/70 ({round(media_acertos/70.0*100, 1)}%)")
        print(f"[DEBUG] Imagens com marcacoes salvas na pasta 'debug/'.")
        return df_resultado

    return None


if __name__ == "__main__":
    corrigir_pasta_cartoes()
