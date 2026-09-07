import os
import sys
import streamlit as st

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.set_page_config(page_title="TapEye - About & Architecture", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About TapEye")
st.caption("Acoustic + Visual Multimodal Produce Quality Scanner")

# Description Paragraphs
st.markdown("""
### 🍏 Project Overview & Motivation
**TapEye** is a software-only, dual-modal produce quality scanner designed to evaluate internal and external produce condition without destructive testing. Traditional commercial quality assessment often relies on expensive NIR spectrometers or destructive acoustic impact sensors. TapEye demonstrates that commodity mobile phone sensors — microphones for tap-impact resonance and cameras for surface inspection — can act as an accurate software proxy for produce quality screening.

### 🧬 Late-Fusion Machine Learning Architecture
Instead of early feature-level concatenation, TapEye uses a **Late-Fusion (Decision-Level) Architecture**. The acoustic pipeline processes impact recordings using `librosa` spectral analysis (FFT magnitude, 13-coefficient MFCCs, spectral centroid, ZCR, RMS energy) to feed an SVM/Random Forest classifier. In parallel, the visual pipeline feeds produce photos into a transfer-learning `MobileNetV2` deep convolutional network. A lightweight Logistic Regression meta-classifier then ensembles the 3-class probability vectors from both branches:
$$F_{\\text{fused}} = [P_{\\text{acoustic}} \\parallel P_{\\text{visual}}]$$
This late-fusion design ensures that internal physical decay (detected acoustically) and surface defects (detected visually) are combined into a single, high-confidence verdict.
""")

st.markdown("---")

# Architecture Diagram
st.subheader("🏗️ System Architecture Diagram")
st.markdown("""
```mermaid
flowchart LR
    subgraph Inputs ["Dual Inputs"]
        A["🎙️ Audio Tap (.wav)"]
        V["📷 Produce Photo (.jpg/.png)"]
    end

    subgraph AcousticBranch ["Acoustic Branch"]
        A1["FFT & MFCC Extraction"] --> A2["Feature Pooling"]
        A2 --> A3["SVM / Random Forest"]
        A3 --> AP["P_acoustic Vector"]
    end

    subgraph VisualBranch ["Visual Branch"]
        V1["OpenCV Resize 224x224"] --> V2["MobileNetV2 Deep Net"]
        V2 --> VP["P_visual Vector"]
    end

    subgraph FusionEngine ["Late Fusion"]
        AP --> F["[P_acoustic || P_visual]"]
        VP --> F
        F --> M["Logistic Regression Meta-Classifier"]
    end

    subgraph Output ["Final Verdict"]
        M --> O["🎯 Final Quality Verdict\n(Good / Borderline / Reject)"]
    end

    A --> A1
    V --> V1
```
""")

st.markdown("---")

# Tech Stack Overview
st.subheader("🛠️ Technical Stack")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    #### 🔊 Acoustic Pipeline
    - **Librosa**: Audio loading, FFT magnitude, 13-coefficient MFCCs
    - **SciPy**: Digital signal processing & windowing
    - **SoundFile**: Wav audio file I/O
    """)

with col2:
    st.markdown("""
    #### 👁️ Visual Pipeline
    - **TensorFlow / Keras**: Pretrained MobileNetV2 architecture
    - **OpenCV**: RGB normalization & image preprocessing
    - **Pillow**: Image data handling
    """)

with col3:
    st.markdown("""
    #### 🎯 Fusion & ML
    - **Scikit-Learn**: SVM, Random Forest, Logistic Regression Meta-Classifier
    - **Joblib**: Model serialization & deployment
    """)

with col4:
    st.markdown("""
    #### 💻 Web & UI Stack
    - **Streamlit**: Multi-page interactive web application
    - **Matplotlib**: Real-time signal & spectrum plotting
    """)
