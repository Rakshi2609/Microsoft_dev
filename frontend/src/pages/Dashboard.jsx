import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart3,
  TrendingUp,
  Calendar,
  Trash2,
  AlertCircle,
  Loader2,
  Camera,
} from 'lucide-react';
import HistoryCard from '../components/HistoryCard';
import { getHistory, getHistoryStats, clearHistory } from '../api';

const Dashboard = () => {
  const navigate = useNavigate();
  
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterRisk, setFilterRisk] = useState('all'); // 'all', 'low', 'medium', 'high'

  // Load history and stats on mount
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const [historyData, statsData] = await Promise.all([
        getHistory(),
        getHistoryStats(),
      ]);

      setHistory(historyData);
      setStats(statsData);
    } catch (err) {
      setError(err.message || 'Failed to load data');
    } finally {
      setIsLoading(false);
    }
  };

  // Handle clear history
  const handleClearHistory = async () => {
    if (!window.confirm('Are you sure you want to clear all scan history?')) {
      return;
    }

    try {
      await clearHistory();
      setHistory([]);
      setStats({
        total_scans: 0,
        risk_distribution: { low: 0, medium: 0, high: 0 },
        average_confidence: 0,
        average_score: 0,
      });
    } catch (err) {
      setError(err.message || 'Failed to clear history');
    }
  };

  // Filter history by risk level
  const filteredHistory = history.filter((scan) => {
    if (filterRisk === 'all') return true;
    return scan.risk?.toLowerCase() === filterRisk.toLowerCase();
  });

  // Handle scan card click
  const handleScanClick = (scan) => {
    navigate('/result', { state: { result: scan } });
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-16 flex flex-col items-center justify-center">
        <Loader2 className="w-12 h-12 text-primary-600 animate-spin mb-4" />
        <p className="text-gray-600">Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto card bg-red-50 border-2 border-red-200">
          <div className="flex items-start space-x-3">
            <AlertCircle className="w-6 h-6 text-red-500 flex-shrink-0" />
            <div>
              <h3 className="font-bold text-red-900 mb-2">Error Loading Dashboard</h3>
              <p className="text-red-700">{error}</p>
              <button
                onClick={loadData}
                className="mt-4 btn-primary text-sm"
              >
                Try Again
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-7xl">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Dashboard</h1>
            <p className="text-gray-600">Track your scan history and trends</p>
          </div>

          <div className="flex items-center space-x-3 mt-4 md:mt-0">
            <button
              onClick={handleClearHistory}
              className="btn-secondary flex items-center space-x-2"
              disabled={history.length === 0}
            >
              <Trash2 className="w-4 h-4" />
              <span>Clear History</span>
            </button>

            <button
              onClick={() => navigate('/scan')}
              className="btn-primary flex items-center space-x-2"
            >
              <Camera className="w-5 h-5" />
              <span>New Scan</span>
            </button>
          </div>
        </div>

        {/* Statistics Cards */}
        {stats && stats.total_scans > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {/* Total Scans */}
            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Total Scans</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {stats.total_scans}
                  </p>
                </div>
                <BarChart3 className="w-10 h-10 text-primary-500" />
              </div>
            </div>

            {/* Average Confidence */}
            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Avg Confidence</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {stats.average_confidence.toFixed(0)}%
                  </p>
                </div>
                <TrendingUp className="w-10 h-10 text-green-500" />
              </div>
            </div>

            {/* Risk Distribution - Low */}
            <div className="card bg-success-50 border border-success-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-success-700 mb-1">Low Risk</p>
                  <p className="text-3xl font-bold text-success-900">
                    {stats.risk_distribution.low}
                  </p>
                </div>
                <div className="text-success-600 text-xl font-bold">
                  {stats.total_scans > 0
                    ? Math.round(
                        (stats.risk_distribution.low / stats.total_scans) * 100
                      )
                    : 0}
                  %
                </div>
              </div>
            </div>

            {/* Risk Distribution - Medium/High */}
            <div className="card bg-warning-50 border border-warning-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-warning-700 mb-1">Med/High Risk</p>
                  <p className="text-3xl font-bold text-warning-900">
                    {stats.risk_distribution.medium + stats.risk_distribution.high}
                  </p>
                </div>
                <div className="text-warning-600 text-xl font-bold">
                  {stats.total_scans > 0
                    ? Math.round(
                        ((stats.risk_distribution.medium +
                          stats.risk_distribution.high) /
                          stats.total_scans) *
                          100
                      )
                    : 0}
                  %
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Filters */}
        {history.length > 0 && (
          <div className="mb-6">
            <div className="flex flex-wrap items-center gap-3">
              <span className="text-sm font-medium text-gray-700">Filter:</span>
              
              <button
                onClick={() => setFilterRisk('all')}
                className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
                  filterRisk === 'all'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                All ({history.length})
              </button>

              <button
                onClick={() => setFilterRisk('low')}
                className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
                  filterRisk === 'low'
                    ? 'bg-success-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Low ({history.filter((s) => s.risk?.toLowerCase() === 'low').length})
              </button>

              <button
                onClick={() => setFilterRisk('medium')}
                className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
                  filterRisk === 'medium'
                    ? 'bg-warning-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Medium (
                {history.filter((s) => s.risk?.toLowerCase() === 'medium').length})
              </button>

              <button
                onClick={() => setFilterRisk('high')}
                className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
                  filterRisk === 'high'
                    ? 'bg-danger-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                High ({history.filter((s) => s.risk?.toLowerCase() === 'high').length})
              </button>
            </div>
          </div>
        )}

        {/* History Grid */}
        {filteredHistory.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredHistory.map((scan, index) => (
              <HistoryCard
                key={scan.id || index}
                scan={scan}
                onClick={() => handleScanClick(scan)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              {history.length === 0 ? 'No Scans Yet' : 'No Results for This Filter'}
            </h3>
            <p className="text-gray-600 mb-6">
              {history.length === 0
                ? 'Start your first scan to see results here'
                : 'Try selecting a different filter'}
            </p>
            <button
              onClick={() => navigate('/scan')}
              className="btn-primary inline-flex items-center space-x-2"
            >
              <Camera className="w-5 h-5" />
              <span>Start First Scan</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
