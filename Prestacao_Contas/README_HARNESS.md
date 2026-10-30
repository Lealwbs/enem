# Manual do Harness de Prestação de Contas CPOP 2026

Este documento descreve a infraestrutura completa de dados, regras, agentes e procedimentos criada no Antigravity para gerenciar a prestação de contas pedagógica da **Bolsa Cursinho Populares (CPOP 2026)** nos eixos de **Linguagens** e **Matemática**.

---

## 1. Estrutura de Pastas e Dados Armazenados

Toda a memória operacional e os documentos estão estruturados em `D:\PreEnem\Prestacao_Contas\`:

```
D:\PreEnem\Prestacao_Contas\
├── Painel_Status_Geral.md                   <-- Dashboard unificado de status e próximas ações
├── README_HARNESS.md                        <-- Este manual de operação do sistema
│
├── Linguagens\                              <-- Eixo Linguagens (Profª Cleonice Leal / Jd. Laguna)
│   ├── 00_Contexto_e_Plano_Ensino\
│   │   └── Plano_Ensino_Linguagens.md       <-- Ementa oficial, objetivos e bibliografia básica
│   ├── Parcelas\
│   │   ├── Parcela_01_Maio_Junho_CONCLUIDA.md
│   │   ├── Parcela_02_Junho_Julho_TEXTO_APROVADO.md
│   │   ├── Ciclo_Agosto_2026_PRELIMINAR.md
│   │   └── Ciclo_Setembro_2026_PRELIMINAR.md
│   ├── Atividades_Didaticas\                <-- Cadernos e listas aplicadas (PDFs de 19/05 a 23/06)
│   └── Evidencias_Fotos\                    <-- Pasta destinada aos registros de sala da turma
│
├── Matematica\                              <-- Eixo Matemática (Profº Ítalo Leal / Gabarita e Voa Voa)
│   ├── 00_Contexto_e_Cronograma\
│   │   ├── Cronograma_Oficial_26_Aulas.md   <-- Cronograma completo (Aulas 0 a 25) mapeado por parcela
│   │   └── Plano_Trabalho_Bolsa_Matematica.md <-- Plano institucional homologado
│   ├── Parcelas\
│   │   ├── Parcela_01_Aulas_00_02_CONCLUIDA.md
│   │   ├── Parcela_02_Aulas_03_04_CONCLUIDA.md
│   │   ├── Parcela_03_Aulas_05_07_MINUTA_PRONTA.md
│   │   ├── Parcela_04_Aulas_08_10_MINUTA_PRONTA.md
│   │   └── Parcela_05_Aulas_11_14_PLANEJAMENTO.md
│   └── Evidencias_Fotos\                    <-- Pasta destinada às fotos de comprovação presencial
│
└── Templates_e_Diretrizes\
    ├── Template_Formulario_CPOP.md          <-- Modelo oficial de preenchimento para o portal
    └── Regras_de_Redacao_e_Estilo.md        <-- Normas estritas (prosa contínua, sem bullets)
```

---

## 2. Componentes do Harness no Antigravity

### 2.1. Regras do Workspace (`AGENTS.md`)
* Arquivos ativos: `D:\PreEnem\AGENTS.md` e `D:\Code\coletivo\AGENTS.md`.
* Função: Carregamento permanente de diretrizes de redação (prosa contínua, tom formal acadêmico, foco estritamente pedagógico sem custos de terceiros, proibição estrita de marcadores no corpo descritivo).

### 2.2. Skill Especializada (`cpop-prestacao-contas`)
* Localização: `.agents/skills/cpop-prestacao-contas/SKILL.md`.
* Função: Ativação sob demanda para orientar o fluxo sequencial de conferência de parcelas anteriores, mapeamento de aulas no cronograma, redação no layout de formulário e atualização do painel geral de status.

### 2.3. Agentes Especializados (Subagents)
* `cpop_linguagens_auditor`: Subagente dedicado ao componente de Linguagens (Profª Cleonice Leal / Jardim Laguna).
* `cpop_matematica_auditor`: Subagente dedicado ao componente de Matemática (Profº Ítalo Leal / Preparatório Gabarita e Coletivo Voa Voa).

---

## 3. Como Operar para as Próximas Parcelas

Quando desejar realizar ou auditar novas parcelas, basta pedir em linguagem natural:

* **Exemplo 1 (Matemática):**  
  > *"Gere a Parcela 5 de Matemática pronta para colar no sistema do CPOP."*  
  O sistema consultará automaticamente o planejamento das Aulas 11 a 14, vinculará os exercícios 08, 09 e 10 que já existem em `D:\PreEnem\Exercícios PDF Preparatório Gabarita`, formatará a prosa contínua e atualizará o painel.

* **Exemplo 2 (Linguagens):**  
  > *"Consolide a Parcela 3 de Linguagens agrupando as aulas de Agosto."*  
  O sistema recuperará a minuta de Agosto/2026, cruzará com a ementa de Linguagens e formatará o texto no padrão oficial.

* **Exemplo 3 (Auditoria Geral):**  
  > *"Mostre o status atual de todas as parcelas e o que ainda está pendente de assinatura."*  
  O agente lerá o `Painel_Status_Geral.md` e apresentará o quadro analítico atualizado.
