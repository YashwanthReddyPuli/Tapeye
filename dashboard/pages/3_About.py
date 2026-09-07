import os
import sys
import streamlit as st

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from dashboard.utils import inject_custom_css

st.set_page_config(page_title="TapEye OS - About & Architecture", page_icon="ℹ️", layout="wide")
inject_custom_css()

st.title("ℹ️ About TapEye OS")
st.caption("Software-Only Dual-Modal (Acoustic + Visual) Produce Quality Scanner")

st.markdown("""
<div class="tapeye-card" style="text-align: left; margin-bottom: 24px;">
    <h3 style="color: #4fc3f7; margin-top: 0;">🍏 Project Overview & Problem Statement</h3>
    <p style="color: #e6edf3; font-size: 15px; line-height: 1.6;">
        <b>TapEye</b> addresses a critical challenge in agricultural supply chain quality control: evaluating internal and external produce condition without destructive testing. Commercial quality assessment systems often depend on expensive industrial Near-Infrared (NIR) spectrometers or mechanical destructive impact testing. TapEye proves that commodity smartphone sensors — built-in microphones for acoustic impact response and cameras for surface inspection — can serve as an effective, non-destructive <b>software proxy</b> for automated quality grading.
    </p>

    <h3 style="color: #ce93d8; margin-top: 20px;">🧬 Late-Fusion Machine Learning Architecture</h3>
    <p style="color: #e6edf3; font-size: 15px; line-height: 1.6;">
        Rather than concatenating raw features early, TapEye utilizes a <b>Late-Fusion (Decision-Level) Architecture</b>. 
        The acoustic branch extracts spectral signal properties (FFT magnitude, 13-coefficient MFCCs, spectral centroid, ZCR, RMS energy) using <code>librosa</code> to train an SVM/Random Forest classifier. 
        Concurrently, the visual branch passes produce photos through a transfer-learned <code>MobileNetV2</code> deep network. 
        A lightweight Logistic Regression meta-classifier then ensembles the 3-class probability vectors from both modalities:
    </p>
    <div style="background: rgba(13,17,23,0.8); border: 1px solid #30363d; border-radius: 8px; padding: 12px; text-align: center; color: #81c784; font-size: 16px; font-weight: bold; margin: 12px 0;">
        F<sub>fused</sub> = [ P<sub>acoustic</sub> ∥ P<sub>visual</sub> ]
    </div>
    <p style="color: #e6edf3; font-size: 15px; line-height: 1.6;">
        This late-fusion design guarantees that internal physical hollows/softness (detected acoustically) and external surface bruises/blemishes (detected visually) are synthesized into a single high-confidence verdict.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# System Architecture Diagram
st.subheader("🏗️ System Architecture Diagram")
st.markdown("""
```mermaid
flowchart LR
    subgraph Inputs ["Dual Commodity Inputs"]
        A["🎙️ Audio Tap (.wav)"]
        V["📷 Produce Photo (.jpg/.png)"]
    end

    subgraph AcousticBranch ["Acoustic Pipeline"]
        A1["FFT & 13 MFCC Extraction"] --> A2["Feature Pooling"]
        A2 --> A3["SVM / Random Forest"]
        A3 --> AP["P_acoustic Vector"]
    end

    subgraph VisualBranch ["Visual Pipeline"]
        V1["OpenCV Resize 224x224"] --> V2["MobileNetV2 Deep Net"]
        V2 --> VP["P_visual Vector"]
    end

    subgraph FusionEngine ["Late Fusion Engine"]
        AP --> F["[P_acoustic || P_visual]"]
        VP --> F
        F --> M["Logistic Regression Meta-Classifier"]
    end

    subgraph Output ["Scanner Verdict"]
        M --> O["🎯 Final Verdict\n(Good / Borderline / Reject)"]
    end

    A --> A1
    V --> V1
```
""")

st.markdown("---")

# Tech Stack Cards
st.subheader("🛠️ Technical Stack Overview")

t_cols = st.columns(4)

with t_cols[0]:
    st.markdown("""
    <div class="tapeye-card" style="text-align: left;">
        <h4 style="color: #29b6f6; margin-top:0;">🔊 Acoustic Branch</h4>
        <ul style="color: #8b949e; font-size: 13px; padding-left: 18px;">
            <li><b>Librosa</b>: Signal loading, FFT magnitude, 13-coefficient MFCCs</li>
            <li><b>SciPy</b>: Digital signal processing & windowing</li>
            <li><b>SoundFile</b>: Audio file format decoding</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with t_cols[1]:
    st.markdown("""
    <div class="tapeye-card" style="text-align: left;">
        <h4 style="color: #ab47bc; margin-top:0;">👁️ Visual Branch</h4>
        <ul style="color: #8b949e; font-size: 13px; padding-left: 18px;">
            <li><b>TensorFlow / Keras</b>: Pretrained MobileNetV2 architecture</li>
            <li><b>OpenCV</b>: Image resizing to 224x224 & BGR-RGB conversion</li>
            <li><b>Pillow</b>: Image array manipulation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with t_cols[2]:
    st.markdown("""
    <div class="tapeye-card" style="text-align: left;">
        <h4 style="color: #66bb6a; margin-top:0;">🎯 Late-Fusion ML</h4>
        <ul style="color: #8b949e; font-size: 13px; padding-left: 18px;">
            <li><b>Scikit-Learn</b>: Logistic Regression & Decision Tree meta-classifiers</li>
            <li><b>Joblib</b>: Binary model serialization & warm deployment</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with t_cols[3]:
    st.markdown("""
    <div class="tapeye-card" style="text-align: left;">
        <h4 style="color: #ffa726; margin-top:0;">💻 UI & Analytics</h4>
        <ul style="color: #8b949e; font-size: 13px; padding-left: 18px;">
            <li><b>Streamlit</b>: Multi-page dark-themed web framework</li>
            <li><b>Plotly</b>: Interactive Spectrogram & 3-Way Radar charts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
