# OMR Exam Sheet Grader (`omr-exam-grader`)

An automated **Optical Mark Recognition (OMR)** engine built in Python using OpenCV, NumPy, and Pandas. Designed to process and evaluate standardized multiple-choice answer sheets (such as ENEM-style 70-question exams) from scanned images or photos with high precision, adaptive lighting normalization, and noise robustness.

---

## 🌟 Key Features

- **Adaptive Illumination Normalization:** Morphological background division to eliminate shadows, uneven flash gradients, and paper folds.
- **Dynamic Geometric Alignment:** Auto-detects sheet layout, fiducial markers, and column anchors across variable resolutions and minor tilts.
- **Robust Bubble Density Scoring:** Calculates optical ink density ratios with dynamic thresholds to differentiate filled bubbles from faint erasures or empty marks.
- **Comprehensive Visual Debugging:** Generates visual overlays with color-coded detections (green = marked, red = unmarked, yellow = multiple/conflict) and confidence contours.
- **Automated Tabular Export:** Exports processed student answers directly to formatted CSV files.

---

## 🚀 Quick Start

### Requirements

```bash
pip install opencv-python numpy pandas
```

### Usage

```bash
python corretor.py
```

Irá processar automaticamente todas as imagens `.jpg` da pasta `cartoes/` e salvar a planilha consolidada em `resultado.xlsx` (com colunas ajustadas e compatibilidade direta com o Excel).

Opções adicionais:
```bash
# Definir pasta personalizada e nome do arquivo de saída:
python corretor.py --pasta cards --saida resultado_final.csv

# Gerar também imagens de conferência visual (salvas na pasta debug/):
python corretor.py --debug

# Gerar CSVs individuais para cada cartão além da planilha consolidada:
python corretor.py --individual
```

### Output

- `resultado_consolidado.csv`: Tabela com 1 linha por cartão e 70 colunas (questões de 1 a 70).
- `debug/debug_<nome>.png`: Visual feedback overlay com detecção das bolinhas (quando `--debug` for ativado).

---

## 📄 License

MIT License. Developed by [@lealwbs](https://github.com/lealwbs).
