import os
import sys
import json
import pickle
import joblib
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import streamlit as st

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from acoustic.feature_extraction import extract_features


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


def generate_audio_plots(audio_path: str):
    """
    Extract acoustic features and render a 2-panel Matplotlib figure:
    (a) Waveform
    (b) MFCC Heatmap
    Returns: matplotlib.figure.Figure
    """
    features = extract_features(audio_path)
    sr = features["sample_rate"]
    y = features["signal"]
    duration = features["duration"]
    time_axis = np.linspace(0, duration, len(y))
    mfcc = features["mfcc"]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 5))
    fig.patch.set_facecolor("#fafafa")

    # Panel 1: Time-Domain Waveform
    ax1.set_facecolor("#ffffff")
    ax1.plot(time_axis, y, color="#1976d2", linewidth=1.2, alpha=0.85)
    ax1.set_title("Acoustic Impact Waveform", fontsize=11, fontweight="bold", pad=8)
    ax1.set_xlabel("Time (s)", fontsize=9)
    ax1.set_ylabel("Amplitude", fontsize=9)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Panel 2: MFCC Heatmap
    ax2.set_facecolor("#ffffff")
    img = librosa.display.specshow(
        mfcc,
        x_axis="time",
        sr=sr,
        ax=ax2,
        cmap="magma"
    )
    ax2.set_title("13-Coefficient MFCC Heatmap", fontsize=11, fontweight="bold", pad=8)
    ax2.set_xlabel("Time (s)", fontsize=9)
    ax2.set_ylabel("MFCC Coefficient", fontsize=9)
    fig.colorbar(img, ax=ax2, format="%+2.0f dB")

    plt.tight_layout()
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
