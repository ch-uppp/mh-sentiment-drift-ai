# services/sentiment-analysis/src/models/vader_analyzer.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict

class VADERAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze(self, text: str) -> Dict[str, float]:
        scores = self.analyzer.polarity_scores(text)
        return {
            "overall_sentiment": scores['compound'],
            "confidence": abs(scores['compound']),
            "emotions": {
                "joy": max(0, scores['pos']),
                "anger": max(0, scores['neg']),
                "sadness": max(0, scores['neg'] * 0.7),  # Rough mapping
            }
        }
