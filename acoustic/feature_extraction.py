import os
import numpy as np
import librosa

def extract_features(audio_path: str) -> dict:
    """
    Extract frequency-domain, time-domain, and spectral features from a raw audio file (.wav).

    Parameters:
        audio_path (str): Path to the target .wav audio file.

    Returns:
        dict: A dictionary containing extracted numpy array features and metadata:
              - 'signal': Raw audio waveform array
              - 'sample_rate': Sampling rate (Hz)
              - 'duration': Signal duration in seconds
              - 'fft_magnitude': FFT magnitude spectrum
              - 'fft_freqs': FFT frequency bins (Hz)
              - 'mfcc': 13-coefficient MFCC matrix (shape: 13 x time_steps)
              - 'spectral_centroid': Spectral centroid array over time
              - 'zero_crossing_rate': Zero-crossing rate array over time
              - 'rms_energy': RMS energy array over time
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Load audio file (sr=None preserves native sampling rate)
    y, sr = librosa.load(audio_path, sr=None)
    duration = float(len(y) / sr)

    # 1. Compute raw FFT magnitude spectrum & frequency bins
    n_fft = len(y)
    fft_complex = np.fft.rfft(y)
    fft_magnitude = np.abs(fft_complex)
    fft_freqs = np.fft.rfftfreq(n_fft, d=1.0 / sr)

    # 2. Compute 13-coefficient MFCCs (using 32 mel filters)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_mels=32)

    # 3. Compute supporting features: spectral centroid, zero-crossing rate, RMS energy
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y=y)
    rms_energy = librosa.feature.rms(y=y)

    return {
        "signal": y,
        "sample_rate": sr,
        "duration": duration,
        "fft_magnitude": fft_magnitude,
        "fft_freqs": fft_freqs,
        "mfcc": mfcc,
        "spectral_centroid": spectral_centroid,
        "zero_crossing_rate": zero_crossing_rate,
        "rms_energy": rms_energy,
    }
