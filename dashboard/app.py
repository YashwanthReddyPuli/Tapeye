import os
import sys
import streamlit as st

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from dashboard.utils import inject_custom_css, check_and_warmup_models

# Configure Streamlit Page
st.set_page_config(
    page_title="TapEye OS",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom Dark Theme CSS
inject_custom_css()

# Sidebar Branding Header
st.sidebar.image("https://img.icons8.com/color/96/apple-cut.png", width=56)
st.sidebar.title("TapEye OS v2.0")
st.sidebar.caption("Dual-Modal (Acoustic + Visual) Late-Fusion Engine")
st.sidebar.markdown("---")

# Header Overview
st.title("👁️ TapEye OS: Multimodal Produce Quality Scanner")
st.markdown("""
Welcome to **TapEye OS** — a software-only, dual-modal produce quality scanner combining internal acoustic impact resonance with surface computer vision via late-fusion machine learning.
""")

# Model Check & Readiness Alert
models_ready, model_status = check_and_warmup_models()

if not models_ready:
    st.markdown("""
    <div style="background: rgba(198, 40, 40, 0.15); border: 1px solid #c62828; border-radius: 12px; padding: 20px; margin: 16px 0;">
        <h4 style="color: #ef5350; margin: 0 0 8px 0;">⚠️ System Alert: Model Binaries Missing</h4>
        <p style="color: #e6edf3; margin: 0;">One or more trained model binaries are missing from the <code>models/</code> directory. Please execute the verification setup script to generate binaries:</p>
        <code style="display: block; background: #0d1117; padding: 8px; border-radius: 6px; margin-top: 8px; color: #81c784;">python scripts/verify_phase5.py</code>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("System Binary Status")
    cols = st.columns(3)
    with cols[0]:
        badge_cls = "badge-ready" if model_status["acoustic"] else "badge-missing"
        badge_text = "READY" if model_status["acoustic"] else "MISSING"
        st.markdown(f"**Acoustic Classifier**: <span class='status-badge {badge_cls}'>{badge_text}</span>", unsafe_allow_html=True)
    with cols[1]:
        badge_cls = "badge-ready" if model_status["visual"] else "badge-missing"
        badge_text = "READY" if model_status["visual"] else "MISSING"
        st.markdown(f"**Visual Classifier**: <span class='status-badge {badge_cls}'>{badge_text}</span>", unsafe_allow_html=True)
    with cols[2]:
        badge_cls = "badge-ready" if model_status["fusion"] else "badge-missing"
        badge_text = "READY" if model_status["fusion"] else "MISSING"
        st.markdown(f"**Late-Fusion Classifier**: <span class='status-badge {badge_cls}'>{badge_text}</span>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background: rgba(46, 125, 50, 0.15); border: 1px solid #2e7d32; border-radius: 12px; padding: 16px; margin: 16px 0;">
        <p style="color: #81c784; margin: 0; font-weight: 600;">✅ System Status: All Acoustic, Visual, and Late-Fusion Engine Models Warm & Active</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
### 🚀 Navigation Dashboard
Select a workspace from the **Sidebar Navigation** on the left:
- **🔍 1_Scan**: Interactive drag-and-drop dual-modal scan interface with step-by-step pipeline status animation, Plotly Spectrogram, Plotly Radar chart, and glowing verdict cards.
- **📊 2_Model_Performance**: Interactive Plotly grouped bar benchmarks and side-by-side confusion matrix heatmaps comparing multimodal fusion against single-sensor baselines.
- **ℹ️ 3_About**: Technical documentation detailing the late-fusion architecture, smartphone sensor proxy concept, and full ML tech stack.
""")

# Footer
st.markdown("---")
st.caption("TapEye OS • Dual-Modal Acoustic + Visual Quality Scanner Engine")
