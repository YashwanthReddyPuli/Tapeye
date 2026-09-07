# TapEye: Dual-Modal Produce Quality Assessment

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.35-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python)](https://python.org)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4.1-38B2AC?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-FF6F00?style=flat-square&logo=tensorflow)](https://tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

**TapEye** is an enterprise-grade, dual-modal AI quality assessment system engineered for agricultural produce. By integrating non-destructive acoustic impact resonance analysis with high-resolution computer vision, TapEye solves the fundamental limitation of unimodal inspection: visual inspection cannot detect internal decay or hollowness, while acoustic analysis cannot detect surface blemishes or discoloration.

---

## Architecture: Late-Fusion Deep Learning

TapEye operates on an asynchronous dual-branch pipeline that fuses spectral audio features and spatial visual representations into a calibrated quality verdict:

```
                  ┌───────────────────────────────┐
                  │   Impact Resonance (.wav)     │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │    DSP & MFCC Feature Ext     │
                  │   (Librosa: 13 MFCCs + FFT)   │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │ Acoustic Classifier (SVM/RF)  │
                  └──────────────┬────────────────┘
                                 │ P(Acoustic) [3-dim]
                                 ▼
┌─────────────────────────┐      │      ┌─────────────────────────┐
│  Produce Image (.jpg)   │      ├─────►│ Late-Fusion Meta Engine │──► Final Quality Verdict
└───────────┬─────────────┘      │      │  (Logistic Regression)  │    (Good / Borderline / Reject)
            │                    ▲      └─────────────────────────┘
            ▼                    │ P(Visual) [3-dim]
┌─────────────────────────┐      │
│  MobileNetV2 (ImageNet) │      │
│   224x224x3 Normalized  │──────┘
└─────────────────────────┘
```

### Key Technical Pillars
1. **Acoustic Resonance Engine (`Librosa`)**:
   - Ingests 22.05 kHz PCM impact audio signals.
   - Extracts Fast Fourier Transform (FFT) magnitude spectrum, 13 Mel-Frequency Cepstral Coefficients (MFCCs), Spectral Centroid, RMS energy, and Zero-Crossing Rate.
   - Fixed-length feature representation via statistical moment pooling (mean, std, min, max).
2. **Visual Processing Branch (`MobileNetV2`)**:
   - High-throughput transfer learning backbone fine-tuned for surface defects, discoloration, bruising, and ripeness.
   - $224 \times 224 \times 3$ RGB inputs normalized to $[-1, 1]$.
3. **Calibrated Meta-Classifier (`Late-Fusion`)**:
   - Concatenates unimodal softmax probability distributions into a combined feature vector $F_{\text{fused}} = [P_{\text{acoustic}} \parallel P_{\text{visual}}]$.
   - Evaluates inter-modal agreement and outputs a unified decision with associated confidence scores.

---

## Liquid Glassmorphism Frontend

The TapEye web client is crafted as an ultra-modern, interactive intelligence dashboard:
- **Liquid Glassmorphism**: Translucent card elevations (`backdrop-blur-2xl`), subtle border highlights, and dark-mode depth palettes.
- **Neural Particle Canvas**: Live background node constellation powered by `@tsparticles/react` simulating active synaptic connections.
- **Micro-Animations & Telemetry**: Dynamic radar probability projections, acoustic waveform rendering, and smooth state transitions via `framer-motion` and `lucide-react`.
- **System Architecture Bento Grid**: Clean Apple/Stripe-style documentation canvas breaking down pipeline stages and latency profiles.

---

## Project Structure

```
TapEye/
├── backend/                  # FastAPI inference & telemetry service
│   └── main.py               # REST API endpoints (/api/scan, /api/performance)
├── frontend/                 # Next.js 14 + Tailwind CSS + Framer Motion UI
│   ├── src/
│   │   ├── app/              # App router pages (/, /performance, /about)
│   │   └── components/       # Glassmorphism UI & visualization components
│   └── package.json
├── acoustic/                 # Acoustic feature extraction & model training
│   ├── batch_extract.py      # Batch DSP processing
│   ├── dataset_builder.py    # Feature aggregation & dataset builder
│   └── train_classifier.py   # Acoustic model training & grid search
├── visual/                   # MobileNetV2 computer vision pipeline
│   ├── dataset_builder.py    # Image normalization & augmentations
│   └── train_classifier.py   # MobileNetV2 fine-tuning
├── fusion/                   # Late-fusion meta-classifier
│   ├── build_fusion_dataset.py # Fusion feature generator
│   ├── train_meta_classifier.py# Meta-classifier training
│   └── predict.py            # End-to-end inference orchestrator
├── data/
│   ├── raw/                  # Raw acoustic and visual assets
│   └── sample_files/         # Validated test samples for evaluation
├── models/                   # Serialized classifiers and evaluation metrics
├── requirements.txt          # Python ecosystem dependencies
└── README.md
```

---

## Quickstart & Installation

### 1. Backend Service (FastAPI)

Clone the repository and set up the Python virtual environment:

```bash
# Clone the repository
git clone https://github.com/YashwanthReddyPuli/Tapeye.git
cd Tapeye

# Create and activate virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be live at `http://127.0.0.1:8000`. Interactive OpenAPI documentation is accessible at `http://127.0.0.1:8000/docs`.

### 2. Frontend Dashboard (Next.js)

In a separate terminal, launch the Next.js web application:

```bash
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to interact with the TapEye Scanner.

---

## API Reference

### `POST /api/scan`
Upload paired acoustic (`.wav`) and visual (`.jpg`/`.png`) files for real-time dual-modal inference.

**Request:** `multipart/form-data`
- `audio`: `.wav` audio recording
- `image`: `.jpg` or `.png` photograph

**Response:**
```json
{
  "final_verdict": "good",
  "fusion_confidence": 0.942,
  "acoustic_branch": {
    "label": "good",
    "confidence": 0.895
  },
  "visual_branch": {
    "label": "good",
    "confidence": 0.961
  },
  "chart_data": [
    { "subject": "Good", "Acoustic": 89.5, "Visual": 96.1, "Fused": 94.2 },
    { "subject": "Borderline", "Acoustic": 7.3, "Visual": 2.5, "Fused": 4.1 },
    { "subject": "Bad", "Acoustic": 3.2, "Visual": 1.4, "Fused": 1.7 }
  ],
  "telemetry": {
    "acoustic_latency_ms": 14.2,
    "visual_latency_ms": 32.1,
    "fusion_latency_ms": 1.8,
    "total_latency_ms": 48.1
  }
}
```

### `GET /api/performance`
Retrieves production validation benchmarks comparing unimodal baselines against the fused system.

---

## Benchmark Results

| Model Architecture | Input Modality | Precision | Recall | F1-Score | Inference Latency |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Acoustic (SVM/RF)** | 22.05 kHz Audio | 84.6% | 83.1% | 83.8% | ~14 ms |
| **Visual (MobileNetV2)** | 224x224x3 Image | 88.2% | 87.5% | 87.8% | ~32 ms |
| **TapEye (Late-Fusion)** | **Audio + Image** | **95.4%** | **94.8%** | **95.1%** | **~48 ms** |

*Late-fusion yields an overall accuracy uplift of +7.3% over visual-only inspection and +11.3% over acoustic-only inspection by eliminating single-sensor failure modes.*

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
