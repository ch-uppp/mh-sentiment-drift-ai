# services/sentiment-analysis/src/models/ensemble_analyzer.py
from .vader_analyzer import VADERAnalyzer
from .transformer_analyzer import TransformerAnalyzer
from typing import Dict, List
import numpy as np

class EnsembleAnalyzer:
    def __init__(self):
        self.analyzers = {
            "vader": VADERAnalyzer(),
            "transformer": TransformerAnalyzer()
        }
        self.weights = {"vader": 0.3, "transformer": 0.7}
    
    def analyze(self, text: str) -> Dict[str, any]:
        results = {}
        for name, analyzer in self.analyzers.items():
            try:
                results[name] = analyzer.analyze(text)
            except Exception as e:
                print(f"Error in {name} analyzer: {e}")
                continue
        
        if not results:
            raise Exception("All analyzers failed")
        
        return self._ensemble_results(results, text)
    
    def _ensemble_results(self, results: Dict[str, Dict], text: str) -> Dict[str, any]:
        # Weighted average of sentiment scores
        overall_sentiment = 0
        total_weight = 0
        confidence_scores = []
        
        all_emotions = {"joy": [], "anger": [], "sadness": []}
        
        for analyzer_name, result in results.items():
            weight = self.weights.get(analyzer_name, 1.0)
            overall_sentiment += result["overall_sentiment"] * weight
            total_weight += weight
            confidence_scores.append(result["confidence"])
            
            for emotion, score in result["emotions"].items():
                if emotion in all_emotions:
                    all_emotions[emotion].append(score)
        
        # Calculate final scores
        final_sentiment = overall_sentiment / total_weight if total_weight > 0 else 0
        final_confidence = np.mean(confidence_scores) if confidence_scores else 0
        
        final_emotions = {}
        for emotion, scores in all_emotions.items():
            final_emotions[emotion] = np.mean(scores) if scores else 0
        
        # Extract linguistic features
        linguistic_features = self._extract_linguistic_features(text)
        
        return {
            "overall_sentiment": final_sentiment,
            "confidence": final_confidence,
            "emotions": final_emotions,
            "linguistic_features": linguistic_features,
            "model_version": "ensemble_v1.0"
        }
    
    def _extract_linguistic_features(self, text: str) -> Dict[str, any]:
        sentences = text.split('.')
        words = text.split()
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
            "exclamation_count": text.count('!'),
            "question_count": text.count('?'),
            "caps_ratio": sum(1 for c in text if c.isupper()) / len(text) if text else 0
        }
