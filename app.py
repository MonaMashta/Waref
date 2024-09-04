from flask import Flask, render_template_string, request, jsonify
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os
import requests

app = Flask(__name__)

# Load your CNN model for wildfire detection
MODEL_PATH = 'WildfireCnn.keras'  # Update with the actual path to your model
model = load_model(MODEL_PATH)

# OpenWeatherMap API key and URL setup
WEATHER_API_KEY = '446c9094b61aa4e8a2a5e748ad8666e6'  # Replace with your OpenWeatherMap API key
CITY = 'ABHA'
WEATHER_URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={WEATHER_API_KEY}'

@app.route('/')
def index():
    # Fetch weather data from OpenWeatherMap API
    weather_data = {}
    try:
        response = requests.get(WEATHER_URL)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'temperature': f"{data['main'].get('temp', 'N/A')}°C",
                'humidity': f"{data['main'].get('humidity', 'N/A')}%",
                'feels_like': f"{data['main'].get('feels_like', 'N/A')}°C",
                'visibility': f"{(data.get('visibility', 0) / 1000):.1f} km",
                'wind_speed': f"{data['wind'].get('speed', 'N/A')} m/s",
                'pressure': f"{data['main'].get('pressure', 'N/A')} hPa",
                'rainfall': f"{data.get('rain', {}).get('1h', 0)} mm",
                'dust': 'Low',  # Placeholder, replace with actual dust data if available
                'rainfall_prob': 'High' if data['main'].get('humidity', 0) > 40 else 'Low',
                'torrents_prob': 'Medium' if data['main'].get('humidity', 0) > 80 else 'Low',
                'wildfire_risk': 'High' if data['main'].get('temp', 0) > 35 and data['wind'].get('speed', 0) > 5 else 'Low',
                'agriculture_impact': 'Check Soil Moisture' if data['main'].get('temp', 0) > 30 else 'Optimal Conditions',
                'planting_time': 'Good' if 20 < data['main'].get('temp', 0) < 30 else 'Not Ideal'
            }
        else:
            weather_data = {'error': 'Failed to fetch weather data'}
    except Exception as e:
        weather_data = {'error': str(e)}

    # HTML content served directly in Flask with weather data injected
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather and AI Detection Dashboard</title>
        <style>
            body {
                margin: 0;
                display: flex;
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                color: #333;
            }
            #map {
                flex: 2;
                height: 100vh;
                border-right: 2px solid #ccc;
            }
            #control-panel {
                flex: 1;
                padding: 20px;
                background-color: #ffffff;
                overflow-y: auto;
                box-shadow: -3px 0 5px rgba(0, 0, 0, 0.2);
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .logo {
                width: 150px;
                margin-bottom: 20px;
            }
            .section {
                margin-bottom: 20px;
                width: 100%;
            }
            .section h3 {
                margin: 10px 0;
                color: #007bff;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5px;
            }
            .input-group {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            .input-group input {
                flex: 1;
                padding: 8px;
                margin-top: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background: #f9f9f9;
                font-size: 14px;
            }
            .button-group {
                display: flex;
                gap: 10px;
                margin-top: 10px;
            }
            button {
                padding: 8px 12px;
                cursor: pointer;
                border: none;
                background-color: #007bff;
                color: white;
                border-radius: 4px;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #0056b3;
            }
            .status-indicator {
                display: flex;
                align-items: center;
                gap: 5px;
                margin-top: 10px;
                font-size: 14px;
            }
            .status {
                width: 15px;
                height: 15px;
                border-radius: 50%;
            }
            .covered {
                background-color: green;
            }
            .not-covered {
                background-color: red;
            }
            .alert {
                background-color: orange;
            }
        </style>
    </head>
    <body>

        <!-- Google Maps container -->
        <div id="map"></div>

        <!-- Control panel container -->
        <div id="control-panel">
            
            <div class="section">
                <h3>Weather List</h3>
                <div class="input-group">
                    <label>Temperature</label>
                    <input type="text" id="temperature" value="{{ weather_data['temperature'] }}" readonly>
                    <label>Humidity %</label>
                    <input type="text" id="humidity" value="{{ weather_data['humidity'] }}" readonly>
                    <label>Feels Like</label>
                    <input type="text" id="feelsLike" value="{{ weather_data['feels_like'] }}" readonly>
                    <label>Visibility KM</label>
                    <input type="text" id="visibility" value="{{ weather_data['visibility'] }}" readonly>
                    <label>Wind mph</label>
                    <input type="text" id="wind" value="{{ weather_data['wind_speed'] }}" readonly>
                    <label>Pr inHg</label>
                    <input type="text" id="pressure" value="{{ weather_data['pressure'] }}" readonly>
                    <label>Rainfall %</label>
                    <input type="text" id="rainfall" value="{{ weather_data['rainfall'] }}" readonly>
                    <label>Dust</label>
                    <input type="text" id="dust" value="{{ weather_data['dust'] }}" readonly>
                </div>
            </div>

            <div class="section">
                <h3>Expectations List</h3>
                <div class="input-group">
                    <label>Rainfall %</label>
                    <input type="text" id="expectedRainfall" value="{{ weather_data['rainfall_prob'] }}" readonly>
                    <label>Torrents of Rain %</label>
                    <input type="text" id="torrents" value="{{ weather_data['torrents_prob'] }}" readonly>
                    <label>Wildfires %</label>
                    <input type="text" id="wildfires" value="{{ weather_data['wildfire_risk'] }}" readonly>
                    <label>Weather Related to Agriculture</label>
                    <input type="text" id="agriculture" value="{{ weather_data['agriculture_impact'] }}" readonly>
                    <label>Best Time to Plant & Harvest</label>
                    <input type="text" id="plantingTime" value="{{ weather_data['planting_time'] }}" readonly>
                </div>
            </div>

            <div class="section">
                <h3>AI Detection Warning</h3>
                <div class="status-indicator" id="pointA082">
                    <div class="status covered"></div> Point A082 - Covered
                </div>
                <div class="status-indicator" id="pointA969">
                    <div class="status not-covered"></div> Point A969 - Not Covered
                </div>
                <div class="status-indicator" id="pointA243">
                    <div class="status alert"></div> Point A243 - Alert
                </div>
            </div>

            <div class="section">
                <h3>Does The Selected Location Covered by Real Time Data Monitors?</h3>
                <div class="button-group">
                    <button onclick="setStatus('covered')">Covered</button>
                    <button onclick="setStatus('not-covered')">Not Covered</button>
                </div>
                <h3>Drone AI Report</h3>
                <button onclick="generateReport()">Click</button>
                <h3>All Wildfires Detection</h3>
                <button>Select the nearest tower to the selected location</button>
                <button>Select the chosen tower</button>
                <h3>Control Options</h3>
                <div class="button-group">
                    <button>Use Drone Manually</button>
                    <button>Send warning to people in the selected zone</button>
                    <button>Report local authorities manually</button>
                    <button>Send live URL to local authorities to see live drone</button>
                </div>
                <h3>Customization / Drone:</h3>
                <div class="button-group">
                    <button>History of Data</button>
                    <button>Download Data</button>
                </div>
            </div>

            <div class="section">
                <h3>Manual Image Upload for Wildfire Detection</h3>
                <form method="POST" action="/predict" enctype="multipart/form-data">
                    <input type="file" name="file" accept="image/*" required>
                    <input type="submit" value="Upload and Detect">
                </form>
            </div>
        </div>

        <script>
            function initMap() {
                const initialLocation = { lat: 18.2164, lng: 42.5053 }; // Coordinates for Abha
                const map = new google.maps.Map(document.getElementById("map"), {
                    zoom: 10,
                    center: initialLocation,
                });
            }

            function generateReport() {
                alert("Generating Drone AI Report...");
            }

            function setStatus(status) {
                if (status === 'covered') {
                    alert("Location is covered by real-time data monitors.");
                } else {
                    alert("Location is not covered by real-time data monitors.");
                }
            }

            window.onload = initMap;
        </script>

        <script async defer
            src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBQIq3vMrupNLwksDeiLZ_z9uGhcFbp6oM&callback=initMap">
        </script>

    </body>
    </html>
    '''  # Insert weather data into HTML content

    return render_template_string(html_content, weather_data=weather_data)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        img = cv2.resize(img, (64, 64))
        img = img / 255.0
        img = img.reshape(1, 64, 64, 3)
        prediction = model.predict(img)
        result = 'Wildfire Detected' if prediction[0][0] > 0.1 else 'No Wildfire Detected'
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Change the port if needed