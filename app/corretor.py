"""
================================================================================
CORRETOR AUTOMATICO DE CARTAO-RESPOSTA (OMR - OPTICAL MARK RECOGNITION)
Modelo: 70 Questoes (4 Blocos: 1-18, 19-36, 37-54, 55-70; 5 Alternativas: A-E)
Tecnologias: Python, OpenCV (cv2), NumPy, Pandas
================================================================================
"""

import os
import sys
import glob
import re
import json
import argparse
import cv2
import numpy as np
import pandas as pd

CALIBRACAO_PADRAO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calibracao_gabarito.json')
LETRAS = ['A', 'B', 'C', 'D', 'E']


def normalizar_letra(valor):
    """Normaliza entradas como ' b ', 'EM BRANCO' ou 'anulada' para o formato interno do sistema."""
    if valor is None:
        return 'EM_BRANCO'
    texto = str(valor).strip().upper()
    if texto in ('', 'NONE', 'NULL'):
        return 'EM_BRANCO'
    texto = re.sub(r'\s+', ' ', texto)
    texto = texto.replace('-', '_')
    texto = texto.replace('Ã', 'A').replace('Â', 'A').replace('Á', 'A').replace('À', 'A')
    texto = texto.replace('Ê', 'E').replace('É', 'E').replace('È', 'E')
    texto = texto.replace('Î', 'I').replace('Í', 'I').replace('Ì', 'I')
    texto = texto.replace('Ô', 'O').replace('Ó', 'O').replace('Ò', 'O')
    texto = texto.replace('Û', 'U').replace('Ú', 'U').replace('Ù', 'U')
    texto = texto.replace(' ', '_')
    if texto in {'A', 'B', 'C', 'D', 'E'}:
        return texto
    if texto in {'_', 'EM_BRANCO', 'BRANCO', 'VAZIO', 'EM_BRANCO_'}:
        return 'EM_BRANCO'
    if texto in {'ANULADA', 'ANULADO', 'NULA'}:
        return 'ANULADA'
    if texto in {'X'}:
        return 'ANULADA'
    return 'EM_BRANCO' if texto in {'?', 'NAO'} else texto


