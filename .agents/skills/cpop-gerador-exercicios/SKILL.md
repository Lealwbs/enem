---
name: cpop-gerador-exercicios
description: >-
  Selecionar questões oficiais do ENEM, recortar prints em alta resolução, diagramar
  e gerar listas de exercícios em PDF (página única, 2 colunas) e DOCX, além de
  gabaritos e resoluções detalhadas para os polos Coletivo Voa Voa e Preparatório
  Gabarita (CPOP 2026). Use sempre que o usuário solicitar gerar novos exercícios
  ou listas de matemática.
---

# Skill: Gerador de Exercícios ENEM — CPOP 2026

Esta skill orienta a criação, seleção pedagógica, recorte e diagramação de listas de exercícios de Matemática para os polos **Preparatório Gabarita** e **Coletivo Voa Voa** no âmbito do programa **Bolsa Cursinhos Populares (CPOP 2026)**.

---

## 1. Diretrizes Estruturais e Formatação Obrigatória

1. **Página Única Mandatória (A4):**
   - O documento do exercício DEVE ocupar **estritamente 1 única página** (210 x 297 mm).
   - O orçamento vertical da página deve ser calculado rigorosamente para evitar que qualquer elemento transborde para a segunda página.

2. **Diagramação em 2 Colunas:**
   - O corpo do exercício é dividido em 2 colunas iguais com linha divisória vertical cinza clara (`#CCCCCC`).
   - **Coluna 1 (Esquerda):** `QUESTÃO 1)` no topo e `QUESTÃO 2)` na base.
   - **Coluna 2 (Direita):** `QUESTÃO 3)` no topo e `QUESTÃO 4)` na base.
   - As duas colunas devem apresentar alturas totais equilibradas (diferença visual menor que 1 cm).

3. **Prints Autênticos das Questões (Recortes Oficiais):**
   - As questões devem ser **prints fiéis** recortados diretamente dos cadernos oficiais do ENEM (`provas_enem/caderno_cinza_segundo_dia/`).
   - Os recortes devem ser gerados em alta resolução (**300 DPI**, escala $300/72 \approx 4,1667$).
   - O cabeçalho original da prova (ex: `QUESTÃO 138`) **não deve ser incluído na imagem recortada**, pois o documento já traz o título formatado `QUESTÃO X)`. O corte inicia logo abaixo do cabeçalho da prova e encerra imediatamente após a Alternativa E.

4. **Borda Completa da Página:**
   - Borda externa contínua em toda a página A4 (1,5 pt, preta), com margens de 10 mm a 12,7 mm.

5. **Cabeçalho Padrão:**
   - Tabela 3x3 com altura compacta (~35 mm).
   - Célula esquerda (38% de largura) mescla as 3 linhas e exibe o logo da instituição correspondente.
   - Células direitas com bordas sólidas:
     - Linha 1: `Matéria: Matemática` | `Data:           /           / 2026`
     - Linha 2: `Professor: Ítalo Leal` (mesclando 2 colunas)
     - Linha 3: `Aluno(a):` (na lista de alunos) ou `Aluno(a): Respostas` (no gabarito).
   - Título centralizado em negrito: `Exercício [XX]`.

---

## 2. Padrão de Arquivos por Exercício

Para cada exercício gerado (ex: Exercício `XX`), devem ser produzidos e conferidos 5 grupos de arquivos:

| Tipo de Arquivo | Caminho no Repositório | Descrição |
| :--- | :--- | :--- |
| **Recortes PNG (300 DPI)** | `exercicios/recortes_enem/ex<XX>/q1.png` a `q4.png` | Imagens das 4 questões recortadas das provas oficiais. |
| **Matriz DOCX** | `exercicios/docx/Exercício <XX> - Matemática.docx` | Documento editável em formato Word (sem logo na célula de cabeçalho). |
| **PDF Coletivo Voa Voa** | `exercicios/pdf_coletivo_voa_voa/Exercício <XX> - Matemática - Coletivo Voa Voa.pdf` | PDF de 1 página com o logotipo do Coletivo Voa Voa. |
| **PDF Gabarita** | `exercicios/pdf_preparatorio_gabarita/Exercício <XX> - Matemática - Preparatório Gabarita.pdf` | PDF de 1 página com o logotipo do Preparatório Gabarita. |
| **Gabarito e Resoluções** | `exercicios/respostas/Respostas Exercício <XX> - Matemática.docx` e `.pdf` | Resoluções comentadas em etapas estruturadas com gabarito oficial em azul. |

