import os
import sys
import pickle
import argparse
import numpy as np
import tensorflow as tf

try:
    from visual.preprocess import preprocess_image
except ModuleNotFoundError:
    from preprocess import preprocess_image

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

_CACHED_VISUAL_MODEL = None


def get_visual_model(model_path: str = os.path.join("models", "visual_classifier.keras")):
    global _CACHED_VISUAL_MODEL
    if _CACHED_VISUAL_MODEL is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Trained visual model not found at '{model_path}'. Run visual/train_classifier.py first.")
        _CACHED_VISUAL_MODEL = tf.keras.models.load_model(model_path)
    return _CACHED_VISUAL_MODEL


def predict_quality(image_path: str,
                    model_path: str = os.path.join("models", "visual_classifier.keras"),
                    dataset_path: str = os.path.join("data", "processed", "visual", "dataset.pkl")) -> dict:
    """
    Predict external produce quality from an input image using MobileNetV2 visual classifier.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Visual image file not found: {image_path}")

    # 1. Preprocess image (224x224 RGB, [-1, 1] scaling)
    processed_img = preprocess_image(image_path)
    img_batch = np.expand_dims(processed_img, axis=0)

    # 2. Load model (cached)
    model = get_visual_model(model_path)

    # 3. Retrieve class names metadata
    if os.path.exists(dataset_path):
        with open(dataset_path, "rb") as f:
            ds = pickle.load(f)
            class_names = ds.get("class_names", ["bad", "borderline", "good"])
    else:
        class_names = ["bad", "borderline", "good"]

    # 4. Run inference
    probs = model.predict(img_batch, verbose=0)[0]
    pred_idx = int(np.argmax(probs))
    predicted_class = class_names[pred_idx]

    prob_dict = {
        cname: round(float(prob), 4)
        for cname, prob in zip(class_names, probs)
    }

    return {
        "predicted_class": predicted_class,
        "probabilities": prob_dict
    }


def main():
    parser = argparse.ArgumentParser(description="Predict produce quality from an image using MobileNetV2 visual classifier.")
    parser.add_argument(
        "--image",
        type=str,
        default=os.path.join("data", "raw", "visual", "good", "good_fruit_1.jpg"),
        help="Path to input produce image"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.path.join("models", "visual_classifier.keras"),
        help="Path to trained .keras model file"
    )

    args = parser.parse_args()

    result = predict_quality(args.image, args.model)
    print("\n--- TapEye Visual Prediction Result ---")
    print(f"Image File: {args.image}")
    print(f"Predicted Quality Class: {result['predicted_class']}")
    print("Class Probabilities:")
    for cls_name, prob in result["probabilities"].items():
        print(f"  - {cls_name}: {prob * 100:.2f}%")
    print("----------------------------------------\n")


if __name__ == "__main__":
    main()
