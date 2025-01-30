from pathlib import Path
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator
class WasteDataGenerator:
    def __init__(self, base_path, batch_size=32, img_size=224):
        self.base_path = Path(base_path)
        self.batch_size = batch_size
        self.img_size = img_size
        
        # Load metadata
        with open(self.base_path / 'metadata.json', 'r') as f:
            self.metadata = json.load(f)
        
        self.setup_data_generators()
    
    def setup_data_generators(self):
        """Setup data generators with augmentation"""
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        val_datagen = ImageDataGenerator(rescale=1./255)
        
        self.train_generator = train_datagen.flow_from_directory(
            self.base_path / 'train',
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='categorical'
        )
        
        self.val_generator = val_datagen.flow_from_directory(
            self.base_path / 'val',
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='categorical'
        )
    