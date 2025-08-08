# services/sentiment-analysis/src/api/schemas.py
from pydantic import BaseModel
from typing import Dict, Optional, Any
from datetime import datetime

class SentimentAnalysisRequest(BaseModel):
    session_id: str
    message: str
    context: Optional[str] = None
    user_id: Optional[str] = None

class SentimentAnalysisResponse(BaseModel):
    session_id: str
    message_id: str
    timestamp: datetime
    overall_sentiment: float
    confidence: float
    emotions: Dict[str, float]
    linguistic_features: Dict[str, Any]
    model_version: str
    processing_time_ms: float
