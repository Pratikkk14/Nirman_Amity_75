# from src.waste_data_preprocessor import WasteDataPreprocessor
# from src.waste_data_generator import WasteDataGenerator
# from src.model import EnhancedWasteClassifier
# from utils.setup_utils import create_directory_structure
# from config.config import *

# def main():
#     # Create directory structure
#     create_directory_structure()
    
#     # Initialize preprocessor
#     preprocessor = WasteDataPreprocessor(BASE_PATH, PROCESSED_PATH)
#     preprocessor.organize_dataset()
#     preprocessor.create_metadata()
    
#     # Setup data generator
#     data_generator = WasteDataGenerator(
#         PROCESSED_PATH,
#         batch_size=BATCH_SIZE,
#         img_size=IMG_SIZE
#     )
    
#     # Create and train model
#     classifier = EnhancedWasteClassifier(img_size=IMG_SIZE)
#     classifier.compile_model(learning_rate=LEARNING_RATE)
    
#     # Train
#     history = classifier.train(
#         data_generator.train_generator,
#         data_generator.val_generator,
#         epochs=EPOCHS
#     )
    
#     # Save model
#     classifier.model.save('models/waste_classifier_final.h5')

# if __name__ == "__main__":
#     main()

#the above code is commented coz the model stopped training in btwn n now we are restarting the same model 
import tensorflow as tf
from src.waste_data_preprocessor import WasteDataPreprocessor
from src.waste_data_generator import WasteDataGenerator
from src.model import EnhancedWasteClassifier
from utils.setup_utils import create_directory_structure
from config.config import *

def main():
    # Enable memory growth to avoid OOM errors
    physical_devices = tf.config.list_physical_devices('GPU')
    if physical_devices:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    
    # Create directory structure
    create_directory_structure()
    
    # Setup data generator with increased batch size
    data_generator = WasteDataGenerator(
        PROCESSED_PATH,
        batch_size=32,
        img_size=IMG_SIZE
    )
    
    # Create model and load weights
    classifier = EnhancedWasteClassifier(img_size=IMG_SIZE)
    classifier.compile_model(learning_rate=5e-4)
    
    try:
        # Try loading the previous best weights
        classifier.model.load_weights('best_model.h5')
        print("Successfully loaded previous weights")
    except:
        print("Could not load previous weights, starting fresh")
    
    # Modified callbacks with correct file naming
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=7,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.3,
            patience=4,
            min_lr=1e-6
        ),
        tf.keras.callbacks.ModelCheckpoint(
            'best_model_continued.weights.h5',
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            save_weights_only=True
        )
    ]
    
    # Resume training with simplified fit call
    try:
        history = classifier.model.fit(
            data_generator.train_generator,
            validation_data=data_generator.val_generator,
            epochs=30,
            callbacks=callbacks,
            initial_epoch=20
        )
        
        # Save final model weights
        classifier.model.save_weights('models/waste_classifier_final.weights.h5')
        print("Training completed successfully")
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        raise

if __name__ == "__main__":
    main()