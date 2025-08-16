import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Home, 
  Sparkles, 
  Target, 
  TrendingUp, 
  BarChart3,
  Settings,
  HelpCircle,
  ChevronLeft,
  ChevronRight,
  Zap,
  Activity
} from 'lucide-react';

const Sidebar = ({ theme, collapsed, onToggle }) => {
  const navigation = [
    { name: 'Dashboard', href: '/', icon: Home, description: 'Overview & Analytics' },
    { name: 'Content Generator', href: '/generate', icon: Sparkles, description: 'AI Content Creation' },
    { name: 'Title Scorer', href: '/score', icon: Target, description: 'Viral Score Analysis' },
    { name: 'Trending Shorts', href: '/trending', icon: TrendingUp, description: 'Discover Viral Content' },
    { name: 'Topic Analyzer', href: '/analyze', icon: BarChart3, description: 'Trend Analysis' },
  ];

  const secondaryNavigation = [
    { name: 'Settings', href: '/settings', icon: Settings, description: 'App Configuration' },
    { name: 'Help', href: '/help', icon: HelpCircle, description: 'Support & Documentation' },
  ];

  if (collapsed) {
    return (
      <div className={`fixed left-0 top-24 h-full z-30 transition-all duration-500 ${
        theme === 'dark' ? 'bg-black/95' : 'bg-white/95'
      } backdrop-blur-xl border-r ${
        theme === 'dark' ? 'border-gray-800/50' : 'border-gray-200/50'
      }`}>
        <div className="p-6">
          {/* Toggle Button */}
          <button
            onClick={onToggle}
            className={`w-full p-4 rounded-2xl transition-all duration-300 hover:scale-110 ${
              theme === 'dark' 
                ? 'bg-gray-900 hover:bg-gray-800 text-orange-400 border border-gray-700' 
                : 'bg-gray-100 hover:bg-gray-200 text-orange-600 border border-gray-200'
            }`}
          >
            <ChevronRight className="w-6 h-6" />
          </button>

          {/* Collapsed Navigation */}
          <nav className="mt-8 space-y-4">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.name}
                  to={item.href}
                  className={({ isActive }) =>
                    `flex items-center justify-center p-4 rounded-2xl transition-all duration-300 hover:scale-110 ${
                      isActive
                        ? 'bg-gradient-to-br from-orange-500/20 to-orange-600/20 text-orange-400 border border-orange-500/30 shadow-lg'
                        : theme === 'dark'
                        ? 'text-gray-400 hover:bg-gray-900 hover:text-white border border-gray-800'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900 border border-gray-200'
                    }`
                  }
                  title={item.description}
                >
                  <Icon className="w-7 h-7" />
                </NavLink>
              );
            })}
          </nav>

          {/* Quick Stats */}
          <div className="mt-8 p-4 bg-gradient-to-br from-orange-500/10 to-orange-600/10 rounded-2xl border border-orange-500/20">
            <div className="text-center">
              <Zap className="w-6 h-6 mx-auto mb-2 text-orange-400" />
              <div className="text-xs text-orange-400 font-bold">AI READY</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`fixed left-0 top-24 h-full w-80 z-30 transition-all duration-500 ${
      theme === 'dark' ? 'bg-black/95' : 'bg-white/95'
    } backdrop-blur-xl border-r ${
      theme === 'dark' ? 'border-gray-800/50' : 'border-gray-200/50'
    }`}>
      <div className="p-8 h-full flex flex-col">
        {/* Toggle Button */}
        <div className="flex justify-end mb-8">
          <button
            onClick={onToggle}
            className={`p-3 rounded-2xl transition-all duration-300 hover:scale-110 ${
              theme === 'dark' 
                ? 'bg-gray-900 hover:bg-gray-800 text-orange-400 border border-gray-700' 
                : 'bg-gray-100 hover:bg-gray-200 text-orange-600 border border-gray-200'
            }`}
          >
            <ChevronLeft className="w-6 h-6" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-4">
          <div className="mb-6">
            <h3 className={`text-xs font-bold tracking-wider uppercase mb-4 ${
              theme === 'dark' ? 'text-gray-500' : 'text-gray-600'
            }`}>
              Main Navigation
            </h3>
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.name}
                  to={item.href}
                  className={({ isActive }) =>
                    `flex items-center space-x-4 p-4 rounded-2xl transition-all duration-300 hover:scale-105 ${
                      isActive
                        ? 'bg-gradient-to-r from-orange-500/20 to-orange-600/20 text-orange-400 border border-orange-500/30 shadow-lg'
                        : theme === 'dark'
                        ? 'text-gray-400 hover:bg-gray-900 hover:text-white border border-gray-800'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900 border border-gray-200'
                    }`
                  }
                >
                  <Icon className="w-6 h-6 flex-shrink-0" />
                  <div>
                    <div className="font-semibold">{item.name}</div>
                    <div className={`text-xs ${theme === 'dark' ? 'text-gray-500' : 'text-gray-500'}`}>
                      {item.description}
                    </div>
                  </div>
                </NavLink>
              );
            })}
          </div>

          {/* Secondary Navigation */}
          <div className="mb-6">
            <h3 className={`text-xs font-bold tracking-wider uppercase mb-4 ${
              theme === 'dark' ? 'text-gray-500' : 'text-gray-600'
            }`}>
              Quick Links
            </h3>
            {secondaryNavigation.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.name}
                  to={item.href}
                  className={({ isActive }) =>
                    `flex items-center space-x-4 p-4 rounded-2xl transition-all duration-300 hover:scale-105 ${
                      isActive
                        ? 'bg-gradient-to-r from-orange-500/20 to-orange-600/20 text-orange-400 border border-orange-500/30 shadow-lg'
                        : theme === 'dark'
                        ? 'text-gray-400 hover:bg-gray-900 hover:text-white border border-gray-800'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900 border border-gray-200'
                    }`
                  }
                >
                  <Icon className="w-6 h-6 flex-shrink-0" />
                  <div>
                    <div className="font-semibold">{item.name}</div>
                    <div className={`text-xs ${theme === 'dark' ? 'text-gray-500' : 'text-gray-500'}`}>
                      {item.description}
                    </div>
                  </div>
                </NavLink>
              );
            })}
          </div>
        </nav>

        {/* Quick Stats */}
        <div className="mt-8 p-6 bg-gradient-to-br from-orange-500/10 to-orange-600/10 rounded-2xl border border-orange-500/20">
          <h3 className={`text-sm font-bold tracking-wider uppercase mb-4 ${
            theme === 'dark' ? 'text-orange-400' : 'text-orange-600'
          }`}>
            Quick Stats
          </h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Activity className="w-4 h-4 text-orange-400" />
                <span className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>
                  Titles Generated
                </span>
              </div>
              <span className="text-sm font-bold text-orange-400">1,234</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Target className="w-4 h-4 text-orange-400" />
                <span className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>
                  Avg. Viral Score
                </span>
              </div>
              <span className="text-sm font-bold text-orange-400">8.7</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Zap className="w-4 h-4 text-orange-400" />
                <span className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>
                  AI Provider
                </span>
              </div>
              <span className="text-sm font-bold text-green-400">Google AI</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