---

## 3. Fluxo Operacional Passo a Passo

### Passo 1: Alinhamento Curricular
1. Consulte `Prestacao_Contas/Matematica/00_Contexto_e_Cronograma/Cronograma_Oficial_26_Aulas.md`.
2. Verifique o número do exercício e o conteúdo programático correspondente à aula.

### Passo 2: Seleção das Questões no Acervo do ENEM
1. Consulte os cadernos disponíveis em `provas_enem/caderno_cinza_segundo_dia/` (especialmente anos recentes: 2025, 2024, 2023).
2. Priorize questões de **nível fácil a médio** segundo a Teoria de Resposta ao Item (TRI) — questões conceituais, intuitivas e motivadoras.
3. Priorize questões com **figuras, tabelas, diagramas ou gráficos**.
4. Calcule a altura das questões candidatas para garantir que caibam perfeitamente duas por coluna.

### Passo 3: Extração e Recorte dos Prints em Alta Resolução
Utilize `pymupdf` (fitz) para renderizar a 300 DPI com matriz `fitz.Matrix(300/72, 300/72)` e salvar em `exercicios/recortes_enem/ex<XX>/q1.png` a `q4.png`.

```python
import fitz

doc = fitz.open('provas_enem/caderno_cinza_segundo_dia/ENEM_2023_Dia2_Caderno6_Cinza_Regular.pdf')
page = doc[page_num - 1]
mat = fitz.Matrix(300 / 72, 300 / 72)
# Define o retângulo contendo da linha abaixo de 'QUESTÃO XXX' até a opção E
rect = fitz.Rect(x0, y0, x1, y1)
pix = page.get_pixmap(matrix=mat, clip=rect)
pix.save('exercicios/recortes_enem/ex<XX>/q1.png')
```

### Passo 4: Geração do DOCX Matriz
Carregue o exercício anterior via `python-docx`, atualize o título para `Exercício <XX>` e substitua as imagens da tabela de 2 colunas com as novas `q1.png` a `q4.png`, ajustando a largura de cada uma (geralmente entre 7,0 cm e 8,2 cm).

### Passo 5: Geração dos PDFs com Renderização Perfeita (Página Única)
1. Monte o template HTML A4 com os dados institucionais, logos em Base64 e os recortes PNG.
2. Compile o PDF via Chrome Headless:
   ```bash
   google-chrome --headless --disable-gpu --no-sandbox --print-to-pdf="[CAMINHO_DO_PDF]" --no-pdf-header-footer "[CAMINHO_DO_HTML]"
   ```
3. **Auditoria Obrigatória de Páginas:**
   Execute `pdfinfo "[CAMINHO_DO_PDF]"` e assegure que o campo `Pages:` seja estritamente `1`.

### Passo 6: Redação do Gabarito Comentado (Resoluções)
1. Redija a resolução de cada questão estruturada em etapas:
   - `QUESTÃO N) — ENEM YYYY - Caderno 6 Cinza (Questão XXX)` em negrito.
   - `Gabarito Oficial: Alternativa X (Texto)` com destaque em azul escuro (`#003399`).
   - Passos numerados (`1. Análise dos dados:`, `2. Resolução algébrica/geométrica:`, `3. Conclusão:`).
2. Salve o arquivo DOCX e gere o PDF correspondente em `exercicios/respostas/`.

### Passo 7: Conferência Visual
Renderize a primeira página dos PDFs gerados usando `pdftoppm -png -r 150` e visualize com `view_file` para assegurar que a tipografia, logos e enquadramentos estejam perfeitos.
