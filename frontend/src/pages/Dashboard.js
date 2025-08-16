import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Sparkles, 
  Target, 
  TrendingUp, 
  BarChart3, 
  Zap, 
  TrendingUp as TrendingIcon,
  ArrowUpRight,
  CheckCircle
} from 'lucide-react';
import { healthAPI } from '../services/api';


const Dashboard = ({ theme }) => {
  const [healthStatus, setHealthStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const status = await healthAPI.checkHealth();
      setHealthStatus(status);
    } catch (error) {
      console.error('Health check failed:', error);
      setHealthStatus({ status: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      title: 'Generate Content',
      description: 'Create viral titles and hashtags with AI',
      icon: Sparkles,
      href: '/generate',
      gradient: 'from-blue-500 to-purple-600',
      bgGradient: 'from-blue-500/10 to-purple-600/10',
      borderColor: 'border-blue-500/20'
    },
    {
      title: 'Score Titles',
      description: 'Analyze title performance and viral potential',
      icon: Target,
      href: '/score',
      gradient: 'from-green-500 to-emerald-600',
      bgGradient: 'from-green-500/10 to-emerald-600/10',
      borderColor: 'border-green-500/20'
    },
    {
      title: 'Trending Shorts',
      description: 'Discover viral content and trending topics',
      icon: TrendingUp,
      href: '/trending',
      gradient: 'from-orange-500 to-red-600',
      bgGradient: 'from-orange-500/10 to-red-600/10',
      borderColor: 'border-orange-500/20'
    },
    {
      title: 'Topic Analysis',
      description: 'Get insights and trends for your content',
      icon: BarChart3,
      href: '/analyze',
      gradient: 'from-purple-500 to-pink-600',
      bgGradient: 'from-purple-500/10 to-pink-600/10',
      borderColor: 'border-purple-500/20'
    }
  ];

  const stats = [
    {
      title: 'Titles Generated',
      value: '1,234',
      change: '+12%',
      changeType: 'positive',
      icon: Sparkles,
      gradient: 'from-blue-500 to-purple-600'
    },
    {
      title: 'Avg. Viral Score',
      value: '8.7',
      change: '+0.3',
      changeType: 'positive',
      icon: Target,
      gradient: 'from-green-500 to-emerald-600'
    },
    {
      title: 'Trending Topics',
      value: '45',
      change: '+5',
      changeType: 'positive',
      icon: TrendingIcon,
      gradient: 'from-orange-500 to-red-600'
    },
    {
      title: 'AI Provider',
      value: 'Google AI',
      change: 'Active',
      changeType: 'neutral',
      icon: Zap,
      gradient: 'from-purple-500 to-pink-600'
    }
  ];

  const recentActivity = [
    { action: 'Generated 10 viral titles', time: '2 min ago', type: 'success' },
    { action: 'Scored "Amazing Cooking Hack"', time: '5 min ago', type: 'info' },
    { action: 'Analyzed "Tech Trends" topic', time: '12 min ago', type: 'success' },
    { action: 'Updated AI model', time: '1 hour ago', type: 'warning' }
  ];

  return (
    <div className="space-y-8 fade-in">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className={`text-4xl font-bold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
            Welcome back! 👋
          </h1>
          <p className={`text-lg ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
            Your AI-powered content assistant is ready to help you create viral content
          </p>
        </div>
        
        <div className="flex items-center space-x-3">
          <div className={`status-indicator ${healthStatus?.status === 'healthy' ? 'status-online' : 'status-offline'}`}>
            <div className={`w-3 h-3 rounded-full ${healthStatus?.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'} animate-pulse`}></div>
            <span>
              {loading ? 'Checking...' : healthStatus?.status === 'healthy' ? 'API Connected' : 'API Disconnected'}
            </span>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={stat.title} className={`stats-card slide-up`} style={{ animationDelay: `${index * 100}ms` }}>
              <div className="flex items-center justify-between">
                <div>
                  <p className={`text-sm font-medium ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                    {stat.title}
                  </p>
                  <p className="stats-value text-3xl font-bold mt-2">{stat.value}</p>
                </div>
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${stat.gradient} flex items-center justify-center shadow-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
              <div className="flex items-center mt-4">
                <span className={`text-sm font-medium ${
                  stat.changeType === 'positive' ? 'text-green-600 dark:text-green-400' :
                  stat.changeType === 'negative' ? 'text-red-600 dark:text-red-400' :
                  'text-gray-600 dark:text-gray-400'
                }`}>
                  {stat.change}
                </span>
                <span className={`text-xs ml-2 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-400'}`}>
                  from last week
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className={`text-2xl font-bold mb-6 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
          Quick Actions
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickActions.map((action, index) => {
            const Icon = action.icon;
            return (
              <Link
                key={action.title}
                to={action.href}
                className={`premium-card premium-card-hover p-6 group slide-up`}
                style={{ animationDelay: `${index * 150}ms` }}
              >
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${action.gradient} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className={`text-lg font-semibold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                  {action.title}
                </h3>
                <p className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'} mb-4`}>
                  {action.description}
                </p>
                <div className="flex items-center text-blue-600 dark:text-blue-400 group-hover:translate-x-1 transition-transform duration-200">
                  <span className="text-sm font-medium">Get Started</span>
                  <ArrowUpRight className="w-4 h-4 ml-1" />
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Recent Activity & Quick Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <div className="lg:col-span-2">
          <div className="premium-card p-6">
            <h3 className={`text-xl font-bold mb-6 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
              Recent Activity
            </h3>
            <div className="space-y-4">
              {recentActivity.map((activity, index) => (
                <div key={index} className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors duration-200">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    activity.type === 'success' ? 'bg-green-100 dark:bg-green-900/30' :
                    activity.type === 'warning' ? 'bg-yellow-100 dark:bg-yellow-900/30' :
                    'bg-blue-100 dark:bg-blue-900/30'
                  }`}>
                    <CheckCircle className={`w-4 h-4 ${
                      activity.type === 'success' ? 'text-green-600 dark:text-green-400' :
                      activity.type === 'warning' ? 'text-yellow-600 dark:text-yellow-400' :
                      'text-blue-600 dark:text-blue-400'
                    }`} />
                  </div>
                  <div className="flex-1">
                    <p className={`text-sm font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                      {activity.action}
                    </p>
                    <p className={`text-xs ${theme === 'dark' ? 'text-gray-500' : 'text-gray-400'}`}>
                      {activity.time}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div>
          <div className="premium-card p-6">
            <h3 className={`text-xl font-bold mb-6 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
              Performance
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>Success Rate</span>
                <span className="text-lg font-bold text-green-600 dark:text-green-400">94.2%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>Avg Response Time</span>
                <span className="text-lg font-bold text-blue-600 dark:text-blue-400">1.2s</span>
              </div>
              <div className="flex items-center justify-between">
                <span className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>Uptime</span>
                <span className="text-lg font-bold text-purple-600 dark:text-purple-400">99.9%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
