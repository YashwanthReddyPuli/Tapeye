import os
import pickle
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def build_mobilenet_classifier(num_classes: int, input_shape=(224, 224, 3)) -> tf.keras.Model:
    """
    Build transfer learning classifier using pretrained MobileNetV2 base + custom classification head.
    """
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet"
    )

    # Freeze base MobileNetV2 layers
    base_model.trainable = False

    # Build classification head
    inputs = tf.keras.Input(shape=input_shape)
    x = base_model(inputs, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="TapEye_Visual_MobileNetV2")
    return model, base_model


def train_visual_classifier(dataset_path: str = os.path.join("data", "processed", "visual", "dataset.pkl"),
                           model_output_path: str = os.path.join("models", "visual_classifier.keras"),
                           metrics_output_path: str = os.path.join("models", "visual_classifier_metrics.txt"),
                           epochs_feature_extraction: int = 8,
                           epochs_fine_tune: int = 5):
    """
    Train MobileNetV2 visual quality classifier, evaluate on test set, save model and metrics report.
    """
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Visual dataset file not found at '{dataset_path}'. Run visual/dataset_builder.py first.")

    with open(dataset_path, "rb") as f:
        dataset = pickle.load(f)

    X_train, y_train = dataset["X_train"], dataset["y_train"]
    X_val, y_val = dataset["X_val"], dataset["y_val"]
    X_test, y_test = dataset["X_test"], dataset["y_test"]
    class_names = dataset["class_names"]
    num_classes = len(class_names)

    print(f"Loaded visual dataset. Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
    print(f"Classes ({num_classes}): {class_names}")

    # Build transfer learning model
    model, base_model = build_mobilenet_classifier(num_classes)

    # Step 1: Feature Extraction Phase (train custom head only)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    print("\n--- Phase 3a: Training Classification Head (Base Frozen) ---")
    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs_feature_extraction,
        batch_size=8,
        verbose=1
    )

    # Step 2: Fine-tuning Phase (unfreeze top 20 layers of MobileNetV2)
    print("\n--- Phase 3b: Fine-Tuning Top Base Layers ---")
    base_model.trainable = True
    # Freeze all layers except top 20
    for layer in base_model.layers[:-20]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs_fine_tune,
        batch_size=8,
        verbose=1
    )

    # Evaluate model on test set
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    y_pred_probs = model.predict(X_test, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average="weighted", zero_division=0
    )
    cm = confusion_matrix(y_test, y_pred, labels=list(range(num_classes)))
    clf_report = classification_report(
        y_test, y_pred, target_names=class_names, zero_division=0
    )

    # Save model binary (.keras format)
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    model.save(model_output_path)
    print(f"\nSaved trained visual model to: {model_output_path}")

    # Save evaluation report
    report_text = f"""==================================================
TapEye Visual Classifier (MobileNetV2) Metrics Report
==================================================
Model Architecture: MobileNetV2 (Transfer Learning + Fine-Tuning)
Input Resolution: 224x224x3

Test Set Metrics:
  - Accuracy:  {test_acc:.4f}
  - Test Loss: {test_loss:.4f}
  - Precision: {precision:.4f} (weighted)
  - Recall:    {recall:.4f} (weighted)
  - F1 Score:  {f1:.4f} (weighted)

Classification Report:
{clf_report}

Confusion Matrix (Labels: {class_names}):
{cm}
==================================================
"""
    with open(metrics_output_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Saved metrics report to: {metrics_output_path}")
    print("\n" + report_text)


if __name__ == "__main__":
    train_visual_classifier()
