import json
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='templates')

# Your OpenWeatherMap API key
api_key = "50109a24ba32ed4b775a064f1fb11237"

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = {}
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        
        # Fetch weather data
        weather_data = get_weather(latitude, longitude)

    return render_template('index.html', weather=weather_data)

@app.route('/get_weather', methods=['GET'])
def get_weather_api():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    
    weather_data = get_weather(latitude, longitude)
    return jsonify(weather_data)

def get_weather(latitude, longitude):
    # Complete URL with latitude and longitude for OpenWeatherMap
    complete_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

    # Make the request to the API
    response = requests.get(complete_url)

    # Convert response data to JSON
    if response.status_code == 200:
        data = response.json()
        weather = {
            'temp': data.get('main', {}).get('temp', 'No temperature data available'),
            'humidity': data.get('main', {}).get('humidity', 'No humidity data available'),
            'description': data.get('weather', [{}])[0].get('description', 'No weather description available')
        }
        
        print(json.dumps(data, indent=4))
        return weather
    else:
        print(f"Error fetching weather data: {response.status_code}, {response.text}")
        return {}

if __name__ == '__main__':
    app.run(debug=True)
