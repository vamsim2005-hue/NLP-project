import os
import sys
import json
import urllib.request
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ml.utils.preprocessing import clean_text
from ml.utils.evaluation import evaluate_binary_model, print_evaluation_summary

DATA_URL = "https://raw.githubusercontent.com/justmarkham/DAT8/master/data/sms.tsv"
DATA_DIR = PROJECT_ROOT / "ml" / "datasets" / "spam"
DATA_FILE = DATA_DIR / "sms_spam.tsv"
MODEL_DIR = PROJECT_ROOT / "backend" / "app" / "models"


def ensure_dataset() -> Path:
    """Downloads SMS spam dataset from public repository if not present."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        print(f"Downloading SMS spam dataset from {DATA_URL}...")
        req = urllib.request.Request(DATA_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response, open(DATA_FILE, "wb") as out_file:
            out_file.write(response.read())
        print(f"Dataset downloaded successfully to {DATA_FILE}")
    else:
        print(f"Using existing dataset from {DATA_FILE}")
    return DATA_FILE


def train_spam_pipeline():
    dataset_path = ensure_dataset()
    df = pd.read_csv(dataset_path, sep="\t", header=None, names=["label", "text"])
    
    df = df.dropna().reset_index(drop=True)
    dataset_size = len(df)
    class_counts = df["label"].value_counts().to_dict()
    
    print("\n--- Exploratory Data Analysis: Spam Detection ---")
    print(f"Total instances: {dataset_size}")
    print(f"Class distribution: {class_counts}")
    print(f"Sample data:\n{df.head(3)}\n")

    # Map labels: ham -> 0, spam -> 1
    label_map = {"ham": 0, "spam": 1}
    df["numeric_label"] = df["label"].map(label_map)

    # Text cleaning
    print("Applying text preprocessing (lowercasing, punctuation, regex)...")
    df["cleaned_text"] = df["text"].apply(lambda t: clean_text(t, remove_stopwords=False, keep_negations=True))
    df = df[df["cleaned_text"].str.strip() != ""].reset_index(drop=True)

    # Train / Test Stratified Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        df["cleaned_text"],
        df["numeric_label"].astype(int),
        test_size=0.2,
        random_state=42,
        stratify=df["numeric_label"]
    )
    print(f"Training set: {len(X_train)} samples | Test set: {len(X_test)} samples")

    # TF-IDF Vectorizer
    print("Fitting TF-IDF Vectorizer (ngram_range=(1, 2), max_features=8000)...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=8000,
        sublinear_tf=True
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Model Training: Multinomial Naive Bayes
    print("Training Multinomial Naive Bayes classifier (alpha=0.2)...")
    model = MultinomialNB(alpha=0.2)
    model.fit(X_train_tfidf, y_train)

    # Evaluation on Test Data
    y_pred = model.predict(X_test_tfidf)
    metrics = evaluate_binary_model(
        y_true=y_test.values,
        y_pred=y_pred,
        labels=["ham", "spam"]
    )

    # Print actual evaluation summary
    print_evaluation_summary("Spam Detection", metrics, dataset_size, class_counts)

    # Serialization
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_DIR / "spam_model.pkl"
    vectorizer_path = MODEL_DIR / "spam_vectorizer.pkl"
    metrics_path = MODEL_DIR / "spam_metrics.json"

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    metrics_payload = {
        "model_name": "Spam Detection",
        "algorithm": "TF-IDF + Multinomial Naive Bayes",
        "task_type": "Binary Classification",
        "labels": ["ham", "spam"],
        "dataset_name": "SMS Spam Collection (UCI)",
        "dataset_size": dataset_size,
        "test_size": len(X_test),
        "metrics": {
            "accuracy": metrics["accuracy"],
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1_score": metrics["f1_score"]
        },
        "confusion_matrix": metrics["confusion_matrix"],
        "classification_report": metrics["classification_report"]
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)

    print(f"Saved model to: {model_path}")
    print(f"Saved vectorizer to: {vectorizer_path}")
    print(f"Saved metrics to: {metrics_path}")
    print("Spam training pipeline completed successfully!\n")


if __name__ == "__main__":
    train_spam_pipeline()
