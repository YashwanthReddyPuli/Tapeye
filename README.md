# TapEye

TapEye is a dual-modal produce quality scanner that leverages late-fusion machine learning to assess produce freshness and quality. By combining acoustic signals (tap/impact response analysis) with computer vision (image classification via MobileNetV2), TapEye produces highly reliable quality predictions that outperform single-modality approaches.

## Project Structure

```
TapEye/
├── acoustic/       # Feature extraction & classifier code for acoustic pipeline
├── visual/         # MobileNetV2 training & inference code for visual pipeline
├── fusion/         # Late-fusion meta-classifier code
├── data/
│   ├── raw/        # Unprocessed audio and image samples
│   └── processed/  # Extracted features and cleaned datasets
├── models/         # Saved/trained model files and weights
├── notebooks/      # Jupyter notebooks for experimentation & EDA
├── scripts/        # Utility and one-off scripts
├── requirements.txt # Python package dependencies
├── .gitignore      # Git ignore configuration
└── README.md       # Project documentation
```

## Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  .\venv\Scripts\activate.bat
  ```
- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Project Phases

- **Phase 1: Acoustic Feature Extraction** - Audio preprocessing, spectral feature analysis (MFCCs, spectral centroid, zero-crossing rate) using `librosa`.
- **Phase 2: Acoustic Classifier** - Machine learning classifier training on extracted acoustic features.
- **Phase 3: Visual Pipeline** - Transfer learning with MobileNetV2 architecture using OpenCV and TensorFlow for image classification.
- **Phase 4: Late Fusion** - Ensembling and meta-classifier implementation combining acoustic and visual prediction probabilities.
- **Phase 5: Integration** - End-to-end evaluation pipeline and unified inference module.
