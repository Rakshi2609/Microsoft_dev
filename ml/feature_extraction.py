"""
MobileNet Feature Extraction Training Script
Extracts features from face images for classifier training

This script:
1. Loads face images from a dataset
2. Detects faces using MediaPipe
3. Extracts MobileNet embeddings
4. Extracts asymmetry features from landmarks
5. Saves combined features for classifier training
"""

import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
import logging
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.face_detection import detect_face
from services.landmarks import extract_landmarks
from services.mobilenet_features import extract_mobilenet_features
from services.asymmetry import calculate_asymmetry_features

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_features_from_image(image_path: str) -> tuple:
    """
    Extract all features from a single image
    
    Args:
        image_path: Path to image file
    
    Returns:
        Tuple of (mobilenet_features, asymmetry_features, success)
    """
    
    try:
        # Read image
        img = cv2.imread(image_path)
        
        if img is None:
            logger.error(f"Failed to read image: {image_path}")
            return None, None, False
        
        # Detect face
        face_detected, face_crop, face_bbox = detect_face(img)
        
        if not face_detected:
            logger.warning(f"No face detected in: {image_path}")
            return None, None, False
        
        # Extract landmarks
        landmarks_success, landmarks = extract_landmarks(img, face_bbox)
        
        if not landmarks_success:
            logger.warning(f"Failed to extract landmarks: {image_path}")
            return None, None, False
        
        # Extract MobileNet features
        mobilenet_features = extract_mobilenet_features(face_crop)
        
        # Calculate asymmetry features
        asymmetry_features = calculate_asymmetry_features(landmarks, img.shape)
        
        return mobilenet_features, asymmetry_features, True
    
    except Exception as e:
        logger.error(f"Error processing {image_path}: {str(e)}")
        return None, None, False

def process_dataset(dataset_dir: str, output_file: str):
    """
    Process entire dataset and extract features
    
    Expected directory structure:
    dataset_dir/
        low/
            image1.jpg
            image2.jpg
        medium/
            image1.jpg
        high/
            image1.jpg
    
    Args:
        dataset_dir: Root directory containing class subdirectories
        output_file: Path to save extracted features CSV
    """
    
    logger.info(f"Processing dataset from: {dataset_dir}")
    
    # Risk level mapping
    risk_labels = {
        "low": 0,
        "medium": 1,
        "high": 2
    }
    
    all_features = []
    all_labels = []
    
    # Process each risk level directory
    for risk_level, label in risk_labels.items():
        risk_dir = os.path.join(dataset_dir, risk_level)
        
        if not os.path.exists(risk_dir):
            logger.warning(f"Directory not found: {risk_dir}")
            continue
        
        logger.info(f"Processing {risk_level} risk images...")
        
        # Get all image files
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            image_files.extend(Path(risk_dir).glob(ext))
        
        logger.info(f"Found {len(image_files)} images in {risk_level}")
        
        for img_path in image_files:
            # Extract features
            mobilenet_feat, asymmetry_feat, success = extract_features_from_image(str(img_path))
            
            if not success:
                continue
            
            # Combine features
            feature_vector = np.concatenate([
                mobilenet_feat,
                np.array([
                    asymmetry_feat["eye_diff"],
                    asymmetry_feat["mouth_diff"],
                    asymmetry_feat["nose_deviation"],
                    asymmetry_feat["tilt_angle"],
                    asymmetry_feat["symmetry_ratio"],
                    asymmetry_feat["eye_openness_diff"],
                    asymmetry_feat["mouth_ratio_diff"]
                ])
            ])
            
            all_features.append(feature_vector)
            all_labels.append(label)
            
            logger.info(f"Processed: {img_path.name} -> {risk_level}")
    
    if not all_features:
        logger.error("No features extracted! Check your dataset.")
        return
    
    # Convert to arrays
    X = np.array(all_features)
    y = np.array(all_labels)
    
    logger.info(f"Total samples: {len(X)}")
    logger.info(f"Feature dimensions: {X.shape[1]}")
    logger.info(f"Class distribution: {np.bincount(y)}")
    
    # Save to CSV
    # Create column names
    mobilenet_cols = [f"mobilenet_{i}" for i in range(1280)]
    asymmetry_cols = [
        "eye_diff", "mouth_diff", "nose_deviation", 
        "tilt_angle", "symmetry_ratio", 
        "eye_openness_diff", "mouth_ratio_diff"
    ]
    column_names = mobilenet_cols + asymmetry_cols + ["label"]
    
    # Create DataFrame
    df_data = np.column_stack([X, y])
    df = pd.DataFrame(df_data, columns=column_names)
    
    # Save
    df.to_csv(output_file, index=False)
    logger.info(f"Features saved to: {output_file}")
    
    # Save feature statistics
    stats_file = output_file.replace(".csv", "_stats.txt")
    with open(stats_file, 'w') as f:
        f.write(f"Dataset Statistics\n")
        f.write(f"==================\n\n")
        f.write(f"Total samples: {len(X)}\n")
        f.write(f"Feature dimensions: {X.shape[1]}\n")
        f.write(f"Class distribution:\n")
        for risk_level, label in risk_labels.items():
            count = np.sum(y == label)
            f.write(f"  {risk_level}: {count} ({count/len(y)*100:.1f}%)\n")
        f.write(f"\nAsymmetry Feature Statistics:\n")
        for i, col in enumerate(asymmetry_cols):
            values = X[:, 1280 + i]
            f.write(f"  {col}: mean={np.mean(values):.4f}, std={np.std(values):.4f}\n")
    
    logger.info(f"Statistics saved to: {stats_file}")

