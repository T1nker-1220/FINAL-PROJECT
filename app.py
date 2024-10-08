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
        # Fetch air quality data for the city
        if weather_data:
            lat = weather_data.get('coord', {}).get('lat')
            lon = weather_data.get('coord', {}).get('lon')
            air_quality_data = get_air_quality(lat, lon)

    # Render the HTML template with weather and air quality data
    return render_template('index.html', weather=weather_data, air_quality=air_quality_data)

# Function to fetch weather data from the OpenWeatherMap API
def get_weather(city):
    complete_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        weather = {
            'temp': data.get('main', {}).get('temp', 'No temperature data available'),
            'humidity': data.get('main', {}).get('humidity', 'No humidity data available'),
            'description': data.get('weather', [{}])[0].get('description', 'No weather description available'),
            'condition': 'Raining' if 'rain' in data else 'Clear' if 'clear' in data['weather'][0]['description'].lower() else 'Cloudy',
            'coord': {
                'lat': data['coord']['lat'],
                'lon': data['coord']['lon']
            }
        }
        print(json.dumps(data, indent=4))  # Log the full weather data to the console
        return weather
    else:
        return {}

# Function to fetch air quality data from the OpenWeatherMap API
def get_air_quality(lat, lon):
    complete_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        air_quality = {
            'aqi': data.get('list', [{}])[0].get('main', {}).get('aqi', 'No AQI data available')
        }
        return air_quality
    else:
        return {}

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
