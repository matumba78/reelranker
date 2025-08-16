import React, { useState, useEffect } from 'react';
import { TrendingUp, Search, Play, Eye, Heart, MessageCircle, Share2, RefreshCw } from 'lucide-react';
import { youtubeAPI } from '../services/api';
import toast from 'react-hot-toast';

const TrendingShorts = ({ theme }) => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [searching, setSearching] = useState(false);
  const [sortBy, setSortBy] = useState('views');

  useEffect(() => {
    loadTrendingShorts();
  }, []);

  const loadTrendingShorts = async () => {
    setLoading(true);
    try {
      const response = await youtubeAPI.getTrendingShorts();
      setVideos(response.videos || []);
    } catch (error) {
      console.error('Failed to load trending shorts:', error);
      toast.error('Failed to load trending shorts');
      // Mock data for demo
      setVideos([
        {
          video_id: 'demo1',
          title: 'The Shocking Truth About Cooking!',
          channel_title: 'Cooking Master',
          views: '2.1M',
          likes: '45K',
          comments: '1.2K',
          thumbnail_url: 'https://via.placeholder.com/300x400/FF6B6B/FFFFFF?text=Cooking',
          engagement_rate: 0.085,
          duration: '0:45'
        },
        {
          video_id: 'demo2',
          title: 'Why This Cat Video Went Viral!',
          channel_title: 'Pet Lovers',
          views: '5.3M',
          likes: '89K',
          comments: '2.8K',
          thumbnail_url: 'https://via.placeholder.com/300x400/4ECDC4/FFFFFF?text=Cats',
          engagement_rate: 0.092,
          duration: '0:32'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const searchShorts = async () => {
    if (!searchQuery.trim()) {
      toast.error('Please enter a search query');
      return;
    }

    setSearching(true);
    try {
      const response = await youtubeAPI.searchShorts(searchQuery);
      setVideos(response.videos || []);
      toast.success(`Found ${response.videos?.length || 0} videos`);
    } catch (error) {
      console.error('Search failed:', error);
      toast.error('Search failed. Please try again.');
    } finally {
      setSearching(false);
    }
  };

  const formatNumber = (num) => {
    if (!num && num !== 0) return '0';
    if (typeof num === 'string') return num;
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const sortedVideos = [...videos].sort((a, b) => {
    switch (sortBy) {
      case 'views':
        return (parseInt(b.views) || 0) - (parseInt(a.views) || 0);
      case 'likes':
        return (parseInt(b.likes) || 0) - (parseInt(a.likes) || 0);
      case 'engagement':
        return (b.engagement_rate || 0) - (a.engagement_rate || 0);
      default:
        return 0;
    }
  });

  return (
    <div className="space-y-8 fade-in">
      {/* Header */}
      <div>
        <h1 className={`text-4xl font-bold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
          Trending Shorts
        </h1>
        <p className={`text-lg ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
          Discover viral content and trending topics from YouTube Shorts
        </p>
      </div>

      {/* Search and Filters */}
      <div className="premium-card p-6">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search for trending shorts..."
                className="input-premium pr-12"
                onKeyPress={(e) => e.key === 'Enter' && searchShorts()}
              />
              <button
                onClick={searchShorts}
                disabled={searching}
                className={`absolute right-3 top-1/2 transform -translate-y-1/2 p-2 rounded-lg transition-all duration-200 ${
                  theme === 'dark'
                    ? 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                    : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
                }`}
              >
                {searching ? (
                  <RefreshCw className="w-4 h-4 animate-spin" />
                ) : (
                  <Search className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className={`px-4 py-3 rounded-xl border transition-all duration-200 ${
                theme === 'dark'
                  ? 'bg-gray-800 border-gray-600 text-white'
                  : 'bg-white border-gray-300 text-gray-900'
              }`}
            >
              <option value="views">Sort by Views</option>
              <option value="likes">Sort by Likes</option>
              <option value="engagement">Sort by Engagement</option>
            </select>
            
            <button
              onClick={loadTrendingShorts}
              className={`p-3 rounded-xl transition-all duration-200 hover:scale-110 ${
                theme === 'dark'
                  ? 'bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700'
                  : 'bg-gray-100 hover:bg-gray-200 text-gray-600 border border-gray-200'
              }`}
            >
              <RefreshCw className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Videos Grid */}
      {loading ? (
        <div className="premium-card p-12">
          <div className="flex items-center justify-center">
            <div className="loading-premium"></div>
            <span className={`ml-3 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
              Loading trending shorts...
            </span>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {sortedVideos.map((video, index) => (
            <div
              key={video.video_id}
              className={`premium-card premium-card-hover overflow-hidden slide-up`}
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Thumbnail */}
              <div className="relative">
                <img
                  src={video.thumbnail_url}
                  alt={video.title}
                  className="w-full h-48 object-cover"
                />
                <div className="absolute inset-0 bg-black/20 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-200">
                  <button className="w-12 h-12 bg-white/90 rounded-full flex items-center justify-center hover:scale-110 transition-transform duration-200">
                    <Play className="w-6 h-6 text-gray-900 ml-1" />
                  </button>
                </div>
                <div className="absolute top-2 right-2 bg-black/80 text-white text-xs px-2 py-1 rounded">
                  {video.duration}
                </div>
              </div>

              {/* Content */}
              <div className="p-4">
                <h3 className={`font-semibold mb-2 line-clamp-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                  {video.title}
                </h3>
                
                <p className={`text-sm mb-3 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                  {video.channel_title}
                </p>

                {/* Stats */}
                <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
                  <div className="flex items-center space-x-3">
                    <div className="flex items-center space-x-1">
                      <Eye className="w-3 h-3" />
                      <span>{formatNumber(video.views)}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Heart className="w-3 h-3" />
                      <span>{formatNumber(video.likes)}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <MessageCircle className="w-3 h-3" />
                      <span>{formatNumber(video.comments)}</span>
                    </div>
                  </div>
                </div>

                {/* Engagement Rate */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className={`w-2 h-2 rounded-full ${
                      (video.engagement_rate || 0) > 0.05 ? 'bg-green-500' :
                      (video.engagement_rate || 0) > 0.02 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}></div>
                    <span className={`text-xs font-medium ${
                      (video.engagement_rate || 0) > 0.05 ? 'text-green-600 dark:text-green-400' :
                      (video.engagement_rate || 0) > 0.02 ? 'text-yellow-600 dark:text-yellow-400' : 'text-red-600 dark:text-red-400'
                    }`}>
                      {((video.engagement_rate || 0) * 100).toFixed(1)}% engagement
                    </span>
                  </div>
                  
                  <button className={`p-2 rounded-lg transition-all duration-200 hover:scale-110 ${
                    theme === 'dark'
                      ? 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                      : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
                  }`}>
                    <Share2 className="w-3 h-3" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* No Results */}
      {!loading && videos.length === 0 && (
        <div className="premium-card p-12 text-center">
          <TrendingUp className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h3 className={`text-xl font-semibold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
            No videos found
          </h3>
          <p className={`${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
            Try adjusting your search terms or check back later for new trending content.
          </p>
        </div>
      )}
    </div>
  );
};

export default TrendingShorts;
