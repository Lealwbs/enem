# Simulado Coletivo (antigo `omr-exam-grader`) 🎓📄

Uma suíte completa em Python para **geração automatizada de simulados e exames no padrão visual oficial do ENEM** (Caderno de Questões, Cartão-Resposta OMR e Folha de Redação) e **correção automática de gabaritos via OMR (Optical Mark Recognition)** com visão computacional.

---

## 🌟 Principais Recursos e Diferenciais

1. **Caderno de Provas Estilo ENEM em 2 Colunas (`Prova_Completa.pdf`):**
   - **Diagramação em 2 Colunas:** Layout oficial com divisor vertical, aproveitamento máximo do espaço e formato compacto.
   - **Caderno Branco (P&B):** Desenvolvido especificamente para cópia e impressão monocromática (sem fundos ciano/azul pesados que gastam toner).
   - **Margens de Segurança:** Margens generosas (>= 36pt / 12.7mm) que garantem que nenhuma questão seja cortada na impressão.
   - **Cabeçalhos e Questões Limpos:** Sem códigos internos aleatórios (ex: `010175AZ1P12`) ou títulos artificiais como `(Item 06)`. Divisor estilizado `QUESTÃO XX`.
   - **Alternativas em Destaque:** Círculos pretos com letras brancas (A, B, C, D, E) de alto contraste.
   - **Proposta de Redação ao Final:** Página dedicada após as 70 questões, com o tema *"A urgência para a inclusão de pessoas neurodiversas no Brasil"* e textos motivadores I, II e III.
   - **Folha de Rascunho da Redação:** 30 linhas pautadas com marca d'água diagonal *"RASCUNHO DA REDAÇÃO"*, localizada estritamente na última página do caderno.

2. **Cartão-Resposta OMR 70 Questões (`Cartao_Resposta_70Q.pdf`):**
   - **4 Marcadores Fiduciais nos Cantos:** Permite correção de perspectiva e homografia via visão computacional, funcionando mesmo com fotos inclinadas tiradas por celular.
   - **Identificação do Aluno:** Campos para Nome, Inscrição/CPF, Data de Nascimento, Assinatura e Transcrição da Frase da Capa.
   - **Alinhamento Geométrico Rigoroso:** 4 blocos de questões perfeitamente alinhados (Q01-18, Q19-36, Q37-54 e Q55-70).

3. **Folha Oficial de Redação (`Folha_Redacao_Oficial.pdf`):**
   - Baseada fielmente no modelo oficial do ENEM, sem poluição visual ou códigos desconhecidos (removido o número estranho "029" e QRs redundantes).
   - **Espaçamento de Linhas Ampliado (21pt):** Mais espaço vertical e conforto para escrita caligráfica do estudante.
   - 30 linhas pautadas e numeradas de 1 a 30 com delimitação de margens.

4. **Motor OMR & Corretor Automático Híbrido:**
   - **Detecção Geométrica via Homografia:** Detecção dos 4 cantos fiduciais nos cartões novos com **100% de precisão**.
   - **Fallback Morfológico:** Mantém compatibilidade com cartões antigos ou recortados sem marcadores fiduciais.
   - **Correção Instantânea:** Compara as marcações com o gabarito oficial definido em `banco_questoes/questoes.json`.
   - **Auditoria Visual:** Gera imagens em `debug/` com círculos indicando acertos (verde), erros (vermelho) e rasuras (amarelo).
   - **Relatório no Excel (`resultado.xlsx`):** Planilha com total de acertos, nota percentual e detalhamento questão a questão.

---

## 📁 Estrutura Organizada do Repositório

```
omr-exam-grader/ (Simulado Coletivo)
├── cli.py                     # CLI unificada do sistema (gerar-tudo, corrigir, etc.)
├── core/                      # Módulos centrais do sistema
│   ├── exam_generator.py      # Gerador do Caderno de Questões (2 Colunas, Caderno Branco)
│   ├── answer_sheet_generator.py # Gerador do Cartão-Resposta OMR 70Q com fiduciais
│   ├── essay_sheet_generator.py  # Gerador da Folha Oficial de Redação (linhas ampliadas)
│   ├── omr_engine.py          # Motor de leitura óptica OMR (homografia + fallback)
│   └── grader.py              # Avaliador contra gabarito e exportador Excel
├── banco_questoes/            # Banco de questões estruturado
│   ├── questoes.json          # 70 questões completas, redação e gabarito oficial
│   ├── README.md              # Guia para edição e inclusão de novas questões
│   └── imagens/               # Estruturas químicas e ilustrações das questões
├── provas_geradas/            # PDFs finais gerados prontos para impressão/aplicação
│   ├── Prova_Completa.pdf     # Caderno completo (Capa, 70Q em 2 colunas, Redação e Rascunho)
│   ├── Cartao_Resposta_70Q.pdf# Folha de respostas OMR de 70 questões
│   └── Folha_Redacao_Oficial.pdf # Folha oficial para transcrição da redação
├── questoes_2/                # Arquivos brutos fornecidos (Word e PDF originais)
│   └── README.md              # Documentação das fontes originais por matéria
├── referencias_enem/          # Modelos oficiais de referência do ENEM (cadernos, folhas)
│   └── README.md              # Documentação dos materiais de referência
├── scripts/                   # Utilitários de processamento e compilação
│   └── parse_and_build_banco.py # Script extrator dos documentos originais para o banco
├── cartoes/                   # Amostras de cartões preenchidos para teste de correção
├── debug/                     # Imagens com demarcações visuais da correção OMR
└── resultado.xlsx             # Planilha consolidada com notas e gabarito dos alunos
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
