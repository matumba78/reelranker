import axios from 'axios';

// API base URL - uses environment variable in production
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging and authentication
apiClient.interceptors.request.use(
  (config) => {
    // Log requests in development only
    if (process.env.NODE_ENV === 'development') {
      console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    }
    
    // Add authentication token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Add request timestamp for performance monitoring
    config.metadata = { startTime: new Date() };
    
    return config;
  },
  (error) => {
    if (process.env.NODE_ENV === 'development') {
      console.error('❌ Request Error:', error);
    }
    return Promise.reject(error);
  }
);

// Response interceptor for error handling and logging
apiClient.interceptors.response.use(
  (response) => {
    // Log responses in development only
    if (process.env.NODE_ENV === 'development') {
      const duration = new Date() - response.config.metadata.startTime;
      console.log(`✅ API Response: ${response.status} ${response.config.url} (${duration}ms)`);
    }
    return response;
  },
  (error) => {
    // Enhanced error handling
    if (error.response) {
      // Server responded with error status
      if (process.env.NODE_ENV === 'development') {
        console.error('❌ API Error:', {
          status: error.response.status,
          url: error.config?.url,
          message: error.response.data?.detail || error.response.data?.message || 'Unknown error',
        });
      }
      
      // Handle specific error cases
      if (error.response.status === 401) {
        // Unauthorized - redirect to login
        localStorage.removeItem('auth_token');
        window.location.href = '/login';
      } else if (error.response.status === 429) {
        // Rate limited
        if (process.env.NODE_ENV === 'development') {
          console.warn('⚠️ Rate limited - please wait before making more requests');
        }
      }
    } else if (error.request) {
      // Network error
      if (process.env.NODE_ENV === 'development') {
        console.error('❌ Network Error:', error.message);
      }
    } else {
      // Other error
      if (process.env.NODE_ENV === 'development') {
        console.error('❌ Error:', error.message);
      }
    }
    
    return Promise.reject(error);
  }
);

// API endpoints
export const contentAPI = {
  // Generate viral content
  generateContent: async (data) => {
    const response = await apiClient.post('/api/v1/generate', data);
    return response.data;
  },
  
  // Analyze topic
  analyzeTopic: async (topic) => {
    const response = await apiClient.post('/api/v1/generate/analyze-topic', { topic });
    return response.data;
  },
  
  // Generate hashtags
  generateHashtags: async (data) => {
    const response = await apiClient.post('/api/v1/generate/hashtags', data);
    return response.data;
  },
};

export const scoringAPI = {
  // Score single title
  scoreTitle: async (title) => {
    const response = await apiClient.post('/api/v1/score', { title });
    return response.data;
  },
  
  // Score multiple titles
  scoreTitles: async (titles) => {
    const response = await apiClient.post('/api/v1/score/batch', { titles });
    return response.data;
  },
};

export const youtubeAPI = {
  // Get trending shorts
  getTrendingShorts: async (params = {}) => {
    const response = await apiClient.get('/api/v1/shorts/trending', { params });
    return response.data;
  },
  
  // Search shorts
  searchShorts: async (query, params = {}) => {
    const response = await apiClient.get('/api/v1/shorts/search', { 
      params: { query, ...params } 
    });
    return response.data;
  },
  
  // Get video details
  getVideoDetails: async (videoId) => {
    const response = await apiClient.get(`/api/v1/shorts/video/${videoId}`);
    return response.data;
  },
};

export const topicsAPI = {
  // Get trending topics
  getTrendingTopics: async () => {
    const response = await apiClient.get('/api/v1/topics/trending');
    return response.data;
  },
  
  // Get topic analysis
  getTopicAnalysis: async (topic) => {
    const response = await apiClient.get(`/api/v1/topics/analysis/${encodeURIComponent(topic)}`);
    return response.data;
  },
};

export const trendsAPI = {
  // Get viral trends
  getViralTrends: async () => {
    const response = await apiClient.get('/api/v1/trends/viral');
    return response.data;
  },
  
  // Get trend analysis
  getTrendAnalysis: async (trend) => {
    const response = await apiClient.get(`/api/v1/trends/analysis/${encodeURIComponent(trend)}`);
    return response.data;
  },
};

export const healthAPI = {
  // Check API health
  checkHealth: async () => {
    try {
      const response = await apiClient.get('/health');
      return { status: 'healthy', data: response.data };
    } catch (error) {
      return { status: 'unhealthy', error: error.message };
    }
  },
  
  // Get API status
  getStatus: async () => {
    const response = await apiClient.get('/api/v1/status');
    return response.data;
  },
};

// Export the axios instance for custom requests
export default apiClient;
