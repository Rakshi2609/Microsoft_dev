"""
Facial Landmarks Extraction Service
Uses MediaPipe Face Mesh for detailed facial landmark detection
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Key landmark indices for facial features
# Based on MediaPipe Face Mesh 468 landmarks
LANDMARK_INDICES = {
    "left_eye": [33, 133, 160, 159, 158, 157, 173],
    "right_eye": [362, 263, 387, 386, 385, 384, 398],
    "left_mouth": [61, 91, 181, 84],
    "right_mouth": [291, 321, 405, 314],
    "nose_tip": [1],
    "nose_bridge": [6],
    "left_cheek": [234],
    "right_cheek": [454],
    "chin": [152],
    "forehead": [10]
}

def extract_landmarks(image: np.ndarray, face_bbox: Optional[Dict] = None) -> Tuple[bool, Optional[Dict]]:
    """
    Extract facial landmarks from image
    
    Args:
        image: Input image (BGR format)
        face_bbox: Optional face bounding box for validation
    
    Returns:
        Tuple of (success, landmarks_dict)
    """
    
    try:
        # Convert to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process image
        results = face_mesh.process(image_rgb)
        
        if not results.multi_face_landmarks:
            logger.warning("No facial landmarks detected")
            return False, None
        
        # Get first face landmarks
        face_landmarks = results.multi_face_landmarks[0]
        
        # Convert to pixel coordinates
        ih, iw, _ = image.shape
        landmarks_dict = {}
        
        for feature_name, indices in LANDMARK_INDICES.items():
            landmarks_dict[feature_name] = []
            
            for idx in indices:
                if idx < len(face_landmarks.landmark):
                    landmark = face_landmarks.landmark[idx]
                    x = int(landmark.x * iw)
                    y = int(landmark.y * ih)
                    z = landmark.z  # Depth information
                    
                    landmarks_dict[feature_name].append({
                        "x": x,
                        "y": y,
                        "z": z
                    })
        
        # Calculate landmark centroids for key features
        landmarks_dict["centroids"] = calculate_centroids(landmarks_dict)
        
        logger.info(f"Successfully extracted landmarks for {len(LANDMARK_INDICES)} features")
        
        return True, landmarks_dict
    
    except Exception as e:
        logger.error(f"Error extracting landmarks: {str(e)}")
        return False, None

def calculate_centroids(landmarks: Dict) -> Dict:
    """
    Calculate centroid positions for facial features
    
    Args:
        landmarks: Dictionary of landmark coordinates
    
    Returns:
        Dictionary of centroid coordinates
    """
    
    centroids = {}
    
    for feature_name, points in landmarks.items():
        if feature_name == "centroids":
            continue
        
        if points and len(points) > 0:
            x_coords = [p["x"] for p in points]
            y_coords = [p["y"] for p in points]
            
            centroids[feature_name] = {
                "x": np.mean(x_coords),
                "y": np.mean(y_coords)
            }
    
    return centroids

def get_eye_aspect_ratio(eye_landmarks: List[Dict]) -> float:
    """
    Calculate Eye Aspect Ratio (EAR) for eye openness detection
    
    Args:
        eye_landmarks: List of eye landmark coordinates
    
    Returns:
        Eye aspect ratio value
    """
    
    try:
        if len(eye_landmarks) < 6:
            return 0.0
        
        # Vertical distances
        v1 = np.linalg.norm(
            np.array([eye_landmarks[1]["x"], eye_landmarks[1]["y"]]) -
            np.array([eye_landmarks[5]["x"], eye_landmarks[5]["y"]])
        )
        v2 = np.linalg.norm(
            np.array([eye_landmarks[2]["x"], eye_landmarks[2]["y"]]) -
            np.array([eye_landmarks[4]["x"], eye_landmarks[4]["y"]])
        )
        
        # Horizontal distance
        h = np.linalg.norm(
            np.array([eye_landmarks[0]["x"], eye_landmarks[0]["y"]]) -
            np.array([eye_landmarks[3]["x"], eye_landmarks[3]["y"]])
        )
        
        # Calculate EAR
        ear = (v1 + v2) / (2.0 * h)
        
        return ear
    
    except Exception as e:
        logger.error(f"Error calculating EAR: {str(e)}")
        return 0.0

def get_mouth_aspect_ratio(mouth_landmarks: List[Dict]) -> float:
    """
    Calculate Mouth Aspect Ratio (MAR) for mouth openness
    
    Args:
        mouth_landmarks: List of mouth landmark coordinates
    
    Returns:
        Mouth aspect ratio value
    """
    
    try:
        if len(mouth_landmarks) < 4:
            return 0.0
        
        # Vertical distance
        v = np.linalg.norm(
            np.array([mouth_landmarks[1]["x"], mouth_landmarks[1]["y"]]) -
            np.array([mouth_landmarks[3]["x"], mouth_landmarks[3]["y"]])
        )
        
        # Horizontal distance
        h = np.linalg.norm(
            np.array([mouth_landmarks[0]["x"], mouth_landmarks[0]["y"]]) -
            np.array([mouth_landmarks[2]["x"], mouth_landmarks[2]["y"]])
        )
        
        # Calculate MAR
        mar = v / h if h > 0 else 0.0
        
        return mar
    
    except Exception as e:
        logger.error(f"Error calculating MAR: {str(e)}")
        return 0.0
