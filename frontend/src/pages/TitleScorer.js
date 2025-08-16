import React, { useState } from 'react';
import { Target, Copy, RefreshCw, AlertCircle, CheckCircle, ArrowRight } from 'lucide-react';
import { scoringAPI } from '../services/api';
import toast from 'react-hot-toast';

const TitleScorer = ({ theme }) => {
  const [formData, setFormData] = useState({
    title: '',
    tags: '',
    hashtags: '',
    topic: ''
  });
  
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [batchMode, setBatchMode] = useState(false);
  const [batchTitles, setBatchTitles] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const scoreTitle = async () => {
    if (!formData.title.trim()) {
      toast.error('Please enter a title');
      return;
    }

    setLoading(true);
    try {
      const data = {
        title: formData.title,
        tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag),
        hashtags: formData.hashtags.split(',').map(tag => tag.trim()).filter(tag => tag),
        topic: formData.topic || null
      };

      const response = await scoringAPI.scoreTitle(data);
      setResults([response]);
      toast.success('Title scored successfully!');
    } catch (error) {
      console.error('Scoring error:', error);
      toast.error('Failed to score title. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const scoreBatch = async () => {
    if (!batchTitles.trim()) {
      toast.error('Please enter titles to score');
      return;
    }

    setLoading(true);
    try {
      const titles = batchTitles.split('\n')
        .map(title => title.trim())
        .filter(title => title)
        .map(title => ({
          title,
          tags: [],
          hashtags: [],
          topic: null
        }));

      const response = await scoringAPI.scoreBatch(titles);
      setResults(response.results);
      toast.success(`Scored ${response.total} titles successfully!`);
    } catch (error) {
      console.error('Batch scoring error:', error);
      toast.error('Failed to score titles. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  const getScoreColor = (score) => {
    if (score >= 8) return 'text-green-600 dark:text-green-400';
    if (score >= 6) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getScoreBg = (score) => {
    if (score >= 8) return 'bg-green-100 dark:bg-green-900/30';
    if (score >= 6) return 'bg-yellow-100 dark:bg-yellow-900/30';
    return 'bg-red-100 dark:bg-red-900/30';
  };

  const getScoreIcon = (score) => {
    if (score >= 8) return <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400" />;
    if (score >= 6) return <AlertCircle className="w-5 h-5 text-yellow-600 dark:text-yellow-400" />;
    return <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400" />;
  };

  return (
    <div className="space-y-8 fade-in">
      {/* Header */}
      <div>
        <h1 className={`text-4xl font-bold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
          Title Scorer
        </h1>
        <p className={`text-lg ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
          Analyze title performance and viral potential with AI-powered scoring
        </p>
      </div>

      {/* Mode Toggle */}
      <div className="premium-card p-6">
        <div className="flex space-x-1 mb-6">
          <button
            onClick={() => setBatchMode(false)}
            className={`px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
              !batchMode
                ? 'bg-blue-600 text-white shadow-lg'
                : theme === 'dark'
                ? 'text-gray-400 hover:text-white hover:bg-gray-800'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
          >
            Single Title
          </button>
          <button
            onClick={() => setBatchMode(true)}
            className={`px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
              batchMode
                ? 'bg-blue-600 text-white shadow-lg'
                : theme === 'dark'
                ? 'text-gray-400 hover:text-white hover:bg-gray-800'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
          >
            Batch Mode
          </button>
        </div>

        {!batchMode ? (
          /* Single Title Form */
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="form-group-premium">
                <label className="form-label-premium">Title</label>
                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  placeholder="Enter your title..."
                  className="input-premium"
                  onKeyPress={(e) => e.key === 'Enter' && scoreTitle()}
                />
              </div>
              <div className="form-group-premium">
                <label className="form-label-premium">Topic (Optional)</label>
                <input
                  type="text"
                  name="topic"
                  value={formData.topic}
                  onChange={handleInputChange}
                  placeholder="e.g., cooking, tech, comedy..."
                  className="input-premium"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="form-group-premium">
                <label className="form-label-premium">Tags (comma-separated)</label>
                <input
                  type="text"
                  name="tags"
                  value={formData.tags}
                  onChange={handleInputChange}
                  placeholder="funny, viral, trending..."
                  className="input-premium"
                />
              </div>
              <div className="form-group-premium">
                <label className="form-label-premium">Hashtags (comma-separated)</label>
                <input
                  type="text"
                  name="hashtags"
                  value={formData.hashtags}
                  onChange={handleInputChange}
                  placeholder="#funny, #viral, #trending..."
                  className="input-premium"
                />
              </div>
            </div>

            <div className="pt-4">
              <button
                onClick={scoreTitle}
                disabled={loading || !formData.title.trim()}
                className="btn-premium w-full disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-5 h-5 animate-spin" />
                    <span>Scoring...</span>
                  </>
                ) : (
                  <>
                    <Target className="w-5 h-5" />
                    <span>Score Title</span>
                    <ArrowRight className="w-5 h-5" />
                  </>
                )}
              </button>
            </div>
          </div>
        ) : (
          /* Batch Mode Form */
          <div className="space-y-6">
            <div className="form-group-premium">
              <label className="form-label-premium">Titles (one per line)</label>
              <textarea
                value={batchTitles}
                onChange={(e) => setBatchTitles(e.target.value)}
                placeholder="Enter titles, one per line...&#10;The Shocking Truth About Cooking&#10;Why This Video Went Viral&#10;Amazing Life Hack You Need to See"
                className="input-premium min-h-[200px] resize-none"
              />
            </div>

            <div className="pt-4">
              <button
                onClick={scoreBatch}
                disabled={loading || !batchTitles.trim()}
                className="btn-premium w-full disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-5 h-5 animate-spin" />
                    <span>Scoring Batch...</span>
                  </>
                ) : (
                  <>
                    <Target className="w-5 h-5" />
                    <span>Score All Titles</span>
                    <ArrowRight className="w-5 h-5" />
                  </>
                )}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Results */}
      {results && (
        <div className="space-y-6 bounce-in">
          <div className="premium-card p-6">
            <h3 className={`text-xl font-semibold mb-6 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
              Scoring Results
            </h3>
            
            <div className="space-y-4">
              {results.map((result, index) => (
                <div
                  key={index}
                  className={`p-6 rounded-xl border transition-all duration-200 hover:scale-[1.02] ${
                    theme === 'dark'
                      ? 'bg-gray-800/50 border-gray-700 hover:border-gray-600'
                      : 'bg-white/50 border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-3">
                        {getScoreIcon(result.viral_score)}
                        <h4 className={`font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                          {result.title}
                        </h4>
                      </div>
                      
                      <div className="flex items-center space-x-6 mb-4">
                        <div className={`px-3 py-1 rounded-full ${getScoreBg(result.viral_score)}`}>
                          <span className={`font-bold text-lg ${getScoreColor(result.viral_score)}`}>
                            {result.viral_score}/10
                          </span>
                        </div>
                        <span className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                          Viral Score
                        </span>
                      </div>

                      {result.reasons && result.reasons.length > 0 && (
                        <div className="mb-4">
                          <h5 className={`text-sm font-medium mb-2 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>
                            Analysis:
                          </h5>
                          <ul className="space-y-1">
                            {result.reasons.map((reason, idx) => (
                              <li key={idx} className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                                • {reason}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {result.suggestions && result.suggestions.length > 0 && (
                        <div>
                          <h5 className={`text-sm font-medium mb-2 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>
                            Suggestions:
                          </h5>
                          <ul className="space-y-1">
                            {result.suggestions.map((suggestion, idx) => (
                              <li key={idx} className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                                • {suggestion}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                    
                    <button
                      onClick={() => copyToClipboard(result.title)}
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
        </div>
      )}
    </div>
  );
};

export default TitleScorer;
