"""
Scan Route - Image Upload and Risk Assessment
Handles facial analysis and stroke risk prediction
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from datetime import datetime
import logging
from typing import Dict, Any

from services.face_detection import detect_face
from services.landmarks import extract_landmarks
from services.mobilenet_features import extract_mobilenet_features
from services.asymmetry import calculate_asymmetry_features
from services.risk_model import predict_risk
from services.history_manager import save_scan_result

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/scan/image")
async def scan_image(image: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Analyze uploaded image for stroke risk assessment
    
    Args:
        image: Uploaded image file (JPG/PNG)
    
    Returns:
        Risk assessment results with confidence, score, and feature breakdown
    """
    
    try:
        # Validate file type
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload a JPG or PNG image."
            )
        
        # Read image
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(
                status_code=400,
                detail="Failed to decode image. Please upload a valid image file."
            )
        
        logger.info(f"Image received: {img.shape}")
        
        # Step 1: Detect face
        face_detected, face_crop, face_bbox = detect_face(img)
        
        if not face_detected:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "No face detected",
                    "message": "Please ensure your face is clearly visible in the image.",
                    "suggestions": [
                        "Make sure there is adequate lighting",
                        "Face the camera directly",
                        "Remove any obstructions"
                    ]
                }
            )
        
        logger.info("Face detected successfully")
        
        # Step 2: Extract facial landmarks
        landmarks_success, landmarks = extract_landmarks(img, face_bbox)
        
        if not landmarks_success:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Failed to extract facial landmarks",
                    "message": "Please try again with a clearer image."
                }
            )
        
        logger.info(f"Extracted {len(landmarks)} facial landmarks")
        
        # Step 3: Extract MobileNet features
        mobilenet_features = extract_mobilenet_features(face_crop)
        logger.info(f"MobileNet features extracted: {mobilenet_features.shape}")
        
        # Step 4: Calculate asymmetry features
        asymmetry_features = calculate_asymmetry_features(landmarks, img.shape)
        logger.info(f"Asymmetry features calculated: {asymmetry_features}")
        
        # Step 5: Predict risk
        risk_result = predict_risk(mobilenet_features, asymmetry_features)
        
        # Step 6: Prepare response
        result = {
            "risk": risk_result["risk_level"],
            "confidence": round(risk_result["confidence"], 2),
            "score": round(risk_result["score"], 2),
            "features": {
                "eye_asymmetry": round(asymmetry_features.get("eye_diff", 0), 3),
                "mouth_asymmetry": round(asymmetry_features.get("mouth_diff", 0), 3),
                "nose_deviation": round(asymmetry_features.get("nose_deviation", 0), 3),
                "face_tilt": round(asymmetry_features.get("tilt_angle", 0), 3),
                "symmetry_ratio": round(asymmetry_features.get("symmetry_ratio", 0), 3)
            },
            "timestamp": datetime.now().isoformat(),
            "disclaimer": "This is a pre-diagnostic screening tool. Consult a healthcare professional for medical diagnosis."
        }
        
        # Step 7: Save to history
        save_scan_result(result)
        
        logger.info(f"Risk assessment complete: {result['risk']} ({result['confidence']})")
        
        return result
    
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/scan/status")
async def scan_status():
    """Check if scan service is operational"""
    return {
        "status": "operational",
        "services": {
            "face_detection": "ready",
            "landmark_extraction": "ready",
            "mobilenet": "ready",
            "risk_model": "ready"
        }
    }
