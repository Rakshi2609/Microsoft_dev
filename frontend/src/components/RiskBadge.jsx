import React from 'react';
import { CheckCircle, AlertTriangle, AlertCircle } from 'lucide-react';

const RiskBadge = ({ risk, confidence, size = 'md' }) => {
  const getRiskConfig = () => {
    switch (risk?.toLowerCase()) {
      case 'low':
        return {
          icon: CheckCircle,
          bgColor: 'bg-success-50',
          borderColor: 'border-success-500',
          textColor: 'text-success-700',
          iconColor: 'text-success-500',
          label: 'Low Risk',
          description: 'Facial symmetry appears normal',
        };
      case 'medium':
        return {
          icon: AlertTriangle,
          bgColor: 'bg-warning-50',
          borderColor: 'border-warning-500',
          textColor: 'text-warning-700',
          iconColor: 'text-warning-500',
          label: 'Medium Risk',
          description: 'Moderate facial asymmetry detected',
        };
      case 'high':
        return {
          icon: AlertCircle,
          bgColor: 'bg-danger-50',
          borderColor: 'border-danger-500',
          textColor: 'text-danger-700',
          iconColor: 'text-danger-500',
          label: 'High Risk',
          description: 'Significant facial asymmetry detected',
        };
      default:
        return {
          icon: AlertCircle,
          bgColor: 'bg-gray-50',
          borderColor: 'border-gray-300',
          textColor: 'text-gray-700',
          iconColor: 'text-gray-500',
          label: 'Unknown',
          description: 'Unable to determine risk',
        };
    }
  };

  const config = getRiskConfig();
  const Icon = config.icon;

  const sizeClasses = {
    sm: 'text-sm py-2 px-3',
    md: 'text-base py-3 px-4',
    lg: 'text-lg py-4 px-6',
  };

  const iconSizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };

  return (
    <div className="space-y-3">
      {/* Badge */}
      <div
        className={`
          ${config.bgColor} ${config.borderColor} ${config.textColor}
          border-2 rounded-full font-bold inline-flex items-center space-x-2
          ${sizeClasses[size]}
        `}
      >
        <Icon className={`${iconSizes[size]} ${config.iconColor}`} />
        <span>{config.label}</span>
      </div>

      {/* Confidence */}
      {confidence !== undefined && (
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-600 font-medium">Confidence:</span>
          <div className="flex-1 bg-gray-200 rounded-full h-2 max-w-xs">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${
                risk?.toLowerCase() === 'low'
                  ? 'bg-success-500'
                  : risk?.toLowerCase() === 'medium'
                  ? 'bg-warning-500'
                  : 'bg-danger-500'
              }`}
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
          <span className="text-sm font-semibold text-gray-900">
            {(confidence * 100).toFixed(0)}%
          </span>
        </div>
      )}

      {/* Description */}
      <p className="text-sm text-gray-600">{config.description}</p>
    </div>
  );
};

export default RiskBadge;