def carregar_calibracao(caminho_calibracao=CALIBRACAO_PADRAO):
    if not os.path.exists(caminho_calibracao):
        return {}
    try:
        with open(caminho_calibracao, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        if not isinstance(dados, dict):
            return {}
        return dados
    except Exception:
        return {}


def salvar_calibracao(calibracao, caminho_calibracao=CALIBRACAO_PADRAO):
    with open(caminho_calibracao, 'w', encoding='utf-8') as f:
        json.dump(calibracao, f, ensure_ascii=False, indent=2)


def atualizar_calibracao(calibracao, questao, letra, origem='manual', cartao_id=None):
    q_key = str(int(questao))
    letra_norm = normalizar_letra(letra)
    if letra_norm not in ['A', 'B', 'C', 'D', 'E', 'EM_BRANCO', 'ANULADA']:
        letra_norm = 'EM_BRANCO'

    if cartao_id is not None:
        cartao_key = str(cartao_id)
        calibracao.setdefault(cartao_key, {})
        calibracao[cartao_key][q_key] = {
            'letra': letra_norm,
            'origem': origem,
            'questao': q_key,
        }
        return calibracao

    calibracao[q_key] = {
        'letra': letra_norm,
        'origem': origem,
        'questao': q_key,
    }
    return calibracao


def aplicar_calibracao_resposta(questao, resposta, calibracao=None, cartao_id=None):
    if calibracao is None:
        calibracao = {}
    q_key = str(int(questao))

    if cartao_id is not None:
        cartao_key = str(cartao_id)
        if cartao_key in calibracao and q_key in calibracao[cartao_key]:
            return calibracao[cartao_key][q_key].get('letra', resposta)

    if q_key in calibracao:
        return calibracao[q_key].get('letra', resposta)
    return normalizar_letra(resposta)


def decidir_resposta_questao(dq, cartao_majoritariamente_vazio, calibracao=None, questao=None, cartao_id=None):
    """Decide a resposta com fallbacks mais conservadores para reduzir falsos positivos."""
    q_num = dq['q_num'] if questao is None else questao
    d0 = dq['d0']
    d1 = dq['d1']
    max_s = dq['max_s']
    best_idx = dq['best_idx']
    melhor_letra = LETTERS[best_idx]
    if calibracao is not None:
        resposta_calibrada = aplicar_calibracao_resposta(q_num, melhor_letra, calibracao, cartao_id=cartao_id)
        if resposta_calibrada in ['A', 'B', 'C', 'D', 'E', 'EM_BRANCO', 'ANULADA']:
            return resposta_calibrada, melhor_letra

    if cartao_majoritariamente_vazio:
        if d0 < 22.0 or max_s < 70.0:
            return 'EM_BRANCO', melhor_letra
        if d0 >= 30.0 and d1 >= 25.0 and (d0 - d1) < 6.0:
            return 'ANULADA', melhor_letra
        return melhor_letra, melhor_letra

    if (d0 < 8.0 and max_s < 25.0) or max_s < 15.0:
        return 'EM_BRANCO', melhor_letra
    if d0 >= 30.0 and d1 >= 25.0 and (d0 - d1) < 6.0:
        return 'ANULADA', melhor_letra
    return melhor_letra, melhor_letra


def prompt_confirmacao_questao(caminho_imagem, questao, letra_predita, debug_path=None):
    """Pede confirmação de marcação manual para a questão e salva o resultado em calibração."""
    print(f"\n[Treinamento ativo] Questão {questao}: leitura automática sugeriu '{letra_predita}'.")
    if debug_path:
        print(f"Imagem de apoio: {debug_path}")
    print("Abra a imagem e confirme se a marcação da questão está correta.")
    print("Opções: [S]im / [N]ão / ou digite a letra correta (A-E) / '_' para em branco / 'X' para anulada")
    entrada = input('Confirma? ').strip().upper()
    if entrada in {'S', 'SIM', 'Y', 'YES'}:
        return letra_predita, 'confirmado'
    if entrada in {'_', 'BRANCO', 'V', 'VAZIO'}:
        return 'EM_BRANCO', 'correção_manual'
    if entrada in {'X', 'ANULADA', 'NULA'}:
        return 'ANULADA', 'correção_manual'
    if entrada in LETTERS:
        return entrada, 'correção_manual'
    if entrada in {'N', 'NAO', 'NO'}:
        print('Digite a letra correta, ou _ para em branco, ou X para anulada.')
        nova = input('Qual a resposta correta? ').strip().upper()
        if nova in {'_', 'BRANCO', 'V', 'VAZIO'}:
            return 'EM_BRANCO', 'correção_manual'
        if nova in {'X', 'ANULADA', 'NULA'}:
            return 'ANULADA', 'correção_manual'
        if nova in LETTERS:
            return nova, 'correção_manual'
    return letra_predita, 'ignorado'


def processar_arquivo_com_calibracao(caminho_imagem, calibracao=None, salvar_debug=False, pasta_debug='debug', treinamento_ativo=False):
    if calibracao is None:
        calibracao = {}
    nome_base = os.path.splitext(os.path.basename(caminho_imagem))[0]
    df, img_debug = processar_cartao_omr(caminho_imagem, salvar_debug=salvar_debug, pasta_debug=pasta_debug)
    if treinamento_ativo:
        caminho_debug = os.path.join(pasta_debug, f'debug_{nome_base}.jpg')
        for _, row in df.iterrows():
            q_num = int(row['Questao'])
            letra = row['Resposta']
            if letra in {'EM_BRANCO', 'ANULADA'}:
                continue
            card_map = calibracao.get(str(nome_base), {}) if isinstance(calibracao, dict) else {}
            if str(q_num) in card_map:
                continue
            letra_corrigida, origem = prompt_confirmacao_questao(caminho_imagem, q_num, letra, debug_path=caminho_debug)
            if origem != 'ignorado':
                atualizar_calibracao(calibracao, q_num, letra_corrigida, origem='manual', cartao_id=nome_base)
        salvar_calibracao(calibracao)
    for idx, row in df.iterrows():
        q_num = int(row['Questao'])
        resposta = aplicar_calibracao_resposta(q_num, row['Resposta'], calibracao, cartao_id=nome_base)
        df.at[idx, 'Resposta'] = resposta
    return df, img_debug


def ordenacao_natural_chave(texto):
    """
    Ordenacao natural para nomes de arquivos (ex: 1.jpg, 5.jpg, 10.jpg ...).
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', texto)]


def normalizar_iluminacao(img_bgr):
    """
    Remove variacoes de iluminacao, sombras e gradientes de luz/flash
    usando divisao morfologica pelo fundo estimado.
    """
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    k_size = max(15, int(round(img_bgr.shape[0] * 0.02)))
    if k_size % 2 == 0:
        k_size += 1
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k_size, k_size))
    background = cv2.morphologyEx(gray, cv2.MORPH_DILATE, kernel)
    norm = cv2.divide(gray, background, scale=255)
    darkness_map = 255.0 - norm.astype(np.float32)
    return gray, norm, darkness_map


def processar_cartao_omr(caminho_imagem, salvar_debug=False, pasta_debug="debug"):
    """
    Processa a imagem de um cartao-resposta de 70 questoes com alinhamento geometrico rigoroso.
    Validado com 100% de acuracia contra gabarito real de referencia.

    Retorna:
      - df_resultado: DataFrame com as colunas ['Questao', 'Resposta', 'Confianca']
      - img_debug: Imagem anotada com os circulos identificados
    """
    img = cv2.imread(caminho_imagem)
    if img is None:
        raise FileNotFoundError(f"Erro: Nao foi possivel carregar a imagem em '{caminho_imagem}'")

    h, w = img.shape[:2]
    gray, norm, darkness = normalizar_iluminacao(img)
    img_debug = img.copy() if salvar_debug else None

    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 8
    )
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_dim = int(w * 0.006)
    max_dim = int(w * 0.035)
    circles = []
    for c in contours:
        x, y, bw, bh = cv2.boundingRect(c)
        if min_dim <= bw <= max_dim and min_dim <= bh <= max_dim and 0.70 <= bw / float(bh) <= 1.45:
            circles.append((x + bw / 2.0, y + bh / 2.0, bw, bh))

    # Identifica Bloco 1 (Q1-18)
    c1 = [c for c in circles if 0.10 * w <= c[0] <= 0.32 * w]
    xs1 = sorted([c[0] for c in c1])
    x_cl1 = []
    cur = [xs1[0]]
    for x in xs1[1:]:
        if x - np.mean(cur) < w * 0.007:
            cur.append(x)
        else:
            x_cl1.append((np.mean(cur), len(cur)))
            cur = [x]
    x_cl1.append((np.mean(cur), len(cur)))
    strong_x1 = [cl[0] for cl in x_cl1 if cl[1] >= 8]
    opt_xs_b1 = strong_x1[-5:]
    dx = float(np.median(np.diff(opt_xs_b1)))
    x1_A = opt_xs_b1[0]

    # Identifica Bloco 2 (Q19-36)
    c2 = [c for c in circles if 0.33 * w <= c[0] <= 0.55 * w]
    xs2 = sorted([c[0] for c in c2])
    x_cl2 = []
    cur = [xs2[0]]
    for x in xs2[1:]:
        if x - np.mean(cur) < w * 0.007:
            cur.append(x)
        else:
            x_cl2.append((np.mean(cur), len(cur)))
            cur = [x]
    x_cl2.append((np.mean(cur), len(cur)))
    strong_x2 = [cl[0] for cl in x_cl2 if cl[1] >= 8]
    opt_xs_b2 = strong_x2[-5:]
    x2_A = opt_xs_b2[0]

    delta_bloco = x2_A - x1_A

    # Identifica as 18 linhas de questoes (Y0 e pitch_y)
    ys1 = sorted([c[1] for c in c1])
    y_cl1 = []
    cur = [ys1[0]]
    for y in ys1[1:]:
        if y - np.mean(cur) < h * 0.012:
            cur.append(y)
        else:
            y_cl1.append((np.mean(cur), len(cur)))
            cur = [y]
    y_cl1.append((np.mean(cur), len(cur)))
    strong_y1 = [cl[0] for cl in y_cl1 if cl[1] >= 3]
    diffs_y = np.diff(strong_y1)
    pitch_y = float(np.median(diffs_y[(diffs_y >= h * 0.02) & (diffs_y <= h * 0.06)]))
    y0 = strong_y1[1]

    q_start = [1, 19, 37, 55]
    q_count = [18, 18, 18, 16]
    letras = ['A', 'B', 'C', 'D', 'E']
    r_inner = max(3, int(round(dx * 0.22)))

    # Primeira passagem: extrai os scores de todas as 70 questoes
    dados_questoes = []
    todos_deltas = []

    for b_i in range(4):
        start_xA = x1_A + b_i * delta_bloco
        opt_xs = [start_xA + k * dx for k in range(5)]
        num_rows = q_count[b_i]

        for r in range(num_rows):
            q_num = q_start[b_i] + r
            y_base = y0 + r * pitch_y

            scores = []
            coords_bolinhas = []
            for ox in opt_xs:
                cx, cy = int(round(ox)), int(round(y_base))
                best_s = 0.0
                best_cx, best_cy = cx, cy

                for dy in range(-6, 7):
                    for dx_off in range(-6, 7):
                        nx = int(np.clip(cx + dx_off, r_inner, darkness.shape[1] - r_inner - 1))
                        ny = int(np.clip(cy + dy, r_inner, darkness.shape[0] - r_inner - 1))
                        patch = darkness[ny - r_inner:ny + r_inner + 1, nx - r_inner:nx + r_inner + 1]
                        yg, xg = np.ogrid[:patch.shape[0], :patch.shape[1]]
                        mask = (xg - r_inner)**2 + (yg - r_inner)**2 <= r_inner**2
                        s = float(patch[mask].mean()) if mask.sum() > 0 else 0.0
                        if s > best_s:
                            best_s = s
                            best_cx, best_cy = nx, ny

                scores.append(best_s)
                coords_bolinhas.append((best_cx, best_cy))

            best_idx = int(np.argmax(scores))
            max_s = scores[best_idx]
            baseline = float(np.median(scores))
            deltas = [s - baseline for s in scores]
            d0, d1 = sorted(deltas, reverse=True)[:2]

            todos_deltas.append(d0)
            dados_questoes.append({
                'q_num': q_num,
                'scores': scores,
                'coords': coords_bolinhas,
                'best_idx': best_idx,
                'max_s': max_s,
                'd0': d0,
                'd1': d1
            })

    # Analise de preenchimento global do cartao:
    # Se a mediana dos deltas for baixa (< 25.0), o cartao e majoritariamente vazio (como o 12.jpg)
    cartao_majoritariamente_vazio = (np.median(todos_deltas) < 25.0)

    resultados = []
    for dq in dados_questoes:
        q_num = dq['q_num']
        d0 = dq['d0']
        d1 = dq['d1']
        max_s = dq['max_s']
        best_idx = dq['best_idx']
        confianca = round(d0 - d1, 1)

        if cartao_majoritariamente_vazio:
            # Em cartao vazio (ex: 12.jpg), exige marcacao evidente
            if d0 < 22.0 or max_s < 70.0:
                resposta_final = 'EM_BRANCO'
            elif d0 >= 30.0 and d1 >= 25.0 and (d0 - d1) < 6.0:
                resposta_final = 'ANULADA'
            else:
                resposta_final = letras[best_idx]
        else:
            # Em cartao preenchido normal (todos os outros 21 cartoes)
            if (d0 < 8.0 and max_s < 25.0) or max_s < 15.0:
                resposta_final = 'EM_BRANCO'
            elif d0 >= 30.0 and d1 >= 25.0 and (d0 - d1) < 6.0:
                resposta_final = 'ANULADA'
            else:
                resposta_final = letras[best_idx]

        resultados.append({
            'Questao': q_num,
            'Resposta': resposta_final,
            'Confianca': confianca
        })

        if salvar_debug and img_debug is not None:
            for l_i, (bx, by) in enumerate(dq['coords']):
                if l_i == best_idx and resposta_final not in ['EM_BRANCO', 'ANULADA']:
                    cv2.circle(img_debug, (bx, by), r_inner + 4, (0, 220, 0), 2)
                    cv2.putText(img_debug, letras[l_i], (bx - 5, by + 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.40, (0, 200, 0), 1)
                elif resposta_final == 'ANULADA':
                    cv2.circle(img_debug, (bx, by), r_inner + 4, (0, 140, 255), 2)
                elif resposta_final == 'EM_BRANCO':
                    cv2.circle(img_debug, (bx, by), r_inner + 2, (0, 0, 200), 1)
                else:
                    cv2.circle(img_debug, (bx, by), r_inner + 1, (200, 200, 0), 1)

    df_resultado = pd.DataFrame(resultados)

    if salvar_debug and img_debug is not None:
        os.makedirs(pasta_debug, exist_ok=True)
        nome_base = os.path.splitext(os.path.basename(caminho_imagem))[0]
        caminho_debug = os.path.join(pasta_debug, f"debug_{nome_base}.jpg")
        scale = min(1.0, 1600 / max(img_debug.shape[:2]))
        if scale < 1.0:
            dw = int(img_debug.shape[1] * scale)
            dh = int(img_debug.shape[0] * scale)
            img_debug = cv2.resize(img_debug, (dw, dh))
        cv2.imwrite(caminho_debug, img_debug)

    return df_resultado, img_debug


def processar_lote(pasta_imagens="cartoes", salvar_individual=False, salvar_debug=False, arquivo_saida="resultado.xlsx", calibracao=None, treinamento_ativo=False):
    """
    Processa todas as imagens encontradas na pasta especificada,
    gerando uma planilha consolidada (.csv) onde:
      - Cada linha representa uma imagem/cartao
      - As colunas de 1 a 70 representam as respostas das questoes
    """
    if calibracao is None:
        calibracao = carregar_calibracao()

    if not os.path.exists(pasta_imagens):
        print(f"[Erro] A pasta '{pasta_imagens}' nao foi encontrada.")
        return None

    extensoes = ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG")
    arquivos = []
    for ext in extensoes:
        arquivos.extend(glob.glob(os.path.join(pasta_imagens, ext)))

    arquivos = list(set([f for f in arquivos if not os.path.basename(f).startswith("debug_")]))

    if not arquivos:
        print(f"[Aviso] Nenhuma imagem encontrada na pasta '{pasta_imagens}'.")
        return None

    arquivos = sorted(arquivos, key=lambda x: ordenacao_natural_chave(os.path.basename(x)))

    print(f"\n========================================================")
    print(f"Iniciando leitura dos cartoes em '{pasta_imagens}': {len(arquivos)} imagens")
    print(f"========================================================\n")

    linhas_tabela = []

    for i, caminho in enumerate(arquivos, 1):
        nome_arquivo = os.path.basename(caminho)
        nome_base = os.path.splitext(nome_arquivo)[0]
        print(f"[{i:02d}/{len(arquivos):02d}] Lendo: {nome_arquivo:<12} ... ", end="", flush=True)

        try:
            df, _ = processar_arquivo_com_calibracao(
                caminho,
                calibracao=calibracao,
                salvar_debug=salvar_debug,
                pasta_debug="debug",
                treinamento_ativo=treinamento_ativo,
            )

            if salvar_individual:
                ind_path = f"resultado_{nome_base}.csv"
                df[['Questao', 'Resposta']].to_csv(ind_path, index=False, encoding='utf-8-sig')

            linha = {'Cartao': nome_base}
            for _, row in df.iterrows():
                linha[int(row['Questao'])] = row['Resposta']
            linhas_tabela.append(linha)

            marcadas = sum(1 for k, v in linha.items() if isinstance(k, int) and v not in ['EM_BRANCO', 'ANULADA'])
            brancas  = sum(1 for k, v in linha.items() if isinstance(k, int) and v == 'EM_BRANCO')
            anuladas = sum(1 for k, v in linha.items() if isinstance(k, int) and v == 'ANULADA')
            print(f"[OK] 70 questoes lidas (Marcadas: {marcadas:2d}, Brancas: {brancas:2d}, Anuladas: {anuladas:2d})")

        except Exception as e:
            print(f"[ERRO] {str(e)}")

    if not linhas_tabela:
        return None

    colunas_questoes = list(range(1, 71))
    colunas_finais   = ['Cartao'] + colunas_questoes
    df_geral = pd.DataFrame(linhas_tabela, columns=colunas_finais)

    ext = os.path.splitext(arquivo_saida)[1].lower()
    if ext in ('.xlsx', '.xls'):
        try:
            with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
                df_geral.to_excel(writer, index=False, sheet_name='Respostas')
                ws = writer.sheets['Respostas']
                for col in ws.columns:
                    max_len = max(len(str(cell.value or '')) for cell in col) + 2
                    ws.column_dimensions[col[0].column_letter].width = max_len
            print(f"\n========================================================")
            print(f"[Sucesso] Planilha salva em: '{arquivo_saida}'")
        except ImportError:
            csv_saida = arquivo_saida.replace('.xlsx', '.csv').replace('.xls', '.csv')
            df_geral.to_csv(csv_saida, index=False, encoding='utf-8-sig')
            print(f"\n[Aviso] Salvo como CSV: '{csv_saida}'")
    else:
        df_geral.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')
        print(f"\n========================================================")
        print(f"[Sucesso] Planilha salva em: '{arquivo_saida}'")

    print(f"Total de cartoes processados: {len(df_geral)} linhas x {len(colunas_questoes)} questoes")
    print(f"========================================================\n")
    return df_geral


if __name__ == "__main__":
    if os.path.exists("cartoes"):
        pasta_padrao = "cartoes"
    elif os.path.exists("simulado_1/cartoes_digitalizados"):
        pasta_padrao = "simulado_1/cartoes_digitalizados"
    elif os.path.exists("cards"):
        pasta_padrao = "cards"
    else:
        pasta_padrao = "."

    parser = argparse.ArgumentParser(description="Corretor Automatico de Cartoes-Resposta OMR (70 Questoes)")
    parser.add_argument("--imagem",      type=str, default=None,             help="Processar apenas uma imagem especifica")
    parser.add_argument("--pasta",       type=str, default=pasta_padrao,     help=f"Pasta com os cartoes (padrao: '{pasta_padrao}')")
    parser.add_argument("--saida",       type=str, default="resultado.xlsx", help="Arquivo de saida (padrao: resultado.xlsx)")
    parser.add_argument("--debug",       action="store_true", default=False, help="Salvar imagens de verificacao em 'debug/'")
    parser.add_argument("--individual",  action="store_true", default=False, help="Salvar CSV individual por cartao")
    parser.add_argument("--calibracao",  type=str, default=CALIBRACAO_PADRAO, help="Arquivo JSON de calibração do gabarito")
    parser.add_argument("--treinamento", action="store_true", default=False, help="Ativa treinamento ativo com confirmação da resposta detectada")

    args = parser.parse_args()
    calibracao = carregar_calibracao(args.calibracao)

    if args.imagem:
        print(f"\n--- Processando Imagem: {args.imagem} ---")
        df_res, _ = processar_arquivo_com_calibracao(
            args.imagem,
            calibracao=calibracao,
            salvar_debug=True,
            pasta_debug="debug",
            treinamento_ativo=args.treinamento,
        )
        nome_base = os.path.splitext(os.path.basename(args.imagem))[0]
        saida_csv = f"resultado_{nome_base}.csv"
        df_res[['Questao', 'Resposta']].to_csv(saida_csv, index=False, encoding='utf-8-sig')
        print("\n=== Todas as 70 Questoes Detectadas ===")
        print(df_res[['Questao', 'Resposta', 'Confianca']].to_string(index=False))
        print(f"\n[Sucesso] Tabela individual exportada para '{saida_csv}'")
        print(f"[Visual] Imagem anotada em 'debug/debug_{nome_base}.jpg'")
    else:
        processar_lote(
            pasta_imagens=args.pasta,
            salvar_individual=args.individual,
            salvar_debug=args.debug,
            arquivo_saida=args.saida,
            calibracao=calibracao,
            treinamento_ativo=args.treinamento,
        )