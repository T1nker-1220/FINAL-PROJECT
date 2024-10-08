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
    air_pollution_data = {}
    if request.method == 'POST':
        # Get city name from the form input
        city = request.form['city']
        # Fetch weather data for the city
        weather_data = get_weather(city)

        # If weather data is found, fetch air pollution data
        if weather_data:
            latitude = weather_data.get('lat')
            longitude = weather_data.get('lon')
            air_pollution_data = get_air_pollution(latitude, longitude)

    # Render the HTML template with weather and air pollution data
    return render_template('index.html', weather=weather_data, air_pollution=air_pollution_data)

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
            'lat': data['coord']['lat'],  # Latitude for air pollution API
            'lon': data['coord']['lon']   # Longitude for air pollution API
        }

        # Print the JSON response for debugging (optional)
        print(json.dumps(data, indent=4))
        return weather
    else:
        # Return an empty dictionary if the API request fails
        return {}

# Function to fetch air pollution data from the OpenWeatherMap API
def get_air_pollution(lat, lon):
    complete_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    
    # Send a GET request to the API
    response = requests.get(complete_url)

    # If the response is OK (200), process the data
    if response.status_code == 200:
        data = response.json()
        air_pollution = {
            'aqi': data.get('list', [{}])[0].get('main', {}).get('aqi', 'No AQI data available')
        }
        return air_pollution
    else:
        return {}

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
