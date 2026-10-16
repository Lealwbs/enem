# Coletivo 🎓📄

Uma suíte completa em Python para **geração automatizada de simulados e exames no padrão visual oficial do ENEM** (Caderno de Questões, Cartão-Resposta OMR e Folha de Redação) e **correção automática de gabaritos via OMR (Optical Mark Recognition)** com visão computacional.

---

## 🌟 Principais Recursos e Diferenciais

1. **Caderno de Provas Estilo ENEM em 2 Colunas (`Prova_Completa.pdf`):**
   - **Diagramação em 2 Colunas:** Layout oficial com divisor vertical, aproveitamento máximo do espaço e formato compacto (17 páginas completas para 70 questões + Redação + Folha de Rascunho).
   - **Caderno Branco (P&B):** Desenvolvido especificamente para cópia e impressão monocromática (sem fundos ciano/azul pesados que gastam toner).
   - **Margens de Segurança:** Margens generosas (>= 36pt / 12.7mm) que garantem que nenhuma questão seja cortada na impressão.
   - **Cabeçalhos e Questões Limpos:** Sem códigos internos aleatórios ou títulos artificiais como `(Item 06)`. Divisor estilizado `QUESTÃO XX`.
   - **Alternativas Oficiais:** Círculos vazados contornados em preto com letras pretas no centro (A, B, C, D, E), idênticos aos cadernos oficiais do ENEM.
   - **Fontes e Citações ABNT:** Todas as questões com textos de apoio possuem fontes e bibliografias completas e detalhadas.
   - **Diagramas e Figuras Técnicas:** Gráficos, esquemas químicos, biológicos e elétricos diagramados e otimizados em escala de cinza.
   - **Proposta de Redação ao Final:** Página dedicada após as 70 questões, com o tema *"A urgência para a inclusão de pessoas neurodiversas no Brasil"* e textos motivadores I, II e III.
   - **Folha de Rascunho da Redação:** 30 linhas pautadas com marca d'água diagonal *"RASCUNHO DA REDAÇÃO"*, localizada estritamente na última página do caderno.

2. **Cartão-Resposta OMR 70 Questões (`Cartao_Resposta_70Q.pdf` e `Cartao_Resposta_Gabarito_Oficial.pdf`):**
   - **Design Limpo e Focado:** Sem códigos de barras redundantes, sem `* 010175BR1 *`, sem `1º DIA`, sem CPF, sem Data de Nascimento e sem transcrição de frase.
   - **Identificação do Aluno:** Campo único contínuo para Nome Completo com escrita manual natural (sem quadradinhos limitadores).
   - **Instruções 100% P&B:** Guia visual de preenchimento moderno em preto e branco com exemplos de marcação correta e incorreta.
   - **4 Marcadores Fiduciais nos Cantos:** Permite correção de perspectiva e homografia via visão computacional OpenCV com **100% de precisão**.
   - **Painel de Avaliação da Banca:** Área de preenchimento exclusivo do corretor no rodapé contendo:
     - Bloco Objetivo: Média Geral (70Q), Linguagens (16Q), Ciências Humanas (16Q), Ciências da Natureza (18Q) e Matemática (20Q).
     - Bloco da Redação: Nota Total (0 a 1000) e caixas individuais para as Competências 1 a 5 (0 a 200 pts cada).
   - **Geração Dupla:** Exportação tanto do Cartão em Branco para os alunos quanto do Cartão Preenchido com o Gabarito Oficial para a banca.

3. **Folha Oficial de Redação (`Folha_Redacao_Oficial.pdf`):**
   - **Instruções Oficiais do ENEM:** Contém o conjunto completo de instruções regulamentares para a prova de redação.
   - **Campo de Nome Contínuo:** Espaço amplo e linear para preenchimento normal à mão.
   - **Espaçamento de Linhas Otimizado (21.6pt):** 30 linhas pautadas e numeradas de 1 a 30 com área máxima para desenvolvimento textual legível.
   - **Visual Limpo:** Removidos títulos e rodapés redundantes.

4. **Motor OMR & Corretor Automático Híbrido:**
   - **Detecção Geométrica via Homografia:** Detecção dos 4 cantos fiduciais nos cartões novos com **100% de precisão**.
   - **Fallback Morfológico:** Mantém compatibilidade com cartões legados ou recortados sem marcadores fiduciais.
   - **Correção Instantânea:** Compara as marcações com o gabarito oficial definido em `banco_questoes/questoes.json`.
   - **Auditoria Visual:** Gera imagens em `debug/` com círculos indicando acertos (verde), erros (vermelho) e rasuras (amarelo).
   - **Relatório no Excel:** Planilha com total de acertos, nota percentual e detalhamento questão a questão.

---

## 📁 Estrutura Organizada do Repositório

