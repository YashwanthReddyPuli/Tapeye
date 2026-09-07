import os
import csv
import pickle
import numpy as np
from sklearn.model_selection import train_test_split

try:
    from acoustic.predict import predict_quality as predict_acoustic
    from visual.predict import predict_quality as predict_visual
except ModuleNotFoundError:
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from acoustic.predict import predict_quality as predict_acoustic
    from visual.predict import predict_quality as predict_visual


def build_fused_dataset(manifest_path: str = os.path.join("data", "raw", "fusion_pairs.csv"),
                        output_path: str = os.path.join("data", "processed", "fusion", "dataset.pkl")) -> dict:
    """
    Build late-fusion dataset by executing acoustic and visual inference for each paired produce item,
    concatenating probability vectors, and performing train/test split.
    """
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Fusion manifest file not found at '{manifest_path}'. Run scripts/create_fusion_pairs.py first.")

    pairs = []
    with open(manifest_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= 3:
                pairs.append((row[0].strip(), row[1].strip(), row[2].strip().lower()))

    if not pairs:
        raise ValueError(f"No valid sample pairs found in manifest '{manifest_path}'")

    print(f"Loaded {len(pairs)} produce pairs from manifest. Extracting unimodal predictions...")

    X_fused_list = []
    X_acoustic_probs_list = []
    X_visual_probs_list = []
    y_list = []

    # Sort class keys to guarantee consistent vector alignment
    class_names = ["bad", "borderline", "good"]

    for audio_p, image_p, label in pairs:
        print(f"Processing Pair: Audio='{os.path.basename(audio_p)}' | Image='{os.path.basename(image_p)}' -> Label='{label}'")

        # 1. Acoustic branch prediction
        ac_res = predict_acoustic(audio_p)
        ac_probs = np.array([ac_res["probabilities"].get(c, 0.0) for c in class_names], dtype=np.float32)

        # 2. Visual branch prediction
        vis_res = predict_visual(image_p)
        vis_probs = np.array([vis_res["probabilities"].get(c, 0.0) for c in class_names], dtype=np.float32)

        # 3. Concatenate late-fusion feature vector [P_A || P_V]
        fused_vec = np.concatenate([ac_probs, vis_probs])

        X_fused_list.append(fused_vec)
        X_acoustic_probs_list.append(ac_probs)
        X_visual_probs_list.append(vis_probs)
        y_list.append(label)

    X_fused = np.array(X_fused_list, dtype=np.float32)
    X_acoustic_probs = np.array(X_acoustic_probs_list, dtype=np.float32)
    X_visual_probs = np.array(X_visual_probs_list, dtype=np.float32)
    y = np.array(y_list)

    # Train / test split (80/20 stratified, fallback for tiny datasets)
    unique_classes, counts = np.unique(y, return_counts=True)
    min_count = np.min(counts) if len(counts) > 0 else 0

    if min_count >= 2 and len(X_fused) >= 5:
        try:
            (X_tr, X_te,
             y_tr, y_te,
             ac_tr, ac_te,
             vis_tr, vis_te) = train_test_split(
                X_fused, y, X_acoustic_probs, X_visual_probs,
                test_size=0.20, random_state=42, stratify=y
            )
        except Exception:
            (X_tr, X_te,
             y_tr, y_te,
             ac_tr, ac_te,
             vis_tr, vis_te) = train_test_split(
                X_fused, y, X_acoustic_probs, X_visual_probs,
                test_size=0.20, random_state=42
            )
    else:
        print("Note: Small fusion dataset detected. Using non-stratified train/test split.")
        X_tr, X_te = X_fused, X_fused
        y_tr, y_te = y, y
        ac_tr, ac_te = X_acoustic_probs, X_acoustic_probs
        vis_tr, vis_te = X_visual_probs, X_visual_probs

    dataset = {
        "X_train": X_tr,
        "X_test": X_te,
        "y_train": y_tr,
        "y_test": y_te,
        "ac_probs_train": ac_tr,
        "ac_probs_test": ac_te,
        "vis_probs_train": vis_tr,
        "vis_probs_test": vis_te,
        "class_names": class_names
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        pickle.dump(dataset, f)

    print(f"\nFusion dataset built successfully and saved to '{output_path}'.")
    print(f" - Total samples: {len(X_fused)}")
    print(f" - Train samples: {len(X_tr)}")
    print(f" - Test samples:  {len(X_te)}")
    print(f" - Fused feature vector shape: {X_fused.shape}")

    return dataset


if __name__ == "__main__":
    build_fused_dataset()
