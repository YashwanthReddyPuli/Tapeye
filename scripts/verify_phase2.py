import os
import sys

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import pickle
import joblib
from acoustic.dataset_builder import build_dataset
from acoustic.train_classifier import train_and_evaluate
from acoustic.predict import predict_quality

def test_phase2_pipeline():
    dataset_path = os.path.join("data", "processed", "acoustic", "dataset.pkl")
    model_path = os.path.join("models", "acoustic_classifier.pkl")
    metrics_path = os.path.join("models", "acoustic_classifier_metrics.txt")

    # 1. Test dataset building
    dataset = build_dataset(output_path=dataset_path)
    assert os.path.exists(dataset_path), "Dataset pickle file missing"
    assert "X_train" in dataset and "y_train" in dataset, "Dataset dict keys missing"
    assert len(dataset["X_train"]) > 0, "Train feature matrix empty"

    # 2. Test model training
    train_and_evaluate(dataset_path=dataset_path, model_output_path=model_path, metrics_output_path=metrics_path)
    assert os.path.exists(model_path), "Trained model binary missing"
    assert os.path.exists(metrics_path), "Metrics report text file missing"

    # 3. Test prediction function
    test_audio = os.path.join("data", "raw", "acoustic", "good_tap_1.wav")
    res = predict_quality(test_audio, model_path=model_path)

    assert "predicted_class" in res, "Prediction missing 'predicted_class'"
    assert "probabilities" in res, "Prediction missing 'probabilities'"
    assert isinstance(res["probabilities"], dict), "Probabilities must be a dictionary"
    assert sum(res["probabilities"].values()) > 0.9, "Probabilities sum must be ~1.0"

    print("\n[Phase 2 Verification Passed] All dataset, training, metric, and inference tests passed successfully!\n")

if __name__ == "__main__":
    test_phase2_pipeline()
