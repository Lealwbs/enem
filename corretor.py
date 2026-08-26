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
import argparse
import cv2
import numpy as np
import pandas as pd


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


def obter_configuracao_colunas(img_shape):
    """
    Retorna as coordenadas normalizadas proporcionais à resolução da imagem
    para os 4 blocos de questões (1-18, 19-36, 37-54, 55-70).
    """
    h_img, w_img = img_shape[:2]
    
    col_configs = [
        {
            'start_q': 1,
            'end_q': 18,
            'hx': 0.1475 * w_img,
            'y0': 0.2902 * h_img,
            'opt_dx': [0.0357 * w_img, 0.0559 * w_img, 0.0766 * w_img, 0.0974 * w_img, 0.1192 * w_img]
        },
        {
            'start_q': 19,
            'end_q': 36,
            'hx': 0.3560 * w_img,
            'y0': 0.2885 * h_img,
            'opt_dx': [0.0357 * w_img, 0.0559 * w_img, 0.0766 * w_img, 0.0974 * w_img, 0.1192 * w_img]
        },
        {
            'start_q': 37,
            'end_q': 54,
            'hx': 0.5634 * w_img,
            'y0': 0.2859 * h_img,
            'opt_dx': [0.0357 * w_img, 0.0559 * w_img, 0.0766 * w_img, 0.0974 * w_img, 0.1192 * w_img]
        },
        {
            'start_q': 55,
            'end_q': 70,
            'hx': 0.7696 * w_img,
            'y0': 0.2824 * h_img,
            'opt_dx': [0.0357 * w_img, 0.0559 * w_img, 0.0766 * w_img, 0.0974 * w_img, 0.1192 * w_img]
        },
    ]
    
    pitch_y = 0.01964 * h_img
    return col_configs, pitch_y


def processar_cartao_omr(caminho_imagem, salvar_debug=True):
    """
    Processa a imagem de um cartão-resposta de 70 questões.
    
    Retorna:
      - df_resultado: DataFrame com as colunas ['Questão', 'Resposta', 'Confiança']
      - img_debug: Imagem anotada com os círculos identificados
    """
    img = cv2.imread(caminho_imagem)
    if img is None:
        raise FileNotFoundError(f"Erro: Não foi possível carregar a imagem em '{caminho_imagem}'")

    gray, norm, darkness = normalizar_iluminacao(img)
    col_configs, pitch_y_padrao = obter_configuracao_colunas(img.shape)
    
    letras = ['A', 'B', 'C', 'D', 'E']
    resultados = []
    img_debug = img.copy()
    
    # Raio de busca e patch proporcional à resolução
    raio_patch = max(3, int(round(img.shape[0] * 0.004)))
    
    # Processa cada um dos 4 blocos de questões
    for col in col_configs:
        start_q = col['start_q']
        end_q = col['end_q']
        hx = col['hx']
        y0 = col['y0']
        opt_dx = col['opt_dx']
        num_questoes_bloco = end_q - start_q + 1
        
        # Rastreamento dinâmico de linhas para absorver rotações/deformações de perspectiva
        y_atual = y0
        linhas_y = [y_atual]
        
        for _ in range(1, num_questoes_bloco):
            y_estimado = y_atual + pitch_y_padrao * 1.015
            melhor_y = y_estimado
            max_intensidade = -1
            
            # Busca local do pico de tinta da linha (bolinhas e números)
            delta_busca = pitch_y_padrao * 0.25
            for dy in np.linspace(-delta_busca, delta_busca, 21):
                y_teste = y_estimado + dy
                y_int = int(round(y_teste))
                if 0 <= y_int < darkness.shape[0]:
                    soma = sum(
                        darkness[y_int, min(darkness.shape[1]-1, int(round(hx + dx)))]
                        for dx in opt_dx
                    )
                    if soma > max_intensidade:
                        max_intensidade = soma
                        melhor_y = y_teste
                        
            y_atual = melhor_y
            linhas_y.append(y_atual)
            
        # Avaliação de preenchimento das alternativas em cada questão
        for q_idx, y_linha in enumerate(linhas_y):
            q_num = start_q + q_idx
            scores_alternativas = []
            coordenadas_bolinhas = []
            
            for dx in opt_dx:
                # Busca do centro exato da bolinha na vizinhança 5x5
                max_densidade = 0.0
                centro_x_otimo = int(round(hx + dx))
                centro_y_otimo = int(round(y_linha))
                
                step_x = max(1, int(round(raio_patch * 0.5)))
                for dy_off in range(-step_x, step_x + 1):
                    for dx_off in range(-step_x, step_x + 1):
                        cx = int(round(hx + dx + dx_off))
                        cy = int(round(y_linha + dy_off))
                        
                        if raio_patch <= cy < darkness.shape[0]-raio_patch and raio_patch <= cx < darkness.shape[1]-raio_patch:
                            patch = darkness[cy-raio_patch:cy+raio_patch+1, cx-raio_patch:cx+raio_patch+1]
                            media = float(np.mean(patch))
                            if media > max_densidade:
                                max_densidade = media
                                centro_x_otimo = cx
                                centro_y_otimo = cy
                                
                scores_alternativas.append(max_densidade)
                coordenadas_bolinhas.append((centro_x_otimo, centro_y_otimo))
                
            # Identificação da alternativa mais escura
            best_idx = int(np.argmax(scores_alternativas))
            scores_ordenados = sorted(scores_alternativas, reverse=True)
            confianca = scores_ordenados[0] - scores_ordenados[1]
            
            # Regras de classificação:
            # 1. Em Branco: nenhum círculo atinge limiar de marcação
            # 2. Anulada / Dupla Marcação: dois círculos muito escuros e com escore próximo
            # 3. Válida: alternativa com maior densidade
            if scores_ordenados[0] < 45.0:
                resposta_final = 'EM_BRANCO'
            elif confianca < 12.0 and scores_ordenados[0] > 70.0 and scores_ordenados[1] > 70.0:
                resposta_final = 'ANULADA'
            else:
                resposta_final = letras[best_idx]
                
            resultados.append({
                'Questão': q_num,
                'Resposta': resposta_final,
                'Confiança': round(confianca, 1)
            })
            
            # Anotação visual no mapa de debug
            for l_i, (bx, by) in enumerate(coordenadas_bolinhas):
                if l_i == best_idx and resposta_final not in ['EM_BRANCO', 'ANULADA']:
                    # Círculo verde para a resposta identificada
                    cv2.circle(img_debug, (bx, by), raio_patch + 3, (0, 220, 0), 2)
                    cv2.putText(img_debug, letras[l_i], (bx - 4, by + 4),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 200, 0), 1)
                else:
                    # Círculo vermelho suave para alternativas não preenchidas
                    cv2.circle(img_debug, (bx, by), raio_patch + 1, (0, 0, 200), 1)
                    
    df_resultado = pd.DataFrame(resultados)
    
    if salvar_debug:
        nome_base = os.path.splitext(os.path.basename(caminho_imagem))[0]
        caminho_debug = f"debug_{nome_base}.png"
        cv2.imwrite(caminho_debug, img_debug)
        
    return df_resultado, img_debug


