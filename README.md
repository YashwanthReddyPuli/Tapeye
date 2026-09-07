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

### Phase 1: Acoustic Feature Extraction
The acoustic feature extraction pipeline processes raw impact/tap `.wav` audio files recorded from produce and extracts spectral, time-domain, and frequency-domain features for downstream quality classification.

#### Extracted Features:
- **Raw Signal & Metadata**: Audio waveform array, native sample rate ($sr$), and recording duration (seconds).
- **FFT Magnitude Spectrum**: Fast Fourier Transform magnitude array and associated frequency bins ($0$ to $sr/2$ Hz).
- **MFCCs**: 13 Mel-Frequency Cepstral Coefficients computed over 32 mel filterbanks (`librosa.feature.mfcc`).
- **Supporting Features**:
  - `spectral_centroid`: Center of mass of the spectrum.
  - `zero_crossing_rate`: Rate of sign-changes along the signal.
  - `rms_energy`: Root-Mean-Square energy across frame windows.

#### How to Run:
1. **Generate Sample Audio Files (Optional/Test Data)**:
   ```bash
   python scripts/create_sample_audio.py
   ```
   *Generates 3 synthetic `.wav` tap recordings (`sample_tap_firm.wav`, `sample_tap_ripe.wav`, `sample_tap_overripe.wav`) in `data/raw/acoustic/`.*

2. **Batch Feature Extraction**:
   ```bash
   python acoustic/batch_extract.py
   ```
   *Processes all `.wav` recordings in `data/raw/acoustic/` and outputs compressed NumPy archives (`.npz`) containing feature dictionaries to `data/processed/acoustic/`.*

3. **Visualize Features (Sanity Checking)**:
   ```bash
   python acoustic/visualize_features.py --audio data/raw/acoustic/sample_tap_firm.wav
   ```
   *Generates a 3-panel visualization figure containing the time-domain waveform, raw FFT spectrum, and 13-coefficient MFCC heatmap, saving it to `data/processed/acoustic_feature_visualization.png`.*

### Phase 2: Acoustic Classifier Pipeline
The acoustic classifier pipeline aggregates extracted acoustic features, constructs a labeled dataset, trains candidate machine learning models (SVM and Random Forest), evaluates model performance, and serves prediction probabilities for individual tap recordings.

#### 1. Data Labeling Conventions:
TapEye supports two flexible ways to label raw tap audio recordings:
- **Option A: `labels.csv` (Recommended)**: Create `data/raw/acoustic/labels.csv` with a header `filename,label`:
  ```csv
  filename,label
  tap_sample_01.wav,good
  tap_sample_02.wav,borderline
  tap_sample_03.wav,bad
  ```
- **Option B: Filename Prefixes**: Prefix filenames with quality classes (e.g., `good_tap_1.wav`, `borderline_tap_1.wav`, `bad_tap_1.wav`, `firm_1.wav`, `overripe_1.wav`).

#### 2. Building the Dataset:
```bash
python acoustic/dataset_builder.py
```
*Aggregates time-series features into fixed-length vectors (mean, std, min, max pooling), splits data 80/20 (stratified), and saves `data/processed/acoustic/dataset.pkl`.*

#### 3. Training & Evaluating Classifiers:
```bash
python acoustic/train_classifier.py
```
*Trains SVM (RBF kernel) and Random Forest models via hyperparameter grid search, picks the top-performing model, saves the binary to `models/acoustic_classifier.pkl`, and writes an evaluation summary report to `models/acoustic_classifier_metrics.txt`.*

#### 4. Running Single-File Quality Inference:
```bash
python acoustic/predict.py --audio data/raw/acoustic/good_tap_1.wav
```
*Outputs structured class prediction and probability distributions:*
```json
{
  "predicted_class": "good",
  "probabilities": {
    "bad": 0.0521,
    "borderline": 0.0924,
    "good": 0.8555
  }
}
```

- **Phase 3: Visual Pipeline** - Transfer learning with MobileNetV2 architecture using OpenCV and TensorFlow for image classification.
- **Phase 4: Late Fusion** - Ensembling and meta-classifier implementation combining acoustic and visual prediction probabilities.
- **Phase 5: Integration** - End-to-end evaluation pipeline and unified inference module.


