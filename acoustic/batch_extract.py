import os
import glob
import numpy as np
try:
    from acoustic.feature_extraction import extract_features
except ModuleNotFoundError:
    from feature_extraction import extract_features


def batch_extract_acoustic_features(raw_dir: str, processed_dir: str):
    """
    Process all .wav audio files in raw_dir, extract acoustic features,
    and save them as compressed NumPy (.npz) files in processed_dir.
    """
    os.makedirs(processed_dir, exist_ok=True)
    audio_files = glob.glob(os.path.join(raw_dir, "*.wav"))

    if not audio_files:
        print(f"No .wav audio files found in: {raw_dir}")
        return

    print(f"Found {len(audio_files)} audio file(s) in '{raw_dir}'. Starting batch extraction...")

    for audio_path in audio_files:
        filename = os.path.basename(audio_path)
        base_name, _ = os.path.splitext(filename)
        output_path = os.path.join(processed_dir, f"{base_name}_features.npz")

        print(f"Processing: {filename} -> {os.path.basename(output_path)}")
        features = extract_features(audio_path)

        # Save feature dictionary as compressed NumPy archive
        np.savez_compressed(output_path, **features)

    print(f"Batch feature extraction completed successfully! Results saved in '{processed_dir}'.")

def main():
    raw_dir = os.path.join("data", "raw", "acoustic")
    processed_dir = os.path.join("data", "processed", "acoustic")
    batch_extract_acoustic_features(raw_dir, processed_dir)

if __name__ == "__main__":
    main()
