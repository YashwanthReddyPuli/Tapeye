import os
import sys
import argparse
import joblib
import numpy as np

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from acoustic.predict import predict_quality as predict_acoustic
from visual.predict import predict_quality as predict_visual

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def predict_final_verdict(audio_path: str,
                           image_path: str,
                           model_path: str = os.path.join("models", "fusion_classifier.pkl")) -> dict:
    """
    Predict final dual-modal produce quality verdict by fusing acoustic and visual probability vectors.

    Parameters:
        audio_path (str): Path to input tap audio file (.wav)
        image_path (str): Path to input produce image (.jpg, .png)
        model_path (str): Path to trained meta-classifier binary (.pkl)

    Returns:
        dict: Structured fusion verdict dictionary containing final verdict, fusion confidence,
              fused probabilities, and unimodal branch breakdown.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained fusion model not found at '{model_path}'. Run fusion/train_meta_classifier.py first.")

    class_names = ["bad", "borderline", "good"]

    # 1. Obtain unimodal branch predictions
    ac_model_path = os.path.join(repo_root, "models", "acoustic_classifier.pkl")
    vis_model_path = os.path.join(repo_root, "models", "visual_classifier.keras")
    vis_dataset_path = os.path.join(repo_root, "data", "processed", "visual", "dataset.pkl")
    acoustic_res = predict_acoustic(audio_path, model_path=ac_model_path)
    visual_res = predict_visual(image_path, model_path=vis_model_path, dataset_path=vis_dataset_path)

    # 2. Extract and align probability vectors
    ac_probs = np.array([acoustic_res["probabilities"].get(c, 0.0) for c in class_names], dtype=np.float32)
    vis_probs = np.array([visual_res["probabilities"].get(c, 0.0) for c in class_names], dtype=np.float32)

    # 3. Concatenate late-fusion feature vector [P_A || P_V]
    fused_vec = np.concatenate([ac_probs, vis_probs]).reshape(1, -1)

    # 4. Load meta-classifier and run inference
    meta_model = joblib.load(model_path)

    if hasattr(meta_model, "predict_proba"):
        fused_probs_raw = meta_model.predict_proba(fused_vec)[0]
    else:
        # Fallback if model doesn't support probability
        pred_label = meta_model.predict(fused_vec)[0]
        fused_probs_raw = np.array([1.0 if c == pred_label else 0.0 for c in class_names])

    model_classes = list(getattr(meta_model, "classes_", class_names))
    fused_prob_dict = {
        cname: round(float(fused_probs_raw[model_classes.index(cname)]), 4)
        if cname in model_classes else 0.0
        for cname in class_names
    }

    final_verdict = str(meta_model.predict(fused_vec)[0])
    fusion_confidence = fused_prob_dict.get(final_verdict, round(float(np.max(fused_probs_raw)), 4))

    return {
        "final_verdict": final_verdict,
        "fusion_confidence": fusion_confidence,
        "fused_probabilities": fused_prob_dict,
        "acoustic_branch": acoustic_res,
        "visual_branch": visual_res
    }


def main():
    parser = argparse.ArgumentParser(description="Predict produce quality using TapEye dual-modal late fusion.")
    parser.add_argument(
        "--audio",
        type=str,
        default=os.path.join("data", "raw", "acoustic", "good_tap_1.wav"),
        help="Path to input tap .wav audio file"
    )
    parser.add_argument(
        "--image",
        type=str,
        default=os.path.join("data", "raw", "visual", "good", "good_fruit_1.jpg"),
        help="Path to input produce image file"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.path.join("models", "fusion_classifier.pkl"),
        help="Path to trained meta-classifier file (.pkl)"
    )

    args = parser.parse_args()

    result = predict_final_verdict(args.audio, args.image, args.model)

    print("\n==============================================")
    print("      TapEye Dual-Modal Late-Fusion Verdict")
    print("==============================================")
    print(f"Inputs:")
    print(f" - Acoustic: {args.audio}")
    print(f" - Visual:   {args.image}")
    print(f"\nFinal Verdict:     >>> {result['final_verdict'].upper()} <<<")
    print(f"Fusion Confidence: {result['fusion_confidence'] * 100:.2f}%")

    print("\nFused Probability Vector:")
    for cname, prob in result["fused_probabilities"].items():
        print(f" - {cname:10s}: {prob * 100:6.2f}%")

    print("\nUnimodal Branch Breakdown:")
    print(f" - Acoustic Branch Verdict: {result['acoustic_branch']['predicted_class'].upper()} (Probabilities: {result['acoustic_branch']['probabilities']})")
    print(f" - Visual Branch Verdict:   {result['visual_branch']['predicted_class'].upper()} (Probabilities: {result['visual_branch']['probabilities']})")
    print("==============================================\n")


if __name__ == "__main__":
    main()
