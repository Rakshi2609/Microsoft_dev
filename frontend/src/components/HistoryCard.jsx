import React from 'react';
import { Clock, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import RiskBadge from './RiskBadge';

const HistoryCard = ({ scan, onClick }) => {
  if (!scan) return null;

  const { risk, confidence, score, timestamp, features } = scan;

  // Format date
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) {
      return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
      return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    } else if (diffDays < 7) {
      return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  // Get risk trend icon
  const getTrendIcon = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'high':
        return <TrendingUp className="w-4 h-4 text-danger-500" />;
      case 'medium':
        return <Minus className="w-4 h-4 text-warning-500" />;
      case 'low':
        return <TrendingDown className="w-4 h-4 text-success-500" />;
      default:
        return null;
    }
  };

  // Get card border color
  const getBorderColor = () => {
    switch (risk?.toLowerCase()) {
      case 'low':
        return 'border-l-4 border-l-success-500';
      case 'medium':
        return 'border-l-4 border-l-warning-500';
      case 'high':
        return 'border-l-4 border-l-danger-500';
      default:
        return 'border-l-4 border-l-gray-300';
    }
  };

  return (
    <div
      onClick={onClick}
      className={`card cursor-pointer transition-all duration-200 hover:scale-[1.02] ${getBorderColor()}`}
    >
      <div className="flex items-center justify-between mb-3">
        {/* Timestamp */}
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <Clock className="w-4 h-4" />
          <span>{formatDate(timestamp)}</span>
        </div>

        {/* Trend Icon */}
        {getTrendIcon(risk)}
      </div>

      {/* Risk Badge */}
      <div className="mb-4">
        <RiskBadge risk={risk} confidence={confidence} size="sm" />
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
        <div>
          <p className="text-xs text-gray-500 mb-1">Risk Score</p>
          <p className="text-lg font-bold text-gray-900">
            {(score * 100).toFixed(1)}%
          </p>
        </div>
        
        <div>
          <p className="text-xs text-gray-500 mb-1">Confidence</p>
          <p className="text-lg font-bold text-gray-900">
            {(confidence * 100).toFixed(0)}%
          </p>
        </div>
      </div>

      {/* Top Features Preview */}
      {features && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-500 mb-2">Key Metrics</p>
          <div className="flex flex-wrap gap-2">
            {Object.entries(features)
              .slice(0, 3)
              .map(([key, value]) => (
                <span
                  key={key}
                  className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded"
                >
                  {key.split('_')[0]}: {(value * 100).toFixed(0)}%
                </span>
              ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default HistoryCard;
