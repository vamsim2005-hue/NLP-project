from fastapi import APIRouter, HTTPException
from backend.app.schemas.prediction import TextRequest, SentimentPredictionResponse
from backend.app.services.sentiment_service import sentiment_service

router = APIRouter(prefix="/sentiment", tags=["Sentiment Analysis"])


@router.post("/predict", response_model=SentimentPredictionResponse)
def predict_sentiment(request: TextRequest):
    """
    Classify the sentiment of input text into positive or negative,
    with confidence and class probability distribution.
    """
    result = sentiment_service.predict(request.text)
    return result


@router.get("/metrics")
def get_sentiment_metrics():
    """
    Retrieve actual trained model metrics (accuracy, precision, recall, f1, confusion matrix)
    from the serialized evaluation results.
    """
    metrics = sentiment_service.get_metrics()
    if not metrics:
        raise HTTPException(
            status_code=404,
            detail="Sentiment model has not been trained yet."
        )
    return metrics
