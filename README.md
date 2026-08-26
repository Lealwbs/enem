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

Process a single answer sheet image:
```bash
python corretor.py 1.jpeg --debug
```

Or run directly without flags (processes `1.jpeg` by default):
```bash
python corretor.py
```

### Output

- `resultado_<nome>.csv`: Extracted answers for all questions.
- `debug_<nome>.png`: Visual feedback overlay with bubble detection and scoring.

---

## 📄 License

MIT License. Developed by [@lealwbs](https://github.com/lealwbs).
