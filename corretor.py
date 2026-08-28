"""
================================================================================
CORRETOR AUTOMÁTICO DE CARTÃO-RESPOSTA (OMR - OPTICAL MARK RECOGNITION)
Modelo: Similar ao ENEM (70 Questões em 4 Blocos, 5 Alternativas A-E)
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
    Função auxiliar para ordenação natural de strings contendo números
    (ex: 1.jpg, 5.jpg, 10.jpg ao invés de 1.jpg, 10.jpg, 5.jpg).
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', texto)]


def normalizar_iluminacao(img_bgr):
    """
    Remove variações de iluminação, sombras e gradientes de flash/luz
    usando divisão morfológica pelo fundo estimado.
    """
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    # Estimação do fundo com dilatação morfológica adaptada à resolução
    k_size = max(15, int(round(img_bgr.shape[0] * 0.02)))
    if k_size % 2 == 0:
        k_size += 1
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k_size, k_size))
    background = cv2.morphologyEx(gray, cv2.MORPH_DILATE, kernel)
    
    # Divisão pelo fundo normaliza a iluminação para papel branco uniforme
    norm = cv2.divide(gray, background, scale=255)
    
    # Mapa de densidade/escuridão de tinta (0 = branco, 255 = preto absoluto)
    darkness_map = 255.0 - norm.astype(np.float32)
    return gray, norm, darkness_map


def processar_cartao_omr(caminho_imagem, salvar_debug=False, pasta_debug="debug"):
    """
    Processa a imagem de um cartão-resposta de 70 questões com detecção geométrica adaptativa.
    
    Retorna:
      - df_resultado: DataFrame com as colunas ['Questão', 'Resposta', 'Confiança']
      - img_debug: Imagem anotada com os círculos identificados
    """
    img = cv2.imread(caminho_imagem)
    if img is None:
        raise FileNotFoundError(f"Erro: Não foi possível carregar a imagem em '{caminho_imagem}'")

    h, w = img.shape[:2]
    gray, norm, darkness = normalizar_iluminacao(img)
    img_debug = img.copy() if salvar_debug else None

    # Detecção adaptativa dos círculos das bolinhas do cartão
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 8)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    min_dim, max_dim = int(w * 0.005), int(w * 0.025)
    circles = []
    for c in contours:
        x, y, bw, bh = cv2.boundingRect(c)
        if min_dim <= bw <= max_dim and min_dim <= bh <= max_dim and 0.70 <= bw / float(bh) <= 1.40:
            circles.append((x + bw / 2.0, y + bh / 2.0, bw, bh))
            
    # Filtra os círculos na região das questões
    circles = [c for c in circles if 0.10 * h <= c[1] <= 0.95 * h]
    if len(circles) < 50:
        raise ValueError(f"Não foi possível detectar bolinhas suficientes em '{caminho_imagem}'.")

    # Agrupa em 4 colunas horizontais principais (Blocos 1-18, 19-36, 37-54, 55-70)
    xs = np.array([[c[0]] for c in circles], dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    _, col_labels, col_centers = cv2.kmeans(xs, 4, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    sorted_cols = np.argsort(col_centers.flatten())
    
    q_start = [1, 19, 37, 55]
    q_count = [18, 18, 18, 16]
    letras = ['A', 'B', 'C', 'D', 'E']
    resultados = []

    for c_i, cluster_id in enumerate(sorted_cols):
        pts = [circles[i] for i in range(len(circles)) if col_labels[i][0] == cluster_id]
        num_rows = q_count[c_i]
        
        # Encontra as 5 colunas de opções A, B, C, D, E
        opt_xs_arr = np.array([[p[0]] for p in pts], dtype=np.float32)
        _, opt_labels, opt_centers = cv2.kmeans(opt_xs_arr, 5, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        opt_xs = sorted(opt_centers.flatten())
        delta_x = np.median(np.diff(opt_xs[-4:])) if len(opt_xs) >= 4 else (w * 0.021)
        opt_xs = [opt_xs[-1] - (4 - k) * delta_x for k in range(5)]
        
        # Agrupa os Ys para encontrar as linhas da coluna
        c_ys = np.sort([p[1] for p in pts])
        row_clusters = []
        cur = [c_ys[0]]
        for y in c_ys[1:]:
            if y - np.mean(cur) < h * 0.015:
                cur.append(y)
            else:
                row_clusters.append((np.mean(cur), len(cur)))
                cur = [y]
        row_clusters.append((np.mean(cur), len(cur)))
        
        strong_rows = [rc[0] for rc in row_clusters if rc[1] >= 2]
        diffs = np.diff(strong_rows)
        pitch = np.median(diffs[(diffs >= h * 0.025) & (diffs <= h * 0.055)]) if len(diffs) > 0 else delta_x * 1.25
        
        # Identifica a linha inicial correta (Y0) para o bloco de questões
        best_y0 = strong_rows[0]
        best_matches = -1
        for cand in strong_rows:
            matches = sum(1 for r in range(num_rows) if np.min(np.abs(strong_rows - (cand + r * pitch))) < pitch * 0.25)
            if matches > best_matches:
                best_matches = matches
                best_y0 = cand
                
        # Refinamento por regressão linear nas linhas detectadas
        matched_y, matched_r = [], []
        for r in range(num_rows):
            exp = best_y0 + r * pitch
            dist = np.abs(strong_rows - exp)
            if np.min(dist) < pitch * 0.25:
                matched_y.append(strong_rows[np.argmin(dist)])
                matched_r.append(r)
                
        if len(matched_r) >= 6:
            poly = np.polyfit(matched_r, matched_y, 1)
            pitch, best_y0 = poly[0], poly[1]
            
        r_inner = max(3, int(round(delta_x * 0.20)))
        
        # Avaliação de preenchimento para cada questão do bloco
        for r in range(num_rows):
            q_num = q_start[c_i] + r
            y_base = best_y0 + r * pitch
            
            scores = []
            coords_bolinhas = []
            for ox in opt_xs:
                cx, cy = int(round(ox)), int(round(y_base))
                max_d = 0.0
                best_cx, best_cy = cx, cy
                for dy_off in range(-2, 3):
                    for dx_off in range(-2, 3):
                        ccx = np.clip(cx + dx_off, r_inner, darkness.shape[1] - r_inner - 1)
                        ccy = np.clip(cy + dy_off, r_inner, darkness.shape[0] - r_inner - 1)
                        patch = darkness[ccy - r_inner:ccy + r_inner + 1, ccx - r_inner:ccx + r_inner + 1]
                        m = float(np.mean(patch))
                        if m > max_d:
                            max_d = m
                            best_cx, best_cy = ccx, ccy
                scores.append(max_d)
                coords_bolinhas.append((best_cx, best_cy))
                
            baseline = float(np.median(scores))
            deltas = [s - baseline for s in scores]
            sorted_deltas = sorted(deltas, reverse=True)
            best_idx = int(np.argmax(scores))
            confianca = sorted_deltas[0] - sorted_deltas[1] if len(sorted_deltas) > 1 else sorted_deltas[0]
            
            # Regras robustas de classificação OMR:
            # 1. EM_BRANCO: nenhum círculo tem contraste significativo acima do fundo da linha
            # 2. ANULADA: dois ou mais círculos preenchidos com intensidade similar
            # 3. Resposta Válida (A, B, C, D, E): alternativa com maior escore de preenchimento
            if sorted_deltas[0] < 12.0:
                resposta_final = 'EM_BRANCO'
            elif sorted_deltas[0] >= 12.0 and sorted_deltas[1] >= 12.0 and confianca < 8.0:
                resposta_final = 'ANULADA'
            else:
                resposta_final = letras[best_idx]
                
            resultados.append({
                'Questão': q_num,
                'Resposta': resposta_final,
                'Confiança': round(confianca, 1)
            })
            
            # Anotação visual de verificação
            if salvar_debug and img_debug is not None:
                for l_i, (bx, by) in enumerate(coords_bolinhas):
                    if l_i == best_idx and resposta_final not in ['EM_BRANCO', 'ANULADA']:
                        cv2.circle(img_debug, (bx, by), r_inner + 4, (0, 220, 0), 2)
                        cv2.putText(img_debug, letras[l_i], (bx - 4, by + 4),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, (0, 200, 0), 1)
                    else:
                        cv2.circle(img_debug, (bx, by), r_inner + 1, (0, 0, 200), 1)
                        
    df_resultado = pd.DataFrame(resultados)
    
    if salvar_debug and img_debug is not None:
        os.makedirs(pasta_debug, exist_ok=True)
        nome_base = os.path.splitext(os.path.basename(caminho_imagem))[0]
        caminho_debug = os.path.join(pasta_debug, f"debug_{nome_base}.png")
        cv2.imwrite(caminho_debug, img_debug)
        
    return df_resultado, img_debug


def processar_lote(pasta_imagens="cartoes", salvar_individual=False, salvar_debug=False, arquivo_saida="resultado.csv"):
    """
    Processa todas as imagens encontradas na pasta especificada (ex: 'cartoes'),
    gerando uma única planilha consolidada onde:
      - Cada linha representa uma imagem/cartão
      - As colunas de 1 a 70 representam as respostas das questões
    """
    if not os.path.exists(pasta_imagens):
        print(f"[Erro] A pasta '{pasta_imagens}' não foi encontrada.")
        return None

    # Busca apenas por arquivos de imagem suportados (.jpg, .jpeg, .png)
    extensoes = ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG")
    arquivos = []
    for ext in extensoes:
        arquivos.extend(glob.glob(os.path.join(pasta_imagens, ext)))
    
    # Remover arquivos de debug e duplicatas
    arquivos = list(set([f for f in arquivos if not os.path.basename(f).startswith("debug_")]))
    
    if not arquivos:
        print(f"[Aviso] Nenhuma imagem encontrada na pasta '{pasta_imagens}'.")
        return None
    
    # Ordenação natural dos arquivos (ex: 1.jpg, 5.jpg, 8.jpg, 10.jpg ...)
    arquivos = sorted(arquivos, key=lambda x: ordenacao_natural_chave(os.path.basename(x)))
    
    print(f"\n========================================================")
    print(f"Iniciando leitura dos cartões em '{pasta_imagens}': {len(arquivos)} imagens")
    print(f"========================================================\n")
    
    linhas_tabela = []
    
    for i, caminho in enumerate(arquivos, 1):
        nome_arquivo = os.path.basename(caminho)
        nome_base = os.path.splitext(nome_arquivo)[0]
        print(f"[{i:02d}/{len(arquivos):02d}] Lendo: {nome_arquivo:<12} ... ", end="", flush=True)
        
        try:
            df, _ = processar_cartao_omr(caminho, salvar_debug=salvar_debug, pasta_debug="debug")
            
            # Salvar CSV individual caso solicitado
            if salvar_individual:
                csv_individual = f"resultado_{nome_base}.csv"
                df[['Questão', 'Resposta']].to_csv(csv_individual, index=False, encoding='utf-8-sig')
            
            # Monta a linha com o identificador do cartão e as respostas de 1 a 70
            linha = {'Cartao': nome_base}
            for _, row in df.iterrows():
                linha[int(row['Questão'])] = row['Resposta']
                
            linhas_tabela.append(linha)
            
            marcadas = sum(1 for v in linha.values() if v not in [nome_base, 'EM_BRANCO', 'ANULADA'])
            brancas = sum(1 for v in linha.values() if v == 'EM_BRANCO')
            anuladas = sum(1 for v in linha.values() if v == 'ANULADA')
            print(f"[OK] 70 questões lidas (Marcadas: {marcadas:2d}, Brancas: {brancas:2d}, Anuladas: {anuladas:2d})")
        except Exception as e:
            print(f"[ERRO] {str(e)}")
            
    if linhas_tabela:
        colunas_questoes = [i for i in range(1, 71)]
        colunas_finais = ['Cartao'] + [q for q in colunas_questoes if q in linhas_tabela[0]]
        
        df_geral = pd.DataFrame(linhas_tabela)
        df_geral = df_geral[colunas_finais]
        
        df_geral.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')
        
        print(f"\n========================================================")
        print(f"[Sucesso] Planilha consolidada salva em: '{arquivo_saida}'")
        print(f"Total de cartões processados: {len(df_geral)} linhas x {len(colunas_finais)-1} questões")
        print(f"========================================================\n")
        return df_geral
    
    return None


if __name__ == "__main__":
    pasta_padrao = "cartoes" if os.path.exists("cartoes") else "cards" if os.path.exists("cards") else "."
    
    parser = argparse.ArgumentParser(description="Corretor Automático de Cartões-Resposta OMR (70 Questões)")
    parser.add_argument("--imagem", type=str, default=None, help="Processar apenas uma imagem específica")
    parser.add_argument("--pasta", type=str, default=pasta_padrao, help=f"Pasta contendo os cartões (padrão: '{pasta_padrao}')")
    parser.add_argument("--saida", type=str, default="resultado.csv", help="Nome do arquivo CSV de saída (padrão: 'resultado.csv')")
    parser.add_argument("--debug", action="store_true", default=False, help="Salvar imagens de verificação visual na pasta 'debug/'")
    parser.add_argument("--individual", action="store_true", default=False, help="Salvar também um CSV individual para cada cartão")
    
    args = parser.parse_args()
    
    if args.imagem:
        imagem_alvo = args.imagem
        print(f"\n--- Processando Imagem: {imagem_alvo} ---")
        df_res, _ = processar_cartao_omr(imagem_alvo, salvar_debug=True, pasta_debug="debug")
        
        nome_base = os.path.splitext(os.path.basename(imagem_alvo))[0]
        saida_csv = f"resultado_{nome_base}.csv"
        df_res[['Questão', 'Resposta']].to_csv(saida_csv, index=False, encoding='utf-8-sig')
        
        print("\n=== Todas as 70 Questões Detectadas ===")
        print(df_res[['Questão', 'Resposta', 'Confiança']].to_string(index=False))
        print(f"\n[Sucesso] Tabela individual exportada para '{saida_csv}'")
        print(f"[Visual] Imagem anotada de verificação salva em 'debug/debug_{nome_base}.png'")
    else:
        processar_lote(
            pasta_imagens=args.pasta,
            salvar_individual=args.individual,
            salvar_debug=args.debug,
            arquivo_saida=args.saida
        )