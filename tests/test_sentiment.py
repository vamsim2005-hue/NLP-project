import math
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sentiment_positive_prediction():
    payload = {"text": "This movie was absolutely wonderful, brilliant, and breathtaking!"}
    response = client.post("/api/sentiment/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "positive"
    assert "confidence" in data
    assert data["confidence"] >= 0.5
    assert "probabilities" in data
    assert "positive" in data["probabilities"]
    assert "negative" in data["probabilities"]
    # Probabilities should roughly sum to 1.0
    total_prob = data["probabilities"]["positive"] + data["probabilities"]["negative"]
    assert math.isclose(total_prob, 1.0, abs_tol=0.01)


def test_sentiment_negative_prediction():
    payload = {"text": "Terrible film, completely boring, horrible acting, and a waste of time."}
    response = client.post("/api/sentiment/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "negative"
    assert data["confidence"] >= 0.5


def test_sentiment_empty_input_validation():
    # Empty string should fail validation
    response = client.post("/api/sentiment/predict", json={"text": ""})
    assert response.status_code == 422

    # Whitespace only should fail validation
    response = client.post("/api/sentiment/predict", json={"text": "   "})
    assert response.status_code == 422


def test_sentiment_metrics_endpoint():
    response = client.get("/api/sentiment/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "accuracy" in data["metrics"]
    assert data["metrics"]["accuracy"] > 0.7
    assert "confusion_matrix" in data


if __name__ == "__main__":
    print("Running backend tests with TestClient...")
    test_health_endpoint()
    print("[PASS] Health endpoint passed")
    test_sentiment_positive_prediction()
    print("[PASS] Positive sentiment prediction passed")
    test_sentiment_negative_prediction()
    print("[PASS] Negative sentiment prediction passed")
    test_sentiment_empty_input_validation()
    print("[PASS] Empty input validation passed")
    test_sentiment_metrics_endpoint()
    print("[PASS] Metrics endpoint passed")
    print("All backend tests PASSED successfully!")

