import os
import pickle
import warnings
import joblib
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report

warnings.filterwarnings("ignore")

def train_and_evaluate(dataset_path: str = os.path.join("data", "processed", "acoustic", "dataset.pkl"),
                       model_output_path: str = os.path.join("models", "acoustic_classifier.pkl"),
                       metrics_output_path: str = os.path.join("models", "acoustic_classifier_metrics.txt")):
    """
    Train candidate classifiers (SVM, Random Forest), evaluate on test set, save winning model and metrics report.
    """
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset file not found at '{dataset_path}'. Run dataset_builder.py first.")

    with open(dataset_path, "rb") as f:
        dataset = pickle.load(f)

    X_train, X_test = dataset["X_train"], dataset["X_test"]
    y_train, y_test = dataset["y_train"], dataset["y_test"]
    classes = dataset["classes"]

    # Adaptive cross-validation fold count for small datasets
    unique_train, train_counts = np.unique(y_train, return_counts=True)
    min_samples = np.min(train_counts) if len(train_counts) > 0 else 1
    n_splits = max(2, min(3, int(min_samples)))

    print(f"Training dataset loaded. X_train: {X_train.shape}, X_test: {X_test.shape}")
    print(f"Using {n_splits}-fold cross-validation for grid search.")

    # 1. Candidate 1: SVM with RBF kernel
    svm_param_grid = {
        "C": [0.1, 1.0, 10.0],
        "gamma": ["scale", "auto", 0.01],
        "kernel": ["rbf"]
    }
    svm_grid = GridSearchCV(
        SVC(probability=True, random_state=42),
        svm_param_grid,
        cv=n_splits,
        scoring="accuracy",
        error_score="raise"
    )
    svm_grid.fit(X_train, y_train)
    best_svm = svm_grid.best_estimator_
    y_pred_svm = best_svm.predict(X_test)
    svm_acc = accuracy_score(y_test, y_pred_svm)

    # 2. Candidate 2: Random Forest
    rf_param_grid = {
        "n_estimators": [20, 50, 100],
        "max_depth": [None, 3, 5],
        "criterion": ["gini", "entropy"]
    }
    rf_grid = GridSearchCV(
        RandomForestClassifier(random_state=42),
        rf_param_grid,
        cv=n_splits,
        scoring="accuracy",
        error_score="raise"
    )
    rf_grid.fit(X_train, y_train)
    best_rf = rf_grid.best_estimator_
    y_pred_rf = best_rf.predict(X_test)
    rf_acc = accuracy_score(y_test, y_pred_rf)

    print(f"\nModel Performance Summary:")
    print(f" - SVM (RBF) Test Accuracy: {svm_acc:.4f} (Best Params: {svm_grid.best_params_})")
    print(f" - Random Forest Test Accuracy: {rf_acc:.4f} (Best Params: {rf_grid.best_params_})")

    # Select best model
    if svm_acc >= rf_acc:
        winning_name = "Support Vector Machine (SVM RBF)"
        winning_model = best_svm
        winning_y_pred = y_pred_svm
        winning_acc = svm_acc
        winning_params = svm_grid.best_params_
    else:
        winning_name = "Random Forest"
        winning_model = best_rf
        winning_y_pred = y_pred_rf
        winning_acc = rf_acc
        winning_params = rf_grid.best_params_

    print(f"\nWinning Model: {winning_name} with Accuracy = {winning_acc:.4f}")

    # Compute metrics
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, winning_y_pred, average="weighted", zero_division=0
    )
    cm = confusion_matrix(y_test, winning_y_pred, labels=classes)
    clf_report = classification_report(y_test, winning_y_pred, labels=classes, zero_division=0)

    # Save model using joblib
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(winning_model, model_output_path)
    print(f"Saved winning model to: {model_output_path}")

    # Save metrics report
    report_text = f"""==================================================
TapEye Acoustic Classifier Training Metrics Report
==================================================
Winning Model: {winning_name}
Best Hyperparameters: {winning_params}

Test Set Metrics:
  - Accuracy:  {winning_acc:.4f}
  - Precision: {precision:.4f} (weighted)
  - Recall:    {recall:.4f} (weighted)
  - F1 Score:  {f1:.4f} (weighted)

Candidate Comparison:
  - SVM (RBF) Test Accuracy:           {svm_acc:.4f}
  - Random Forest Test Accuracy:     {rf_acc:.4f}

Classification Report:
{clf_report}

Confusion Matrix (Labels: {classes.tolist()}):
{cm}
==================================================
"""
    with open(metrics_output_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Saved metrics report to: {metrics_output_path}")
    print("\n" + report_text)

if __name__ == "__main__":
    train_and_evaluate()