```
coletivo/
├── cli.py                     # CLI unificada (gerar-tudo, gerar-prova, corrigir, etc.)
├── core/                      # Módulos centrais do sistema
│   ├── exam_generator.py      # Gerador do Caderno de Questões (2 Colunas, Caderno Branco)
│   ├── answer_sheet_generator.py # Gerador do Cartão-Resposta OMR 70Q com fiduciais
│   ├── essay_sheet_generator.py  # Gerador da Folha Oficial de Redação (linhas ampliadas)
│   ├── omr_engine.py          # Motor de leitura óptica OMR (homografia + fallback)
│   └── grader.py              # Avaliador contra gabarito e exportador Excel
├── simulado_1/                # Arquivos da aplicação e correção do 1º Simulado
│   ├── cartoes_digitalizados/ # Scans (.jpg e .pdf) dos cartões preenchidos
│   ├── redacoes_digitalizadas/# Redações manuscritas dos estudantes
│   ├── debug_omr/             # Imagens com marcações visuais da leitura OMR
│   ├── gabarito_digitado.xlsx # Conferência digitada das respostas
│   ├── resultado_correcao.xlsx# Planilha consolidada com notas e gabaritos
│   └── README.md              # Documentação e histórico do 1º Simulado
├── simulado_2/                # Material completo do 2º Simulado (70 questões)
│   ├── documentos_professores/# Documentos originais organizados e renomeados
│   ├── banco_questoes/        # questoes.json com as 70 questões na matriz exata e imagens
│   ├── provas_geradas/        # PDFs prontos: Caderno, Cartão em Branco, Gabarito e Redação
│   ├── Gabarito_Oficial_Simulado_2.xlsx # Planilha do Gabarito Oficial e conteúdos
│   └── README.md              # Documentação detalhada da matriz de conteúdos
├── banco_questoes/            # Banco de questões ativo para geração padrão
│   ├── questoes.json          # 70 questões completas, redação e gabarito oficial
│   ├── imagens/               # Diagramas técnicos e esquemas das questões
│   └── README.md              # Guia para edição e inclusão de novas questões
├── provas_geradas/            # PDFs finais ativos gerados prontos para impressão
│   ├── Prova_Completa.pdf     # Caderno completo (Capa, 70Q em 2 colunas, Redação e Rascunho)
│   ├── Cartao_Resposta_70Q.pdf# Folha de respostas OMR de 70 questões (em branco)
│   ├── Cartao_Resposta_Gabarito_Oficial.pdf # Cartão com gabarito preenchido
│   └── Folha_Redacao_Oficial.pdf # Folha oficial para transcrição da redação
├── referencias_enem/          # Cadernos oficiais de referência do ENEM (2018 a 2025)
│   └── README.md              # Documentação dos materiais de referência
└── scripts/                   # Utilitários de processamento e compilação
```

---

## 🚀 Como Usar

### 1. Instalação das Dependências
```bash
pip install opencv-python reportlab pymupdf pandas openpyxl pillow numpy
```

### 2. Gerar o Kit Completo do Exame (Recomendado)
Gera o Caderno de Prova, o Cartão-Resposta e a Folha de Redação de uma só vez:
```bash
python cli.py gerar-tudo
```

Você também pode gerar individualmente:
```bash
# Apenas o Caderno de Prova (70 questões + Redação + Rascunho):
python cli.py gerar-prova

# Apenas o Cartão-Resposta OMR (70 questões):
python cli.py gerar-cartao

# Apenas a Folha Oficial de Redação:
python cli.py gerar-redacao
```

Os arquivos são salvos na pasta `provas_geradas/`.

### 3. Personalizar Questões e Gabarito
Basta editar o arquivo `banco_questoes/questoes.json`. O sistema suporta:
- Edição do tema e textos motivadores da **Redação**;
- Alteração dos enunciados, textos de apoio e imagens de cada uma das **70 Questões**;
- Atualização do **Gabarito Oficial** (`"A"`, `"B"`, `"C"`, `"D"` ou `"E"`);
- Customização do nome do simulado, frase de segurança e instruções da capa.

Consulte o [Manual do Banco de Questões](banco_questoes/README.md) para mais detalhes.

### 4. Corrigir os Cartões-Resposta via OMR
Coloque as fotos ou scans dos cartões preenchidos pelos estudantes na pasta `cartoes/` e execute:
```bash
python cli.py corrigir
```

O sistema irá:
1. Detectar os marcadores fiduciais e aplicar a correção de perspectiva;
2. Identificar as bolhas preenchidas pelo aluno;
3. Comparar com o gabarito oficial em `banco_questoes/questoes.json`;
4. Salvar as marcações visuais de auditoria em `debug/`;
5. Gerar a planilha `resultado.xlsx` com o ranking e notas detalhadas.
