"""
Face Detection Service
Uses MediaPipe Face Detection for robust face localization
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(
    model_selection=1,  # 1 for full-range detection (0-5 meters)
    min_detection_confidence=0.5
)

def detect_face(image: np.ndarray) -> Tuple[bool, Optional[np.ndarray], Optional[dict]]:
    """
    Detect face in image and return cropped face region
    
    Args:
        image: Input image (BGR format from OpenCV)
    
    Returns:
        Tuple of (success, cropped_face, bounding_box)
        - success: Boolean indicating if face was detected
        - cropped_face: Cropped face image
        - bounding_box: Dict with x, y, width, height
    """
    
    try:
        # Convert BGR to RGB for MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        results = face_detection.process(image_rgb)
        
        if not results.detections:
            logger.warning("No face detected in image")
            return False, None, None
        
        # Use first detected face
        detection = results.detections[0]
        
        # Get bounding box
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = image.shape
        
        # Convert relative coordinates to absolute
        x = int(bboxC.xmin * iw)
        y = int(bboxC.ymin * ih)
        w = int(bboxC.width * iw)
        h = int(bboxC.height * ih)
        
        # Add padding for better crop
        padding = 20
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(iw - x, w + 2 * padding)
        h = min(ih - y, h + 2 * padding)
        
        # Crop face
        face_crop = image[y:y+h, x:x+w]
        
        bbox = {
            "x": x,
            "y": y,
            "width": w,
            "height": h
        }
        
        logger.info(f"Face detected at: {bbox}")
        
        return True, face_crop, bbox
    
    except Exception as e:
        logger.error(f"Error in face detection: {str(e)}")
        return False, None, None

def validate_face_quality(image: np.ndarray) -> Tuple[bool, str]:
    """
    Validate if image quality is sufficient for analysis
    
    Args:
        image: Input image
    
    Returns:
        Tuple of (is_valid, message)
    """
    
    try:
        # Check image size
        if image.shape[0] < 100 or image.shape[1] < 100:
            return False, "Image resolution too low"
        
        # Check brightness
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        
        if mean_brightness < 30:
            return False, "Image too dark"
        elif mean_brightness > 225:
            return False, "Image too bright"
        
        # Check blur (Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        if laplacian_var < 100:
            return False, "Image too blurry"
        
        return True, "Image quality acceptable"
    
    except Exception as e:
        logger.error(f"Error validating image quality: {str(e)}")
        return False, f"Validation error: {str(e)}"
