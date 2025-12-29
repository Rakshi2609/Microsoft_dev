"""
Risk Prediction Model Service
Combines MobileNet and asymmetry features to predict stroke risk
"""

import numpy as np
from typing import Dict, Any
import logging
import os

logger = logging.getLogger(__name__)

# Try to load trained classifier if available
try:
    import joblib
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "classifier.pkl")
    
    if os.path.exists(MODEL_PATH):
        classifier = joblib.load(MODEL_PATH)
        logger.info("Trained classifier loaded successfully")
        USE_TRAINED_MODEL = True
    else:
        logger.warning("No trained classifier found, using rule-based model")
        USE_TRAINED_MODEL = False
except Exception as e:
    logger.warning(f"Could not load classifier: {str(e)}, using rule-based model")
    USE_TRAINED_MODEL = False

def predict_risk(mobilenet_features: np.ndarray, asymmetry_features: Dict[str, float]) -> Dict[str, Any]:
    """
    Predict stroke risk level from combined features
    
    Args:
        mobilenet_features: MobileNet feature embeddings (1280-dim)
        asymmetry_features: Dictionary of asymmetry feature values
    
    Returns:
        Dictionary containing risk level, confidence, score, and explanation
    """
    
    try:
        if USE_TRAINED_MODEL:
            # Use trained ML classifier
            return predict_with_classifier(mobilenet_features, asymmetry_features)
        else:
            # Use rule-based heuristic model
            return predict_with_rules(asymmetry_features)
    
    except Exception as e:
        logger.error(f"Error in risk prediction: {str(e)}")
        # Return safe default
        return {
            "risk_level": "Low",
            "confidence": 0.5,
            "score": 0.0,
            "explanation": "Error in prediction, defaulting to Low risk"
        }

def predict_with_classifier(mobilenet_features: np.ndarray, asymmetry_features: Dict[str, float]) -> Dict[str, Any]:
    """
    Predict using trained ML classifier
    
    Args:
        mobilenet_features: MobileNet embeddings
        asymmetry_features: Asymmetry features
    
    Returns:
        Prediction results
    """
    
    try:
        # Combine features
        combined_features = combine_features(mobilenet_features, asymmetry_features)
        
        # Reshape for prediction
        X = combined_features.reshape(1, -1)
        
        # Predict
        prediction = classifier.predict(X)[0]
        probabilities = classifier.predict_proba(X)[0]
        
        # Map prediction to risk level
        risk_levels = ["Low", "Medium", "High"]
        risk_level = risk_levels[prediction]
        confidence = probabilities[prediction]
        
        # Calculate overall score
        score = calculate_risk_score(asymmetry_features)
        
        return {
            "risk_level": risk_level,
            "confidence": float(confidence),
            "score": float(score),
            "explanation": f"ML model prediction based on {len(combined_features)} features"
        }
    
    except Exception as e:
        logger.error(f"Error in classifier prediction: {str(e)}")
        return predict_with_rules(asymmetry_features)

def predict_with_rules(asymmetry_features: Dict[str, float]) -> Dict[str, Any]:
    """
    Rule-based risk prediction (fallback for demo/hackathon)
    
    Based on facial asymmetry thresholds:
    - Low: score < 0.3
    - Medium: 0.3 <= score < 0.6
    - High: score >= 0.6
    
    Args:
        asymmetry_features: Dictionary of asymmetry features
    
    Returns:
        Prediction results
    """
    
    try:
        # Calculate weighted risk score
        score = calculate_risk_score(asymmetry_features)
        
        # Determine risk level based on thresholds
        if score < 0.3:
            risk_level = "Low"
            confidence = 0.85 - score  # Higher confidence for lower scores
        elif score < 0.6:
            risk_level = "Medium"
            confidence = 0.70 + (score - 0.3) * 0.2  # Moderate confidence
        else:
            risk_level = "High"
            confidence = 0.75 + (score - 0.6) * 0.5  # Higher confidence for higher scores
        
        # Cap confidence at 0.95 for rule-based system
        confidence = min(0.95, confidence)
        
        explanation = generate_explanation(asymmetry_features, risk_level)
        
        return {
            "risk_level": risk_level,
            "confidence": float(confidence),
            "score": float(score),
            "explanation": explanation
        }
    
    except Exception as e:
        logger.error(f"Error in rule-based prediction: {str(e)}")
        return {
            "risk_level": "Low",
            "confidence": 0.5,
            "score": 0.0,
            "explanation": "Error in calculation"
        }

