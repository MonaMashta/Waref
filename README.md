# Wildfire Detection System

## Overview

The Wildfire Detection System is an innovative project that leverages AI, machine learning, and real-time data to monitor, detect, and respond to wildfires and other environmental disasters. The system integrates weather data, satellite imagery, and drone feeds to predict wildfire risks, providing early warnings and rapid intervention capabilities to mitigate potential damage.

## Key Features

- **Real-Time Monitoring:** The system uses a live map that integrates data from the OpenWeatherMap API, displaying critical weather information such as temperature, wind speed, and humidity.
- **AI-Based Predictions:** Utilizes Convolutional Neural Networks (CNN) to analyze satellite imagery and weather data, achieving a 96% accuracy rate in wildfire detection.
- **Drone Integration:** Drones equipped with 360-degree cameras are deployed to verify wildfire alerts, providing live feeds to local authorities for immediate assessment and response.
- **Support for Saudi Green Initiative:** Aims to reduce the impact of wildfires, preserve forests, and combat desertification, contributing to the sustainability goals of Saudi Arabia.

## Project Structure

- `model/`: Contains the CNN model used for wildfire detection.
- `app.py`: The main backend of the web application, built using Flask, which handles the data processing, predictions, and alert generation.
- `home.html`: The frontend of the web application, providing a user interface for displaying live maps, weather data, and wildfire alerts.

## How It Works

1. **Data Collection:** The system collects data from multiple sources, including satellite imagery, weather data from OpenWeatherMap, and live feeds from drones equipped with 360-degree cameras.
2. **Training Data:** The data is devided to be trained in 70/30 teqnique where 70% of the data is used for training and 30% of the data for validation and testing
3. **Prediction Model:** The data is processed through a CNN model that predicts the probability of wildfire occurrence based on environmental conditions.
4. **Alert and Response:** If the probability of a wildfire exceeds 20%, drones are automatically deployed to verify the situation. The system then sends alerts to local authorities for immediate action if necessary. 
## Installation

To set up the project locally, follow these steps:

1. Download all files in this repository
2. Run the FinalProductionWildFireDetectionSystem.ipynb
3. Run App.Py
4. Run Home.HTML

The minute you follow these three steps you will have the model conected with the web pages and is ready to be used.

