# Nirman_Amity_75
This is the repo for the hacathon Nirman  
FOR THE ML MODEL:
the directory format is :
```
ML/
├── src/
│   ├── __init__.py
│   ├── preprocessing.py        # Contains WasteDataPreprocessor class
│   ├── data_generator.py      # Contains WasteDataGenerator class
│   ├── model.py               # Contains EnhancedWasteClassifier class
│   └── pipeline.py            # Contains WasteClassifierPipeline class
├── utils/
│   └── setup_utils.py         # Contains directory creation and path setup functions
├── config/
│   └── config.py              # Contains all configurations and paths
├── train.py                   # Main script to run training
└── predict.py                 # Script for making predictions
```
FOR TESTING IT :


app.py -> flask app to run this code for predicting the img


home.html -> html file containing the html code for this ml model
