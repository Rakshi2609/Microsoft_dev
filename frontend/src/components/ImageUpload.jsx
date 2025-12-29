import React, { useState, useRef } from 'react';
import { Upload, X, Image as ImageIcon, CheckCircle } from 'lucide-react';

const ImageUpload = ({ onUpload, onError }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  // Handle file selection
  const handleFileSelect = (file) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      onError('Please select an image file (JPG, PNG)');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      onError('File size too large. Maximum 10MB allowed.');
      return;
    }

    setSelectedFile(file);

    // Generate preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);

    // Call onUpload callback
    if (onUpload) {
      onUpload(file);
    }
  };

  // Handle file input change
  const handleInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  // Handle drag and drop
  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  // Clear selection
  const clearSelection = () => {
    setSelectedFile(null);
    setPreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Trigger file input click
  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  return (
    <div>
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleInputChange}
        className="hidden"
      />

      {/* Upload area */}
      {!preview ? (
        <div
          onClick={triggerFileInput}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            border-2 border-dashed rounded-xl p-12 text-center cursor-pointer
            transition-all duration-200
            ${
              isDragging
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-300 hover:border-primary-400 bg-gray-50 hover:bg-gray-100'
            }
          `}
        >
          <div className="flex flex-col items-center">
            <div className="bg-primary-100 p-4 rounded-full mb-4">
              <Upload className="w-8 h-8 text-primary-600" />
            </div>
            
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Upload Image
            </h3>
            
            <p className="text-gray-600 mb-4">
              Click to browse or drag and drop
            </p>
            
            <p className="text-sm text-gray-500">
              Supported: JPG, PNG (Max 10MB)
            </p>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Preview */}
          <div className="relative bg-gray-100 rounded-xl overflow-hidden">
            <img
              src={preview}
              alt="Preview"
              className="w-full h-auto max-h-96 object-contain"
            />
            
            {/* Clear button */}
            <button
              onClick={clearSelection}
              className="absolute top-4 right-4 bg-red-500 hover:bg-red-600 text-white p-2 rounded-full transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
            
            {/* Success indicator */}
            <div className="absolute bottom-4 left-4 bg-success-500 text-white px-4 py-2 rounded-full flex items-center space-x-2">
              <CheckCircle className="w-5 h-5" />
              <span className="font-semibold">Image Selected</span>
            </div>
          </div>

          {/* File info */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center space-x-3">
              <ImageIcon className="w-6 h-6 text-primary-600" />
              <div className="flex-1">
                <p className="font-medium text-gray-900">
                  {selectedFile?.name}
                </p>
                <p className="text-sm text-gray-500">
                  {(selectedFile?.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>
          </div>

          {/* Change button */}
          <button
            onClick={triggerFileInput}
            className="btn-secondary w-full"
          >
            Choose Different Image
          </button>
        </div>
      )}

      {/* Guidelines */}
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 mb-2">Image Guidelines:</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>✓ Clear, well-lit photo of face</li>
          <li>✓ Face looking directly at camera</li>
          <li>✓ No obstructions (hands, hair, etc.)</li>
          <li>✓ Neutral expression preferred</li>
          <li>✓ Single person in frame</li>
        </ul>
      </div>
    </div>
  );
};

export default ImageUpload;
