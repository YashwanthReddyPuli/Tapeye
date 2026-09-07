import os
import csv
import glob
import pickle
import numpy as np
from sklearn.model_selection import train_test_split

LABEL_MAP = {
    "good": "good",
    "firm": "good",
    "borderline": "borderline",
    "ripe": "borderline",
    "bad": "bad",
    "overripe": "bad"
}

def aggregate_features(features_dict: dict) -> np.ndarray:
    """
    Pool variable-length acoustic feature arrays into a fixed-length 1D feature vector.

    Parameters:
        features_dict (dict): Dictionary output from feature_extraction.extract_features()

    Returns:
        np.ndarray: 1D numpy array of aggregated numerical features (~72 features).
    """
    vec_components = []

    # 1. MFCC Summary Statistics (13 coefficients x 4 stats = 52 features)
    mfcc = features_dict["mfcc"]
    vec_components.extend([
        np.mean(mfcc, axis=1),
        np.std(mfcc, axis=1),
        np.min(mfcc, axis=1),
        np.max(mfcc, axis=1)
    ])

    # 2. Spectral Centroid Statistics (4 features)
    sc = features_dict["spectral_centroid"]
    vec_components.extend([
        np.array([np.mean(sc), np.std(sc), np.min(sc), np.max(sc)])
    ])

    # 3. Zero-Crossing Rate Statistics (4 features)
    zcr = features_dict["zero_crossing_rate"]
    vec_components.extend([
        np.array([np.mean(zcr), np.std(zcr), np.min(zcr), np.max(zcr)])
    ])

    # 4. RMS Energy Statistics (4 features)
    rms = features_dict["rms_energy"]
    vec_components.extend([
        np.array([np.mean(rms), np.std(rms), np.min(rms), np.max(rms)])
    ])

    # 5. FFT Magnitude & Peak Frequency Statistics (8 features)
    fft_mag = features_dict["fft_magnitude"]
    fft_freqs = features_dict["fft_freqs"]

    peak_idx = np.argmax(fft_mag)
    dominant_freq = fft_freqs[peak_idx] if peak_idx < len(fft_freqs) else 0.0
    mean_mag = np.mean(fft_mag)
    std_mag = np.std(fft_mag)
    total_energy = np.sum(fft_mag ** 2)
    top5_mags = np.sort(fft_mag)[-4:]  # Top 4 magnitude values

    vec_components.extend([
        np.array([dominant_freq, mean_mag, std_mag, total_energy]),
        top5_mags
    ])

    # Concatenate into 1D array
    return np.concatenate(vec_components).astype(np.float64)


def load_label_mapping(raw_acoustic_dir: str) -> dict:
    """
    Load filename -> label mapping from labels.csv if present.
    Returns a dictionary mapping audio filenames to class labels.
    """
    csv_path = os.path.join(raw_acoustic_dir, "labels.csv")
    label_dict = {}

    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    filename, label = row[0].strip(), row[1].strip()
                    norm_label = LABEL_MAP.get(label.lower(), label.lower())
                    label_dict[filename] = norm_label

    return label_dict


def parse_label_from_filename(filename: str) -> str:
    """
    Infer class label from filename prefix if not listed in labels.csv.
    """
    fname_lower = filename.lower()
    for prefix, mapped_label in LABEL_MAP.items():
        if fname_lower.startswith(prefix) or f"_{prefix}_" in fname_lower or f"_{prefix}." in fname_lower:
            return mapped_label

    # Fallback to string before first underscore
    parts = fname_lower.split("_")
    return LABEL_MAP.get(parts[0], parts[0])


def build_dataset(processed_dir: str = os.path.join("data", "processed", "acoustic"),
                  raw_dir: str = os.path.join("data", "raw", "acoustic"),
                  output_path: str = os.path.join("data", "processed", "acoustic", "dataset.pkl")) -> dict:
    """
    Build structured train/test dataset from extracted feature files.
    """
    feature_files = glob.glob(os.path.join(processed_dir, "*_features.npz"))

    if not feature_files:
        raise FileNotFoundError(f"No feature files (*_features.npz) found in {processed_dir}")

    csv_labels = load_label_mapping(raw_dir)

    X_list = []
    y_list = []
    file_names = []

    for fpath in feature_files:
        basename = os.path.basename(fpath)
        # Determine corresponding audio file name
        audio_name = basename.replace("_features.npz", ".wav")

        # Get label from CSV or filename
        if audio_name in csv_labels:
            label = csv_labels[audio_name]
        else:
            label = parse_label_from_filename(audio_name)

        # Load features and aggregate
        npz_data = np.load(fpath)
        features_dict = {key: npz_data[key] for key in npz_data.files}
        feat_vec = aggregate_features(features_dict)

        X_list.append(feat_vec)
        y_list.append(label)
        file_names.append(audio_name)

    X = np.array(X_list)
    y = np.array(y_list)

    print(f"Loaded {len(X)} samples with {X.shape[1]} features each across classes: {np.unique(y)}")

    # Check for tiny dataset fallback
    unique_classes, counts = np.unique(y, return_counts=True)
    can_stratify = len(unique_classes) > 1 and np.min(counts) >= 2 and len(X) >= 5

    if can_stratify:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    else:
        print("Warning: Small or single-class dataset detected. Falling back to non-stratified split.")
        if len(X) > 1:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        else:
            X_train, X_test, y_train, y_test = X, X, y, y

    dataset = {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "classes": np.unique(y),
        "file_names": file_names
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        pickle.dump(dataset, f)

    print(f"Dataset successfully created and saved to '{output_path}'.")
    print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")
    return dataset


if __name__ == "__main__":
    build_dataset()
