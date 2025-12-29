import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Brain, Activity } from 'lucide-react';

const Header = () => {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="bg-primary-600 p-2 rounded-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">
              NeuroScan <span className="text-primary-600">AI</span>
            </span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link
              to="/"
              className={`font-medium transition-colors ${
                isActive('/')
                  ? 'text-primary-600'
                  : 'text-gray-600 hover:text-primary-600'
              }`}
            >
              Home
            </Link>
            <Link
              to="/scan"
              className={`font-medium transition-colors ${
                isActive('/scan')
                  ? 'text-primary-600'
                  : 'text-gray-600 hover:text-primary-600'
              }`}
            >
              Scan
            </Link>
            <Link
              to="/dashboard"
              className={`font-medium transition-colors ${
                isActive('/dashboard')
                  ? 'text-primary-600'
                  : 'text-gray-600 hover:text-primary-600'
              }`}
            >
              Dashboard
            </Link>
          </nav>

          {/* Mobile menu button */}
          <button className="md:hidden p-2 rounded-lg hover:bg-gray-100">
            <Activity className="w-6 h-6 text-gray-600" />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
