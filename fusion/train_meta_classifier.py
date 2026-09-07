import os
import pickle
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report


def train_meta_classifier(dataset_path: str = os.path.join("data", "processed", "fusion", "dataset.pkl"),
                          model_output_path: str = os.path.join("models", "fusion_classifier.pkl"),
                          metrics_output_path: str = os.path.join("models", "fusion_comparison_report.txt")):
    """
    Train late-fusion meta-classifier, evaluate performance against unimodal acoustic and visual branches,
    save winning model and comparative report.
    """
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Fused dataset file not found at '{dataset_path}'. Run fusion/build_fusion_dataset.py first.")

    with open(dataset_path, "rb") as f:
        dataset = pickle.load(f)

    X_train, X_test = dataset["X_train"], dataset["X_test"]
    y_train, y_test = dataset["y_train"], dataset["y_test"]
    ac_probs_test = dataset["ac_probs_test"]
    vis_probs_test = dataset["vis_probs_test"]
    class_names = dataset["class_names"]

    print(f"Loaded fused dataset. Train: {X_train.shape}, Test: {X_test.shape}")
    print(f"Classes: {class_names}")

    # 1. Unimodal Acoustic-Only Evaluation on Test Set
    ac_pred_indices = np.argmax(ac_probs_test, axis=1)
    ac_y_pred = np.array([class_names[idx] for idx in ac_pred_indices])
    ac_acc = accuracy_score(y_test, ac_y_pred)
    ac_prec, ac_rec, ac_f1, _ = precision_recall_fscore_support(y_test, ac_y_pred, average="weighted", zero_division=0)

    # 2. Unimodal Visual-Only Evaluation on Test Set
    vis_pred_indices = np.argmax(vis_probs_test, axis=1)
    vis_y_pred = np.array([class_names[idx] for idx in vis_pred_indices])
    vis_acc = accuracy_score(y_test, vis_y_pred)
    vis_prec, vis_rec, vis_f1, _ = precision_recall_fscore_support(y_test, vis_y_pred, average="weighted", zero_division=0)

    # 3. Multimodal Meta-Classifier Candidate A: Logistic Regression
    lr_model = LogisticRegression(C=1.0, random_state=42)
    lr_model.fit(X_train, y_train)
    lr_y_pred = lr_model.predict(X_test)
    lr_acc = accuracy_score(y_test, lr_y_pred)
    lr_prec, lr_rec, lr_f1, _ = precision_recall_fscore_support(y_test, lr_y_pred, average="weighted", zero_division=0)

    # 4. Multimodal Meta-Classifier Candidate B: Decision Tree
    dt_model = DecisionTreeClassifier(max_depth=3, random_state=42)
    dt_model.fit(X_train, y_train)
    dt_y_pred = dt_model.predict(X_test)
    dt_acc = accuracy_score(y_test, dt_y_pred)
    dt_prec, dt_rec, dt_f1, _ = precision_recall_fscore_support(y_test, dt_y_pred, average="weighted", zero_division=0)

    # Select winning fusion model (preferring Logistic Regression on tie for smoother probabilities)
    if lr_acc >= dt_acc:
        winning_name = "Logistic Regression Meta-Classifier"
        winning_model = lr_model
        winning_y_pred = lr_y_pred
        winning_acc = lr_acc
        winning_f1 = lr_f1
    else:
        winning_name = "Decision Tree Meta-Classifier"
        winning_model = dt_model
        winning_y_pred = dt_y_pred
        winning_acc = dt_acc
        winning_f1 = dt_f1

    # Save winning model binary
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(winning_model, model_output_path)
    print(f"Saved winning meta-classifier to: {model_output_path}")

    # Generate comparative report
    cm = confusion_matrix(y_test, winning_y_pred, labels=class_names)
    clf_report = classification_report(y_test, winning_y_pred, target_names=class_names, zero_division=0)

    report_text = f"""====================================================================
TapEye Late-Fusion Multimodal Performance Comparison Report
====================================================================
Winning Fusion Model: {winning_name}

Summary Performance Comparison (Held-Out Test Set):
--------------------------------------------------------------------
 Pipeline Branch             | Accuracy | Precision | Recall | F1-Score
--------------------------------------------------------------------
 Acoustic-Only Branch        |  {ac_acc*100:6.2f}% |   {ac_prec:7.4f} | {ac_rec:6.4f} |  {ac_f1:7.4f}
 Visual-Only Branch          |  {vis_acc*100:6.2f}% |   {vis_prec:7.4f} | {vis_rec:6.4f} |  {vis_f1:7.4f}
 Fused (Decision Tree)       |  {dt_acc*100:6.2f}% |   {dt_prec:7.4f} | {dt_rec:6.4f} |  {dt_f1:7.4f}
 Fused (Logistic Regression) |  {lr_acc*100:6.2f}% |   {lr_prec:7.4f} | {lr_rec:6.4f} |  {lr_f1:7.4f}
--------------------------------------------------------------------
 Fusion Advantage over Acoustic-Only: {(winning_acc - ac_acc)*100:+.2f}% Accuracy
 Fusion Advantage over Visual-Only:   {(winning_acc - vis_acc)*100:+.2f}% Accuracy

Winning Fused Model Classification Report:
{clf_report}

Confusion Matrix (Labels: {class_names}):
{cm}
====================================================================
"""
    with open(metrics_output_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Saved comparison report to: {metrics_output_path}")
    print("\n" + report_text)


if __name__ == "__main__":
    train_meta_classifier()