def processar_lote(pasta_imagens=".", padrao="*.jp*g", salvar_individual=True):
    """
    Processa todas as imagens encontradas em lote (ex: as 22 imagens de prova),
    gerando CSVs individuais e uma tabela geral consolidada.
    """
    arquivos = glob.glob(os.path.join(pasta_imagens, padrao))
    arquivos.extend(glob.glob(os.path.join(pasta_imagens, "*.png")))
    # Remover arquivos de debug gerados
    arquivos = [f for f in arquivos if not os.path.basename(f).startswith("debug_")]
    
    if not arquivos:
        print(f"[Aviso] Nenhuma imagem encontrada em '{pasta_imagens}' com o padrão especificado.")
        return None
    
    print(f"\n========================================================")
    print(f"Iniciando processamento em lote: {len(arquivos)} imagens encontradas")
    print(f"========================================================\n")
    
    tabela_consolidada = {}
    
    for i, caminho in enumerate(sorted(arquivos), 1):
        nome_arquivo = os.path.basename(caminho)
        nome_base = os.path.splitext(nome_arquivo)[0]
        print(f"[{i:02d}/{len(arquivos):02d}] Processando: {nome_arquivo} ... ", end="")
        
        try:
            df, _ = processar_cartao_omr(caminho, salvar_debug=True)
            
            # Salvar CSV individual
            if salvar_individual:
                csv_individual = f"resultado_{nome_base}.csv"
                df[['Questão', 'Resposta']].to_csv(csv_individual, index=False, encoding='utf-8')
                
            tabela_consolidada[nome_base] = df.set_index('Questão')['Resposta']
            print(f"[OK] 70 questões lidas.")
        except Exception as e:
            print(f"[ERRO] {str(e)}")
            
    # Criar DataFrame consolidado com todas as folhas
    if tabela_consolidada:
        df_geral = pd.DataFrame(tabela_consolidada)
        df_geral.index.name = 'Questão'
        df_geral.reset_index(inplace=True)
        
        csv_geral = "resultado_consolidado_provas.csv"
        df_geral.to_csv(csv_geral, index=False, encoding='utf-8')
        print(f"\n========================================================")
        print(f"[Sucesso] Tabela consolidada exportada para: '{csv_geral}'")
        print(f"========================================================\n")
        return df_geral
    
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Corretor Automático de Cartões-Resposta OMR (70 Questões)")
    parser.add_argument("--imagem", type=str, default="1.jpeg", help="Caminho para uma imagem específica")
    parser.add_argument("--pasta", type=str, default=None, help="Caminho para a pasta com as 22 imagens de prova")
    parser.add_argument("--todas", action="store_true", help="Processar todas as imagens na pasta atual")
    
    args = parser.parse_args()
    
    if args.pasta or args.todas:
        pasta = args.pasta if args.pasta else "."
        processar_lote(pasta_imagens=pasta)
    else:
        imagem_alvo = args.imagem
        print(f"\n--- Processando Imagem: {imagem_alvo} ---")
        df_res, _ = processar_cartao_omr(imagem_alvo, salvar_debug=True)
        
        nome_base = os.path.splitext(os.path.basename(imagem_alvo))[0]
        saida_csv = f"resultado_{nome_base}.csv"
        df_res[['Questão', 'Resposta']].to_csv(saida_csv, index=False, encoding='utf-8')
        
        print("\n=== Todas as 70 Questões Detectadas ===")
        print(df_res[['Questão', 'Resposta', 'Confiança']].to_string(index=False))
        print(f"\n[Sucesso] Tabela exportada para '{saida_csv}'")
        print(f"[Visual] Imagem anotada de verificação salva em 'debug_{nome_base}.png'")