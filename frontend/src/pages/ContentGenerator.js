import React, { useState } from 'react';
import { Sparkles, Copy, RefreshCw, Zap, Hash, Target, ArrowRight } from 'lucide-react';
import { contentAPI } from '../services/api';
import toast from 'react-hot-toast';

const ContentGenerator = ({ theme }) => {
  const [formData, setFormData] = useState({
    topic: '',
    count: 5,
    style: 'viral'
  });
  
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('all');

  const styles = [
    { 
      value: 'viral', 
      label: 'Viral', 
      description: 'High engagement, trending',
      icon: Sparkles,
      gradient: 'from-red-500 to-pink-600'
    },
    { 
      value: 'educational', 
      label: 'Educational', 
      description: 'Informative, learning',
      icon: Target,
      gradient: 'from-blue-500 to-cyan-600'
    },
    { 
      value: 'entertaining', 
      label: 'Entertaining', 
      description: 'Fun, engaging',
      icon: Zap,
      gradient: 'from-yellow-500 to-orange-600'
    },
    { 
      value: 'controversial', 
      label: 'Controversial', 
      description: 'Debate, discussion',
      icon: Hash,
      gradient: 'from-purple-500 to-indigo-600'
    }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'count' ? parseInt(value) : value
    }));
  };

  const generateContent = async () => {
    if (!formData.topic.trim()) {
      toast.error('Please enter a topic');
      return;
    }

    setLoading(true);
    try {
      const response = await contentAPI.generateContent(formData);
      setResults(response);
      toast.success(`Generated ${response.titles.length} titles and ${response.hashtags.length} hashtags!`);
    } catch (error) {
      console.error('Generation error:', error);
      toast.error('Failed to generate content. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  const copyAllTitles = () => {
    if (!results?.titles) return;
    const titlesText = results.titles.map(t => t.title).join('\n');
    copyToClipboard(titlesText);
  };

  const copyAllHashtags = () => {
    if (!results?.hashtags) return;
    const hashtagsText = results.hashtags.join(' ');
    copyToClipboard(hashtagsText);
  };

  return (
    <div className="space-y-8 fade-in">
      {/* Header */}
      <div>
        <h1 className={`text-4xl font-bold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
          Content Generator
        </h1>
        <p className={`text-lg ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
          Create viral titles and hashtags with AI-powered content generation
        </p>
      </div>

      {/* Input Form */}
      <div className="premium-card p-8">
        <div className="space-y-6">
          {/* Topic Input */}
          <div className="form-group-premium">
            <label className="form-label-premium">Topic or Theme</label>
            <input
              type="text"
              name="topic"
              value={formData.topic}
              onChange={handleInputChange}
              placeholder="Enter your topic (e.g., cooking, tech, comedy, fitness)..."
              className="input-premium"
              onKeyPress={(e) => e.key === 'Enter' && generateContent()}
            />
          </div>

          {/* Count and Style Selection */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="form-group-premium">
              <label className="form-label-premium">Number of Titles</label>
              <select
                name="count"
                value={formData.count}
                onChange={handleInputChange}
                className="input-premium"
              >
                <option value={3}>3 titles</option>
                <option value={5}>5 titles</option>
                <option value={10}>10 titles</option>
                <option value={15}>15 titles</option>
              </select>
            </div>
          </div>

          {/* Style Selection */}
          <div className="form-group-premium">
            <label className="form-label-premium">Content Style</label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {styles.map((style) => {
                const Icon = style.icon;
                return (
                  <button
                    key={style.value}
                    onClick={() => setFormData(prev => ({ ...prev, style: style.value }))}
                    className={`p-4 rounded-xl border-2 transition-all duration-200 hover:scale-105 ${
                      formData.style === style.value
                        ? `border-blue-500 bg-gradient-to-r ${style.gradient} bg-opacity-10`
                        : theme === 'dark'
                        ? 'border-gray-700 hover:border-gray-600 bg-gray-800/50'
                        : 'border-gray-200 hover:border-gray-300 bg-white/50'
                    }`}
                  >
                    <div className={`w-8 h-8 rounded-lg bg-gradient-to-r ${style.gradient} flex items-center justify-center mb-2`}>
                      <Icon className="w-4 h-4 text-white" />
                    </div>
                    <div className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                      {style.label}
                    </div>
                    <div className={`text-xs ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                      {style.description}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Generate Button */}
          <div className="pt-4">
            <button
              onClick={generateContent}
              disabled={loading || !formData.topic.trim()}
              className="btn-premium w-full disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  <span>Generating...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  <span>Generate Content</span>
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Results */}
      {results && (
        <div className="space-y-6 bounce-in">
          {/* Provider Info */}
          <div className="premium-card p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                  <Zap className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className={`font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                    Generated with {results.provider}
                  </h3>
                  <p className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                    {results.titles.length} titles • {results.hashtags.length} hashtags
                  </p>
                </div>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={copyAllTitles}
                  className="btn-premium-secondary text-sm px-4 py-2"
                >
                  <Copy className="w-4 h-4 mr-2" />
                  Copy All Titles
                </button>
                <button
                  onClick={copyAllHashtags}
                  className="btn-premium-secondary text-sm px-4 py-2"
                >
                  <Hash className="w-4 h-4 mr-2" />
                  Copy Hashtags
                </button>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="premium-card p-6">
            <div className="flex space-x-1 mb-6">
              {['all', 'titles', 'hashtags'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                    activeTab === tab
                      ? 'bg-blue-600 text-white'
                      : theme === 'dark'
                      ? 'text-gray-400 hover:text-white hover:bg-gray-800'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>

            {/* Titles */}
            {(activeTab === 'all' || activeTab === 'titles') && results.titles && (
              <div className="space-y-4">
                <h3 className={`text-lg font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                  Generated Titles
                </h3>
                <div className="grid gap-4">
                  {results.titles.map((title, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-xl border transition-all duration-200 hover:scale-[1.02] ${
                        theme === 'dark'
                          ? 'bg-gray-800/50 border-gray-700 hover:border-gray-600'
                          : 'bg-white/50 border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <p className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                            {title.title}
                          </p>
                          <div className="flex items-center mt-2 space-x-4">
                            <span className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                              Viral Score: <span className="font-medium text-green-600 dark:text-green-400">{title.viral_score}</span>
                            </span>
                          </div>
                        </div>
                        <button
                          onClick={() => copyToClipboard(title.title)}
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
            )}

            {/* Hashtags */}
            {(activeTab === 'all' || activeTab === 'hashtags') && results.hashtags && (
              <div className="space-y-4 mt-8">
                <h3 className={`text-lg font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                  Generated Hashtags
                </h3>
                <div className="flex flex-wrap gap-2">
                  {results.hashtags.map((hashtag, index) => (
                    <button
                      key={index}
                      onClick={() => copyToClipboard(hashtag)}
                      className={`px-3 py-2 rounded-lg font-medium transition-all duration-200 hover:scale-105 ${
                        theme === 'dark'
                          ? 'bg-gray-800 border border-gray-700 text-gray-300 hover:bg-gray-700 hover:border-gray-600'
                          : 'bg-gray-100 border border-gray-200 text-gray-700 hover:bg-gray-200 hover:border-gray-300'
                      }`}
                    >
                      {hashtag}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ContentGenerator;
