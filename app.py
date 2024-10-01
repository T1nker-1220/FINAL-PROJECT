from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Your API Ninjas API key (without leading slashes)
api_key = "vTftsNwDaweVZNqQLyePw==nYcCW3NVHxLYnUNw"

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = {}
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        
        # Fetch weather data
        weather_data = get_weather(latitude, longitude)

    return render_template('index.html', weather=weather_data)  # Correctly passing weather_data


@app.route('/get_weather', methods=['GET'])
def get_weather_api():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    
    weather_data = get_weather(latitude, longitude)
    return jsonify(weather_data)

def get_weather(latitude, longitude):
    # Complete URL with latitude and longitude
    complete_url = f"https://api.api-ninjas.com/v1/weather?lon={longitude}&lat={latitude}"

    # Headers with API key
    headers = {
        'X-Api-Key': api_key
    }

    # Make the request
    response = requests.get(complete_url, headers=headers)

    # Convert response data to JSON
    if response.status_code == 200:
        data = response.json()
        weather = {
            'temp': data.get('temp', 'No temperature data available'),
            'humidity': data.get('humidity', 'No humidity data available'),
            'description': data['weather'][0]['description'] if 'weather' in data and isinstance(data['weather'], list) and len(data['weather']) > 0 else "No weather description available"
        }
        return weather
    else:
        return {'error': f"Error fetching data: {response.status_code}, {response.text}"}

if __name__ == '__main__':
    app.run(debug=True)
