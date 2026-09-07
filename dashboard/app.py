import os
import sys
import streamlit as st

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from dashboard.utils import check_and_warmup_models

# Configure Streamlit Page
st.set_page_config(
    page_title="TapEye - Dual-Modal Produce Quality Scanner",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Branding Header
st.sidebar.image("https://img.icons8.com/color/96/apple-cut.png", width=64)
st.sidebar.title("TapEye Scanner")
st.sidebar.caption("Dual-Modal (Acoustic + Visual) Produce Quality Assessor")
st.sidebar.markdown("---")

# Header Overview
st.title("🍏 TapEye: Late-Fusion Multimodal Produce Quality Scanner")
st.markdown("""
**TapEye** combines internal acoustic resonance analysis (tap/impact sound signals) with external computer vision (MobileNetV2 surface inspection) to deliver robust produce quality classification that outperforms single-modality baselines.
""")

# Model Check & Readiness Alert
models_ready, model_status = check_and_warmup_models()

if not models_ready:
    st.warning("""
    ⚠️ **Setup Required**: One or more trained model binaries are missing from the `models/` directory.
    
    Please run the training pipeline to generate model binaries before scanning:
    ```bash
    python scripts/verify_phase5.py
    ```
    """)
    
    st.subheader("Model Binary Status")
    cols = st.columns(3)
    with cols[0]:
        st.metric("Acoustic Classifier", "Ready" if model_status["acoustic"] else "Missing")
    with cols[1]:
        st.metric("Visual Classifier", "Ready" if model_status["visual"] else "Missing")
    with cols[2]:
        st.metric("Late-Fusion Meta-Classifier", "Ready" if model_status["fusion"] else "Missing")
else:
    st.success("✅ **System Ready**: All acoustic, visual, and late-fusion ML models are loaded and warm.")

st.markdown("""
### 🚀 Quick Navigation
Use the **Sidebar Menu** on the left to navigate the application:
1. **🔍 1_Scan**: Upload audio & photo to run real-time dual-modal produce quality classification.
2. **📊 2_Model_Performance**: Inspect multimodal vs unimodal accuracy benchmarks & confusion matrices.
3. **ℹ️ 3_About**: Explore TapEye architecture, smartphone sensor proxy design, and technical stack.
""")

# Footer
st.markdown("---")
st.caption("TapEye Multimodal ML Pipeline • Dual-Modal Acoustic-Visual Fusion System")
