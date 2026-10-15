# Banco de Questões - Instruções e Formato

Esta pasta contém os arquivos de entrada com as **questões**, **redação** e **gabarito** para o gerador de provas e o corretor automático OMR.

---

## 📁 Estrutura da Pasta

```
banco_questoes/
├── questoes.json       # Arquivo principal com todas as 70 questões, redação e gabarito oficial
├── README.md           # Este manual de instruções
└── imagens/            # Pasta para colocar imagens de apoio (gráficos, charges, tirinhas, mapas)
```

---

## 📝 Como Estruturar o `questoes.json`

O arquivo `questoes.json` possui 3 seções principais:

### 1. Metadados da Prova (`metadados`)
Define as informações que aparecem na Capa, Cabeçalhos e Rodapés:
```json
{
  "metadados": {
    "titulo_exame": "EXAME NACIONAL DO ENSINO MÉDIO",
    "subtitulo": "SIMULADO PREPARATÓRIO - 70 QUESTÕES",
    "ano": "2026",
    "dia": "1º DIA",
    "caderno_nome": "CADERNO 1",
    "cor_caderno": "AZUL",
    "codigo_caderno": "010175AZ1",
    "frase_seguranca": "A perseverança é o caminho do êxito e da transformação.",
    "tempo_prova": "cinco horas",
    "total_questoes": 70
  }
}
```

### 2. Proposta de Redação (`redacao`)
Define a página oficial de redação da prova com os textos motivadores:
```json
{
  "redacao": {
    "tema": "Desafios para a democratização do acesso à tecnologia e à inteligência artificial no Brasil",
    "instrucoes": "A partir da leitura dos textos motivadores e com base nos conhecimentos construídos...",
    "textos_motivadores": [
      {
        "titulo": "TEXTO I",
        "conteudo": "A inclusão digital é um direito fundamental no século XXI...",
        "fonte": "IBGE, Pesquisa Nacional por Amostra de Domicílios (adaptado)."
      },
      {
        "titulo": "TEXTO II",
        "conteudo": "Gráfico sobre o percentual de domicílios com internet por região.",
        "imagem": "imagens/grafico_redacao.png",
        "fonte": "Cetic.br, 2025."
      }
    ]
  }
}
```

### 3. Lista de Questões (`questoes`)
Cada uma das 70 questões deve conter:
- `numero`: Inteiro de 1 a 70.
- `area`: Nome da área de conhecimento (ex: "Linguagens e Códigos", "Ciências Humanas", etc.).
- `texto_apoio` (opcional): Objeto com `titulo`, `conteudo` e `fonte`.
- `imagem` (opcional): Caminho relativo da imagem dentro de `banco_questoes/` (ex: `imagens/q05_mapa.png`).
- `enunciado`: O comando ou pergunta da questão.
- `alternativas`: Objeto com as chaves `"A"`, `"B"`, `"C"`, `"D"`, `"E"`.
- `gabarito`: A alternativa correta (`"A"`, `"B"`, `"C"`, `"D"` ou `"E"`).

Exemplo de Questão:
```json
{
  "numero": 1,
  "area": "Linguagens, Códigos e suas Tecnologias",
  "texto_apoio": {
    "titulo": "A hora da estrela",
    "conteudo": "Ela era incompetente. Quase não sabia datilografar, mas esforçava-se bravamente...",
    "fonte": "LISPECTOR, C. A hora da estrela. Rio de Janeiro: Rocco, 1998."
  },
  "enunciado": "No fragmento apresentado, os traços atribuídos à personagem Macabéa expressam",
  "alternativas": {
    "A": "a desumanização provocada pelas exigências do ambiente urbano.",
    "B": "a superação das adversidades mediante a resignação pacífica.",
    "C": "a solidariedade dos colegas em face de sua vulnerabilidade.",
    "D": "a crítica à apatia moral dos setores marginalizados.",
    "E": "a idealização romântica das relações de trabalho."
  },
  "gabarito": "A"
}
```

---

## 🚀 Como Usar no Gerador e Corretor

1. Preencha ou modifique o arquivo `questoes.json`.
2. Para gerar a prova completa, execute:
   ```bash
   python cli.py gerar-prova
   ```
3. Para gerar o cartão resposta OMR e a folha de redação oficial:
   ```bash
   python cli.py gerar-cartao
   python cli.py gerar-redacao
   ```
4. Para corrigir os cartões digitalizados com o gabarito definido neste arquivo:
   ```bash
   python cli.py corrigir
   ```
