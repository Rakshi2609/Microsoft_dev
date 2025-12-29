"""
Classifier Training Script
Trains a classifier on extracted features for stroke risk prediction

This script:
1. Loads feature dataset (from feature_extraction.py)
2. Splits into train/test sets
3. Trains multiple classifiers (Logistic Regression, Random Forest, etc.)
4. Evaluates performance
5. Saves best model
"""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score,
    f1_score,
    roc_auc_score
)
import logging
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_dataset(csv_path: str):
    """
    Load feature dataset from CSV
    
    Args:
        csv_path: Path to CSV file with features
    
    Returns:
        Tuple of (X, y, feature_names)
    """
    
    logger.info(f"Loading dataset from: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Separate features and labels
    X = df.drop('label', axis=1).values
    y = df['label'].values
    feature_names = df.drop('label', axis=1).columns.tolist()
    
    logger.info(f"Loaded {len(X)} samples with {X.shape[1]} features")
    logger.info(f"Class distribution: {np.bincount(y.astype(int))}")
    
    return X, y, feature_names

def train_classifiers(X_train, y_train, X_test, y_test):
    """
    Train multiple classifiers and compare performance
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_test: Test features
        y_test: Test labels
    
    Returns:
        Dictionary of trained models with their scores
    """
    
    logger.info("Training classifiers...")
    
    # Define classifiers
    classifiers = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            class_weight='balanced',
            random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',
            random_state=42
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        ),
        "SVM": SVC(
            kernel='rbf',
            probability=True,
            class_weight='balanced',
            random_state=42
        )
    }
    
    results = {}
    
    for name, clf in classifiers.items():
        logger.info(f"\nTraining {name}...")
        
        # Train
        clf.fit(X_train, y_train)
        
        # Predict
        y_pred = clf.predict(X_test)
        y_pred_proba = clf.predict_proba(X_test)
        
        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        # Cross-validation score
        cv_scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='f1_weighted')
        
        results[name] = {
            "model": clf,
            "accuracy": accuracy,
            "f1_score": f1,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
            "predictions": y_pred,
            "probabilities": y_pred_proba
        }
        
        logger.info(f"{name} Results:")
        logger.info(f"  Accuracy: {accuracy:.4f}")
        logger.info(f"  F1 Score: {f1:.4f}")
        logger.info(f"  CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        # Classification report
        print(f"\n{name} Classification Report:")
        print(classification_report(y_test, y_pred, target_names=['Low', 'Medium', 'High']))
    
    return results

def plot_confusion_matrices(results, y_test, output_dir):
    """
    Plot confusion matrices for all classifiers
    
    Args:
        results: Dictionary of classifier results
        y_test: Test labels
        output_dir: Directory to save plots
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.ravel()
    
    for idx, (name, result) in enumerate(results.items()):
        cm = confusion_matrix(y_test, result['predictions'])
        
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=['Low', 'Medium', 'High'],
            yticklabels=['Low', 'Medium', 'High'],
            ax=axes[idx]
        )
        axes[idx].set_title(f'{name}\nAccuracy: {result["accuracy"]:.3f}')
        axes[idx].set_ylabel('True Label')
        axes[idx].set_xlabel('Predicted Label')
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'confusion_matrices.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    logger.info(f"Confusion matrices saved to: {plot_path}")
    plt.close()

def save_best_model(results, scaler, output_dir):
    """
    Save the best performing model
    
    Args:
        results: Dictionary of classifier results
        scaler: Fitted StandardScaler
        output_dir: Directory to save model
    """
    
    # Find best model by F1 score
    best_name = max(results.items(), key=lambda x: x[1]['f1_score'])[0]
    best_model = results[best_name]['model']
    best_f1 = results[best_name]['f1_score']
    
    logger.info(f"\nBest model: {best_name} (F1: {best_f1:.4f})")
    
    # Save model
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, 'classifier.pkl')
    scaler_path = os.path.join(output_dir, 'scaler.pkl')
    
    joblib.dump(best_model, model_path)
    joblib.dump(scaler, scaler_path)
    
    logger.info(f"Model saved to: {model_path}")
    logger.info(f"Scaler saved to: {scaler_path}")
    
    # Save model metadata
    metadata = {
        "model_type": best_name,
        "f1_score": best_f1,
        "accuracy": results[best_name]['accuracy'],
        "cv_mean": results[best_name]['cv_mean'],
        "cv_std": results[best_name]['cv_std'],
        "classes": ["Low", "Medium", "High"]
    }
    
    metadata_path = os.path.join(output_dir, 'model_metadata.txt')
    with open(metadata_path, 'w') as f:
        f.write("Model Metadata\n")
        f.write("==============\n\n")
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")
    
    logger.info(f"Metadata saved to: {metadata_path}")

def main():
    """Main training pipeline"""
    
    # Paths
    dataset_path = "./ml/synthetic_dataset.csv"  # Change to your dataset
    models_dir = "../backend/models"
    plots_dir = "./ml/plots"
    
    # Load dataset
    X, y, feature_names = load_dataset(dataset_path)
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42,
        stratify=y
    )
    
    logger.info(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    logger.info("Features scaled using StandardScaler")
    
    # Train classifiers
    results = train_classifiers(X_train_scaled, y_train, X_test_scaled, y_test)
    
    # Plot results
    plot_confusion_matrices(results, y_test, plots_dir)
    
    # Save best model
    save_best_model(results, scaler, models_dir)
    
    logger.info("\n✅ Training complete!")
    
    # Print summary
    print("\n" + "="*60)
    print("TRAINING SUMMARY")
    print("="*60)
    for name, result in results.items():
        print(f"\n{name}:")
        print(f"  Accuracy:  {result['accuracy']:.4f}")
        print(f"  F1 Score:  {result['f1_score']:.4f}")
        print(f"  CV Score:  {result['cv_mean']:.4f} ± {result['cv_std']:.4f}")
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
