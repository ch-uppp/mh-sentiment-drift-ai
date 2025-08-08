# services/sentiment-analysis/src/api/routes.py
from fastapi import APIRouter, HTTPException, Depends
from .schemas import SentimentAnalysisRequest, SentimentAnalysisResponse
from ..models.ensemble_analyzer import EnsembleAnalyzer
import time
import uuid
from datetime import datetime

router = APIRouter(prefix="/sentiment", tags=["sentiment"])

# Global analyzer instance
analyzer = EnsembleAnalyzer()

@router.post("/analyze", response_model=SentimentAnalysisResponse)
async def analyze_sentiment(request: SentimentAnalysisRequest):
    start_time = time.time()
    
    try:
        # Analyze sentiment
        result = analyzer.analyze(request.message)
        
        # Create response
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        response = SentimentAnalysisResponse(
            session_id=request.session_id,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            overall_sentiment=result["overall_sentiment"],
            confidence=result["confidence"], 
            emotions=result["emotions"],
            linguistic_features=result["linguistic_features"],
            model_version=result["model_version"],
            processing_time_ms=processing_time
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "sentiment-analysis"}
