import os
import numpy as np
from scipy.io import wavfile

def generate_tap_sound(frequency: float, decay: float, duration: float = 0.5, sr: int = 22050) -> np.ndarray:
    """Generate a synthetic acoustic tap sound (damped sine wave + transient click)."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    # Exponentially decaying sinusoid simulating acoustic impact response
    sine_decay = np.sin(2 * np.pi * frequency * t) * np.exp(-decay * t)
    # Adding a short initial impact click
    click = np.random.normal(0, 0.1, size=len(t)) * np.exp(-150 * t)
    signal = sine_decay + click
    # Normalize to [-1.0, 1.0]
    signal = signal / np.max(np.abs(signal))
    return (signal * 32767).astype(np.int16)

def main():
    output_dir = os.path.join("data", "raw", "acoustic")
    os.makedirs(output_dir, exist_ok=True)
    
    samples = {
        "sample_tap_firm.wav": (440.0, 30.0),      # High resonance frequency, quick decay (firm fruit)
        "sample_tap_ripe.wav": (280.0, 20.0),      # Medium resonance frequency, moderate decay (ripe fruit)
        "sample_tap_overripe.wav": (160.0, 10.0)   # Low resonance frequency, slow decay (overripe/soft fruit)
    }
    
    sr = 22050
    for filename, (freq, decay) in samples.items():
        audio_data = generate_tap_sound(frequency=freq, decay=decay, duration=0.5, sr=sr)
        filepath = os.path.join(output_dir, filename)
        wavfile.write(filepath, sr, audio_data)
        print(f"Generated sample audio: {filepath}")

if __name__ == "__main__":
    main()
