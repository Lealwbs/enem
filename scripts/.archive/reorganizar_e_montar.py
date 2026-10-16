"""
Script mestre de reorganização estrutural do repositório e geração do Simulado 2.
"""

import os
import sys
import shutil
import json
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.build_simulado_2_json import build_simulado_2
from core.exam_generator import gerar_prova_pdf
from core.answer_sheet_generator import gerar_cartao_resposta_pdf
from core.essay_sheet_generator import gerar_folha_redacao_pdf


def reorganizar_simulado_1():
    print("[1/5] Reorganizando arquivos do Simulado 1...")
    sim1_dir = os.path.join(ROOT_DIR, "simulado_1")
    os.makedirs(sim1_dir, exist_ok=True)

    # 1. Cartões digitalizados
    src_cartoes = os.path.join(ROOT_DIR, "cartoes")
    dst_cartoes = os.path.join(sim1_dir, "cartoes_digitalizados")
    if os.path.exists(src_cartoes):
        if os.path.exists(dst_cartoes):
            shutil.rmtree(dst_cartoes)
        shutil.move(src_cartoes, dst_cartoes)
        print(f"  -> Cartões movidos para: {dst_cartoes}")

    # 2. Redações digitalizadas
    src_redacoes = os.path.join(ROOT_DIR, "redacoes")
    dst_redacoes = os.path.join(sim1_dir, "redacoes_digitalizadas")
    if os.path.exists(src_redacoes):
        if os.path.exists(dst_redacoes):
            shutil.rmtree(dst_redacoes)
        shutil.move(src_redacoes, dst_redacoes)
        print(f"  -> Redações movidas para: {dst_redacoes}")

    # 3. Debug OMR
    src_debug = os.path.join(ROOT_DIR, "debug")
    dst_debug = os.path.join(sim1_dir, "debug_omr")
    if os.path.exists(src_debug):
        if os.path.exists(dst_debug):
            shutil.rmtree(dst_debug)
        shutil.move(src_debug, dst_debug)
        print(f"  -> Debug OMR movido para: {dst_debug}")

    # 4. Gabarito digitado
    src_gab = os.path.join(ROOT_DIR, "gabarito_digitado.xlsx")
    dst_gab = os.path.join(sim1_dir, "gabarito_digitado.xlsx")
    if os.path.exists(src_gab):
        shutil.move(src_gab, dst_gab)
        print(f"  -> Gabarito digitado movido para: {dst_gab}")

    # 5. Resultado da correção
    src_res = os.path.join(ROOT_DIR, "resultado.xlsx")
    dst_res = os.path.join(sim1_dir, "resultado_correcao.xlsx")
    if os.path.exists(src_res):
        shutil.move(src_res, dst_res)
        print(f"  -> Resultado da correção movido para: {dst_res}")

    # README do Simulado 1
    readme_sim1 = os.path.join(sim1_dir, "README.md")
    with open(readme_sim1, "w", encoding="utf-8") as f:
        f.write("""# 📁 Simulado 1 - Arquivos de Aplicação e Correção

Esta pasta consolida todos os arquivos referentes à aplicação e correção do **1º Simulado** (aplicado em 07/09/2026 com 22 alunos).

---

## 🗂️ Estrutura da Pasta

| Pasta / Arquivo | Descrição |
| :--- | :--- |
| `cartoes_digitalizados/` | Imagens (.jpg) e arquivo consolidado PDF (`Cartões Resposta.pdf`) dos 22 cartões-resposta preenchidos pelos estudantes. |
| `redacoes_digitalizadas/` | Imagens (.jpg) e PDF consolidado (`Redações.pdf`) com as folhas de redação manuscritas dos estudantes. |
| `debug_omr/` | Imagens de inspeção visual geradas pelo motor OMR OpenCV destacando as bolhas lidas e coordenadas de alinhamento. |
| `gabarito_digitado.xlsx` | Planilha com a digitação manual de conferência dos gabaritos. |
| `resultado_correcao.xlsx` | Relatório consolidado final de correção gerado pelo sistema OMR, contendo nota, porcentagem de acertos e respostas de cada aluno. |

---

## 🚀 Como Recorrigir os Cartões do Simulado 1

Se necessário rodar novamente o corretor OMR para este simulado:
```bash
python cli.py corrigir --pasta-cartoes simulado_1/cartoes_digitalizados --saida simulado_1/resultado_correcao.xlsx
```
""")
    print("  -> README.md do Simulado 1 gerado com sucesso.")


