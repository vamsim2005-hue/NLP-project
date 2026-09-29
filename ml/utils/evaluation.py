from typing import Dict, Any, List
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


def evaluate_binary_model(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    labels: List[str] = None
) -> Dict[str, Any]:
    """
    Computes standard evaluation metrics for binary classification:
    accuracy, precision, recall, f1, confusion matrix, and full classification report.
    """
    if labels is None:
        labels = ["negative", "positive"]

    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, average="weighted", zero_division=0))
    rec = float(recall_score(y_true, y_pred, average="weighted", zero_division=0))
    f1 = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
    cm = confusion_matrix(y_true, y_pred).tolist()
    report = classification_report(y_true, y_pred, target_names=labels, output_dict=True, zero_division=0)

    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": cm,
        "labels": labels,
        "classification_report": report
    }


def print_evaluation_summary(task_name: str, metrics: Dict[str, Any], dataset_size: int, class_distribution: Dict[str, int]):
    """
    Nicely formats the training and evaluation results to the console.
    """
    print("=" * 60)
    print(f"  MODEL EVALUATION SUMMARY: {task_name.upper()}")
    print("=" * 60)
    print(f"Dataset Total Size : {dataset_size}")
    print(f"Class Distribution : {class_distribution}")
    print("-" * 60)
    print(f"Accuracy           : {metrics['accuracy']:.4f} ({metrics['accuracy'] * 100:.2f}%)")
    print(f"Weighted Precision : {metrics['precision']:.4f}")
    print(f"Weighted Recall    : {metrics['recall']:.4f}")
    print(f"Weighted F1 Score  : {metrics['f1_score']:.4f}")
    print("-" * 60)
    print("Confusion Matrix:")
    labels = metrics.get("labels", ["Class 0", "Class 1"])
    cm = metrics["confusion_matrix"]
    print(f"                 Predicted {labels[0]:<10} Predicted {labels[1]}")
    for idx, row in enumerate(cm):
        print(f"Actual {labels[idx]:<8}: {row[0]:<20} {row[1]}")
    print("=" * 60)
