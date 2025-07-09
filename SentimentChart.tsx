import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { Message } from '../App';

interface SentimentChartProps {
  messages: Message[];
}

const SentimentChart: React.FC<SentimentChartProps> = ({ messages }) => {
  const maxMessages = 20;
  const displayMessages = messages.slice(-maxMessages);

  const getSentimentColor = (sentiment: number) => {
    if (sentiment > 0.3) return 'bg-green-500';
    if (sentiment < -0.3) return 'bg-red-500';
    return 'bg-yellow-500';
  };

  const getSentimentIcon = (sentiment: number) => {
    if (sentiment > 0.3) return <TrendingUp className="h-4 w-4 text-green-600" />;
    if (sentiment < -0.3) return <TrendingDown className="h-4 w-4 text-red-600" />;
    return <Minus className="h-4 w-4 text-yellow-600" />;
  };

  const getBarHeight = (sentiment: number) => {
    // Convert sentiment (-1 to 1) to height (20% to 100%)
    return Math.max(20, (sentiment + 1) * 40 + 20);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-6">Sentiment Timeline</h2>
      
      {displayMessages.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <TrendingUp className="h-12 w-12 mx-auto" />
          </div>
          <p className="text-gray-500">No data to display yet. Add some messages to see the sentiment timeline.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Chart */}
          <div className="flex items-end justify-between h-40 border-b border-gray-100 pb-4">
            {displayMessages.map((message, index) => (
              <div key={message.id} className="flex flex-col items-center space-y-2 flex-1 max-w-[40px]">
                <div className="text-xs text-gray-500 font-medium">
                  {message.sentiment.toFixed(1)}
                </div>
                <div 
                  className={`w-6 rounded-t-md transition-all duration-300 ${getSentimentColor(message.sentiment)}`}
                  style={{ height: `${getBarHeight(message.sentiment)}%` }}
                />
                <div className="text-xs text-gray-400">
                  {index + 1}
                </div>
              </div>
            ))}
          </div>

          {/* Legend */}
          <div className="flex items-center justify-center space-x-8 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded"></div>
              <span className="text-gray-600">Positive ({'>'} 0.3)</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-yellow-500 rounded"></div>
              <span className="text-gray-600">Neutral (-0.3 to 0.3)</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-red-500 rounded"></div>
              <span className="text-gray-600">Negative ({'<'} -0.3)</span>
            </div>
          </div>

          {/* Recent Trend */}
          {displayMessages.length >= 3 && (
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-900 mb-2">Recent Trend</h3>
              <div className="flex items-center space-x-2">
                {getSentimentIcon(displayMessages[displayMessages.length - 1].sentiment)}
                <span className="text-sm text-gray-600">
                  Last 3 messages show{' '}
                  {displayMessages.slice(-3).reduce((sum, msg) => sum + msg.sentiment, 0) / 3 > 0 
                    ? 'positive' 
                    : displayMessages.slice(-3).reduce((sum, msg) => sum + msg.sentiment, 0) / 3 < 0
                    ? 'negative'
                    : 'neutral'} sentiment trend
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SentimentChart;