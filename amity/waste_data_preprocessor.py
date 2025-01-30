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
class WasteDataPreprocessor:
    def __init__(self, base_path, output_path):
        self.base_path = Path(base_path)
        self.output_path = Path(output_path)
        self.category_mapping = {
            # Biodegradable
            'food_waste': ['organic'],
            'leaf_waste': ['organic'],
            'paper_waste': ['paper'],
            'wood_waste': ['organic'],
            # Non-biodegradable
            'metal_cans': ['metal'],
            'e_waste': ['e_waste'],
            'plastic_bags': ['plastic'],
            'plastic_bottles': ['plastic'],
            'batteries': ['batteries'],
            'glass': ['glass'],
            'cloth': ['cloth'],
            'light_bulbs': ['light_bulbs']
        }
        
        self.biodegradable_categories = ['food_waste', 'leaf_waste', 'paper_waste', 'wood_waste']
    def organize_dataset(self):
        """Organize and combine both datasets into a unified structure"""
        # Create necessary directories
        for split in ['train', 'val', 'test']:
            (self.output_path / split).mkdir(parents=True, exist_ok=True)
            for category in self.category_mapping.values():
                (self.output_path / split / category[0]).mkdir(exist_ok=True)

        # Process and distribute images
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    source_path = Path(root) / file
                    category = root.split(os.sep)[-1]
                    
                    if category in self.category_mapping:
                        target_category = self.category_mapping[category][0]
                        # Randomly assign to train/val/test
                        split = np.random.choice(['train', 'val', 'test'], p=[0.7, 0.15, 0.15])
                        target_path = self.output_path / split / target_category / file
                        shutil.copy2(source_path, target_path)
                        
    def create_metadata(self):
        """Create metadata file with category information"""
        metadata = {
            'categories': list(set([cat[0] for cat in self.category_mapping.values()])),
            'biodegradable_mapping': {
                cat: cat in self.biodegradable_categories 
                for cat in self.category_mapping.keys()
            }
        }
        with open(self.output_path / 'metadata.json', 'w') as f:
            json.dump(metadata, f)