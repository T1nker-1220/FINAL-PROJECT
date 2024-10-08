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
    city_id = None  # Initialize city_id variable

    if request.method == 'POST':
        # Get city name from the form input
        city = request.form['city']
        # Fetch weather data for the city
        weather_data = get_weather(city)

        # Get the city ID from the weather data for the widget
        if weather_data:
            city_id = weather_data.get('id')  # Get the city ID

            # Optional: Fetch air quality data based on coordinates
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            air_quality_data = get_air_quality(lat, lon)

    # Render the HTML template with weather data
    return render_template('index.html', weather=weather_data, air_pollution=air_quality_data, city_id=city_id)

# Function to fetch weather data from the OpenWeatherMap API
def get_weather(city):
    # Construct the API request URL using the city name and API key
    complete_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    # Send a GET request to the API
    response = requests.get(complete_url)

    # If the response status is OK (200), process the data
    if response.status_code == 200:
        data = response.json()

        # Extract important weather details from the API response
        weather = {
            'temp': data.get('main', {}).get('temp', 'No temperature data available'),
            'humidity': data.get('main', {}).get('humidity', 'No humidity data available'),
            'description': data.get('weather', [{}])[0].get('description', 'No weather description available'),
            'condition': 'Raining' if 'rain' in data else 'Clear' if 'clear' in data['weather'][0]['description'].lower() else 'Cloudy',
            'id': data['id'],  # Store the city ID
            'coord': data['coord']  # Store coordinates for air quality
        }

        return weather
    else:
        return {}

# Function to fetch air quality data
def get_air_quality(lat, lon):
    complete_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        return {
            'aqi': data['list'][0]['main']['aqi']
        }
    return {}

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
