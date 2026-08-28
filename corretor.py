"""
================================================================================
CORRETOR AUTOMATICO DE CARTAO-RESPOSTA (OMR - OPTICAL MARK RECOGNITION)
Modelo: Similar ao ENEM (70 Questoes em 4 Blocos, 5 Alternativas A-E)
Tecnologias: Python, OpenCV (cv2), NumPy, Pandas, OpenPyXL
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
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', texto)]


def normalizar_iluminacao(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    k_size = max(15, int(round(img_bgr.shape[0] * 0.02)))
    if k_size % 2 == 0:
        k_size += 1
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k_size, k_size))
    background = cv2.morphologyEx(gray, cv2.MORPH_DILATE, kernel)
    norm = cv2.divide(gray, background, scale=255)
    darkness_map = 255.0 - norm.astype(np.float32)
    return gray, norm, darkness_map


def score_bolinha(darkness, cx, cy, r_inner):
    """
    Calcula o score de preenchimento amostrado no centro da bolinha.
    Usa mascara circular para evitar a borda impressa.
    Pequena busca local (+-2px) para compensar desalinhamentos leves.
    """
    best_score = 0.0
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            nx = int(np.clip(cx + dx, r_inner, darkness.shape[1] - r_inner - 1))
            ny = int(np.clip(cy + dy, r_inner, darkness.shape[0] - r_inner - 1))
            patch = darkness[ny - r_inner:ny + r_inner + 1, nx - r_inner:nx + r_inner + 1]
            if patch.size == 0:
                continue
            y_grid, x_grid = np.ogrid[:patch.shape[0], :patch.shape[1]]
            mask = (x_grid - r_inner) ** 2 + (y_grid - r_inner) ** 2 <= r_inner ** 2
            if mask.sum() == 0:
                continue
            s = float(patch[mask].mean())
            if s > best_score:
                best_score = s
    return best_score


def processar_cartao_omr(caminho_imagem, salvar_debug=False, pasta_debug="debug"):
    img = cv2.imread(caminho_imagem)
    if img is None:
        raise FileNotFoundError(f"Erro: Nao foi possivel carregar a imagem em '{caminho_imagem}'")

    h, w = img.shape[:2]
    gray, norm, darkness = normalizar_iluminacao(img)
    img_debug = img.copy() if salvar_debug else None

    # --- Deteccao dos contornos das bolinhas ---
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 8
    )
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_dim = int(w * 0.005)
    max_dim = int(w * 0.028)
    circles = []
    for cont in contours:
        x, y, bw, bh = cv2.boundingRect(cont)
        if min_dim <= bw <= max_dim and min_dim <= bh <= max_dim and 0.65 <= bw / float(bh) <= 1.50:
            circles.append((x + bw / 2.0, y + bh / 2.0, bw, bh))

    circles = [ci for ci in circles if 0.08 * h <= ci[1] <= 0.97 * h]
    if len(circles) < 50:
        raise ValueError(f"Nao foi possivel detectar bolinhas suficientes em '{caminho_imagem}'.")

    # --- Agrupa em 4 colunas (blocos de questoes) ---
    xs = np.array([[ci[0]] for ci in circles], dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.0001)
    _, col_labels, col_centers = cv2.kmeans(xs, 4, None, criteria, 15, cv2.KMEANS_RANDOM_CENTERS)
    sorted_cols = np.argsort(col_centers.flatten())

    q_start = [1, 19, 37, 55]
    q_count = [18, 18, 18, 16]
    letras = ['A', 'B', 'C', 'D', 'E']
    resultados = []

    for c_i, cluster_id in enumerate(sorted_cols):
        pts = [circles[i] for i in range(len(circles)) if col_labels[i][0] == cluster_id]
        num_rows = q_count[c_i]

        # --- Encontra as 5 sub-colunas (A B C D E) ---
        opt_xs_arr = np.array([[p[0]] for p in pts], dtype=np.float32)
        _, _, opt_centers_sub = cv2.kmeans(
            opt_xs_arr, 5, None, criteria, 15, cv2.KMEANS_RANDOM_CENTERS
        )
        opt_xs = sorted(opt_centers_sub.flatten().tolist())
        diffs = np.diff(opt_xs)
        delta_x = float(np.median(diffs))

        # Raio: 12% do espacamento. Pequeno o suficiente para ficar no centro
        # da bolinha e longe da borda impressa (que fica a ~35-45% do raio total)
        r_inner = max(4, int(round(delta_x * 0.12)))

        # --- Agrupa Ys em linhas ---
        c_ys = np.sort([p[1] for p in pts])
        row_clusters = []
        cur = [c_ys[0]]
        for y in c_ys[1:]:
            if y - np.mean(cur) < h * 0.018:
                cur.append(y)
            else:
                row_clusters.append((np.mean(cur), len(cur)))
                cur = [y]
        row_clusters.append((np.mean(cur), len(cur)))

        strong_rows = [rc[0] for rc in row_clusters if rc[1] >= 2]

        diffs_y = np.diff(strong_rows)
        valid_diffs = diffs_y[(diffs_y >= h * 0.020) & (diffs_y <= h * 0.060)]
        pitch = float(np.median(valid_diffs)) if len(valid_diffs) > 0 else delta_x * 1.3

        # --- Encontra Y0 ---
        best_y0 = strong_rows[0] if strong_rows else h * 0.12
        best_matches = -1
        for cand in strong_rows:
            sa_tmp = np.array(strong_rows)
            matches = sum(
                1 for r in range(num_rows)
                if np.min(np.abs(sa_tmp - (cand + r * pitch))) < pitch * 0.30
            )
            if matches > best_matches:
                best_matches = matches
                best_y0 = cand

        # --- Refinamento via regressao linear ---
        matched_y, matched_r = [], []
        sa = np.array(strong_rows)
        for r in range(num_rows):
            exp = best_y0 + r * pitch
            dist = np.abs(sa - exp)
            if np.min(dist) < pitch * 0.30:
                matched_y.append(sa[np.argmin(dist)])
                matched_r.append(r)
        if len(matched_r) >= 5:
            poly = np.polyfit(matched_r, matched_y, 1)
            pitch, best_y0 = float(poly[0]), float(poly[1])

        # --- Avaliacao por questao ---
        for r in range(num_rows):
            q_num = q_start[c_i] + r
            y_base = best_y0 + r * pitch

            scores = [
                score_bolinha(darkness, int(round(ox)), int(round(y_base)), r_inner)
                for ox in opt_xs
            ]

            best_idx = int(np.argmax(scores))
            best_score_abs = scores[best_idx]

            # Baseline = mediana dos 5 scores da linha (estimativa do fundo)
            baseline = float(np.median(scores))
            deltas = [s - baseline for s in scores]
            sorted_deltas = sorted(deltas, reverse=True)
            d0 = sorted_deltas[0]
            d1 = sorted_deltas[1] if len(sorted_deltas) > 1 else 0.0
            margem = d0 - d1

            # --- Classificacao ---
            # REGRA 1 - EM_BRANCO: score absoluto maximo muito baixo
            #   Bolinhas vazias tem score ~1-15 no centro (papel branco)
            #   Bolinhas preenchidas tem score >= 30 mesmo com iluminacao fraca
            if best_score_abs < 25.0:
                resposta_final = 'EM_BRANCO'

            # REGRA 2 - ANULADA: dois bubbles com score absoluto alto e similares
            #   Exige d0 >= 30 (marcacao forte) E d1 >= 30 E margem pequena
            elif d0 >= 30.0 and d1 >= 30.0 and margem < 15.0:
                resposta_final = 'ANULADA'

            # REGRA 3 - Valida: resposta com maior score
            else:
                resposta_final = letras[best_idx]

            confianca = round(margem, 1)
            resultados.append({'Questao': q_num, 'Resposta': resposta_final, 'Confianca': confianca})

            if salvar_debug and img_debug is not None:
                for l_i, ox in enumerate(opt_xs):
                    bx, by = int(round(ox)), int(round(y_base))
                    if l_i == best_idx and resposta_final not in ['EM_BRANCO', 'ANULADA']:
                        cv2.circle(img_debug, (bx, by), r_inner + 6, (0, 220, 0), 2)
                        cv2.putText(img_debug, letras[l_i], (bx - 5, by + 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 200, 0), 1)
                    elif resposta_final == 'ANULADA':
                        cv2.circle(img_debug, (bx, by), r_inner + 6, (0, 100, 255), 2)
                    elif resposta_final == 'EM_BRANCO':
                        cv2.circle(img_debug, (bx, by), r_inner + 3, (0, 0, 200), 1)
                    else:
                        cv2.circle(img_debug, (bx, by), r_inner + 2, (200, 200, 0), 1)

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


def processar_lote(pasta_imagens="cartoes", salvar_individual=False, salvar_debug=False, arquivo_saida="resultado.xlsx"):
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
            print(f"[Sucesso] Planilha Excel salva em: '{arquivo_saida}'")
        except ImportError:
            csv_saida = arquivo_saida.replace('.xlsx', '.csv').replace('.xls', '.csv')
            df_geral.to_csv(csv_saida, index=False, encoding='utf-8-sig')
            print(f"\n[Aviso] openpyxl nao encontrado. Salvo como CSV: '{csv_saida}'")
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
    parser.add_argument("--saida",      type=str, default="resultado.xlsx", help="Arquivo de saida (padrao: resultado.xlsx)")
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