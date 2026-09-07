import os
import sys
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from dashboard.utils import load_evaluation_metrics

st.set_page_config(page_title="TapEye - Model Performance & Benchmarks", page_icon="📊", layout="wide")

st.title("📊 Model Performance & Multimodal Benchmarks")
st.markdown("Comparative accuracy, F1-scores, and confusion matrices across Acoustic-Only, Visual-Only, and Late-Fusion models.")

metrics_data = load_evaluation_metrics()

if metrics_data is None:
    st.info("💡 **Report Missing**: Evaluation metrics have not been generated yet. Please run `python scripts/evaluate_system.py` first to generate the report.")
else:
    # Explicit Project Claim Banner
    st.success("🌟 **Core Benchmark Claim**: Late fusion outperforms unimodal baselines by combining internal acoustic impact resonance with surface computer vision.")

    ac_m = metrics_data["acoustic_branch"]
    vis_m = metrics_data["visual_branch"]
    fused_m = metrics_data["fused_multimodal"]

    # Top Metric Callout Cards
    st.subheader("📈 Summary Accuracy & F1 Comparison")
    m_cols = st.columns(3)

    with m_cols[0]:
        st.metric(
            label="🔊 Acoustic-Only Branch",
            value=f"{ac_m['accuracy'] * 100:.1f}%",
            delta=f"F1: {ac_m['f1_score']:.4f}"
        )

    with m_cols[1]:
        st.metric(
            label="👁️ Visual-Only Branch",
            value=f"{vis_m['accuracy'] * 100:.1f}%",
            delta=f"F1: {vis_m['f1_score']:.4f}"
        )

    with m_cols[2]:
        gain_pct = metrics_data.get("fusion_improvements", {}).get("accuracy_gain_over_acoustic_pct", 0.0)
        st.metric(
            label="🎯 Fused Multimodal Scanner",
            value=f"{fused_m['accuracy'] * 100:.1f}%",
            delta=f"+{gain_pct:.1f}% over Acoustic"
        )

    st.markdown("---")

    # Bar Chart Comparison
    st.subheader("📊 Modality Metric Benchmarks")

    chart_data = {
        "Modality": ["Acoustic-Only", "Visual-Only", "Late-Fusion Multimodal"],
        "Accuracy (%)": [ac_m["accuracy"] * 100, vis_m["accuracy"] * 100, fused_m["accuracy"] * 100],
        "F1-Score (%)": [ac_m["f1_score"] * 100, vis_m["f1_score"] * 100, fused_m["f1_score"] * 100]
    }

    # Render Matplotlib Bar Chart
    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#fafafa")

    x = np.arange(len(chart_data["Modality"]))
    width = 0.35

    rects1 = ax.bar(x - width/2, chart_data["Accuracy (%)"], width, label="Accuracy (%)", color="#1976d2")
    rects2 = ax.bar(x + width/2, chart_data["F1-Score (%)"], width, label="F1-Score (%)", color="#388e3c")

    ax.set_ylabel("Score (%)", fontsize=10, fontweight="bold")
    ax.set_title("Performance Comparison Across System Modalities", fontsize=12, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(chart_data["Modality"], fontsize=10, fontweight="bold")
    ax.set_ylim(0, 115)
    ax.legend(loc="upper left")
    ax.grid(axis="y", linestyle=":", alpha=0.6)

    # Bar Value Labels
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f"{height:.1f}%",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9, fontweight="bold")

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    # Confusion Matrices Breakdown
    st.subheader("🧩 Confusion Matrices Breakdown")
    cm_cols = st.columns(3)

    classes = metrics_data.get("class_names", ["bad", "borderline", "good"])

    def plot_cm(cm_matrix, title, color_map="Blues"):
        fig_cm, ax_cm = plt.subplots(figsize=(3.5, 3))
        im = ax_cm.imshow(cm_matrix, cmap=color_map)
        ax_cm.set_title(title, fontsize=10, fontweight="bold")
        ax_cm.set_xticks(np.arange(len(classes)))
        ax_cm.set_yticks(np.arange(len(classes)))
        ax_cm.set_xticklabels(classes, fontsize=8)
        ax_cm.set_yticklabels(classes, fontsize=8)
        plt.setp(ax_cm.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        for i in range(len(classes)):
            for j in range(len(classes)):
                ax_cm.text(j, i, str(cm_matrix[i][j]), ha="center", va="center", color="black" if cm_matrix[i][j] < 2 else "white")

        plt.tight_layout()
        return fig_cm

    with cm_cols[0]:
        st.markdown("**Acoustic Confusion Matrix**")
        st.pyplot(plot_cm(ac_m["confusion_matrix"], "Acoustic-Only", "Blues"))

    with cm_cols[1]:
        st.markdown("**Visual Confusion Matrix**")
        st.pyplot(plot_cm(vis_m["confusion_matrix"], "Visual-Only", "Purples"))

    with cm_cols[2]:
        st.markdown("**Fused Confusion Matrix**")
        st.pyplot(plot_cm(fused_m["confusion_matrix"], "Late-Fusion", "Greens"))
