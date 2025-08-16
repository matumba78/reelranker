import React, { useState } from 'react';
import { BarChart3, Target, RefreshCw, Copy, ArrowRight, TrendingUp as TrendingIcon } from 'lucide-react';
import { contentAPI } from '../services/api';
import toast from 'react-hot-toast';

const TopicAnalyzer = ({ theme }) => {
  const [topic, setTopic] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeTopic = async () => {
    if (!topic.trim()) {
      toast.error('Please enter a topic to analyze');
      return;
    }

    setLoading(true);
    try {
      const response = await contentAPI.analyzeTopic({
        topic: topic,
        count: 10
      });
      setAnalysis(response);
      toast.success('Topic analysis completed!');
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error('Failed to analyze topic. Please try again.');
      // Mock data for demo
      setAnalysis({
        top_tags: [
          { tag: 'Cooking', score: 0.9 },
          { tag: 'Recipe', score: 0.8 },
          { tag: 'Food', score: 0.7 },
          { tag: 'Kitchen', score: 0.6 },
          { tag: 'Chef', score: 0.5 }
        ],
        top_hashtags: [
          { hashtag: '#Cooking', score: 0.9 },
          { hashtag: '#Recipe', score: 0.8 },
          { hashtag: '#Food', score: 0.7 },
          { hashtag: '#Kitchen', score: 0.6 },
          { hashtag: '#Chef', score: 0.5 }
        ],
        viral_patterns: [
          'The Shocking Truth About {topic}',
          'Why {topic} is Going Viral',
          'How {topic} Changed Everything'
        ],
        trending_keywords: ['cooking', 'recipe', 'food', 'kitchen', 'chef']
      });
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  return (
    <div className="space-y-8 fade-in">
      {/* Header */}
      <div>
        <h1 className={`text-4xl font-bold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
          Topic Analyzer
        </h1>
        <p className={`text-lg ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
          Get insights and trends for your content topics with AI-powered analysis
        </p>
      </div>

      {/* Input Form */}
      <div className="premium-card p-8">
        <div className="flex flex-col lg:flex-row space-y-4 lg:space-y-0 lg:space-x-4">
          <div className="flex-1">
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter a topic to analyze (e.g., cooking, tech, comedy, fitness)..."
              className="input-premium"
              onKeyPress={(e) => e.key === 'Enter' && analyzeTopic()}
            />
          </div>
          <button
            onClick={analyzeTopic}
            disabled={loading || !topic.trim()}
            className="btn-premium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 lg:w-auto"
          >
            {loading ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <BarChart3 className="w-5 h-5" />
                <span>Analyze Topic</span>
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Results */}
      {analysis && (
        <div className="space-y-6 bounce-in">
          {/* Top Tags */}
          <div className="premium-card p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className={`text-xl font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                Top Tags
              </h3>
              <button
                onClick={() => copyToClipboard(analysis.top_tags.map(t => t.tag).join(', '))}
                className={`p-2 rounded-lg transition-all duration-200 hover:scale-110 ${
                  theme === 'dark'
                    ? 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                    : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
                }`}
              >
                <Copy className="w-4 h-4" />
              </button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {analysis.top_tags.map((tag, index) => (
                <div
                  key={index}
                  className={`p-4 rounded-xl border transition-all duration-200 hover:scale-105 ${
                    theme === 'dark'
                      ? 'bg-gray-800/50 border-gray-700 hover:border-gray-600'
                      : 'bg-white/50 border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className={`font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                        {tag.tag}
                      </h4>
                      <p className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                        Relevance Score
                      </p>
                    </div>
                    <div className="text-right">
                      <div className={`text-2xl font-bold ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`}>
                        {(tag.score * 100).toFixed(0)}%
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Top Hashtags */}
          <div className="premium-card p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className={`text-xl font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                Trending Hashtags
              </h3>
              <button
                onClick={() => copyToClipboard(analysis.top_hashtags.map(h => h.hashtag).join(' '))}
                className={`p-2 rounded-lg transition-all duration-200 hover:scale-110 ${
                  theme === 'dark'
                    ? 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                    : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
                }`}
              >
                <Copy className="w-4 h-4" />
              </button>
            </div>
            
            <div className="flex flex-wrap gap-3">
              {analysis.top_hashtags.map((hashtag, index) => (
                <button
                  key={index}
                  onClick={() => copyToClipboard(hashtag.hashtag)}
                  className={`px-4 py-2 rounded-xl font-medium transition-all duration-200 hover:scale-105 ${
                    theme === 'dark'
                      ? 'bg-gray-800 border border-gray-700 text-gray-300 hover:bg-gray-700 hover:border-gray-600'
                      : 'bg-gray-100 border border-gray-200 text-gray-700 hover:bg-gray-200 hover:border-gray-300'
                  }`}
                >
                  {hashtag.hashtag}
                  <span className={`ml-2 text-xs ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                    {(hashtag.score * 100).toFixed(0)}%
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Viral Patterns */}
          <div className="premium-card p-6">
            <h3 className={`text-xl font-semibold mb-6 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
              Viral Title Patterns
            </h3>
            
            <div className="space-y-4">
              {analysis.viral_patterns.map((pattern, index) => (
                <div
                  key={index}
                  className={`p-4 rounded-xl border transition-all duration-200 hover:scale-105 ${
                    theme === 'dark'
                      ? 'bg-gray-800/50 border-gray-700 hover:border-gray-600'
                      : 'bg-white/50 border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <Target className={`w-5 h-5 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
                      <span className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                        {pattern}
                      </span>
                    </div>
                    <button
                      onClick={() => copyToClipboard(pattern)}
                      className={`p-2 rounded-lg transition-all duration-200 hover:scale-110 ${
                        theme === 'dark'
                          ? 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                          : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
                      }`}
                    >
                      <Copy className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Trending Keywords */}
          <div className="premium-card p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className={`text-xl font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                Trending Keywords
              </h3>
              <TrendingIcon className={`w-6 h-6 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
            </div>
            
            <div className="flex flex-wrap gap-2">
              {analysis.trending_keywords.map((keyword, index) => (
                <span
                  key={index}
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    theme === 'dark'
                      ? 'bg-blue-900/30 text-blue-400 border border-blue-500/30'
                      : 'bg-blue-100 text-blue-700 border border-blue-200'
                  }`}
                >
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TopicAnalyzer;
