import React, { useState, useEffect, Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import './App.css';

// Components
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ErrorBoundary from './components/ErrorBoundary';
import LoadingSpinner from './components/LoadingSpinner';

// Lazy load pages for better performance
const Dashboard = lazy(() => import('./pages/Dashboard'));
const ContentGenerator = lazy(() => import('./pages/ContentGenerator'));
const TitleScorer = lazy(() => import('./pages/TitleScorer'));
const TrendingShorts = lazy(() => import('./pages/TrendingShorts'));
const TopicAnalyzer = lazy(() => import('./pages/TopicAnalyzer'));

function App() {
  const [theme, setTheme] = useState('dark');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  useEffect(() => {
    // Check for saved theme preference or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);
    document.documentElement.classList.toggle('dark', savedTheme === 'dark');
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  return (
    <Router>
      <div className={`min-h-screen transition-all duration-300 ${
        theme === 'dark' 
          ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white' 
          : 'bg-gradient-to-br from-gray-50 via-white to-gray-100 text-gray-900'
      }`}>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: theme === 'dark' ? '#1f2937' : '#ffffff',
              color: theme === 'dark' ? '#ffffff' : '#1f2937',
              border: theme === 'dark' ? '1px solid #374151' : '1px solid #e5e7eb',
              boxShadow: '0 10px 25px rgba(0, 0, 0, 0.1)',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#10b981',
                secondary: theme === 'dark' ? '#1f2937' : '#ffffff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#ef4444',
                secondary: theme === 'dark' ? '#1f2937' : '#ffffff',
              },
            },
          }}
        />
        
        <Header theme={theme} toggleTheme={toggleTheme} />
        
        <div className="flex">
          <Sidebar 
            theme={theme} 
            collapsed={sidebarCollapsed} 
            onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
          />
          
          <main className={`flex-1 transition-all duration-300 ${
            sidebarCollapsed ? 'ml-20' : 'ml-80'
          } p-8`}>
            <div className="max-w-7xl mx-auto">
              <ErrorBoundary>
                <Suspense fallback={<LoadingSpinner size="lg" text="Loading page..." theme={theme} />}>
                  <Routes>
                    <Route path="/" element={<Dashboard theme={theme} />} />
                    <Route path="/generate" element={<ContentGenerator theme={theme} />} />
                    <Route path="/score" element={<TitleScorer theme={theme} />} />
                    <Route path="/trending" element={<TrendingShorts theme={theme} />} />
                    <Route path="/analyze" element={<TopicAnalyzer theme={theme} />} />
                  </Routes>
                </Suspense>
              </ErrorBoundary>
            </div>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
