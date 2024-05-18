# ExtraSensory Dataset - Data Analysis and Machine Learning

This repository contains a machine learning project using the **ExtraSensory** dataset. The dataset was used to predict human activities based on sensor data collected from smartphones and smartwatches.

## Files
- `Extra_Sensory.ipynb`: A Jupyter notebook containing the data preprocessing, feature selection, and machine learning models applied to the ExtraSensory dataset.

## Dataset Overview

The **ExtraSensory** dataset is a large, multi-sensor dataset collected from 60 participants over approximately 362 days. Each participant is identified by a unique UUID and contributes thousands of data points. The data includes measurements from various sensors, including accelerometers, gyroscopes, magnetometers, and location services. Additionally, the dataset contains user-provided context labels for a variety of activities, such as walking, sitting, and sleeping.

- **Sensors used**: Accelerometer, gyroscope, magnetometer, location, audio, and phone state indicators.
- **Frequency**: Data was typically recorded at one-minute intervals.
- **Labels**: The dataset contains binary labels for multiple human activities like sitting, walking, running, etc.

For more detailed information about the dataset, visit the official website: [ExtraSensory Dataset](http://extrasensory.ucsd.edu/).

## Project Overview

This project implements two machine learning approaches to predict the activity label "SITTING" using features derived from the sensor data:
1. Logistic Regression
2. Logistic Regression with Stochastic Gradient Descent (SGD)

### Preprocessing
- Data cleansing included handling missing values by imputing mean values for certain features.
- Feature scaling was performed using Min-Max normalization.

### Feature Selection
- Specific features were selected for the model, focusing on:
  - Location measurements (e.g., max altitude, speed)
  - Phone state indicators (e.g., app state, battery status)
  - Screen brightness levels

### Model Performance
The models were trained using 70% of the data, and the remaining 30% was used for testing. The following metrics were used for model evaluation:
- **Accuracy**
- **Precision**
- **Recall**
- **F1 Score**

##### Logistic Regression Results:
- **Accuracy**: 0.7155675288136698
- **Precision**: 0.6303217036701405
- **Recall**: 0.8426481758263299
- **F1 Score**: 0.7242802687277552

##### Logistic Regression with SGD:
- **Accuracy**: 0.7128735457379667
- **Precision**: 0.6303217036701405
- **Recall**: 0.8521304486315635
- **F1 Score**: 0.7246322456973788

##### Logistic Regression with Tuning:
- **Accuracy**: 0.7093865757085284
- **Precision**: 0.6196555010893247
- **Recall**: 0.8920196996055179
- **F1 Score**: 0.731301160046201


### Install Dependencies
```python

pip install -r requirements.txt
```