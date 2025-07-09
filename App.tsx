import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, BarChart3, MessageSquare, Brain, Github, AlertTriangle, Zap } from 'lucide-react';
import SentimentChart from './components/SentimentChart';
import ConversationInput from './components/ConversationInput';
import DriftAnalytics from './components/DriftAnalytics';
import Header from './components/Header';

export interface Message {
  id: string;
  text: string;
  timestamp: number;
  sentiment: number;
  confidence: number;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentDrift, setCurrentDrift] = useState(0);
  const [averageSentiment, setAverageSentiment] = useState(0);

  // Calculate sentiment drift and average
  useEffect(() => {
    if (messages.length < 2) return;

    const recent = messages.slice(-5);
    const earlier = messages.slice(-10, -5);
    
    if (earlier.length === 0) return;

    const recentAvg = recent.reduce((sum, msg) => sum + msg.sentiment, 0) / recent.length;
    const earlierAvg = earlier.reduce((sum, msg) => sum + msg.sentiment, 0) / earlier.length;
    
    setCurrentDrift(recentAvg - earlierAvg);
    setAverageSentiment(messages.reduce((sum, msg) => sum + msg.sentiment, 0) / messages.length);
  }, [messages]);

  const addMessage = (text: string) => {
    // Simple sentiment analysis simulation
    const sentiment = analyzeSentiment(text);
    const confidence = Math.random() * 0.3 + 0.7; // 70-100% confidence
    
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      timestamp: Date.now(),
      sentiment,
      confidence
    };

    setMessages(prev => [...prev, newMessage]);
  };

  const analyzeSentiment = (text: string): number => {
    // Simple keyword-based sentiment analysis
    const positiveWords = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'perfect', 'awesome', 'brilliant'];
    const negativeWords = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointed', 'frustrated', 'angry', 'sad'];
    
    const words = text.toLowerCase().split(/\s+/);
    let score = 0;

    words.forEach(word => {
      if (positiveWords.includes(word)) score += 0.1;
      if (negativeWords.includes(word)) score -= 0.1;
    });

    // Add some randomness for demonstration
    score += (Math.random() - 0.5) * 0.3;
    
    return Math.max(-1, Math.min(1, score));
  };

  const clearHistory = () => {
    setMessages([]);
    setCurrentDrift(0);
    setAverageSentiment(0);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4 rounded-2xl shadow-lg">
              <Brain className="h-8 w-8 text-white" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Sentiment Drift Tracker
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Monitor and analyze emotional changes in GenAI conversations to better understand user sentiment patterns and drift over time.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <MessageSquare className="h-8 w-8 text-blue-500" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Messages</p>
                <p className="text-2xl font-bold text-gray-900">{messages.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BarChart3 className="h-8 w-8 text-green-500" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Average Sentiment</p>
                <p className="text-2xl font-bold text-gray-900">
                  {averageSentiment.toFixed(2)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                {currentDrift > 0 ? (
                  <TrendingUp className="h-8 w-8 text-green-500" />
                ) : currentDrift < 0 ? (
                  <TrendingDown className="h-8 w-8 text-red-500" />
                ) : (
                  <Zap className="h-8 w-8 text-yellow-500" />
                )}
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Current Drift</p>
                <p className={`text-2xl font-bold ${
                  currentDrift > 0 ? 'text-green-600' : 
                  currentDrift < 0 ? 'text-red-600' : 'text-gray-600'
                }`}>
                  {currentDrift > 0 ? '+' : ''}{currentDrift.toFixed(2)}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Input and Chart */}
          <div className="lg:col-span-2 space-y-8">
            <ConversationInput onAddMessage={addMessage} onClear={clearHistory} />
            <SentimentChart messages={messages} />
          </div>

          {/* Right Column - Analytics */}
          <div className="space-y-8">
            <DriftAnalytics messages={messages} currentDrift={currentDrift} />
            
            {/* Recent Messages */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Messages</h3>
              <div className="space-y-3 max-h-64 overflow-y-auto">
                {messages.slice(-5).reverse().map((message) => (
                  <div key={message.id} className="p-3 rounded-lg bg-gray-50 border border-gray-100">
                    <p className="text-sm text-gray-700 mb-2">{message.text}</p>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>Sentiment: {message.sentiment.toFixed(2)}</span>
                      <span className={`px-2 py-1 rounded-full ${
                        message.sentiment > 0.3 ? 'bg-green-100 text-green-700' :
                        message.sentiment < -0.3 ? 'bg-red-100 text-red-700' :
                        'bg-yellow-100 text-yellow-700'
                      }`}>
                        {message.sentiment > 0.3 ? 'Positive' :
                         message.sentiment < -0.3 ? 'Negative' : 'Neutral'}
                      </span>
                    </div>
                  </div>
                ))}
                {messages.length === 0 && (
                  <p className="text-gray-500 text-center py-8">
                    No messages yet. Start a conversation to see sentiment analysis.
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* GitHub Integration Info */}
        <div className="mt-12 bg-gradient-to-r from-gray-900 to-blue-900 rounded-2xl p-8 text-white">
          <div className="flex items-start space-x-4">
            <Github className="h-8 w-8 text-blue-300 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-xl font-bold mb-2">Python Package Structure</h3>
              <p className="text-blue-100 mb-4">
                This web demo showcases the sentiment drift concept. For production use, implement the Python package with the following structure:
              </p>
              <div className="bg-black/30 rounded-lg p-4 font-mono text-sm text-green-300">
                <div>user-sentidrift/</div>
                <div className="ml-2">├── user_sentidrift/</div>
                <div className="ml-4">│   ├── tracker.py</div>
                <div className="ml-4">│   ├── sentiment.py</div>
                <div className="ml-4">│   └── drift.py</div>
                <div className="ml-2">├── examples/</div>
                <div className="ml-2">├── tests/</div>
                <div className="ml-2">└── README.md</div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;