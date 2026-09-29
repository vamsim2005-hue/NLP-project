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


def test_spam_positive_prediction():
    payload = {
        "text": "URGENT! You have won a 1 week FREE holiday to Spain or 1000 cash! Call 09061701461 to claim your guaranteed prize!"
    }
    response = client.post("/api/spam/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "SPAM"
    assert data["confidence"] >= 0.7
    assert "probabilities" in data
    assert "spam" in data["probabilities"]
    assert "ham" in data["probabilities"]
    total = data["probabilities"]["spam"] + data["probabilities"]["ham"]
    assert math.isclose(total, 1.0, abs_tol=0.01)


def test_ham_legitimate_prediction():
    payload = {
        "text": "Hey are we still meeting up for coffee tomorrow afternoon around 2pm?"
    }
    response = client.post("/api/spam/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "NOT SPAM"
    assert data["confidence"] >= 0.7


def test_spam_empty_input_validation():
    response = client.post("/api/spam/predict", json={"text": ""})
    assert response.status_code == 422

    response = client.post("/api/spam/predict", json={"text": "   "})
    assert response.status_code == 422


def test_spam_metrics_endpoint():
    response = client.get("/api/spam/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "accuracy" in data["metrics"]
    assert data["metrics"]["accuracy"] > 0.95
    assert "confusion_matrix" in data


if __name__ == "__main__":
    print("Running Spam backend tests with TestClient...")
    test_spam_positive_prediction()
    print("[PASS] Spam message prediction passed")
    test_ham_legitimate_prediction()
    print("[PASS] Ham legitimate message prediction passed")
    test_spam_empty_input_validation()
    print("[PASS] Empty input validation passed")
    test_spam_metrics_endpoint()
    print("[PASS] Spam metrics endpoint passed")
    print("All Spam backend tests PASSED successfully!")
