# shared/utils/config.py
import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/sentiment_drift"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Services
    SENTIMENT_SERVICE_URL: str = "http://localhost:8001"
    DRIFT_SERVICE_URL: str = "http://localhost:8002" 
    SESSION_SERVICE_URL: str = "http://localhost:8003"
    ADAPTATION_SERVICE_URL: str = "http://localhost:8004"
    
    # ML Models
    MODEL_CACHE_DIR: str = "./models"
    VADER_ENABLED: bool = True
    TRANSFORMER_MODEL: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    
    # API
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Performance  
    MAX_CONCURRENT_REQUESTS: int = 100
    SENTIMENT_ANALYSIS_TIMEOUT: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings()
