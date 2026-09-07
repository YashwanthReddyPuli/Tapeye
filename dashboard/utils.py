import os
import sys
import json
import pickle
import joblib
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from acoustic.feature_extraction import extract_features


def inject_custom_css():
    """
    Inject premium Dark Theme CSS styling:
    - Custom dark glassmorphism card containers
    - Glowing verdict borders
    - Customized typography and badge styling
    - Hide default Streamlit footer and hamburger menu
    """
    custom_css = """
    <style>
    /* Dark Theme Global Background */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
        color: #e6edf3;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d !important;
    }

    /* Card Containers */
    .tapeye-card {
        background: rgba(22, 27, 34, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid #30363d;
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .tapeye-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
    }

    /* Glowing Verdict Cards */
    .verdict-card-good {
        background: linear-gradient(145deg, rgba(27, 94, 32, 0.35) 0%, rgba(13, 17, 23, 0.9) 100%) !important;
        border: 2px solid #2e7d32 !important;
        box-shadow: 0 0 25px rgba(46, 125, 50, 0.45) !important;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
    }
    .verdict-card-borderline {
        background: linear-gradient(145deg, rgba(245, 127, 23, 0.35) 0%, rgba(13, 17, 23, 0.9) 100%) !important;
        border: 2px solid #f57f17 !important;
        box-shadow: 0 0 25px rgba(245, 127, 23, 0.45) !important;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
    }
    .verdict-card-bad {
        background: linear-gradient(145deg, rgba(183, 28, 28, 0.35) 0%, rgba(13, 17, 23, 0.9) 100%) !important;
        border: 2px solid #c62828 !important;
        box-shadow: 0 0 25px rgba(198, 40, 40, 0.45) !important;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
    }

    /* Status Container Styling */
    [data-testid="stStatus"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
    }

    /* Custom Badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-ready { background-color: rgba(46, 125, 50, 0.2); color: #81c784; border: 1px solid #2e7d32; }
    .badge-missing { background-color: rgba(198, 40, 40, 0.2); color: #e57373; border: 1px solid #c62828; }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


@st.cache_resource
def check_and_warmup_models():
    """
    Check if all required model binary files exist and load them into cache.
    Returns: (bool, dict_of_status)
    """
    models = {
        "acoustic": os.path.join("models", "acoustic_classifier.pkl"),
        "visual": os.path.join("models", "visual_classifier.keras"),
        "fusion": os.path.join("models", "fusion_classifier.pkl")
    }

    status = {}
    all_exist = True
    for key, path in models.items():
        exists = os.path.exists(path)
        status[key] = exists
        if not exists:
            all_exist = False

    return all_exist, status


def generate_plotly_spectrogram(audio_path: str) -> go.Figure:
    """
    Extract acoustic features and render an interactive Plotly Heatmap Spectrogram (13 MFCCs over time).
    Returns: plotly.graph_objects.Figure
    """
    features = extract_features(audio_path)
    mfcc = features["mfcc"]
    duration = features["duration"]
    time_frames = np.linspace(0, duration, mfcc.shape[1])

    fig = go.Figure(data=go.Heatmap(
        z=mfcc,
        x=time_frames,
        y=[f"MFCC {i+1}" for i in range(mfcc.shape[0])],
        colorscale="Viridis",
        colorbar=dict(title="dB Power", tickfont=dict(color="#e6edf3"))
    ))

    fig.update_layout(
        title=dict(text="🔊 Interactive Acoustic MFCC Spectrogram", font=dict(size=14, color="#e6edf3")),
        xaxis=dict(title="Time (seconds)", color="#8b949e", gridcolor="#21262d"),
        yaxis=dict(title="Coefficient", color="#8b949e", gridcolor="#21262d"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=40, b=40),
        height=320
    )
    return fig


def generate_radar_chart(acoustic_probs: dict, visual_probs: dict, fused_probs: dict) -> go.Figure:
    """
    Render a 3-way Plotly Radar/Spider Chart comparing probability distributions
    ('bad', 'borderline', 'good') across Acoustic, Visual, and Fused predictions.
    """
    categories = ["bad", "borderline", "good"]

    # Close the radar loop by repeating the first category
    categories_closed = categories + [categories[0]]
    ac_vals = [acoustic_probs.get(c, 0.0) * 100 for c in categories] + [acoustic_probs.get(categories[0], 0.0) * 100]
    vis_vals = [visual_probs.get(c, 0.0) * 100 for c in categories] + [visual_probs.get(categories[0], 0.0) * 100]
    fused_vals = [fused_probs.get(c, 0.0) * 100 for c in categories] + [fused_probs.get(categories[0], 0.0) * 100]

    fig = go.Figure()

    # Acoustic Branch Trace
    fig.add_trace(go.Scatterpolar(
        r=ac_vals,
        theta=categories_closed,
        fill='toself',
        name='Acoustic Branch',
        line=dict(color='#29b6f6', width=2),
        fillcolor='rgba(41, 182, 246, 0.2)'
    ))

    # Visual Branch Trace
    fig.add_trace(go.Scatterpolar(
        r=vis_vals,
        theta=categories_closed,
        fill='toself',
        name='Visual Branch',
        line=dict(color='#ab47bc', width=2),
        fillcolor='rgba(171, 71, 188, 0.2)'
    ))

    # Late-Fusion Verdict Trace
    fig.add_trace(go.Scatterpolar(
        r=fused_vals,
        theta=categories_closed,
        fill='toself',
        name='Late-Fusion Verdict',
        line=dict(color='#66bb6a', width=3),
        fillcolor='rgba(102, 187, 106, 0.35)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color="#8b949e",
                gridcolor="#30363d"
            ),
            angularaxis=dict(
                color="#e6edf3",
                gridcolor="#30363d"
            ),
            bgcolor="rgba(22,27,34,0.7)"
        ),
        title=dict(text="🎯 Multimodal Class Probability Alignment (Radar View)", font=dict(size=14, color="#e6edf3")),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#e6edf3"), bgcolor="rgba(16,22,30,0.8)"),
        margin=dict(l=40, r=40, t=40, b=40),
        height=350
    )
    return fig


def load_evaluation_metrics():
    """
    Load evaluated performance metrics from models/system_evaluation_metrics.json.
    Returns dict or None if missing.
    """
    json_path = os.path.join("models", "system_evaluation_metrics.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None
