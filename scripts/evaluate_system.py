import os
import sys
import json
import pickle
import joblib
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

def evaluate_full_system(dataset_path: str = os.path.join("data", "processed", "fusion", "dataset.pkl"),
                         fusion_model_path: str = os.path.join("models", "fusion_classifier.pkl"),
                         txt_report_path: str = os.path.join("models", "system_evaluation_report.txt"),
                         json_report_path: str = os.path.join("models", "system_evaluation_metrics.json")):
    """
    Run comprehensive system evaluation comparing Acoustic-Only, Visual-Only, and Late-Fusion Multimodal Scanner
    performance across the held-out test set.
    """
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset file missing at '{dataset_path}'. Run fusion/build_fusion_dataset.py first.")

    if not os.path.exists(fusion_model_path):
        raise FileNotFoundError(f"Fusion model binary missing at '{fusion_model_path}'. Run fusion/train_meta_classifier.py first.")

    with open(dataset_path, "rb") as f:
        dataset = pickle.load(f)

    X_test = dataset["X_test"]
    y_test = dataset["y_test"]
    ac_probs_test = dataset["ac_probs_test"]
    vis_probs_test = dataset["vis_probs_test"]
    class_names = list(dataset["class_names"])

    # 1. Acoustic-Only Evaluation
    ac_pred_indices = np.argmax(ac_probs_test, axis=1)
    ac_preds = np.array([class_names[i] for i in ac_pred_indices])
    ac_acc = float(accuracy_score(y_test, ac_preds))
    ac_p, ac_r, ac_f1, _ = precision_recall_fscore_support(y_test, ac_preds, average="weighted", zero_division=0)
    ac_cm = confusion_matrix(y_test, ac_preds, labels=class_names)

    # 2. Visual-Only Evaluation
    vis_pred_indices = np.argmax(vis_probs_test, axis=1)
    vis_preds = np.array([class_names[i] for i in vis_pred_indices])
    vis_acc = float(accuracy_score(y_test, vis_preds))
    vis_p, vis_r, vis_f1, _ = precision_recall_fscore_support(y_test, vis_preds, average="weighted", zero_division=0)
    vis_cm = confusion_matrix(y_test, vis_preds, labels=class_names)

    # 3. Late-Fusion Multimodal Evaluation
    meta_model = joblib.load(fusion_model_path)
    fusion_preds = meta_model.predict(X_test)
    fusion_acc = float(accuracy_score(y_test, fusion_preds))
    fusion_p, fusion_r, fusion_f1, _ = precision_recall_fscore_support(y_test, fusion_preds, average="weighted", zero_division=0)
    fusion_cm = confusion_matrix(y_test, fusion_preds, labels=class_names)
    clf_report = classification_report(y_test, fusion_preds, target_names=class_names, zero_division=0)

    # Calculate improvements
    gain_over_acoustic = (fusion_acc - ac_acc) * 100
    gain_over_visual = (fusion_acc - vis_acc) * 100

    # Format Text Report
    txt_report = f"""================================================================================
           TapEye System Evaluation & Benchmark Report
================================================================================
Test Set Size: {len(y_test)} samples | Target Classes: {class_names}

1. CONSOLIDATED ACCURACY & METRICS COMPARISON:
--------------------------------------------------------------------------------
 Modality / Branch           | Accuracy | Precision |  Recall  | F1-Score
--------------------------------------------------------------------------------
 Acoustic Branch (Internal)  | {ac_acc*100:7.2f}% |  {ac_p:8.4f} | {ac_r:8.4f} | {ac_f1:8.4f}
 Visual Branch   (Surface)   | {vis_acc*100:7.2f}% |  {vis_p:8.4f} | {vis_r:8.4f} | {vis_f1:8.4f}
 Fused Scanner   (Late-Fusion)| {fusion_acc*100:7.2f}% |  {fusion_p:8.4f} | {fusion_r:8.4f} | {fusion_f1:8.4f}
--------------------------------------------------------------------------------
 Late-Fusion Accuracy Boost over Acoustic-Only: {gain_over_acoustic:+.2f}%
 Late-Fusion Accuracy Boost over Visual-Only:   {gain_over_visual:+.2f}%

2. FUSED MULTIMODAL CLASSIFICATION REPORT:
{clf_report}

3. CONFUSION MATRICES (Order: {class_names}):
--------------------------------------------------------------------------------
Acoustic-Only Confusion Matrix:
{ac_cm}

Visual-Only Confusion Matrix:
{vis_cm}

Fused Late-Fusion Confusion Matrix:
{fusion_cm}
================================================================================
"""

    os.makedirs(os.path.dirname(txt_report_path), exist_ok=True)
    with open(txt_report_path, "w", encoding="utf-8") as f:
        f.write(txt_report)

    # Format JSON Report
    json_data = {
        "test_samples": len(y_test),
        "class_names": class_names,
        "acoustic_branch": {
            "accuracy": ac_acc,
            "precision": float(ac_p),
            "recall": float(ac_r),
            "f1_score": float(ac_f1),
            "confusion_matrix": ac_cm.tolist()
        },
        "visual_branch": {
            "accuracy": vis_acc,
            "precision": float(vis_p),
            "recall": float(vis_r),
            "f1_score": float(vis_f1),
            "confusion_matrix": vis_cm.tolist()
        },
        "fused_multimodal": {
            "accuracy": fusion_acc,
            "precision": float(fusion_p),
            "recall": float(fusion_r),
            "f1_score": float(fusion_f1),
            "confusion_matrix": fusion_cm.tolist()
        },
        "fusion_improvements": {
            "accuracy_gain_over_acoustic_pct": gain_over_acoustic,
            "accuracy_gain_over_visual_pct": gain_over_visual
        }
    }

    with open(json_report_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)

    print(f"System evaluation completed successfully!")
    print(f" - Text report saved to: {txt_report_path}")
    print(f" - JSON metrics saved to: {json_report_path}\n")
    print(txt_report)

if __name__ == "__main__":
    evaluate_full_system()
