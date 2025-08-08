# services/drift-detection/src/detectors/statistical_detector.py
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple
from collections import deque

class StatisticalDriftDetector:
    def __init__(self, window_size: int = 10, threshold: float = 0.3):
        self.window_size = window_size
        self.threshold = threshold
        self.sentiment_history = deque(maxlen=100)  # Keep last 100 scores
    
    def add_sentiment_score(self, score: float) -> None:
        """Add a new sentiment score to history"""
        self.sentiment_history.append(score)
    
    def detect_drift(self, current_score: float) -> Dict[str, any]:
        """Detect if there's significant drift in sentiment"""
        self.add_sentiment_score(current_score)
        
        if len(self.sentiment_history) < self.window_size:
            return {
                "drift_detected": False,
                "drift_magnitude": 0.0,
                "drift_direction": "stable",
                "confidence": 0.0,
                "method": "insufficient_data"
            }
        
        # Get recent window and baseline
        recent_scores = list(self.sentiment_history)[-self.window_size:]
        baseline_scores = list(self.sentiment_history)[:self.window_size]
        
        # Calculate drift using multiple methods
        cusum_result = self._cusum_detection(recent_scores, baseline_scores)
        mean_shift_result = self._mean_shift_detection(recent_scores, baseline_scores)
        trend_result = self._trend_detection(recent_scores)
        
        # Combine results
        return self._combine_results([cusum_result, mean_shift_result, trend_result])
    
    def _cusum_detection(self, recent: List[float], baseline: List[float]) -> Dict[str, any]:
        """CUSUM (Cumulative Sum) change point detection"""
        baseline_mean = np.mean(baseline)
        baseline_std = np.std(baseline) or 0.1  # Avoid division by zero
        
        # Calculate CUSUM
        cusum_pos = 0
        cusum_neg = 0
        max_cusum = 0
        
        for score in recent:
            standardized = (score - baseline_mean) / baseline_std
            cusum_pos = max(0, cusum_pos + standardized - 0.5)
            cusum_neg = max(0, cusum_neg - standardized - 0.5)
            max_cusum = max(max_cusum, cusum_pos, cusum_neg)
        
        drift_detected = max_cusum > self.threshold * 5  # Scale threshold
        drift_direction = "positive" if cusum_pos > cusum_neg else "negative"
        
        return {
            "drift_detected": drift_detected,
            "drift_magnitude": max_cusum / 5,  # Normalize
            "drift_direction": drift_direction if drift_detected else "stable",
            "confidence": min(1.0, max_cusum / 10),
            "method": "cusum"
        }
    
    def _mean_shift_detection(self, recent: List[float], baseline: List[float]) -> Dict[str, any]:
        """Simple mean shift detection"""
        recent_mean = np.mean(recent)
        baseline_mean = np.mean(baseline)
        
        drift_