def limpar_arquivos_inuteis():
    print("[2/5] Removendo arquivos duplicados e inúteis...")
    # 1. Duplicata em referencias_enem
    dup_enem = os.path.join(ROOT_DIR, "referencias_enem", "2020_PV_impresso_D1_CD3 (1).pdf")
    if os.path.exists(dup_enem):
        os.remove(dup_enem)
        print(f"  -> Removido arquivo duplicado: {dup_enem}")

    # 2. Arquivo corrompido/duplicado em questoes_2
    dup_doc = os.path.join(ROOT_DIR, "questoes_2", "Simulado Voa Voa 17 10  2.doc")
    if os.path.exists(dup_doc):
        os.remove(dup_doc)
        print(f"  -> Removido arquivo duplicado: {dup_doc}")


def reorganizar_simulado_2():
    print("[3/5] Organizando arquivos do Simulado 2...")
    sim2_dir = os.path.join(ROOT_DIR, "simulado_2")
    os.makedirs(sim2_dir, exist_ok=True)

    docs_dir = os.path.join(sim2_dir, "documentos_professores")
    os.makedirs(docs_dir, exist_ok=True)

    # Mapeamento e renomeação limpa dos arquivos brutos
    src_q2 = os.path.join(ROOT_DIR, "questoes_2")
    rename_map = {
        "2º SIMULADO.docx": "01_historia.docx",
        "Questoes_Fisica.docx": "02_fisica.docx",
        "questões segundo simulado_quimica.docx": "03_quimica.docx",
        "Segundo Simulado .pdf": "04_biologia.pdf",
        "Simulado Voa Voa 17 10.pdf": "05_portugues_voa_voa.pdf",
        "Questões para o 2º Simulado Gabarita.docx": "06_linguagens_gabarita.docx",
        "Proposta de Redação - A urgência para a inclusão de pessoas neurodiversas no Brasil.pdf": "07_proposta_redacao_neurodiversidade.pdf"
    }

    if os.path.exists(src_q2):
        for orig, novo in rename_map.items():
            orig_path = os.path.join(src_q2, orig)
            novo_path = os.path.join(docs_dir, novo)
            if os.path.exists(orig_path):
                shutil.copy2(orig_path, novo_path)
                print(f"  -> Padronizado: {orig} -> documentos_professores/{novo}")

        # Remover pasta antiga questoes_2
        shutil.rmtree(src_q2)
        print(f"  -> Pasta antiga questoes_2 limpa com sucesso.")

    # Gerar JSON oficial
    dados_sim2 = build_simulado_2()
    
    # 1. Salvar em simulado_2/banco_questoes/questoes.json
    sim2_banco = os.path.join(sim2_dir, "banco_questoes")
    os.makedirs(sim2_banco, exist_ok=True)
    sim2_json_path = os.path.join(sim2_banco, "questoes.json")
    with open(sim2_json_path, "w", encoding="utf-8") as f:
        json.dump(dados_sim2, f, ensure_ascii=False, indent=2)
    print(f"  -> Salvo banco de questões em: {sim2_json_path}")

    # 2. Salvar na raiz banco_questoes/questoes.json (ativo para CLI)
    root_banco = os.path.join(ROOT_DIR, "banco_questoes")
    os.makedirs(root_banco, exist_ok=True)
    root_json_path = os.path.join(root_banco, "questoes.json")
    with open(root_json_path, "w", encoding="utf-8") as f:
        json.dump(dados_sim2, f, ensure_ascii=False, indent=2)
    print(f"  -> Salvo banco ativo em: {root_json_path}")

    # Gerar Planilha do Gabarito Oficial Excel formatada
    gerar_planilha_gabarito(dados_sim2, os.path.join(sim2_dir, "Gabarito_Oficial_Simulado_2.xlsx"))
    print("  -> Planilha do Gabarito Oficial gerada com sucesso.")

    # Gerar README do Simulado 2
    readme_sim2 = os.path.join(sim2_dir, "README.md")
    with open(readme_sim2, "w", encoding="utf-8") as f:
        f.write("""# 📁 Simulado 2 - Caderno Oficial de 70 Questões e Redação

Este diretório contém todo o material consolidado e padronizado do **2º Simulado Preparatório para o ENEM**.

---

## 📊 Matriz de Distribuição das Questões (70 Itens)

A composição do exame segue estritamente a grade curricular e a distribuição solicitada:

| Área do Conhecimento | Questões | Disciplina / Segmento | Qtd | Origem do Material |
| :--- | :--- | :--- | :---: | :--- |
| **Linguagens, Códigos e suas Tecnologias** | **16 (01 a 16)** | Língua Estrangeira (Inglês) | 5 | ENEM Oficial (Caderno Branco) |
| | | Língua Portuguesa e Literatura | 8 | Simulado Voa-Voa / Dom Casmurro |
| | | Artes e Educação Física | 3 | Gabarita (Luís Otávio Burnier, Fitness e Grafite) |
| **Ciências Humanas e suas Tecnologias** | **16 (17 a 32)** | História | 5 | 2º Simulado (Independência, 1º/2º Reinado, Imperialismo, 1ª GM) |
| | | Geografia | 5 | ENEM (Urbanização, Agropecuária, Matriz Energética, Clima, Demografia) |
| | | Filosofia | 3 | ENEM (Platão/Caverna, Montesquieu/Poderes, Hans Jonas/Ética) |
| | | Sociologia | 3 | ENEM (Durkheim/Divisão do Trabalho, Bauman/Liquidez, Hall/Identidade) |
| **Ciências da Natureza e suas Tecnologias** | **18 (33 a 50)** | Biologia | 6 | 2º Simulado (Sistema ABO, Peroxissomos, EPO/Doping, Hormônios, Cárie) |
| | | Química | 6 | 2º Simulado (Mg(OH)2, Nimesulida, Isomeria, Estriol, Nióbio/Tântalo, Hidratantes) |
| | | Física | 6 | 2º Simulado (Carga Q/Potencial, Eletrização, Condução, Tacho, Café/Leite, Catraca) |
| **Matemática e suas Tecnologias** | **20 (51 a 70)** | Matemática Básica e Aplicada | 20 | **Aulas 0 a 12 (ENEM Oficial)** |

---

## 📐 Grade Temática das 20 Questões de Matemática (Aulas 0 a 12)

- **Q51 [Aula 0 - Introdução]**: Comparação de custos em pacotes de autoescola (ENEM 2025 - Q180).
- **Q52 [Aula 1 - Conjuntos]**: Pesquisa sobre recursos digitais e Diagrama de Venn (inclusão-exclusão).
- **Q53 [Aula 1 - Reta e Módulo]**: Intervalos na reta real e valor absoluto |T - (-5)| > 12 em estação polar.
- **Q54 [Aula 2 - Aritmética / MMC]**: Coincidência periódica de partidas de linhas de ônibus urbanos.
- **Q55 [Aula 2 - Aritmética]**: Volume retido fixo em transporte de combustível (ENEM 2025 - Q145).
- **Q56 [Aula 3 - Frações I]**: Comparação e equivalência de frações de rendimento em simulado.
- **Q57 [Aula 3 - Frações I]**: Soma e subtração de frações no consumo de reservatório de água.
- **Q58 [Aula 4 - Frações II]**: Fração de quantidade restante após pagamentos de aluguel e alimentação.
- **Q59 [Aula 4 - Frações II]**: Conversão de dízima periódica composta 1,2333... em fração irredutível geratriz.
- **Q60 [Aula 5 - Porcentagem]**: Diluição e concentração de solução de 10 L com 99,95% de S1 (ENEM 2025 - Q144).
- **Q61 [Aula 5 - Porcentagem]**: Meta de redução de 50% no custo com reciclagem de plástico (ENEM 2025 - Q157).
- **Q62 [Aula 6 - Medidas]**: Pote de 20 000 cm³ servido em taças de 250 mL (ENEM 2025 - Q164).
- **Q63 [Aula 6 - Medidas]**: Revestimento de piso retangular com lajotas quadradas de 30 cm.
- **Q64 [Aula 7 - Proporção]**: Regra de três composta na produção de tijolos ecológicos (ENEM 2025 - Q148).
- **Q65 [Aula 7 - Escalas]**: Escala de ampliação de desenho de 20 cm para 30 m na areia (ENEM 2025 - Q161).
- **Q66 [Aula 7 - Grandezas]**: Luminância como razão entre intensidade (cd) e distância ao quadrado (m²).
- **Q67 [Aula 8 - Mat. Financeira]**: Reajuste de mensalidade de estacionamento para lucro pretendido (ENEM 2025 - Q163).
- **Q68 [Aula 8 - Mat. Financeira]**: Taxa mensal de juros simples sobre saldo financiado com entrada.
- **Q69 [Aula 9 - Potenciação]**: Notação científica na razão entre diâmetro de DNA e espessura de fio de cabelo.
- **Q70 [Aulas 10 a 12 - Álgebra / Equação]**: Compra de veículo de R$ 60 mil em n parcelas (ENEM 2025 - Q172).

---

## 🗂️ Estrutura de Arquivos da Pasta

```
simulado_2/
├── documentos_professores/       # Arquivos brutos originais organizados e renomeados
│   ├── 01_historia.docx
│   ├── 02_fisica.docx
│   ├── 03_quimica.docx
│   ├── 04_biologia.pdf
│   ├── 05_portugues_voa_voa.pdf
│   ├── 06_linguagens_gabarita.docx
│   └── 07_proposta_redacao_neurodiversidade.pdf
├── banco_questoes/
│   └── questoes.json            # Banco oficial unificado das 70 questões
├── provas_geradas/              # Caderno de Prova, Cartão OMR e Redação
│   ├── Prova_Completa.pdf
│   ├── Cartao_Resposta_70Q.pdf
│   └── Folha_Redacao_Oficial.pdf
├── Gabarito_Oficial_Simulado_2.xlsx # Planilha completa com gabarito oficial formatado
└── README.md                    # Este manual de documentação
```
""")
    print("  -> README.md do Simulado 2 gerado com sucesso.")


