# shared/models/sentiment_models.py
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from enum import Enum

class EmotionType(str, Enum):
    JOY = "joy"
    ANGER = "anger"  
    SADNESS = "sadness"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"

class SentimentScore(BaseModel):
    session_id: str
    message_id: str
    timestamp: datetime
    overall_sentiment: float  # -1.0 to 1.0
    confidence: float        # 0.0 to 1.0
    emotions: Dict[EmotionType, float]
    linguistic_features: Dict[str, Any]
    model_version: str
    
class DriftDetection(BaseModel):
    session_id: str
    timestamp: datetime
    drift_magnitude: float
    drift_direction: str     # "positive", "negative", "stable"
    confidence: float
    window_analyzed: int
    detection_method: str
    recommended_action: str

class Session(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    start_time: datetime
    last_activity: datetime
    sentiment_history: List[SentimentScore] = []
    drift_events: List[DriftDetection] = []
    metadata: Dict[str, Any] = {}
