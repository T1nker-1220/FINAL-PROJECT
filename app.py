import json
from flask import Flask, render_template, request
import requests

# Initialize the Flask application
app = Flask(__name__, template_folder='templates')

# Your OpenWeatherMap API key
api_key = "50109a24ba32ed4b775a064f1fb11237"

# Define the home route (the main page)
@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = {}
    air_quality_data = {}
    
    if request.method == 'POST':
        # Get city name from the form input
        city = request.form['city']
        # Fetch weather data for the city
        weather_data = get_weather(city)
        
        # Fetch air quality data using the city coordinates
        if weather_data:
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            air_quality_data = get_air_quality(lat, lon)

    # Render the HTML template with weather and air quality data
    return render_template('index.html', weather=weather_data, air_quality=air_quality_data)

# Function to fetch weather data from the OpenWeatherMap API
def get_weather(city):
    # Construct the API request URL using the city name and API key
    complete_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    # Send a GET request to the API
    response = requests.get(complete_url)

    # If the response status is OK (200), process the data
    if response.status_code == 200:
        data = response.json()
        return data  # Return the entire data for later use (lat, lon, etc.)
    else:
        # Return an empty dictionary if the API request fails
        return {}

# Function to fetch air quality data from the OpenWeatherMap API
def get_air_quality(lat, lon):
    # Construct the API request URL using latitude and longitude
    complete_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

    # Send a GET request to the API
    response = requests.get(complete_url)

    # If the response is successful (status code 200), process the data
    if response.status_code == 200:
        data = response.json()
        # Extract relevant air quality data
        air_quality = {
            'aqi': data.get('list', [{}])[0].get('main', {}).get('aqi', 'No data available'),
            'pm2_5': data.get('list', [{}])[0].get('components', {}).get('pm2_5', 'No data available'),
            'pm10': data.get('list', [{}])[0].get('components', {}).get('pm10', 'No data available'),
            'no2': data.get('list', [{}])[0].get('components', {}).get('no2', 'No data available'),
            'so2': data.get('list', [{}])[0].get('components', {}).get('so2', 'No data available'),
            'o3': data.get('list', [{}])[0].get('components', {}).get('o3', 'No data available'),
            'co': data.get('list', [{}])[0].get('components', {}).get('co', 'No data available'),
        }
        return air_quality
    else:
        # Return an empty dictionary if the API request fails
        return {}

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
