/**
 * API Service for NeuroScan AI
 * Handles all backend communication
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

/**
 * Scan image for stroke risk assessment
 * @param {File} imageFile - Image file to analyze
 * @returns {Promise} - Risk assessment results
 */
export const scanImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);

  try {
    const response = await api.post('/scan/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error scanning image:', error);
    throw handleApiError(error);
  }
};

/**
 * Get scan service status
 * @returns {Promise} - Service status
 */
export const getScanStatus = async () => {
  try {
    const response = await api.get('/scan/status');
    return response.data;
  } catch (error) {
    console.error('Error checking scan status:', error);
    throw handleApiError(error);
  }
};

/**
 * Get all scan history
 * @returns {Promise} - Array of scan records
 */
export const getHistory = async () => {
  try {
    const response = await api.get('/history');
    return response.data;
  } catch (error) {
    console.error('Error fetching history:', error);
    throw handleApiError(error);
  }
};

/**
 * Get specific scan by ID
 * @param {string} scanId - Scan identifier
 * @returns {Promise} - Scan record
 */
export const getHistoryById = async (scanId) => {
  try {
    const response = await api.get(`/history/${scanId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching history item:', error);
    throw handleApiError(error);
  }
};

/**
 * Get history statistics
 * @returns {Promise} - Statistics summary
 */
export const getHistoryStats = async () => {
  try {
    const response = await api.get('/history/stats/summary');
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw handleApiError(error);
  }
};

/**
 * Clear all history
 * @returns {Promise} - Success confirmation
 */
export const clearHistory = async () => {
  try {
    const response = await api.delete('/history');
    return response.data;
  } catch (error) {
    console.error('Error clearing history:', error);
    throw handleApiError(error);
  }
};

/**
 * Handle API errors consistently
 * @param {Error} error - Axios error object
 * @returns {Error} - Formatted error
 */
const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    const message = error.response.data?.detail || 
                   error.response.data?.message || 
                   'An error occurred while processing your request';
    return new Error(message);
  } else if (error.request) {
    // Request made but no response
    return new Error('Unable to connect to server. Please check your connection.');
  } else {
    // Something else happened
    return new Error(error.message || 'An unexpected error occurred');
  }
};

export default {
  scanImage,
  getScanStatus,
  getHistory,
  getHistoryById,
  getHistoryStats,
  clearHistory,
};