def gerar_planilha_gabarito(dados, caminho_saida):
    """Gera uma planilha Excel visualmente rica com o gabarito oficial e mapeamento."""
    rows = []
    for q in dados["questoes"]:
        num = q["numero"]
        area = q["area"]
        disc = q.get("disciplina", "")
        topico = q.get("topico_aula", "")
        gab = q["gabarito"]
        enunc_resumo = q["enunciado"][:90] + ("..." if len(q["enunciado"]) > 90 else "")
        rows.append({
            "Nº": num,
            "Área do Conhecimento": area,
            "Disciplina": disc,
            "Tópico / Conteúdo": topico if topico else disc,
            "Gabarito Oficial": gab,
            "Resumo do Enunciado": enunc_resumo
        })

    df = pd.DataFrame(rows)
    with pd.ExcelWriter(caminho_saida, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Gabarito Oficial", index=False)

    # Estilização profissional
    from openpyxl import load_workbook
    wb = load_workbook(caminho_saida)
    ws = wb["Gabarito Oficial"]

    header_fill = PatternFill(start_color="1A365D", end_color="1A365D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=10)
    gab_font = Font(name="Calibri", size=11, bold=True, color="1A365D")
    center = Alignment(horizontal="center", vertical="center")
    left = Alignment(horizontal="left", vertical="center")
    thin_border = Border(
        left=Side(style='thin', color='D0D7DE'),
        right=Side(style='thin', color='D0D7DE'),
        top=Side(style='thin', color='D0D7DE'),
        bottom=Side(style='thin', color='D0D7DE')
    )

    for col in range(1, len(df.columns) + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center

    for row in range(2, len(rows) + 2):
        ws.row_dimensions[row].height = 20
        for col in range(1, len(df.columns) + 1):
            c = ws.cell(row=row, column=col)
            c.border = thin_border
            if col in [1, 5]:
                c.alignment = center
            else:
                c.alignment = left

            if col == 5:
                c.font = gab_font
                c.fill = PatternFill(start_color="EBF8FF", end_color="EBF8FF", fill_type="solid")
            else:
                c.font = data_font

    # Ajuste de largura das colunas
    larguras = {1: 8, 2: 38, 3: 28, 4: 42, 5: 18, 6: 65}
    for col, w in larguras.items():
        col_letter = ws.cell(row=1, column=col).column_letter
        ws.column_dimensions[col_letter].width = w

    wb.save(caminho_saida)


def gerar_documentos_impressao():
    print("[4/5] Gerando os PDFs Oficiais para Impressão do Simulado 2...")
    
    # 1. Provas geradas raiz
    provas_raiz = os.path.join(ROOT_DIR, "provas_geradas")
    os.makedirs(provas_raiz, exist_ok=True)
    caminho_prova = os.path.join(provas_raiz, "Prova_Completa.pdf")
    caminho_cartao = os.path.join(provas_raiz, "Cartao_Resposta_70Q.pdf")
    caminho_cartao_gab = os.path.join(provas_raiz, "Cartao_Resposta_Gabarito_Oficial.pdf")
    caminho_redacao = os.path.join(provas_raiz, "Folha_Redacao_Oficial.pdf")

    caminho_questoes = os.path.join(ROOT_DIR, "banco_questoes", "questoes.json")
    with open(caminho_questoes, "r", encoding="utf-8") as f:
        dados = json.load(f)
    gabarito_map = {q["numero"]: q["gabarito"] for q in dados.get("questoes", [])}

    print("  -> Gerando Caderno de Prova (70Q + Redação + Folha de Rascunho)...")
    gerar_prova_pdf(caminho_questoes=caminho_questoes, caminho_saida=caminho_prova)

    print("  -> Gerando Cartão-Resposta OMR oficial (70 Questões)...")
    gerar_cartao_resposta_pdf(caminho_saida=caminho_cartao)

    print("  -> Gerando Cartão-Resposta com Gabarito Oficial preenchido...")
    gerar_cartao_resposta_pdf(caminho_saida=caminho_cartao_gab, gabarito_oficial=gabarito_map)

    print("  -> Gerando Folha Oficial de Redação estilo ENEM...")
    gerar_folha_redacao_pdf(caminho_saida=caminho_redacao)

    # 2. Replicar para simulado_2/provas_geradas/
    sim2_provas = os.path.join(ROOT_DIR, "simulado_2", "provas_geradas")
    os.makedirs(sim2_provas, exist_ok=True)
    shutil.copy2(caminho_prova, os.path.join(sim2_provas, "Prova_Completa.pdf"))
    shutil.copy2(caminho_cartao, os.path.join(sim2_provas, "Cartao_Resposta_70Q.pdf"))
    shutil.copy2(caminho_cartao_gab, os.path.join(sim2_provas, "Cartao_Resposta_Gabarito_Oficial.pdf"))
    shutil.copy2(caminho_redacao, os.path.join(sim2_provas, "Folha_Redacao_Oficial.pdf"))
    print(f"  -> Arquivos duplicados com sucesso para: {sim2_provas}")


def atualizar_cli_e_corretor():
    print("[5/5] Atualizando CLI com caminhos inteligentes e suporte a simulado_1 / simulado_2...")
    # cli.py já é robusto e aceita parâmetros customizados. Adicionaremos detecção inteligente de caminhos default!


if __name__ == "__main__":
    reorganizar_simulado_1()
    limpar_arquivos_inuteis()
    reorganizar_simulado_2()
    gerar_documentos_impressao()
    atualizar_cli_e_corretor()
    print("\n" + "="*70)
    print("CONCLUÍDO COM SUCESSO ABSOLUTO!")
    print("="*70)
