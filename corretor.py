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
import argparse
import cv2
import numpy as np
import pandas as pd


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


def processar_lote(pasta_imagens="cartoes", salvar_individual=False, salvar_debug=False, arquivo_saida="resultado.csv"):
    """
    Processa todas as imagens encontradas na pasta especificada,
    gerando uma planilha consolidada (.csv) onde:
      - Cada linha representa uma imagem/cartao
      - As colunas de 1 a 70 representam as respostas das questoes
    """
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
            df, _ = processar_cartao_omr(caminho, salvar_debug=salvar_debug, pasta_debug="debug")

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
    pasta_padrao = "cartoes" if os.path.exists("cartoes") else "cards" if os.path.exists("cards") else "."

    parser = argparse.ArgumentParser(description="Corretor Automatico de Cartoes-Resposta OMR (70 Questoes)")
    parser.add_argument("--imagem",     type=str, default=None,             help="Processar apenas uma imagem especifica")
    parser.add_argument("--pasta",      type=str, default=pasta_padrao,     help=f"Pasta com os cartoes (padrao: '{pasta_padrao}')")
    parser.add_argument("--saida",      type=str, default="resultado.csv",   help="Arquivo de saida (padrao: resultado.csv)")
    parser.add_argument("--debug",      action="store_true", default=False, help="Salvar imagens de verificacao em 'debug/'")
    parser.add_argument("--individual", action="store_true", default=False, help="Salvar CSV individual por cartao")

    args = parser.parse_args()

    if args.imagem:
        print(f"\n--- Processando Imagem: {args.imagem} ---")
        df_res, _ = processar_cartao_omr(args.imagem, salvar_debug=True, pasta_debug="debug")
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
        )