def create_synthetic_dataset(output_dir: str, num_samples_per_class: int = 50):
    """
    Create a synthetic dataset for demo/testing purposes
    
    This generates random feature vectors with realistic distributions
    for hackathon demonstration when real data is not available.
    
    Args:
        output_dir: Directory to save synthetic data
        num_samples_per_class: Number of samples per risk class
    """
    
    logger.info("Creating synthetic dataset for demo purposes...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    all_features = []
    all_labels = []
    
    for label in range(3):  # Low, Medium, High
        for _ in range(num_samples_per_class):
            # Generate synthetic MobileNet features (1280-dim)
            mobilenet_feat = np.random.randn(1280) * 0.5
            
            # Generate synthetic asymmetry features with class-dependent distributions
            if label == 0:  # Low risk
                eye_diff = np.random.uniform(0.0, 0.1)
                mouth_diff = np.random.uniform(0.0, 0.1)
                nose_dev = np.random.uniform(0.0, 0.08)
                tilt = np.random.uniform(0.0, 0.05)
                symmetry = np.random.uniform(0.9, 1.0)
                eye_open_diff = np.random.uniform(0.0, 0.08)
                mouth_ratio_diff = np.random.uniform(0.0, 0.08)
            elif label == 1:  # Medium risk
                eye_diff = np.random.uniform(0.08, 0.20)
                mouth_diff = np.random.uniform(0.08, 0.20)
                nose_dev = np.random.uniform(0.06, 0.15)
                tilt = np.random.uniform(0.04, 0.12)
                symmetry = np.random.uniform(0.7, 0.9)
                eye_open_diff = np.random.uniform(0.07, 0.15)
                mouth_ratio_diff = np.random.uniform(0.07, 0.15)
            else:  # High risk
                eye_diff = np.random.uniform(0.15, 0.35)
                mouth_diff = np.random.uniform(0.15, 0.35)
                nose_dev = np.random.uniform(0.12, 0.25)
                tilt = np.random.uniform(0.10, 0.20)
                symmetry = np.random.uniform(0.4, 0.7)
                eye_open_diff = np.random.uniform(0.12, 0.25)
                mouth_ratio_diff = np.random.uniform(0.12, 0.25)
            
            asymmetry_feat = np.array([
                eye_diff, mouth_diff, nose_dev, tilt, 
                symmetry, eye_open_diff, mouth_ratio_diff
            ])
            
            # Combine features
            feature_vector = np.concatenate([mobilenet_feat, asymmetry_feat])
            
            all_features.append(feature_vector)
            all_labels.append(label)
    
    # Save to CSV
    X = np.array(all_features)
    y = np.array(all_labels)
    
    mobilenet_cols = [f"mobilenet_{i}" for i in range(1280)]
    asymmetry_cols = [
        "eye_diff", "mouth_diff", "nose_deviation", 
        "tilt_angle", "symmetry_ratio", 
        "eye_openness_diff", "mouth_ratio_diff"
    ]
    column_names = mobilenet_cols + asymmetry_cols + ["label"]
    
    df_data = np.column_stack([X, y])
    df = pd.DataFrame(df_data, columns=column_names)
    
    output_file = os.path.join(output_dir, "synthetic_dataset.csv")
    df.to_csv(output_file, index=False)
    
    logger.info(f"Synthetic dataset created: {output_file}")
    logger.info(f"Total samples: {len(X)} ({num_samples_per_class} per class)")

if __name__ == "__main__":
    # Example usage
    
    # Option 1: Process real dataset
    # process_dataset(
    #     dataset_dir="./dataset",
    #     output_file="./ml/features_dataset.csv"
    # )
    
    # Option 2: Create synthetic dataset for demo
    create_synthetic_dataset(
        output_dir="./ml",
        num_samples_per_class=50
    )
    
    logger.info("Feature extraction complete!")
