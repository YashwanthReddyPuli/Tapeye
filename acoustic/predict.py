import os
import sys
import argparse
import joblib
import numpy as np

try:
    from acoustic.feature_extraction import extract_features
    from acoustic.dataset_builder import aggregate_features
except ModuleNotFoundError:
    from feature_extraction import extract_features
    from dataset_builder import aggregate_features


def predict_quality(audio_path: str, model_path: str = os.path.join("models", "acoustic_classifier.pkl")) -> dict:
    """
    Predict produce quality from an input acoustic .wav audio file.

    Parameters:
        audio_path (str): Path to target .wav audio file.
        model_path (str): Path to trained classifier binary (.pkl).

    Returns:
        dict: {
            "predicted_class": str,
            "probabilities": {
                "class_name": float, ...
            }
        }
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model not found at '{model_path}'. Run train_classifier.py first.")

    # 1. Extract raw features via Phase 1 module
    raw_features = extract_features(audio_path)

    # 2. Aggregate features into fixed-length 1D feature vector
    feat_vector = aggregate_features(raw_features).reshape(1, -1)

    # 3. Load trained classifier model
    model = joblib.load(model_path)

    # 4. Predict probabilities & class label
    probs = model.predict_proba(feat_vector)[0]
    classes = model.classes_

    prob_dict = {cls_name: round(float(prob), 4) for cls_name, prob in zip(classes, probs)}
    predicted_label = str(model.predict(feat_vector)[0])

    return {
        "predicted_class": predicted_label,
        "probabilities": prob_dict
    }

def main():
    parser = argparse.ArgumentParser(description="Predict produce quality from tap audio using trained acoustic classifier.")
    parser.add_argument(
        "--audio",
        type=str,
        default=os.path.join("data", "raw", "acoustic", "good_tap_1.wav"),
        help="Path to input .wav audio file"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.path.join("models", "acoustic_classifier.pkl"),
        help="Path to trained model file"
    )

    args = parser.parse_args()

    result = predict_quality(args.audio, args.model)
    print("\n--- TapEye Acoustic Prediction Result ---")
    print(f"Audio File: {args.audio}")
    print(f"Predicted Quality Class: {result['predicted_class']}")
    print("Class Probabilities:")
    for cls_name, prob in result["probabilities"].items():
        print(f"  - {cls_name}: {prob * 100:.2f}%")
    print("------------------------------------------\n")

if __name__ == "__main__":
    main()
