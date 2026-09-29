from fastapi import APIRouter, HTTPException
from backend.app.schemas.prediction import TextRequest, SpamPredictionResponse
from backend.app.services.spam_service import spam_service

router = APIRouter(prefix="/spam", tags=["Spam Detection"])


@router.post("/predict", response_model=SpamPredictionResponse)
def predict_spam(request: TextRequest):
    """
    Classify input text into SPAM or NOT SPAM,
    with confidence and class probability distribution.
    """
    result = spam_service.predict(request.text)
    return result


@router.get("/metrics")
def get_spam_metrics():
    """
    Retrieve evaluated model metrics for Spam Detection.
    """
    metrics = spam_service.get_metrics()
    if not metrics:
        raise HTTPException(
            status_code=404,
            detail="Spam detection model has not been trained yet."
        )
    return metrics
