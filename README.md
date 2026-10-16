# 🎯 Coletivo • Sistema Integrado de Criação de Provas Estilo ENEM e Correção OMR

Sistema completo desenvolvido para o **Coletivo Voa Voa & Preparatório Gabarita** para:
1. **Geração Automatizada de Provas e Exames:** Caderno completo padrão ENEM (Caderno Branco, layout 2 colunas, proposta de redação no meio, rascunho de 30 linhas e tipografia TrueType).
2. **Folha Unificada Frente e Verso:** Cartão-Resposta OMR (Página 1) + Folha Oficial de Redação (Página 2) em um único arquivo PDF otimizado para impressão duplex.
3. **Correção Automática por Visão Computacional (OMR):** Motor óptico com correção de iluminação, alinhamento por marcadores fiduciais (homografia) e fallback morfológico robusto.

---

## 📁 Arquitetura do Repositório

```
omr-exam-grader/
├── app/                                # Pacote principal da aplicação
│   ├── __init__.py
│   ├── __main__.py                     # Permite executar via: python -m app
│   ├── cli.py                          # CLI com subcomandos (gerar-tudo, gerar-prova, corrigir, etc.)
│   ├── corretor.py                     # Motor OMR direto para calibração e leitura em lote
│   └── core/                           # Módulos centrais do sistema
│       ├── __init__.py
│       ├── exam_generator.py           # Geração do Caderno de Questões (2 Colunas, Caderno Branco)
│       ├── answer_sheet_generator.py   # Renderizador do Cartão-Resposta 70Q com marcadores OMR
│       ├── essay_sheet_generator.py    # Renderizador da Folha Oficial de Redação (30 linhas)
│       ├── unified_sheet_generator.py  # Gerador do PDF Unificado Frente e Verso (Duplex)
│       ├── omr_engine.py               # Motor OMR (visão computacional, homografia e OpenCV)
│       └── grader.py                   # Comparador contra gabarito e gerador de relatórios Excel
├── scripts/                            # Scripts executáveis de automação
│   ├── gerar_simulado_2.py             # Script master que executa e valida todo o 2º Simulado
│   ├── build_simulado_2_json.py        # Compilador das 70 questões autênticas e proposta de redação
│   └── .archive/                       # Scripts legados e utilitários arquivados
├── simulado_1/                         # Histórico e aplicação do 1º Simulado
│   ├── cartoes_digitalizados/          # Scans (.jpg e .pdf) dos cartões preenchidos
│   ├── redacoes_digitalizadas/         # Redações manuscritas dos estudantes
│   ├── debug_omr/                      # Auditoria visual com acertos e erros marcados
│   ├── gabarito_digitado.xlsx          # Conferência manual de gabaritos
│   └── resultado_correcao.xlsx         # Planilha de notas consolidada
├── simulado_2/                         # Material Oficial do 2º Simulado (70 Questões)
│   ├── banco_questoes/                 # questoes.json oficial e imagens originais extraídas
│   ├── documentos_professores/         # Provas e matrizes originais enviadas pelos professores
│   └── resultado/                      # Entregáveis finais prontos para aplicação e impressão
│       ├── Caderno_Questoes_70Q.pdf    # Caderno de Prova estilo ENEM (16 páginas com capa e redação)
│       ├── Cartao_Resposta_e_Redacao_Frente_Verso.pdf # Folha Unificada pronta para impressão frente/verso
│       ├── Gabarito_Oficial_Preenchido_Frente_Verso.pdf # Gabarito Oficial preenchido frente e verso
│       ├── Gabarito_Oficial_Simulado_2.xlsx # Planilha formatada com habilidades, áreas e gabarito
│       └── .old/                       # Versões legadas/anteriores arquivadas
└── referencias_enem/                   # Cadernos oficiais de referência do ENEM (2018 a 2025)
```

---

## 🚀 Como Executar

### 1. Instalação das Dependências
```bash
pip install opencv-python reportlab pymupdf pandas openpyxl pillow numpy
```

### 2. Geração Completa do 2º Simulado (Comando Único)
Para gerar todos os arquivos finais de uma só vez (Caderno, Folha Frente/Verso, Gabarito e Excel):
```bash
python scripts/gerar_simulado_2.py
```

### 3. Usando a CLI Unificada (`app.cli`)
Você também pode invocar qualquer comando modularmente via linha de comando:

```bash
# Gerar tudo (Caderno de Prova + Folha Frente e Verso)
python -m app gerar-tudo

# Gerar apenas o Caderno de Questões
python -m app gerar-prova

# Gerar apenas a Folha Unificada Frente e Verso
python -m app gerar-unificada

# Executar a correção OMR automática de cartões
python -m app corrigir --simulado 2
```

---

## 📋 Resumo dos Componentes do 2º Simulado

1. **Caderno de Questões (`Caderno_Questoes_70Q.pdf` - 16 páginas):**
   - **Capa Oficial:** Detalhamento das 4 grandes áreas, numeração das questões, aviso rigoroso de caneta preta obrigatória (proibido azul), frase de segurança oficial e título institucional *Coletivo Voa Voa & Preparatório Gabarita*.
   - **Cabeçalhos de Área Colados:** Títulos de área vinculados à primeira questão da seção, sem páginas órfãs.
   - **Questões 100% Autênticas:** 70 questões reais do ENEM e documentos dos professores, sem questões inventadas.
   - **Riqueza Visual:** Mais de 12 imagens e tabelas oficiais integradas (Segall, cartuns em inglês, mapas de satélite, gráficos IPCC, tabelas nutricionais, figuras geométricas).
   - **Proposta de Redação no Meio (Página 8):** Tema oficial sobre Neurodiversidade com 4 textos motivadores e imagens originais.
   - **Folha de Rascunho (Página 9):** 30 linhas numeradas com marca d'água e critérios oficiais de nota zero do ENEM.
   - **Fontes TrueType (Arial):** Renderização perfeita de fórmulas químicas e físicas (`H2O2`, `q0`, `Mg2+`) sem caracteres quadrados.
   - **Rodapé:** Padronizado como `2º SIMULADO ENEM`.

2. **Folha Unificada Frente e Verso (`Cartao_Resposta_e_Redacao_Frente_Verso.pdf`):**
   - **Página 1 (Frente - Cartão-Resposta 70Q):**
     - Cabeçalho institucional e campo contínuo para Nome do Participante.
     - Campo para Transcrição da Frase de Segurança da capa.
     - Instruções compactas com exemplo visual de preenchimento.
     - Grid das 70 questões com 4 cantos fiduciais pretos e marcadores laterais para visão computacional.
     - Campo para assinatura do participante.
     - Painel de Desempenho ancorado no rodapé com amplo espaçamento, detalhando as 4 áreas e redação.
   - **Página 2 (Verso - Folha de Redação):**
     - 30 linhas pautadas numeradas com espaçamento confortável.
     - Regras oficiais de anulação e critérios de correção.
     - Marcadores fiduciais nos 4 cantos para digitalização.

3. **Gabarito Oficial (`Gabarito_Oficial_Simulado_2.xlsx` e `Gabarito_Oficial_Preenchido_Frente_Verso.pdf`):**
   - Planilha Excel estilizada com cores por área do conhecimento, disciplinas, códigos de habilidades e gabarito destacado.
   - PDF preenchido pronto para fixação no mural de avisos e conferência dos estudantes.
