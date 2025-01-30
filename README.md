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


to get the flutter link prototype this is the link :
https://app.flutterflow.io/share/ecosort-rgsyjk


EcoSort - Waste Segregation and Rewards App

Introduction

EcoSort is an innovative mobile application designed to promote proper waste segregation in a neat and efficient manner. The app educates users on how to separate waste correctly and rewards their contributions with a coin-based system. Users can earn coins for properly segregating waste and redeem vouchers by participating in social cleaning initiatives.

Features

Educational Waste Segregation: Learn how to properly separate waste into different categories.

Coin Reward System: Earn coins when you correctly segregate waste.

Voucher Redemption: Use collected coins to redeem vouchers.

Social Cleaning Contribution: Participate in cleaning drives and earn additional rewards.

Event Notifier: Get notified about upcoming cleaning drives and events.

Video Tutorials: Watch step-by-step guides on waste segregation best practices.

How It Works

Open the EcoSort app and navigate to the waste segregation guide.

Follow the provided guidelines to separate your waste properly.

Scan or submit proof of segregation to earn coins.

Participate in social cleaning activities to gain additional rewards.

Redeem your collected coins for vouchers from partnered businesses.

Technologies Used

Frontend: Flutter (using FlutterFlow)

Backend: MongoDB

Authentication: Secure login system for users
