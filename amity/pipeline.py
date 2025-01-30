
# class WasteClassifierPipeline:
#     def __init__(self, model_path=None):
#         self.model = None
#         self.metadata = None
#         if model_path:
#             self.load_model(model_path)
    
#     def preprocess_image(self, image_path):
#         """Preprocess a single image for prediction"""
#         img = tf.keras.preprocessing.image.load_img(
#             image_path,
#             target_size=(224, 224)
#         )
#         img_array = tf.keras.preprocessing.image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         return img_array / 255.0
    
#     def postprocess_prediction(self, prediction):
#         """Convert model output to meaningful predictions"""
#         class_idx = np.argmax(prediction[0])
#         confidence = float(prediction[0][class_idx])
        
#         category = self.metadata['categories'][class_idx]
#         is_biodegradable = self.metadata['biodegradable_mapping'].get(category, False)
        
#         return {
#             'category': category,
#             'confidence': confidence,
#             'is_biodegradable': is_biodegradable,
#             'disposal_instructions': self.get_disposal_instructions(category)
#         }

#     def get_disposal_instructions(self, category):
#         """Get disposal instructions for each category"""
#         instructions = {
#             'organic': 'Dispose in composting bin',
#             'paper': 'Recycle in paper recycling bin',
#             'plastic': 'Clean and recycle in plastic recycling bin',
#             'metal': 'Recycle in metal recycling bin',
#             'glass': 'Clean and recycle in glass recycling bin',
#             'e_waste': 'Take to electronic waste recycling center',
#             'batteries': 'Take to battery recycling point',
#             'light_bulbs': 'Take to specific light bulb recycling point',
#             'cloth': 'Donate if in good condition, or take to textile recycling'
#         }
#         return instructions.get(category, 'Please check local recycling guidelines')
# src/pipeline.py
# src/pipeline.py
# src/pipeline.py
# src/pipeline.py

import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from .model import EnhancedWasteClassifier  # Changed from src.model to model

class WasteClassifierPipeline:
    def __init__(self, weights_path):
        self.model = None
        self.img_size = 224
        self.class_names = [
            'batteries',
            'cloth',
            'e_waste',
            'glass',
            'light_bulbs',
            'metal',
            'organic',
            'paper',
            'plastic'
        ]
        self.load_model(weights_path)
    
    def load_model(self, weights_path):
        """Create model architecture and load weights."""
        try:
            # Create model architecture using your EnhancedWasteClassifier
            classifier = EnhancedWasteClassifier(img_size=self.img_size)
            classifier.compile_model(learning_rate=1e-4)
            self.model = classifier.model
            
            # Load weights
            self.model.load_weights(weights_path)
            print("Model weights loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
    
    def preprocess_image(self, image_path):
        """Preprocess a single image for prediction."""
        try:
            # Handle Windows paths properly
            image_path = str(image_path).replace('\\', '/')
            
            # Load and resize image
            img = load_img(image_path, target_size=(self.img_size, self.img_size))
            # Convert to array and add batch dimension
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            # Normalize pixel values
            img_array = img_array / 255.0
            return img_array
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            raise
    
    def predict(self, image_path):
        """Make a prediction for a single image."""
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image_path)
            
            # Make prediction with verbose=0 to suppress progress bar
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Get the predicted class index and probability
            predicted_class_idx = np.argmax(predictions[0])
            probability = predictions[0][predicted_class_idx]
            
            # Get the class name
            predicted_class = self.class_names[predicted_class_idx]
            
            return {
                'class': predicted_class,
                'probability': float(probability),
                'probabilities': {
                    class_name: float(prob)
                    for class_name, prob in zip(self.class_names, predictions[0])
                }
            }
        except Exception as e:
            print(f"Error making prediction: {str(e)}")
            raise