"""
Motor OMR (Optical Mark Recognition) de Alta Precisão para Correção de Cartões-Resposta.
Suporta:
1. Novo Cartão Padrão 70 Questões (com marcadores fiduciais nos 4 cantos e alinhamento por homografia).
2. Cartões Legados / Recortados (com alinhamento geométrico por agrupamento de contornos morfológicos).
"""

import os
import cv2
import numpy as np
import pandas as pd

OPCOES = ["A", "B", "C", "D", "E"]
CANONICAL_W = 1654
CANONICAL_H = 2338


def normalizar_iluminacao(img_bgr):
    """
    Remove variações de iluminação, sombras e gradientes de luz/flash
    usando divisão morfológica pelo fundo estimado.
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


def order_points(pts):
    """Ordena 4 pontos nas posições: top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # top-left
    rect[2] = pts[np.argmax(s)]  # bottom-right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left
    return rect


def detectar_marcadores_fiduciais(gray):
    """
    Busca os 4 marcadores quadrados nos 4 cantos da folha para alinhamento por homografia.
    Retorna os 4 cantos ordenados se encontrar com alta confiança, ou None.
    """
    h, w = gray.shape[:2]
    # Binarização inversa para destacar os quadrados pretos
    _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = (w * 0.015) * (h * 0.01)
    max_area = (w * 0.08) * (h * 0.08)

    candidates = []
    for c in contours:
        area = cv2.contourArea(c)
        if min_area <= area <= max_area:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            if len(approx) == 4:
                x, y, bw, bh = cv2.boundingRect(approx)
                aspect = bw / float(bh)
                if 0.70 <= aspect <= 1.40:
                    M = cv2.moments(c)
                    if M["m00"] > 0:
                        cx = M["m10"] / M["m00"]
                        cy = M["m01"] / M["m00"]
                        candidates.append((cx, cy, approx))

    if len(candidates) < 4:
        return None

    # Tenta encontrar 1 candidato em cada um dos 4 quadrantes
    tl, tr, bl, br = None, None, None, None
    for cand in candidates:
        cx, cy, approx = cand
        if cx < w * 0.25 and cy < h * 0.25:
            tl = (cx, cy)
        elif cx > w * 0.75 and cy < h * 0.25:
            tr = (cx, cy)
        elif cx < w * 0.25 and cy > h * 0.75:
            bl = (cx, cy)
        elif cx > w * 0.75 and cy > h * 0.75:
            br = (cx, cy)

    if tl and tr and bl and br:
        pts = np.array([tl, tr, br, bl], dtype="float32")
        return order_points(pts)
    return None


def get_canonical_bubble_coordinates():
    """
    Calcula as coordenadas teóricas de cada uma das 70 questões na imagem canônica
    (CANONICAL_W x CANONICAL_H) gerada a partir do PDF do Cartão-Resposta.
    """
    # Escalas entre pontos do PDF A4 (595.27 x 841.89) e pixels canônicos (1654 x 2338)
    sx = CANONICAL_W / 595.27
    sy = CANONICAL_H / 841.89

    fid_margin = 20.0
    grid_x = (fid_margin + 20) * sx
    grid_w = (595.27 - 2 * (fid_margin + 20)) * sx
    col_w = (grid_w - 3 * 10 * sx) / 4.0

    # No gerador:
    # y_after_cand = PAGE_HEIGHT - 95 - 100 = 646.89
    # y_after_inst = 646.89 - 44 - 8 = 594.89
    # cy_top = 594.89 - 12 = 582.89 (em coordenadas ReportLab, de baixo para cima)
    # Na imagem do OpenCV (de cima para baixo):
    # y_img = (PAGE_HEIGHT - y_pdf) * sy

    col_defs = [
        {"start": 1, "end": 18},
        {"start": 19, "end": 36},
        {"start": 37, "end": 54},
        {"start": 55, "end": 70},
    ]

    header_h = 18.0
    row_h = 16.5
    opt_dx = 15.0

    coords = {}

    for col_idx, col_def in enumerate(col_defs):
        cx = grid_x + col_idx * (col_w + 10 * sx)
        first_opt_x = cx + 33.0 * sx

        start_q = col_def["start"]
        end_q = col_def["end"]
        num_q = end_q - start_q + 1

        for r in range(num_q):
            q_num = start_q + r
            # Em coordenadas de baixo para cima do PDF:
            pdf_y = 582.89 - header_h - 14.0 - r * row_h
            # Converte para coordenadas de imagem (origem no topo):
            img_y = (841.89 - pdf_y) * sy

            coords[q_num] = {}
            for opt_idx, opt_letter in enumerate(OPCOES):
                bx = first_opt_x + opt_idx * opt_dx * sx
                coords[q_num][opt_letter] = (int(round(bx)), int(round(img_y)))

    return coords


