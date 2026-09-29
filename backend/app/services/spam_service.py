import json
from pathlib import Path
from typing import Dict, Any, Optional
import joblib
from fastapi import HTTPException

from ml.utils.preprocessing import clean_text

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODEL_DIR / "spam_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "spam_vectorizer.pkl"
METRICS_PATH = MODEL_DIR / "spam_metrics.json"


class SpamService:
    _instance: Optional["SpamService"] = None

    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.metrics = None
        self._load_artifacts()

    @classmethod
    def get_instance(cls) -> "SpamService":
        if cls._instance is None:
            cls._instance = SpamService()
        return cls._instance

    def _load_artifacts(self):
        """Loads serialized model and vectorizer once at startup or on demand."""
        if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
            return

        try:
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            if METRICS_PATH.exists():
                with open(METRICS_PATH, "r", encoding="utf-8") as f:
                    self.metrics = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load spam model artifacts: {str(e)}")

    def is_ready(self) -> bool:
        return self.model is not None and self.vectorizer is not None

    def predict(self, text: str) -> Dict[str, Any]:
        if not self.is_ready():
            self._load_artifacts()
            if not self.is_ready():
                raise HTTPException(
                    status_code=503,
                    detail="Spam detection model is not trained yet. Please run ml/scripts/train_spam.py first."
                )

        cleaned = clean_text(text, remove_stopwords=False, keep_negations=True)
        if not cleaned:
            cleaned = text.lower().strip()

        features = self.vectorizer.transform([cleaned])

        prediction_idx = int(self.model.predict(features)[0])
        probabilities_array = self.model.predict_proba(features)[0]

        # 0 -> ham (NOT SPAM), 1 -> spam (SPAM)
        predicted_label = "SPAM" if prediction_idx == 1 else "NOT SPAM"
        confidence = float(probabilities_array[prediction_idx])

        probabilities = {
            "ham": round(float(probabilities_array[0]), 4),
            "spam": round(float(probabilities_array[1]), 4)
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


spam_service = SpamService.get_instance()
