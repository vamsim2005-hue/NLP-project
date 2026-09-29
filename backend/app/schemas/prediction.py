from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(..., description="The raw input text to classify")

    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Input text cannot be empty or contain only whitespace.")
        if len(v) > 100000:
            raise ValueError("Input text exceeds the maximum allowed length of 100,000 characters.")
        return v


class SentimentPredictionResponse(BaseModel):
    prediction: str = Field(..., description="Predicted sentiment class (positive or negative)")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")
    probabilities: Dict[str, float] = Field(..., description="Class probability distribution")


class SpamPredictionResponse(BaseModel):
    prediction: str = Field(..., description="Predicted label (SPAM or NOT SPAM)")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")
    probabilities: Dict[str, float] = Field(..., description="Probability distribution between ham and spam")


class HealthResponse(BaseModel):
    status: str = Field(..., example="ok")
