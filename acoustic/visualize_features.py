import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

from feature_extraction import extract_features

def plot_acoustic_features(features: dict, audio_filename: str, output_path: str):
    """
    Generate and save a 3-panel visual sanity check plot:
    (a) Raw waveform
    (b) FFT magnitude spectrum
    (c) MFCC heatmap
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 10))
    fig.suptitle(f"Acoustic Feature Visualization - {audio_filename}", fontsize=14, fontweight="bold")

    sr = features["sample_rate"]
    y = features["signal"]
    time_axis = np.linspace(0, features["duration"], len(y))

    # Panel (a): Raw Waveform
    axes[0].plot(time_axis, y, color="#1f77b4", alpha=0.8)
    axes[0].set_title("(a) Time-Domain Raw Waveform")
    axes[0].set_xlabel("Time (seconds)")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True, linestyle="--", alpha=0.5)

    # Panel (b): FFT Magnitude Spectrum
    fft_freqs = features["fft_freqs"]
    fft_mag = features["fft_magnitude"]
    axes[1].plot(fft_freqs, fft_mag, color="#ff7f0e")
    axes[1].set_title("(b) Raw FFT Magnitude Spectrum")
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_ylabel("Magnitude")
    axes[1].set_xlim(0, sr / 2)  # Nyquist limit
    axes[1].grid(True, linestyle="--", alpha=0.5)

    # Panel (c): MFCC Heatmap
    mfcc = features["mfcc"]
    img = librosa.display.specshow(
        mfcc,
        x_axis="time",
        sr=sr,
        ax=axes[2],
        cmap="viridis"
    )
    axes[2].set_title("(c) 13-Coefficient MFCC Heatmap")
    axes[2].set_xlabel("Time (seconds)")
    axes[2].set_ylabel("MFCC Coefficient")
    fig.colorbar(img, ax=axes[2], format="%+2.0f dB")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Feature visualization saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Visualize acoustic features extracted from a .wav audio file.")
    parser.add_argument(
        "--audio",
        type=str,
        default=os.path.join("data", "raw", "acoustic", "sample_tap_firm.wav"),
        help="Path to input audio file (.wav)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.path.join("data", "processed", "acoustic_feature_visualization.png"),
        help="Path to output visualization PNG image"
    )

    args = parser.parse_args()
    
    audio_path = args.audio
    if not os.path.exists(audio_path):
        print(f"Error: Specified audio file '{audio_path}' does not exist.")
        sys.exit(1)

    print(f"Extracting features for visualization from: {audio_path}")
    features = extract_features(audio_path)
    filename = os.path.basename(audio_path)
    plot_acoustic_features(features, filename, args.output)

if __name__ == "__main__":
    main()
