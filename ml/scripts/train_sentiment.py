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
from sklearn.linear_model import LogisticRegression

# Add project root to sys.path to import ml.utils
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ml.utils.preprocessing import clean_text
from ml.utils.evaluation import evaluate_binary_model, print_evaluation_summary

DATA_URL = "https://raw.githubusercontent.com/clairett/pytorch-sentiment-classification/master/data/SST2/train.tsv"
DATA_DIR = PROJECT_ROOT / "ml" / "datasets" / "sentiment"
DATA_FILE = DATA_DIR / "sentiment_train.tsv"
MODEL_DIR = PROJECT_ROOT / "backend" / "app" / "models"


def ensure_dataset() -> Path:
    """Downloads dataset from official benchmark repository if not present locally."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        print(f"Downloading sentiment dataset from {DATA_URL}...")
        req = urllib.request.Request(DATA_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response, open(DATA_FILE, "wb") as out_file:
            out_file.write(response.read())
        print(f"Dataset downloaded successfully to {DATA_FILE}")
    else:
        print(f"Using existing dataset from {DATA_FILE}")
    return DATA_FILE


def train_sentiment_pipeline():
    # 1. Dataset loading & EDA
    dataset_path = ensure_dataset()
    df = pd.read_csv(dataset_path, sep="\t", header=None, names=["text", "label"])
    
    # Drop any nulls
    df = df.dropna().reset_index(drop=True)
    
    dataset_size = len(df)
    class_counts = df["label"].value_counts().to_dict()
    # 0 -> negative, 1 -> positive
    class_distribution = {
        "negative (0)": int(class_counts.get(0, 0)),
        "positive (1)": int(class_counts.get(1, 0))
    }
    
    print("\n--- Initial Exploratory Data Analysis ---")
    print(f"Total instances: {dataset_size}")
    print(f"Class distribution: {class_distribution}")
    print(f"Sample data:\n{df.head(3)}\n")

    # 2. Text Preprocessing
    print("Cleaning text with NLP preprocessing (lowercasing, punctuation, regex)...")
    df["cleaned_text"] = df["text"].apply(lambda t: clean_text(t, remove_stopwords=False, keep_negations=True))
    
    # Drop rows that might have become empty
    df = df[df["cleaned_text"].str.strip() != ""].reset_index(drop=True)

    # 3. Train/Test Split (Stratified 80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        df["cleaned_text"],
        df["label"].astype(int),
        test_size=0.2,
        random_state=42,
        stratify=df["label"]
    )
    print(f"Training set: {len(X_train)} samples | Test set: {len(X_test)} samples")

    # 4. TF-IDF Feature Extraction
    print("Fitting TF-IDF Vectorizer (ngram_range=(1, 2), max_features=10000)...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=10000,
        sublinear_tf=True
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # 5. Model Training: Logistic Regression
    print("Training Logistic Regression classifier (C=1.5, max_iter=1000)...")
    model = LogisticRegression(C=1.5, max_iter=1000, random_state=42)
    model.fit(X_train_tfidf, y_train)

    # 6. Evaluation on Unseen Test Data
    y_pred = model.predict(X_test_tfidf)
    metrics = evaluate_binary_model(
        y_true=y_test.values,
        y_pred=y_pred,
        labels=["negative", "positive"]
    )

    # Print actual evaluation summary to console
    print_evaluation_summary("Sentiment Analysis", metrics, dataset_size, class_distribution)

    # 7. Model Serialization
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_DIR / "sentiment_model.pkl"
    vectorizer_path = MODEL_DIR / "sentiment_vectorizer.pkl"
    metrics_path = MODEL_DIR / "sentiment_metrics.json"

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    # Save metrics metadata for the Performance page
    metrics_payload = {
        "model_name": "Sentiment Analysis",
        "algorithm": "TF-IDF + Logistic Regression",
        "task_type": "Binary Classification",
        "labels": ["negative", "positive"],
        "dataset_name": "Stanford Sentiment Treebank (SST-2)",
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
    print("Sentiment training pipeline completed successfully!\n")


if __name__ == "__main__":
    train_sentiment_pipeline()
