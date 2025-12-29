"""
MobileNet Feature Extraction Service
Uses pretrained MobileNetV2 for facial feature encoding
"""

import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Model
import logging

logger = logging.getLogger(__name__)

# Initialize MobileNetV2 (load once at module level)
# Remove top classification layer to get feature embeddings
logger.info("Loading MobileNetV2 model...")
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg'  # Global average pooling
)

# Model is frozen for feature extraction only
base_model.trainable = False

logger.info("MobileNetV2 loaded successfully")

def extract_mobilenet_features(face_image: np.ndarray) -> np.ndarray:
    """
    Extract feature embeddings from face image using MobileNetV2
    
    Args:
        face_image: Cropped face image (BGR format from OpenCV)
    
    Returns:
        Feature vector (1280-dimensional for MobileNetV2)
    """
    
    try:
        # Resize to MobileNet input size
        face_resized = cv2.resize(face_image, (224, 224))
        
        # Convert BGR to RGB
        face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
        
        # Expand dimensions for batch processing
        face_batch = np.expand_dims(face_rgb, axis=0)
        
        # Preprocess for MobileNet
        face_preprocessed = preprocess_input(face_batch.astype(np.float32))
        
        # Extract features
        features = base_model.predict(face_preprocessed, verbose=0)
        
        # Flatten to 1D array
        feature_vector = features.flatten()
        
        logger.info(f"Extracted MobileNet features: shape={feature_vector.shape}")
        
        return feature_vector
    
    except Exception as e:
        logger.error(f"Error extracting MobileNet features: {str(e)}")
        # Return zero vector as fallback
        return np.zeros(1280)

def get_feature_dimension() -> int:
    """
    Get the dimension of MobileNet feature vectors
    
    Returns:
        Feature dimension (1280 for MobileNetV2)
    """
    return 1280

def normalize_features(features: np.ndarray) -> np.ndarray:
    """
    Normalize feature vector using L2 normalization
    
    Args:
        features: Input feature vector
    
    Returns:
        Normalized feature vector
    """
    
    try:
        norm = np.linalg.norm(features)
        if norm > 0:
            return features / norm
        return features
    
    except Exception as e:
        logger.error(f"Error normalizing features: {str(e)}")
        return features
