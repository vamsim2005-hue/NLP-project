import json
from pathlib import Path
from typing import Dict, Any, Optional
import joblib
from fastapi import HTTPException

from ml.utils.preprocessing import clean_text

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODEL_DIR / "sentiment_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "sentiment_vectorizer.pkl"
METRICS_PATH = MODEL_DIR / "sentiment_metrics.json"


class SentimentService:
    _instance: Optional["SentimentService"] = None

    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.metrics = None
        self._load_artifacts()

    @classmethod
    def get_instance(cls) -> "SentimentService":
        if cls._instance is None:
            cls._instance = SentimentService()
        return cls._instance

    def _load_artifacts(self):
        """Loads serialized model and vectorizer once at startup or on demand."""
        if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
            # Will be handled gracefully when a prediction is attempted
            return

        try:
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            if METRICS_PATH.exists():
                with open(METRICS_PATH, "r", encoding="utf-8") as f:
                    self.metrics = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load sentiment model artifacts: {str(e)}")

    def is_ready(self) -> bool:
        return self.model is not None and self.vectorizer is not None

    def predict(self, text: str) -> Dict[str, Any]:
        if not self.is_ready():
            # Try reloading once in case training finished after service init
            self._load_artifacts()
            if not self.is_ready():
                raise HTTPException(
                    status_code=503,
                    detail="Sentiment model is not trained or model files are missing. Please run ml/scripts/train_sentiment.py first."
                )

        # 1. Clean incoming text using identical preprocessing pipeline
        cleaned = clean_text(text, remove_stopwords=False, keep_negations=True)
        if not cleaned:
            # Fallback if text becomes empty after stripping symbols
            cleaned = text.lower().strip()

        # 2. Vectorize
        features = self.vectorizer.transform([cleaned])

        # 3. Model predict and probability estimation
        prediction_idx = int(self.model.predict(features)[0])
        probabilities_array = self.model.predict_proba(features)[0]

        # 0 -> negative, 1 -> positive
        label_names = ["negative", "positive"]
        predicted_label = label_names[prediction_idx]
        confidence = float(probabilities_array[prediction_idx])

        probabilities = {
            "negative": round(float(probabilities_array[0]), 4),
            "positive": round(float(probabilities_array[1]), 4)
        }

        return {
            "prediction": predicted_label,
            "confidence": round(confidence, 4),
            "probabilities": probabilities
        }

    def get_metrics(self) -> Optional[Dict[str, Any]]:
        if self.metrics is None and METRICS_PATH.exists():
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                self.metrics = json.load(f)
        return self.metrics


sentiment_service = SentimentService.get_instance()
