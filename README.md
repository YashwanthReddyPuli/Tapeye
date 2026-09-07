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

### Phase 3: Visual Pipeline
The visual pipeline utilizes transfer learning with a MobileNetV2 architecture pretrained on ImageNet to predict external produce quality from images (surface blemishes, bruising, discoloration, ripeness).

#### 1. Image Data Organization:
Place raw produce images into subdirectories inside `data/raw/visual/` named by quality class:
```text
data/raw/visual/
├── good/       # Fresh, unblemished produce images
├── borderline/ # Slightly spotty or ripening produce images
└── bad/        # Bruised, rotten, or discolored produce images
```

#### 2. Building the Visual Dataset:
```bash
python visual/dataset_builder.py
```
*Preprocesses images to $224 \times 224$ RGB, scales pixel values to $[-1, 1]$, splits data into 70/15/15 train/val/test sets, applies data augmentation to training data (horizontal flip, random brightness jitter), and saves `data/processed/visual/dataset.pkl`.*

#### 3. Training the MobileNetV2 Classifier:
```bash
python visual/train_classifier.py
```
*Loads pretrained MobileNetV2, freezes base layers to train the custom classification head, fine-tunes top convolutional layers, evaluates test performance, saves the model to `models/visual_classifier.keras`, and outputs metrics to `models/visual_classifier_metrics.txt`.*

#### 4. Running Single-Image Quality Inference:
```bash
python visual/predict.py --image data/raw/visual/good/good_fruit_1.jpg
```
*Outputs structured class prediction and probability distributions matching the acoustic branch format:*
```json
{
  "predicted_class": "good",
  "probabilities": {
    "bad": 0.0130,
    "borderline": 0.0566,
    "good": 0.9304
  }
}
```

### Phase 4: Late-Fusion Meta-Classifier
The late-fusion module concatenates the probability distributions from both the acoustic branch ($P_{\text{acoustic}}$) and visual branch ($P_{\text{visual}}$) into a fused feature vector ($F_{\text{fused}} = [P_A \parallel P_V]$), training a meta-classifier to output the final produce quality verdict.

#### 1. Manifest Pairing (`fusion_pairs.csv`):
Create `data/raw/fusion_pairs.csv` pairing corresponding audio recordings and produce images:
```csv
audio_path,image_path,label
data/raw/acoustic/good_tap_1.wav,data/raw/visual/good/good_fruit_1.jpg,good
data/raw/acoustic/borderline_tap_1.wav,data/raw/visual/borderline/borderline_fruit_1.jpg,borderline
data/raw/acoustic/bad_tap_1.wav,data/raw/visual/bad/bad_fruit_1.jpg,bad
```
*(Or auto-generate paired samples via `python scripts/create_fusion_pairs.py`)*

#### 2. Building the Fused Dataset:
```bash
python fusion/build_fusion_dataset.py
```
*Runs acoustic and visual branch inference on every pair, concatenates 3-class probability vectors into a 6-element feature vector, splits data 80/20 (stratified), and saves `data/processed/fusion/dataset.pkl`.*

#### 3. Training the Meta-Classifier & Benchmark Evaluation:
```bash
python fusion/train_meta_classifier.py
```
*Trains Logistic Regression and Decision Tree meta-classifiers. Evaluates unimodal acoustic-only vs unimodal visual-only vs multimodal late-fusion predictions on the same test set, saving the winning model to `models/fusion_classifier.pkl` and writing a comparison report to `models/fusion_comparison_report.txt`.*

#### 4. Running Final Verdict Dual-Modal Inference:
```bash
python fusion/predict.py --audio data/raw/acoustic/good_tap_1.wav --image data/raw/visual/good/good_fruit_1.jpg
```
*Outputs final verdict, fusion confidence, and individual branch breakdowns:*
```json
{
  "final_verdict": "good",
  "fusion_confidence": 0.5418,
  "fused_probabilities": {
    "bad": 0.1610,
    "borderline": 0.2972,
    "good": 0.5418
  },
  "acoustic_branch": {
    "predicted_class": "good",
    "probabilities": { "bad": 0.0817, "borderline": 0.4210, "good": 0.4973 }
  },
  "visual_branch": {
    "predicted_class": "good",
    "probabilities": { "bad": 0.1494, "borderline": 0.1986, "good": 0.6520 }
  }
}
```

- **Phase 5: Integration** - End-to-end evaluation pipeline and unified inference module.




