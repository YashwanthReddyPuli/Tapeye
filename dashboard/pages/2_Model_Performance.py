import os
import sys
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from dashboard.utils import inject_custom_css, load_evaluation_metrics

st.set_page_config(page_title="TapEye OS - Performance Benchmarks", page_icon="📊", layout="wide")
inject_custom_css()

st.title("📊 Multimodal Performance & Model Benchmarks")
st.markdown("Comparative accuracy, F1-scores, and confusion matrices comparing Acoustic-Only, Visual-Only, and Late-Fusion models.")

metrics_data = load_evaluation_metrics()

if metrics_data is None:
    st.info("💡 **Report Missing**: Evaluation metrics have not been generated yet. Please run `python scripts/evaluate_system.py` first to generate the report.")
else:
    # Core Claim Callout Banner
    st.markdown("""
    <div style="background: rgba(41, 182, 246, 0.15); border: 1px solid #29b6f6; border-radius: 12px; padding: 18px; margin-bottom: 24px;">
        <h4 style="color: #4fc3f7; margin: 0 0 6px 0;">🌟 Core Benchmark Claim</h4>
        <p style="color: #e6edf3; margin: 0; font-size: 15px;">
            Late fusion outperforms unimodal baselines by combining internal acoustic impact resonance with surface computer vision, mitigating single-modality error modes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    ac_m = metrics_data["acoustic_branch"]
    vis_m = metrics_data["visual_branch"]
    fused_m = metrics_data["fused_multimodal"]
    gain_pct = metrics_data.get("fusion_improvements", {}).get("accuracy_gain_over_acoustic_pct", 0.0)

    # Top st.metric components with explicit delta parameters
    st.subheader("📈 Summary Metrics & Fusion Delta Gains")
    m_cols = st.columns(3)

    with m_cols[0]:
        st.metric(
            label="🔊 Acoustic-Only Branch",
            value=f"{ac_m['accuracy'] * 100:.1f}% Accuracy",
            delta=f"F1: {ac_m['f1_score']:.4f}",
            delta_color="off"
        )

    with m_cols[1]:
        st.metric(
            label="👁️ Visual-Only Branch",
            value=f"{vis_m['accuracy'] * 100:.1f}% Accuracy",
            delta=f"F1: {vis_m['f1_score']:.4f}",
            delta_color="off"
        )

    with m_cols[2]:
        st.metric(
            label="🎯 Late-Fusion Multimodal",
            value=f"{fused_m['accuracy'] * 100:.1f}% Accuracy",
            delta=f"+{gain_pct:.1f}% gain over Acoustic baseline",
            delta_color="normal"
        )

    st.markdown("---")

    # Grouped Interactive Plotly Bar Chart
    st.subheader("📊 Modality Metric Benchmarks (Plotly)")

    modalities = ["Acoustic-Only", "Visual-Only", "Late-Fusion Multimodal"]
    accuracies = [ac_m["accuracy"] * 100, vis_m["accuracy"] * 100, fused_m["accuracy"] * 100]
    f1_scores = [ac_m["f1_score"] * 100, vis_m["f1_score"] * 100, fused_m["f1_score"] * 100]

    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(
        x=modalities,
        y=accuracies,
        name="Accuracy (%)",
        marker_color="#29b6f6",
        text=[f"{v:.1f}%" for v in accuracies],
        textposition="auto"
    ))

    fig_bar.add_trace(go.Bar(
        x=modalities,
        y=f1_scores,
        name="F1-Score (%)",
        marker_color="#66bb6a",
        text=[f"{v:.1f}%" for v in f1_scores],
        textposition="auto"
    ))

    fig_bar.update_layout(
        barmode="group",
        title=dict(text="Comparative Accuracy & F1-Score Across Modalities", font=dict(color="#e6edf3", size=15)),
        xaxis=dict(title="Pipeline Modality", color="#8b949e", gridcolor="#21262d"),
        yaxis=dict(title="Score (%)", range=[0, 115], color="#8b949e", gridcolor="#21262d"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(22,27,34,0.6)",
        legend=dict(font=dict(color="#e6edf3"), bgcolor="rgba(16,22,30,0.8)"),
        height=400,
        margin=dict(l=40, r=40, t=50, b=40)
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # Interactive Plotly Confusion Matrices
    st.subheader("🧩 Confusion Matrices Breakdown")
    cm_cols = st.columns(3)
    classes = metrics_data.get("class_names", ["bad", "borderline", "good"])

    def create_plotly_cm(cm_array, title, colorscale):
        fig_cm = px.imshow(
            cm_array,
            x=classes,
            y=classes,
            labels=dict(x="Predicted Class", y="True Ground Truth"),
            color_continuous_scale=colorscale,
            text_auto=True
        )
        fig_cm.update_layout(
            title=dict(text=title, font=dict(color="#e6edf3", size=13)),
            xaxis=dict(color="#8b949e"),
            yaxis=dict(color="#8b949e"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            height=320,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig_cm

    with cm_cols[0]:
        st.plotly_chart(create_plotly_cm(ac_m["confusion_matrix"], "🔊 Acoustic Confusion Matrix", "Blues"), use_container_width=True)

    with cm_cols[1]:
        st.plotly_chart(create_plotly_cm(vis_m["confusion_matrix"], "👁️ Visual Confusion Matrix", "Purples"), use_container_width=True)

    with cm_cols[2]:
        st.plotly_chart(create_plotly_cm(fused_m["confusion_matrix"], "🎯 Fused Confusion Matrix", "Greens"), use_container_width=True)
