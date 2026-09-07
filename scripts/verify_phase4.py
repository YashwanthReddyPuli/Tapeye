import os
import sys

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import pickle
import joblib
from scripts.create_fusion_pairs import create_fusion_manifest
from fusion.build_fusion_dataset import build_fused_dataset
from fusion.train_meta_classifier import train_meta_classifier
from fusion.predict import predict_final_verdict

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def test_phase4_pipeline():
    manifest_path = os.path.join("data", "raw", "fusion_pairs.csv")
    dataset_path = os.path.join("data", "processed", "fusion", "dataset.pkl")
    model_path = os.path.join("models", "fusion_classifier.pkl")
    report_path = os.path.join("models", "fusion_comparison_report.txt")

    # 1. Test fusion manifest creation
    create_fusion_manifest()
    assert os.path.exists(manifest_path), "Fusion manifest CSV missing"

    # 2. Test fusion dataset building
    dataset = build_fused_dataset(manifest_path=manifest_path, output_path=dataset_path)
    assert os.path.exists(dataset_path), "Fused dataset pickle missing"
    assert "X_train" in dataset and "y_train" in dataset, "Dataset dict keys missing"
    assert dataset["X_train"].shape[1] == 6, f"Fused feature dimension must be 6, got {dataset['X_train'].shape[1]}"

    # 3. Test meta-classifier training & comparison reporting
    train_meta_classifier(dataset_path=dataset_path, model_output_path=model_path, metrics_output_path=report_path)
    assert os.path.exists(model_path), "Trained fusion model binary missing"
    assert os.path.exists(report_path), "Fusion comparison report text file missing"

    # 4. Test final verdict inference function
    audio_sample = os.path.join("data", "raw", "acoustic", "good_tap_1.wav")
    image_sample = os.path.join("data", "raw", "visual", "good", "good_fruit_1.jpg")

    verdict = predict_final_verdict(audio_sample, image_sample, model_path=model_path)
    assert "final_verdict" in verdict, "Verdict missing 'final_verdict'"
    assert "fusion_confidence" in verdict, "Verdict missing 'fusion_confidence'"
    assert "acoustic_branch" in verdict, "Verdict missing 'acoustic_branch'"
    assert "visual_branch" in verdict, "Verdict missing 'visual_branch'"

    print("\n[Phase 4 Verification Passed] All late-fusion dataset, meta-classifier, comparison reporting, and prediction tests passed successfully!\n")


if __name__ == "__main__":
    test_phase4_pipeline()
