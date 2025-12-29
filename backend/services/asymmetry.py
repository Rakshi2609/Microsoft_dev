"""
Asymmetry Feature Calculation Service
Computes facial asymmetry features for stroke risk assessment
"""

import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

def calculate_asymmetry_features(landmarks: Dict, image_shape: tuple) -> Dict[str, float]:
    """
    Calculate facial asymmetry features from landmarks
    
    Features computed:
    - Eye asymmetry (vertical position difference)
    - Mouth asymmetry (corner height difference)
    - Nose deviation (from vertical midline)
    - Face tilt angle
    - Left-right symmetry ratio
    
    Args:
        landmarks: Dictionary of facial landmarks
        image_shape: Shape of the image (height, width, channels)
    
    Returns:
        Dictionary of asymmetry features
    """
    
    try:
        centroids = landmarks.get("centroids", {})
        
        # Get key feature positions
        left_eye = centroids.get("left_eye", {"x": 0, "y": 0})
        right_eye = centroids.get("right_eye", {"x": 0, "y": 0})
        left_mouth = centroids.get("left_mouth", {"x": 0, "y": 0})
        right_mouth = centroids.get("right_mouth", {"x": 0, "y": 0})
        nose_tip = centroids.get("nose_tip", {"x": 0, "y": 0})
        left_cheek = centroids.get("left_cheek", {"x": 0, "y": 0})
        right_cheek = centroids.get("right_cheek", {"x": 0, "y": 0})
        
        # Image dimensions
        img_height, img_width = image_shape[:2]
        img_center_x = img_width / 2
        
        # Feature 1: Eye vertical asymmetry
        eye_diff = abs(left_eye["y"] - right_eye["y"]) / img_height
        
        # Feature 2: Mouth corner asymmetry
        mouth_diff = abs(left_mouth["y"] - right_mouth["y"]) / img_height
        
        # Feature 3: Nose deviation from center
        nose_deviation = abs(nose_tip["x"] - img_center_x) / img_width
        
        # Feature 4: Face tilt angle
        # Calculate angle between eye line and horizontal
        eye_dx = right_eye["x"] - left_eye["x"]
        eye_dy = right_eye["y"] - left_eye["y"]
        tilt_angle = abs(np.arctan2(eye_dy, eye_dx)) if eye_dx != 0 else 0
        
        # Feature 5: Left-right cheek symmetry ratio
        left_dist = np.linalg.norm(
            np.array([left_eye["x"], left_eye["y"]]) -
            np.array([left_cheek["x"], left_cheek["y"]])
        )
        right_dist = np.linalg.norm(
            np.array([right_eye["x"], right_eye["y"]]) -
            np.array([right_cheek["x"], right_cheek["y"]])
        )
        
        symmetry_ratio = min(left_dist, right_dist) / max(left_dist, right_dist) if max(left_dist, right_dist) > 0 else 1.0
        
        # Feature 6: Eye openness asymmetry
        from services.landmarks import get_eye_aspect_ratio
        left_eye_points = landmarks.get("left_eye", [])
        right_eye_points = landmarks.get("right_eye", [])
        
        left_ear = get_eye_aspect_ratio(left_eye_points)
        right_ear = get_eye_aspect_ratio(right_eye_points)
        eye_openness_diff = abs(left_ear - right_ear)
        
        # Feature 7: Mouth asymmetry ratio
        from services.landmarks import get_mouth_aspect_ratio
        left_mouth_points = landmarks.get("left_mouth", [])
        right_mouth_points = landmarks.get("right_mouth", [])
        
        left_mar = get_mouth_aspect_ratio(left_mouth_points)
        right_mar = get_mouth_aspect_ratio(right_mouth_points)
        mouth_ratio_diff = abs(left_mar - right_mar)
        
        features = {
            "eye_diff": float(eye_diff),
            "mouth_diff": float(mouth_diff),
            "nose_deviation": float(nose_deviation),
            "tilt_angle": float(tilt_angle),
            "symmetry_ratio": float(symmetry_ratio),
            "eye_openness_diff": float(eye_openness_diff),
            "mouth_ratio_diff": float(mouth_ratio_diff)
        }
        
        logger.info(f"Asymmetry features calculated: {features}")
        
        return features
    
    except Exception as e:
        logger.error(f"Error calculating asymmetry features: {str(e)}")
        # Return default features
        return {
            "eye_diff": 0.0,
            "mouth_diff": 0.0,
            "nose_deviation": 0.0,
            "tilt_angle": 0.0,
            "symmetry_ratio": 1.0,
            "eye_openness_diff": 0.0,
            "mouth_ratio_diff": 0.0
        }

def calculate_asymmetry_score(features: Dict[str, float]) -> float:
    """
    Calculate overall asymmetry score (0-1, higher = more asymmetric)
    
    Args:
        features: Dictionary of asymmetry features
    
    Returns:
        Overall asymmetry score
    """
    
    try:
        # Weighted combination of features
        weights = {
            "eye_diff": 0.25,
            "mouth_diff": 0.25,
            "nose_deviation": 0.15,
            "tilt_angle": 0.10,
            "symmetry_ratio": -0.10,  # Negative because higher ratio means more symmetric
            "eye_openness_diff": 0.15,
            "mouth_ratio_diff": 0.10
        }
        
        score = 0.0
        for feature, weight in weights.items():
            value = features.get(feature, 0.0)
            if feature == "symmetry_ratio":
                # Invert symmetry ratio (1.0 = symmetric, 0 = asymmetric)
                value = 1.0 - value
            score += weight * value
        
        # Normalize to 0-1 range
        score = max(0.0, min(1.0, score))
        
        return score
    
    except Exception as e:
        logger.error(f"Error calculating asymmetry score: {str(e)}")
        return 0.0

def get_feature_importance() -> Dict[str, float]:
    """
    Get feature importance weights for explainability
    
    Returns:
        Dictionary mapping feature names to importance weights
    """
    return {
        "eye_diff": 0.25,
        "mouth_diff": 0.25,
        "eye_openness_diff": 0.15,
        "nose_deviation": 0.15,
        "mouth_ratio_diff": 0.10,
        "tilt_angle": 0.10
    }
