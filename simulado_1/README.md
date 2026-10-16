# 📁 Simulado 1 - Arquivos de Aplicação e Correção

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