def calculate_risk_score(asymmetry_features: Dict[str, float]) -> float:
    """
    Calculate overall risk score (0-1) from asymmetry features
    
    Args:
        asymmetry_features: Dictionary of feature values
    
    Returns:
        Risk score between 0 and 1
    """
    
    # Feature weights based on clinical relevance
    weights = {
        "eye_diff": 0.20,
        "mouth_diff": 0.25,
        "eye_openness_diff": 0.20,
        "nose_deviation": 0.15,
        "mouth_ratio_diff": 0.10,
        "tilt_angle": 0.10
    }
    
    score = 0.0
    
    for feature, weight in weights.items():
        value = asymmetry_features.get(feature, 0.0)
        
        # Apply non-linear scaling for better discrimination
        scaled_value = np.tanh(value * 10)  # Sigmoid-like scaling
        
        score += weight * scaled_value
    
    # Normalize to 0-1
    score = max(0.0, min(1.0, score))
    
    return score

def combine_features(mobilenet_features: np.ndarray, asymmetry_features: Dict[str, float]) -> np.ndarray:
    """
    Combine MobileNet and asymmetry features into single feature vector
    
    Args:
        mobilenet_features: MobileNet embeddings (1280-dim)
        asymmetry_features: Asymmetry features dict
    
    Returns:
        Combined feature vector
    """
    
    # Extract asymmetry values in consistent order
    asymmetry_values = np.array([
        asymmetry_features.get("eye_diff", 0.0),
        asymmetry_features.get("mouth_diff", 0.0),
        asymmetry_features.get("nose_deviation", 0.0),
        asymmetry_features.get("tilt_angle", 0.0),
        asymmetry_features.get("symmetry_ratio", 1.0),
        asymmetry_features.get("eye_openness_diff", 0.0),
        asymmetry_features.get("mouth_ratio_diff", 0.0)
    ])
    
    # Concatenate
    combined = np.concatenate([mobilenet_features, asymmetry_values])
    
    return combined

def generate_explanation(asymmetry_features: Dict[str, float], risk_level: str) -> str:
    """
    Generate human-readable explanation of the prediction
    
    Args:
        asymmetry_features: Feature values
        risk_level: Predicted risk level
    
    Returns:
        Explanation string
    """
    
    # Find most significant features
    significant_features = []
    
    if asymmetry_features.get("eye_diff", 0) > 0.15:
        significant_features.append("notable eye asymmetry")
    
    if asymmetry_features.get("mouth_diff", 0) > 0.15:
        significant_features.append("mouth corner asymmetry")
    
    if asymmetry_features.get("eye_openness_diff", 0) > 0.10:
        significant_features.append("uneven eye openness")
    
    if asymmetry_features.get("nose_deviation", 0) > 0.10:
        significant_features.append("nose alignment deviation")
    
    if significant_features:
        features_text = ", ".join(significant_features)
        explanation = f"{risk_level} risk detected based on: {features_text}."
    else:
        explanation = f"{risk_level} risk - facial features appear relatively symmetric."
    
    return explanation

def get_risk_thresholds() -> Dict[str, tuple]:
    """
    Get risk level thresholds for reference
    
    Returns:
        Dictionary mapping risk levels to (min_score, max_score) tuples
    """
    return {
        "Low": (0.0, 0.3),
        "Medium": (0.3, 0.6),
        "High": (0.6, 1.0)
    }
