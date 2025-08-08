# services/sentiment-analysis/src/main.py
from fastapi import FastAPI
from .api.routes import router
import uvicorn

app = FastAPI(
    title="Sentiment Analysis Service",
    description="Real-time sentiment analysis for drift detection",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
