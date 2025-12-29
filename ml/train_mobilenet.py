"""
MobileNet Transfer Learning Training (Optional)
Fine-tune MobileNetV2 on facial asymmetry dataset

Note: This is optional - the default MobileNetV2 pretrained on ImageNet
works well for feature extraction. This script is for advanced fine-tuning
if you have a large labeled dataset of faces.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_model(num_classes=3, input_shape=(224, 224, 3)):
    """
    Create MobileNetV2-based model for facial asymmetry classification
    
    Args:
        num_classes: Number of risk classes (Low, Medium, High)
        input_shape: Input image shape
    
    Returns:
        Compiled Keras model
    """
    
    # Load pretrained MobileNetV2
    base_model = MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model layers initially
    base_model.trainable = False
    
    # Build model
    inputs = keras.Input(shape=input_shape)
    
    # Preprocessing
    x = keras.applications.mobilenet_v2.preprocess_input(inputs)
    
    # Base model
    x = base_model(x, training=False)
    
    # Global pooling
    x = layers.GlobalAveragePooling2D()(x)
    
    # Dense layers
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    
    # Output layer
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    # Create model
    model = keras.Model(inputs, outputs)
    
    return model, base_model

def train_model(data_dir, output_dir, epochs=50, batch_size=32):
    """
    Train MobileNet model on facial dataset
    
    Expected directory structure:
    data_dir/
        train/
            low/
            medium/
            high/
        validation/
            low/
            medium/
            high/
    
    Args:
        data_dir: Root directory with train/validation splits
        output_dir: Directory to save trained model
        epochs: Number of training epochs
        batch_size: Batch size
    """
    
    logger.info("Creating model...")
    model, base_model = create_model()
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    )
    
    logger.info(model.summary())
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.1,
        brightness_range=[0.9, 1.1]
    )
    
    # No augmentation for validation
    val_datagen = ImageDataGenerator()
    
    # Load data
    train_generator = train_datagen.flow_from_directory(
        os.path.join(data_dir, 'train'),
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True
    )
    
    val_generator = val_datagen.flow_from_directory(
        os.path.join(data_dir, 'validation'),
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )
    
    # Callbacks
    os.makedirs(output_dir, exist_ok=True)
    
    callbacks = [
        ModelCheckpoint(
            os.path.join(output_dir, 'mobilenet_best.h5'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        )
    ]
    
    # Phase 1: Train only top layers
    logger.info("\n=== Phase 1: Training top layers ===")
    
    history1 = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=epochs // 2,
        callbacks=callbacks,
        verbose=1
    )
    
    # Phase 2: Fine-tune base model
    logger.info("\n=== Phase 2: Fine-tuning base model ===")
    
    # Unfreeze last few layers of base model
    base_model.trainable = True
    
    for layer in base_model.layers[:-30]:
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    )
    
    history2 = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=epochs // 2,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    final_model_path = os.path.join(output_dir, 'mobilenet_final.h5')
    model.save(final_model_path)
    logger.info(f"Final model saved to: {final_model_path}")
    
    # Evaluate
    logger.info("\nEvaluating model on validation set...")
    results = model.evaluate(val_generator)
    
    logger.info(f"\nFinal Results:")
    logger.info(f"  Loss: {results[0]:.4f}")
    logger.info(f"  Accuracy: {results[1]:.4f}")
    logger.info(f"  Precision: {results[2]:.4f}")
    logger.info(f"  Recall: {results[3]:.4f}")
    
    return model, history1, history2

def create_feature_extractor(model_path, output_path):
    """
    Create feature extractor model from trained classifier
    
    Args:
        model_path: Path to trained model
        output_path: Path to save feature extractor
    """
    
    # Load trained model
    model = keras.models.load_model(model_path)
    
    # Create feature extractor (remove classification layers)
    feature_extractor = keras.Model(
        inputs=model.input,
        outputs=model.layers[-4].output  # Before final dense layers
    )
    
    # Save
    feature_extractor.save(output_path)
    logger.info(f"Feature extractor saved to: {output_path}")

if __name__ == "__main__":
    # Example usage
    
    logger.info("""
    ╔══════════════════════════════════════════════════════════╗
    ║  MobileNet Transfer Learning Training                   ║
    ║                                                          ║
    ║  This script is OPTIONAL - use only if you have a       ║
    ║  large labeled dataset of facial images.                ║
    ║                                                          ║
    ║  The default pretrained MobileNetV2 works well for      ║
    ║  feature extraction in most cases.                      ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Uncomment to train:
    # train_model(
    #     data_dir="./dataset",
    #     output_dir="./models",
    #     epochs=50,
    #     batch_size=32
    # )
    
    logger.info("To use this script, prepare your dataset and uncomment the train_model() call.")
