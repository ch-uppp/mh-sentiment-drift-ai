import React, { useState } from 'react';
import { Send, Trash2, MessageSquare } from 'lucide-react';

interface ConversationInputProps {
  onAddMessage: (text: string) => void;
  onClear: () => void;
}

const ConversationInput: React.FC<ConversationInputProps> = ({ onAddMessage, onClear }) => {
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sampleMessages = [
    "I love this new feature! It's working perfectly.",
    "This is getting frustrating. Nothing seems to work properly.",
    "The interface is okay, but could be better.",
    "Absolutely amazing! This exceeded my expectations.",
    "I'm having issues with the login process again.",
    "Great improvement from the last version. Keep it up!",
    "This is terrible. I want my money back.",
    "Not bad, but there's definitely room for improvement."
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    setIsLoading(true);
    
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    onAddMessage(inputText);
    setInputText('');
    setIsLoading(false);
  };

  const addSampleMessage = () => {
    const randomMessage = sampleMessages[Math.floor(Math.random() * sampleMessages.length)];
    onAddMessage(randomMessage);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900 flex items-center">
          <MessageSquare className="h-5 w-5 mr-2 text-blue-500" />
          Add Conversation Message
        </h2>
        <button
          onClick={onClear}
          className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-md transition-colors"
        >
          <Trash2 className="h-4 w-4" />
          <span>Clear History</span>
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter a message to analyze sentiment..."
            className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none transition-shadow"
            rows={3}
            disabled={isLoading}
          />
        </div>
        
        <div className="flex items-center justify-between">
          <button
            type="button"
            onClick={addSampleMessage}
            className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-700 hover:bg-gray-50 rounded-md border border-gray-200 transition-colors"
          >
            Add Sample Message
          </button>
          
          <button
            type="submit"
            disabled={!inputText.trim() || isLoading}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            ) : (
              <Send className="h-4 w-4 mr-2" />
            )}
            {isLoading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ConversationInput;