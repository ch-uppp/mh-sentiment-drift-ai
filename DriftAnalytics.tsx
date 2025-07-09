import React from 'react';
import { AlertTriangle, TrendingUp, TrendingDown, BarChart3, CheckCircle } from 'lucide-react';
import { Message } from '../App';

interface DriftAnalyticsProps {
  messages: Message[];
  currentDrift: number;
}

const DriftAnalytics: React.FC<DriftAnalyticsProps> = ({ messages, currentDrift }) => {
  const getDriftSeverity = () => {
    const absChange = Math.abs(currentDrift);
    if (absChange > 0.5) return 'high';
    if (absChange > 0.2) return 'medium';
    return 'low';
  };

  const getDriftInsight = () => {
    if (messages.length < 5) {
      return "Need more messages to detect meaningful drift patterns.";
    }

    const severity = getDriftSeverity();
    const direction = currentDrift > 0 ? 'positive' : 'negative';
    
    switch (severity) {
      case 'high':
        return `Significant ${direction} sentiment shift detected. This indicates a major change in user experience or perception.`;
      case 'medium':
        return `Moderate ${direction} sentiment drift observed. Monitor closely for continued trends.`;
      default:
        return `Minimal sentiment drift. User sentiment appears stable.`;
    }
  };

  const getAlertLevel = () => {
    const severity = getDriftSeverity();
    if (severity === 'high') return 'error';
    if (severity === 'medium') return 'warning';
    return 'success';
  };

  const alertStyles = {
    error: 'border-red-200 bg-red-50',
    warning: 'border-yellow-200 bg-yellow-50',
    success: 'border-green-200 bg-green-50'
  };

  const alertIconStyles = {
    error: 'text-red-600',
    warning: 'text-yellow-600',
    success: 'text-green-600'
  };

  const alertLevel = getAlertLevel();

  const getStatistics = () => {
    if (messages.length === 0) return null;

    const sentiments = messages.map(m => m.sentiment);
    const positive = sentiments.filter(s => s > 0.3).length;
    const negative = sentiments.filter(s => s < -0.3).length;
    const neutral = sentiments.length - positive - negative;

    return { positive, negative, neutral, total: sentiments.length };
  };

  const stats = getStatistics();

  return (
    <div className="space-y-6">
      {/* Drift Alert */}
      <div className={`border rounded-xl p-4 ${alertStyles[alertLevel]}`}>
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            {alertLevel === 'error' && <AlertTriangle className={`h-5 w-5 ${alertIconStyles[alertLevel]}`} />}
            {alertLevel === 'warning' && <AlertTriangle className={`h-5 w-5 ${alertIconStyles[alertLevel]}`} />}
            {alertLevel === 'success' && <CheckCircle className={`h-5 w-5 ${alertIconStyles[alertLevel]}`} />}
          </div>
          <div>
            <h3 className={`text-sm font-medium ${
              alertLevel === 'error' ? 'text-red-800' :
              alertLevel === 'warning' ? 'text-yellow-800' :
              'text-green-800'
            }`}>
              Drift Analysis
            </h3>
            <p className={`mt-1 text-sm ${
              alertLevel === 'error' ? 'text-red-700' :
              alertLevel === 'warning' ? 'text-yellow-700' :
              'text-green-700'
            }`}>
              {getDriftInsight()}
            </p>
          </div>
        </div>
      </div>

      {/* Statistics */}
      {stats && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <BarChart3 className="h-5 w-5 mr-2 text-blue-500" />
            Sentiment Distribution
          </h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Positive</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(stats.positive / stats.total) * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-gray-900 w-8 text-right">
                  {stats.positive}
                </span>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Neutral</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-yellow-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(stats.neutral / stats.total) * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-gray-900 w-8 text-right">
                  {stats.neutral}
                </span>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Negative</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-red-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(stats.negative / stats.total) * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-gray-900 w-8 text-right">
                  {stats.negative}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Drift Metrics */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Drift Metrics</h3>
        
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Current Drift</span>
            <span className={`text-sm font-medium ${
              currentDrift > 0 ? 'text-green-600' : 
              currentDrift < 0 ? 'text-red-600' : 'text-gray-600'
            }`}>
              {currentDrift > 0 ? '+' : ''}{currentDrift.toFixed(3)}
            </span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Drift Magnitude</span>
            <span className="text-sm font-medium text-gray-900">
              {Math.abs(currentDrift).toFixed(3)}
            </span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Alert Level</span>
            <span className={`text-sm font-medium capitalize ${
              alertLevel === 'error' ? 'text-red-600' :
              alertLevel === 'warning' ? 'text-yellow-600' :
              'text-green-600'
            }`}>
              {getDriftSeverity()}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DriftAnalytics;