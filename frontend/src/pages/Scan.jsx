import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Upload as UploadIcon, Loader2, AlertCircle } from 'lucide-react';
import CameraCapture from '../components/CameraCapture';
import ImageUpload from '../components/ImageUpload';
import { scanImage } from '../api';

const Scan = () => {
  const navigate = useNavigate();
  
  const [scanMode, setScanMode] = useState('camera'); // 'camera' or 'upload'
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [capturedFile, setCapturedFile] = useState(null);

  // Handle image capture from camera
  const handleCapture = (file) => {
    setCapturedFile(file);
    setError(null);
  };

  // Handle image upload
  const handleUpload = (file) => {
    setCapturedFile(file);
    setError(null);
  };

  // Handle error messages
  const handleError = (errorMessage) => {
    setError(errorMessage);
  };

  // Process scan
  const processScan = async () => {
    if (!capturedFile) {
      setError('Please capture or upload an image first');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      // Call API to scan image
      const result = await scanImage(capturedFile);
      
      // Navigate to result page with data
      navigate('/result', { state: { result } });
    } catch (err) {
      setError(err.message || 'Failed to process image. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-3">
          Stroke Risk Screening
        </h1>
        <p className="text-lg text-gray-600">
          Choose your preferred method to scan
        </p>
      </div>

      {/* Mode Selector */}
      <div className="flex justify-center mb-8">
        <div className="inline-flex rounded-lg border-2 border-gray-200 p-1 bg-gray-50">
          <button
            onClick={() => {
              setScanMode('camera');
              setCapturedFile(null);
              setError(null);
            }}
            className={`
              flex items-center space-x-2 px-6 py-3 rounded-md font-semibold transition-all
              ${
                scanMode === 'camera'
                  ? 'bg-primary-600 text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900'
              }
            `}
          >
            <Camera className="w-5 h-5" />
            <span>Camera</span>
          </button>

          <button
            onClick={() => {
              setScanMode('upload');
              setCapturedFile(null);
              setError(null);
            }}
            className={`
              flex items-center space-x-2 px-6 py-3 rounded-md font-semibold transition-all
              ${
                scanMode === 'upload'
                  ? 'bg-primary-600 text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900'
              }
            `}
          >
            <UploadIcon className="w-5 h-5" />
            <span>Upload</span>
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-red-900">Error</p>
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        </div>
      )}

      {/* Scan Area */}
      <div className="card mb-6">
        {scanMode === 'camera' ? (
          <CameraCapture onCapture={handleCapture} onError={handleError} />
        ) : (
          <ImageUpload onUpload={handleUpload} onError={handleError} />
        )}
      </div>

      {/* Process Button */}
      {capturedFile && (
        <div className="flex justify-center">
          <button
            onClick={processScan}
            disabled={isProcessing}
            className="btn-primary text-lg flex items-center space-x-3 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isProcessing ? (
              <>
                <Loader2 className="w-6 h-6 animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Activity className="w-6 h-6" />
                <span>Analyze Image</span>
              </>
            )}
          </button>
        </div>
      )}

      {/* Processing Message */}
      {isProcessing && (
        <div className="mt-6 text-center">
          <div className="inline-block bg-blue-50 border border-blue-200 rounded-lg px-6 py-4">
            <p className="text-blue-900 font-semibold mb-2">
              Analyzing facial features...
            </p>
            <p className="text-sm text-blue-700">
              This may take a few seconds
            </p>
          </div>
        </div>
      )}

      {/* Info Section */}
      <div className="mt-12 grid md:grid-cols-2 gap-6">
        <div className="card bg-blue-50">
          <h3 className="font-bold text-blue-900 mb-2">What We Analyze</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Eye symmetry and openness</li>
            <li>• Mouth corner alignment</li>
            <li>• Nose position and deviation</li>
            <li>• Overall facial symmetry</li>
            <li>• Face tilt and alignment</li>
          </ul>
        </div>

        <div className="card bg-green-50">
          <h3 className="font-bold text-green-900 mb-2">Privacy & Security</h3>
          <ul className="text-sm text-green-800 space-y-1">
            <li>• Images processed locally</li>
            <li>• No data stored on servers</li>
            <li>• HIPAA-compliant architecture</li>
            <li>• Results saved only on device</li>
            <li>• Complete data control</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

// Import Activity
import { Activity } from 'lucide-react';

export default Scan;
