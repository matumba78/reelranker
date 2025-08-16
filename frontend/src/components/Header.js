import React from 'react';
import { Sparkles, Moon, Sun, Bell, Settings, Menu, Search } from 'lucide-react';

const Header = ({ theme, toggleTheme }) => {
  return (
    <header className={`sticky top-0 z-50 backdrop-blur-xl border-b transition-all duration-500 ${
      theme === 'dark' 
        ? 'bg-black/95 border-gray-800/50' 
        : 'bg-white/95 border-gray-200/50'
    }`}>
      <div className="w-full px-6 lg:px-8">
        <div className="flex justify-between items-center h-24">
          {/* Logo and Brand - Absolute Leftmost */}
          <div className="flex items-center space-x-6 flex-shrink-0">
            <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-br from-orange-500 via-orange-600 to-orange-700 rounded-2xl shadow-2xl hover:shadow-orange-500/25 transition-all duration-300 hover:scale-110 border-2 border-orange-400/20">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
            <div className="hidden sm:block">
              <h1 className="text-3xl font-black tracking-tight text-white">ReelRanker</h1>
              <p className={`text-sm font-medium tracking-wide ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                AI-POWERED CONTENT GENERATOR
              </p>
            </div>
          </div>

          {/* Center - Navigation Menu */}
          <div className="hidden lg:flex items-center space-x-8 flex-1 justify-center">
            <nav className="flex items-center space-x-8">
              <a href="/" className={`text-sm font-bold tracking-wider uppercase transition-all duration-200 hover:scale-105 ${
                theme === 'dark' ? 'text-white hover:text-orange-400' : 'text-gray-900 hover:text-orange-600'
              }`}>
                Dashboard
              </a>
              <a href="/generate" className={`text-sm font-bold tracking-wider uppercase transition-all duration-200 hover:scale-105 ${
                theme === 'dark' ? 'text-white hover:text-orange-400' : 'text-gray-900 hover:text-orange-600'
              }`}>
                Generate
              </a>
              <a href="/score" className={`text-sm font-bold tracking-wider uppercase transition-all duration-200 hover:scale-105 ${
                theme === 'dark' ? 'text-white hover:text-orange-400' : 'text-gray-900 hover:text-orange-600'
              }`}>
                Score
              </a>
              <a href="/trending" className={`text-sm font-bold tracking-wider uppercase transition-all duration-200 hover:scale-105 ${
                theme === 'dark' ? 'text-white hover:text-orange-400' : 'text-gray-900 hover:text-orange-600'
              }`}>
                Trending
              </a>
              <a href="/analyze" className={`text-sm font-bold tracking-wider uppercase transition-all duration-200 hover:scale-105 ${
                theme === 'dark' ? 'text-white hover:text-orange-400' : 'text-gray-900 hover:text-orange-600'
              }`}>
                Analyze
              </a>
            </nav>
          </div>

          {/* Right - User Menu - Absolute Rightmost */}
          <div className="flex items-center space-x-4 flex-shrink-0">
            {/* Search */}
            <button className={`p-3 rounded-xl transition-all duration-200 hover:scale-110 ${
              theme === 'dark' 
                ? 'bg-gray-900 hover:bg-gray-800 text-gray-300 border border-gray-700' 
                : 'bg-gray-100 hover:bg-gray-200 text-gray-600 border border-gray-200'
            }`}>
              <Search className="w-5 h-5" />
            </button>

            {/* Mobile Menu Button */}
            <button className={`lg:hidden p-3 rounded-xl transition-all duration-200 hover:scale-110 ${
              theme === 'dark' 
                ? 'bg-gray-900 hover:bg-gray-800 text-gray-300 border border-gray-700' 
                : 'bg-gray-100 hover:bg-gray-200 text-gray-600 border border-gray-200'
            }`}>
              <Menu className="w-5 h-5" />
            </button>

            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className={`p-3 rounded-xl transition-all duration-200 hover:scale-110 ${
                theme === 'dark' 
                  ? 'bg-gray-900 hover:bg-gray-800 text-orange-400 border border-gray-700' 
                  : 'bg-gray-100 hover:bg-gray-200 text-orange-600 border border-gray-200'
              }`}
              title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
            >
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>

            {/* Notifications */}
            <button className={`p-3 rounded-xl transition-all duration-200 hover:scale-110 ${
              theme === 'dark' 
                ? 'bg-gray-900 hover:bg-gray-800 text-gray-300 border border-gray-700' 
                : 'bg-gray-100 hover:bg-gray-200 text-gray-600 border border-gray-200'
            }`}>
              <Bell className="w-5 h-5" />
            </button>

            {/* Settings */}
            <button className={`p-3 rounded-xl transition-all duration-200 hover:scale-110 ${
              theme === 'dark' 
                ? 'bg-gray-900 hover:bg-gray-800 text-gray-300 border border-gray-700' 
                : 'bg-gray-100 hover:bg-gray-200 text-gray-600 border border-gray-200'
            }`}>
              <Settings className="w-5 h-5" />
            </button>

            {/* User Avatar */}
            <div className="w-14 h-14 bg-gradient-to-br from-orange-500 to-orange-700 rounded-2xl shadow-2xl flex items-center justify-center cursor-pointer hover:scale-110 transition-all duration-300 border-2 border-orange-400/20">
              <span className="text-white text-xl font-black">U</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
