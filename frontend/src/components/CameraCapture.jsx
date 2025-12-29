import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import { Camera, RefreshCw, Check, AlertCircle } from 'lucide-react';

const CameraCapture = ({ onCapture, onError }) => {
  const webcamRef = useRef(null);
  const [isCaptured, setIsCaptured] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [countdown, setCountdown] = useState(null);
  const [hasCamera, setHasCamera] = useState(true);

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: 'user',
  };

  // Handle camera errors
  const handleUserMediaError = useCallback((error) => {
    console.error('Camera error:', error);
    setHasCamera(false);
    if (onError) {
      onError('Unable to access camera. Please check permissions.');
    }
  }, [onError]);

  // Start countdown and capture
  const startCountdown = () => {
    let count = 3;
    setCountdown(count);

    const timer = setInterval(() => {
      count--;
      if (count > 0) {
        setCountdown(count);
      } else {
        clearInterval(timer);
        setCountdown(null);
        captureImage();
      }
    }, 1000);
  };

  // Capture image from webcam
  const captureImage = () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      setCapturedImage(imageSrc);
      setIsCaptured(true);
      
      // Convert base64 to blob for upload
      fetch(imageSrc)
        .then(res => res.blob())
        .then(blob => {
          const file = new File([blob], 'capture.jpg', { type: 'image/jpeg' });
          onCapture(file);
        });
    }
  };

  // Retake photo
  const retake = () => {
    setIsCaptured(false);
    setCapturedImage(null);
    setCountdown(null);
  };

  if (!hasCamera) {
    return (
      <div className="flex flex-col items-center justify-center h-96 bg-gray-100 rounded-xl">
        <AlertCircle className="w-16 h-16 text-gray-400 mb-4" />
        <p className="text-gray-600 text-center">
          Camera access denied or not available.
          <br />
          Please check your browser permissions.
        </p>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Webcam or Captured Image */}
      <div className="relative bg-black rounded-xl overflow-hidden shadow-lg">
        {!isCaptured ? (
          <>
            <Webcam
              ref={webcamRef}
              audio={false}
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              onUserMediaError={handleUserMediaError}
              className="w-full h-auto"
            />
            
            {/* Countdown Overlay */}
            {countdown !== null && (
              <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
                <div className="text-white text-8xl font-bold animate-pulse">
                  {countdown}
                </div>
              </div>
            )}
            
            {/* Capture Guide */}
            <div className="absolute top-4 left-4 right-4">
              <div className="bg-black bg-opacity-70 text-white px-4 py-2 rounded-lg text-sm">
                <p className="font-semibold">📸 Position your face in the center</p>
                <p className="text-xs mt-1">Ensure good lighting and face camera directly</p>
              </div>
            </div>
          </>
        ) : (
          <img
            src={capturedImage}
            alt="Captured"
            className="w-full h-auto"
          />
        )}
      </div>

      {/* Controls */}
      <div className="flex justify-center items-center space-x-4 mt-6">
        {!isCaptured ? (
          <button
            onClick={startCountdown}
            disabled={countdown !== null}
            className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Camera className="w-5 h-5" />
            <span>{countdown !== null ? 'Capturing...' : 'Capture Photo'}</span>
          </button>
        ) : (
          <>
            <button
              onClick={retake}
              className="btn-secondary flex items-center space-x-2"
            >
              <RefreshCw className="w-5 h-5" />
              <span>Retake</span>
            </button>
            
            <button
              className="btn-primary flex items-center space-x-2"
              disabled
            >
              <Check className="w-5 h-5" />
              <span>Photo Captured</span>
            </button>
          </>
        )}
      </div>

      {/* Instructions */}
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 mb-2">Tips for Best Results:</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>✓ Face the camera directly</li>
          <li>✓ Ensure adequate lighting</li>
          <li>✓ Remove glasses if possible</li>
          <li>✓ Keep a neutral expression</li>
          <li>✓ Stay still during capture</li>
        </ul>
      </div>
    </div>
  );
};

export default CameraCapture;