def ler_cartao_fiducial(img_bgr, pts_fiduciais):
    """
    Processa o cartão-resposta alinhando por homografia contra os 4 marcadores dos cantos.
    Garante máxima precisão de leitura para cartões novos gerados pelo sistema.
    """
    # Mapeia os cantos para a resolução canônica
    sx = CANONICAL_W / 595.27
    sy = CANONICAL_H / 841.89
    fid_margin = 20.0
    fid_size = 18.0
    half_fid = fid_size / 2.0

    dst_pts = np.array([
        [(fid_margin + half_fid) * sx, (fid_margin + half_fid) * sy],  # TL
        [(595.27 - fid_margin - half_fid) * sx, (fid_margin + half_fid) * sy],  # TR
        [(595.27 - fid_margin - half_fid) * sx, (841.89 - fid_margin - half_fid) * sy],  # BR
        [(fid_margin + half_fid) * sx, (841.89 - fid_margin - half_fid) * sy]   # BL
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(pts_fiduciais, dst_pts)
    warped = cv2.warpPerspective(img_bgr, M, (CANONICAL_W, CANONICAL_H))

    _, norm, darkness = normalizar_iluminacao(warped)
    coords_teoricas = get_canonical_bubble_coordinates()

    r_inner = int(round(4.8 * sx * 0.75))
    resultados = []
    debug_img = warped.copy()

    for q_num in range(1, 71):
        if q_num not in coords_teoricas:
            continue

        q_opts = coords_teoricas[q_num]
        scores = []
        locs = []

        for opt in OPCOES:
            bx, by = q_opts[opt]
            # Busca melhor intensidade em pequena vizinhança de 3 pixels
            best_s = 0.0
            best_pt = (bx, by)
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    nx = int(np.clip(bx + dx, r_inner, CANONICAL_W - r_inner - 1))
                    ny = int(np.clip(by + dy, r_inner, CANONICAL_H - r_inner - 1))
                    patch = darkness[ny - r_inner:ny + r_inner + 1, nx - r_inner:nx + r_inner + 1]
                    s = float(patch.mean())
                    if s > best_s:
                        best_s = s
                        best_pt = (nx, ny)

            scores.append(best_s)
            locs.append(best_pt)

        best_idx = int(np.argmax(scores))
        max_s = scores[best_idx]
        baseline = float(np.median(scores))
        deltas = [s - baseline for s in scores]
        d0, d1 = sorted(deltas, reverse=True)[:2]

        # Decisão de marcação:
        # Se max_s for baixa ou o contraste (d0) for baixo -> Em branco
        if d0 < 12.0 or max_s < 35.0:
            resposta = "EM_BRANCO"
        elif d0 >= 28.0 and d1 >= 22.0 and (d0 - d1) < 8.0:
            resposta = "ANULADA"
        else:
            resposta = OPCOES[best_idx]

        confianca = round(d0 - d1, 1)

        # Desenho no debug
        for idx, opt in enumerate(OPCOES):
            pt = locs[idx]
            if resposta == opt:
                cv2.circle(debug_img, pt, r_inner + 3, (0, 220, 0), 2)  # Verde: marcada
            elif resposta == "ANULADA" and (scores[idx] - baseline) > 18.0:
                cv2.circle(debug_img, pt, r_inner + 3, (0, 200, 255), 2)  # Amarelo: dupla marcação
            else:
                cv2.circle(debug_img, pt, r_inner + 2, (180, 180, 180), 1)  # Cinza: não marcada

        resultados.append({
            "Questao": q_num,
            "Resposta": resposta,
            "Confianca": confianca
        })

    return pd.DataFrame(resultados), debug_img


def ler_cartao_legado(img_bgr):
    """
    Fallback automático para cartões existentes/legados sem marcadores fiduciais nos cantos
    (como os recortes 1.jpg, 10.jpg na pasta cartoes/).
    Utiliza agrupamento de contornos por colunas e detecção de densidade.
    """
    h, w = img_bgr.shape[:2]
    gray, norm, darkness = normalizar_iluminacao(img_bgr)
    debug_img = img_bgr.copy()

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

    if len(circles) < 30:
        raise ValueError("Não foi possível detectar bolinhas suficientes no cartão.")

    # Identifica Bloco 1 (Q01-18)
    c1 = [c for c in circles if 0.10 * w <= c[0] <= 0.32 * w]
    if not c1:
        c1 = [c for c in circles if c[0] <= 0.35 * w]
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
    opt_xs_b1 = strong_x1[-5:] if len(strong_x1) >= 5 else [cl[0] for cl in x_cl1[-5:]]
    dx = float(np.median(np.diff(opt_xs_b1))) if len(opt_xs_b1) > 1 else w * 0.03
    x1_A = opt_xs_b1[0]

    # Identifica Bloco 2 (Q19-36)
    c2 = [c for c in circles if 0.33 * w <= c[0] <= 0.55 * w]
    if c2:
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
        opt_xs_b2 = strong_x2[-5:] if len(strong_x2) >= 5 else [cl[0] for cl in x_cl2[-5:]]
        x2_A = opt_xs_b2[0]
        delta_bloco = x2_A - x1_A
    else:
        delta_bloco = w * 0.23

    # Identifica as 18 linhas de questões (Y0 e pitch_y)
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
    diffs_y = np.diff(strong_y1) if len(strong_y1) > 1 else [h * 0.04]
    valid_diffs = diffs_y[(diffs_y >= h * 0.02) & (diffs_y <= h * 0.06)]
    pitch_y = float(np.median(valid_diffs)) if len(valid_diffs) > 0 else float(np.median(diffs_y))
    y0 = strong_y1[1] if len(strong_y1) > 1 else strong_y1[0]

    q_start = [1, 19, 37, 55]
    q_count = [18, 18, 18, 16]
    r_inner = max(3, int(round(dx * 0.22)))

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

    cartao_vazio = (np.median(todos_deltas) < 25.0)
    resultados = []

    for dq in dados_questoes:
        q_num = dq['q_num']
        d0 = dq['d0']
        d1 = dq['d1']
        max_s = dq['max_s']
        best_idx = dq['best_idx']
        confianca = round(d0 - d1, 1)

        if cartao_vazio:
            if d0 < 22.0 or max_s < 70.0:
                resposta = 'EM_BRANCO'
            elif d0 >= 30.0 and d1 >= 25.0 and (d0 - d1) < 6.0:
                resposta = 'ANULADA'
            else:
                resposta = OPCOES[best_idx]
        else:
            if (d0 < 8.0 and max_s < 25.0) or max_s < 15.0:
                resposta = 'EM_BRANCO'
            elif d0 >= 30.0 and d1 >= 25.0 and (d0 - d1) < 6.0:
                resposta = 'ANULADA'
            else:
                resposta = OPCOES[best_idx]

        # Debug
        coords = dq['coords']
        for idx, (bx, by) in enumerate(coords):
            if resposta == OPCOES[idx]:
                cv2.circle(debug_img, (bx, by), r_inner + 4, (0, 220, 0), 2)
            elif resposta == 'ANULADA' and dq['scores'][idx] > baseline + 15:
                cv2.circle(debug_img, (bx, by), r_inner + 4, (0, 215, 255), 2)
            else:
                cv2.circle(debug_img, (bx, by), r_inner + 2, (180, 180, 180), 1)

        resultados.append({
            'Questao': q_num,
            'Resposta': resposta,
            'Confianca': confianca
        })

    return pd.DataFrame(resultados), debug_img


def processar_cartao(caminho_imagem, salvar_debug=True, pasta_debug="debug"):
    """
    Função unificada de leitura:
    Tenta primeiro o alinhamento com marcadores fiduciais; se não encontrar, usa o método legado.
    """
    img = cv2.imread(caminho_imagem)
    if img is None:
        raise FileNotFoundError(f"Erro: Não foi possível carregar a imagem em '{caminho_imagem}'")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pts_fiduciais = detectar_marcadores_fiduciais(gray)

    if pts_fiduciais is not None:
        metodo = "Fiducial 4-Corners (Homografia)"
        df, img_debug = ler_cartao_fiducial(img, pts_fiduciais)
    else:
        metodo = "Legado (Agrupamento Morfológico)"
        df, img_debug = ler_cartao_legado(img)

    if salvar_debug and img_debug is not None:
        os.makedirs(pasta_debug, exist_ok=True)
        nome_base = os.path.splitext(os.path.basename(caminho_imagem))[0]
        caminho_out = os.path.join(pasta_debug, f"debug_{nome_base}.jpg")
        cv2.imwrite(caminho_out, img_debug)

    return df, metodo
