# services/sentiment-analysis/src/models/transformer_analyzer.py
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict

class TransformerAnalyzer:
    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.pipeline = pipeline("sentiment-analysis", 
                                model=self.model, 
                                tokenizer=self.tokenizer,
                                device=0 if torch.cuda.is_available() else -1)
    
    def analyze(self, text: str) -> Dict[str, float]:
        results = self.pipeline(text, top_k=None)
        
        # Convert to standardized format
        sentiment_map = {"NEGATIVE": -1, "NEUTRAL": 0, "POSITIVE": 1}
        overall_sentiment = 0
        confidence = 0
        
        for result in results:
            label = result['label']
            score = result['score']
            if label in sentiment_map:
                overall_sentiment += sentiment_map[label] * score
                confidence = max(confidence, score)
        
        return {
            "overall_sentiment": max(-1, min(1, overall_sentiment)),
            "confidence": confidence,
            "emotions": self._extract_emotions(results)
        }
    
    def _extract_emotions(self, results) -> Dict[str, float]:
        # Simple mapping - in production you'd use emotion-specific models
        emotion_map = {
            "NEGATIVE": {"anger": 0.6, "sadness": 0.4},
            "POSITIVE": {"joy": 1.0},
            "NEUTRAL": {}
        }
        
        emotions = {"joy": 0.0, "anger": 0.0, "sadness": 0.0}
        for result in results:
            if result['label'] in emotion_map:
                for emotion, weight in emotion_map[result['label']].items():
                    emotions[emotion] += result['score'] * weight
        
        return emotions
