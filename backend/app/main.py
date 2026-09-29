import os
import sys
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure project root is in python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.schemas.prediction import HealthResponse
from backend.app.api.sentiment import router as sentiment_router
from backend.app.api.spam import router as spam_router
from backend.app.services.sentiment_service import sentiment_service
from backend.app.services.spam_service import spam_service

app = FastAPI(
    title="NLP Classification Dashboard API",
    description="High-performance FastAPI backend serving classical NLP classifiers for Sentiment, Spam, Fake News, and Toxicity detection.",
    version="1.0.0"
)

# CORS configuration to permit React frontend local dev & Docker environments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Ensure no raw stack traces leak to the client; return friendly error messages.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected server error occurred while processing the request. Please try again later."}
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """
    Health check endpoint returning system status.
    """
    return {"status": "ok"}


# Mount API routers
app.include_router(sentiment_router, prefix="/api")
app.include_router(spam_router, prefix="/api")


@app.get("/api/metrics", tags=["Metrics"])
def get_all_metrics():
    """
    Returns performance metrics of all currently trained and serialized models.
    Un-trained models will display status: 'not_trained'.
    """
    models = []
    
    # 1. Sentiment Analysis
    sentiment_metrics = sentiment_service.get_metrics()
    if sentiment_metrics:
        models.append({
            "task": "sentiment",
            "name": "Sentiment Analysis",
            "status": "ready",
            **sentiment_metrics
        })
    else:
        models.append({
            "task": "sentiment",
            "name": "Sentiment Analysis",
            "status": "not_trained"
        })

    # 2. Spam Detection
    spam_metrics = spam_service.get_metrics()
    if spam_metrics:
        models.append({
            "task": "spam",
            "name": "Spam Detection",
            "status": "ready",
            **spam_metrics
        })
    else:
        models.append({
            "task": "spam",
            "name": "Spam Detection",
            "status": "not_trained"
        })

    # Placeholders for future phases (Fake News, Toxicity)
    for task_key, task_name, algo in [
        ("fake_news", "Fake News Detection", "Logistic Regression"),
        ("toxicity", "Toxic Comment Detection", "Multi-label Logistic Regression")
    ]:
        models.append({
            "task": task_key,
            "name": task_name,
            "algorithm": algo,
            "status": "not_trained",
            "metrics": None
        })

    return {"models": models}
