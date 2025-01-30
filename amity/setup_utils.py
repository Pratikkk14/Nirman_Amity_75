import os
from config.config import BASE_PATH, PROCESSED_PATH, CATEGORIES

def create_directory_structure():
    """Create necessary directories for the project"""
    directories = [
        BASE_PATH,
        PROCESSED_PATH,
        os.path.join(PROCESSED_PATH, 'train'),
        os.path.join(PROCESSED_PATH, 'val'),
        os.path.join(PROCESSED_PATH, 'test')
    ]
    
    for dir in directories:
        os.makedirs(dir, exist_ok=True)
        
        if any(split in dir for split in ['train', 'val', 'test']):
            for category in CATEGORIES:
                os.makedirs(os.path.join(dir, category), exist_ok=True)