import React from 'react';
import RiskBadge from './RiskBadge';
import { Activity, Eye, Smile, Navigation, TrendingUp } from 'lucide-react';

const ResultDetails = ({ result }) => {
  if (!result) {
    return null;
  }

  const { risk, confidence, score, features, explanation, timestamp } = result;

  // Feature icons mapping
  const featureIcons = {
    eye_asymmetry: Eye,
    mouth_asymmetry: Smile,
    nose_deviation: Navigation,
    face_tilt: Activity,
    symmetry_ratio: TrendingUp,
  };

  // Format feature names
  const formatFeatureName = (name) => {
    return name
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  // Get feature severity color
  const getFeatureSeverity = (value) => {
    if (value < 0.1) return 'text-success-600';
    if (value < 0.2) return 'text-warning-600';
    return 'text-danger-600';
  };

  return (
    <div className="space-y-6">
      {/* Risk Badge */}
      <div className="card">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Assessment Result
        </h2>
        <RiskBadge risk={risk} confidence={confidence} size="lg" />
        
        {/* Overall Score */}
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <div className="flex justify-between items-center">
            <span className="text-gray-700 font-medium">Risk Score:</span>
            <span className="text-2xl font-bold text-gray-900">
              {(score * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </div>

      {/* Feature Breakdown */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <Activity className="w-6 h-6 mr-2 text-primary-600" />
          Feature Analysis
        </h3>
        
        <div className="space-y-4">
          {features && Object.entries(features).map(([key, value]) => {
            const Icon = featureIcons[key] || Activity;
            return (
              <div key={key} className="border-b border-gray-200 pb-3 last:border-b-0">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <Icon className="w-5 h-5 text-gray-400" />
                    <span className="font-medium text-gray-700">
                      {formatFeatureName(key)}
                    </span>
                  </div>
                  <span className={`font-bold ${getFeatureSeverity(value)}`}>
                    {(value * 100).toFixed(1)}%
                  </span>
                </div>
                
                {/* Progress bar */}
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-500 ${
                      value < 0.1
                        ? 'bg-success-500'
                        : value < 0.2
                        ? 'bg-warning-500'
                        : 'bg-danger-500'
                    }`}
                    style={{ width: `${Math.min(value * 100, 100)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Explanation */}
      {explanation && (
        <div className="card bg-blue-50 border border-blue-200">
          <h3 className="text-lg font-bold text-blue-900 mb-2">
            Explanation
          </h3>
          <p className="text-blue-800">{explanation}</p>
        </div>
      )}

      {/* Disclaimer */}
      <div className="card bg-yellow-50 border border-yellow-300">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            <AlertCircle className="w-6 h-6 text-yellow-600" />
          </div>
          <div>
            <h3 className="font-bold text-yellow-900 mb-2">
              Important Disclaimer
            </h3>
            <p className="text-sm text-yellow-800">
              This is a <strong>pre-diagnostic screening tool</strong>, not a
              medical diagnosis. The results indicate facial asymmetry patterns
              that may warrant further evaluation. Always consult with a
              healthcare professional for proper medical assessment and advice.
            </p>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          Next Steps
        </h3>
        
        {risk?.toLowerCase() === 'high' && (
          <div className="space-y-3 text-sm text-gray-700">
            <p className="font-semibold text-danger-700">
              ⚠️ High Risk Detected - Immediate Action Recommended
            </p>
            <ul className="space-y-2 ml-4">
              <li>• Contact your healthcare provider immediately</li>
              <li>• Consider visiting an emergency room if experiencing symptoms</li>
              <li>• Do not ignore warning signs</li>
              <li>• Document any symptoms you're experiencing</li>
            </ul>
          </div>
        )}
        
        {risk?.toLowerCase() === 'medium' && (
          <div className="space-y-3 text-sm text-gray-700">
            <p className="font-semibold text-warning-700">
              ⚠️ Medium Risk - Medical Consultation Advised
            </p>
            <ul className="space-y-2 ml-4">
              <li>• Schedule an appointment with your doctor</li>
              <li>• Monitor for any developing symptoms</li>
              <li>• Maintain healthy lifestyle habits</li>
              <li>• Keep track of results over time</li>
            </ul>
          </div>
        )}
        
        {risk?.toLowerCase() === 'low' && (
          <div className="space-y-3 text-sm text-gray-700">
            <p className="font-semibold text-success-700">
              ✓ Low Risk - Continue Healthy Practices
            </p>
            <ul className="space-y-2 ml-4">
              <li>• Maintain regular health checkups</li>
              <li>• Continue healthy lifestyle habits</li>
              <li>• Stay aware of stroke warning signs</li>
              <li>• Perform periodic self-assessments</li>
            </ul>
          </div>
        )}
      </div>

      {/* Timestamp */}
      {timestamp && (
        <p className="text-sm text-gray-500 text-center">
          Scan performed: {new Date(timestamp).toLocaleString()}
        </p>
      )}
    </div>
  );
};

// Import AlertCircle
import { AlertCircle } from 'lucide-react';

export default ResultDetails;
