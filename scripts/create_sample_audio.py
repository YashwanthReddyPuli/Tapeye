import os
import csv
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
    
    # 15 synthetic tap files across 3 quality classes
    categories = {
        "good": {"freq_range": (420, 480), "decay_range": (28, 35), "count": 5},
        "borderline": {"freq_range": (260, 310), "decay_range": (18, 24), "count": 5},
        "bad": {"freq_range": (140, 190), "decay_range": (8, 14), "count": 5}
    }
    
    labels = []
    sr = 22050
    np.random.seed(42)  # For reproducibility

    for cat_name, params in categories.items():
        freqs = np.linspace(params["freq_range"][0], params["freq_range"][1], params["count"])
        decays = np.linspace(params["decay_range"][0], params["decay_range"][1], params["count"])
        
        for i in range(params["count"]):
            filename = f"{cat_name}_tap_{i+1}.wav"
            filepath = os.path.join(output_dir, filename)
            audio_data = generate_tap_sound(frequency=freqs[i], decay=decays[i], duration=0.5, sr=sr)
            wavfile.write(filepath, sr, audio_data)
            labels.append((filename, cat_name))

    # Also save labels.csv in data/raw/acoustic/
    csv_path = os.path.join(output_dir, "labels.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "label"])
        writer.writerows(labels)

    print(f"Generated {len(labels)} synthetic labeled audio files and labels.csv in '{output_dir}'.")

if __name__ == "__main__":
    main()
