import tensorflow as tf
import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, Model
from tensorflow.keras.applications import VGG16
import shutil
from pathlib import Path
import json
class EnhancedWasteClassifier:
    def __init__(self, img_size=224, weights_path=None):
        self.img_size = img_size
        self.model = self._build_model()
        if weights_path:
            self.model.load_weights(weights_path)
    
    def _build_model(self):
        # Base model
        base_model = VGG16(
            input_shape=(self.img_size, self.img_size, 3),
            weights='imagenet',
            include_top=False
        )
        
        # Freeze early layers
        for layer in base_model.layers[:-4]:
            layer.trainable = False
        
        # Build enhanced model
        x = base_model.output
        x = layers.GlobalAveragePooling2D()(x)
        
        # Common features
        x = layers.Dense(1024, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(512, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.3)(x)
        
        # Classification head
        outputs = layers.Dense(9, activation='softmax')(x)  # 9 categories
        
        model = Model(inputs=base_model.input, outputs=outputs)
        return model
    def compile_model(self, learning_rate=1e-4):
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
    def train(self, train_generator, val_generator, epochs=50):
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=3,
                min_lr=1e-6
            ),
            tf.keras.callbacks.ModelCheckpoint(
                'best_model.h5',
                monitor='val_accuracy',
                save_best_only=True,
                mode='max'
            )
        ]
        
        history = self.model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=epochs,
            callbacks=callbacks
        )
        return history