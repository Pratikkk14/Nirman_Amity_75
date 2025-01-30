# from src.pipeline import WasteClassifierPipeline
# from config.config import *

# def predict_image(image_path):
#     pipeline = WasteClassifierPipeline('models/waste_classifier_final.h5')
#     result = pipeline.predict(image_path)
#     return result

# if __name__ == "__main__":
#     # Example usage
#     image_path = "C:\\Users\\prati\\Desktop\\Nirman_Amity_75\\datasets\\set1\\e-waste\\artificial-ingelligence-circuit-board-closeup-view-with-electronic-picture-id1204292317.jpg"
#     result = predict_image(image_path)
#     print(result)
# predict.py
# predict.py
# predict.py

import os
import sys
from src.pipeline import WasteClassifierPipeline  # Make sure predict.py is in the root directory

def predict_image(image_path):
    """Predict the class of a single image."""
    try:
        # Use the weights file path - adjust if needed based on your directory structure
        weights_path = os.path.join('models', 'waste_classifier_final.weights.h5')
        
        # Check if weights file exists
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Weights file not found at {weights_path}")
            
        # Check if image file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found at {image_path}")
        
        # Initialize the pipeline with the trained weights
        pipeline = WasteClassifierPipeline(weights_path)
        
        # Make prediction
        result = pipeline.predict(image_path)
        return result
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        raise

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Please provide an image path")
        print("Usage: python predict.py path/to/your/image.jpg")
        sys.exit(1)
        
    image_path = sys.argv[1]
    
    try:
        # Make prediction
        result = predict_image(image_path)
        
        # Print results
        print("\nPrediction Results:")
        print(f"Predicted Class: {result['class']}")
        print(f"Confidence: {result['probability']*100:.2f}%")
        
        print("\nAll Class Probabilities:")
        for class_name, prob in result['probabilities'].items():
            print(f"{class_name}: {prob*100:.2f}%")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)