import os
import sys

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import pickle
import tensorflow as tf
from visual.preprocess import preprocess_image
from visual.dataset_builder import build_visual_dataset
from visual.train_classifier import train_visual_classifier
from visual.predict import predict_quality

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def test_phase3_pipeline():
    dataset_path = os.path.join("data", "processed", "visual", "dataset.pkl")
    model_path = os.path.join("models", "visual_classifier.keras")
    metrics_path = os.path.join("models", "visual_classifier_metrics.txt")

    # 1. Test image preprocessing
    test_img_path = os.path.join("data", "raw", "visual", "good", "good_fruit_1.jpg")
    proc_img = preprocess_image(test_img_path)
    assert proc_img.shape == (224, 224, 3), f"Preprocessed shape mismatch: {proc_img.shape}"

    # 2. Test dataset building
    dataset = build_visual_dataset(output_path=dataset_path)
    assert os.path.exists(dataset_path), "Visual dataset pickle file missing"
    assert "X_train" in dataset and "y_train" in dataset, "Dataset dict keys missing"
    assert len(dataset["X_train"]) > 0, "Train image batch empty"

    # 3. Test model training
    train_visual_classifier(
        dataset_path=dataset_path,
        model_output_path=model_path,
        metrics_output_path=metrics_path,
        epochs_feature_extraction=2,
        epochs_fine_tune=1
    )
    assert os.path.exists(model_path), "Trained visual model binary missing"
    assert os.path.exists(metrics_path), "Visual metrics report text file missing"

    # 4. Test prediction function
    res = predict_quality(test_img_path, model_path=model_path, dataset_path=dataset_path)
    assert "predicted_class" in res, "Prediction missing 'predicted_class'"
    assert "probabilities" in res, "Prediction missing 'probabilities'"
    assert isinstance(res["probabilities"], dict), "Probabilities must be a dictionary"
    assert abs(sum(res["probabilities"].values()) - 1.0) < 0.05, "Probabilities must sum to ~1.0"

    print("\n[Phase 3 Verification Passed] All visual preprocessing, dataset, training, metric, and inference tests passed successfully!\n")


if __name__ == "__main__":
    test_phase3_pipeline()
