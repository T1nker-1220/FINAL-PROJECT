from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your API Ninjas API key (including leading slashes)
api_key = "/vTftsNwDaweVZNqQLyePw==nYcCW3NVHxLYnUNw"

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = {}
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        
        # Complete URL with latitude and longitude
        complete_url = f"https://api.api-ninjas.com/v1/weather?lon={longitude}&lat={latitude}"

        # Headers with API key
        headers = {
            'X-Api-Key': "/vTftsNwDaweVZNqQLyePw==nYcCW3NVHxLYnUNw"
        }

        # Make the request
        response = requests.get(complete_url, headers=headers)

        # Convert response data to JSON
        if response.status_code == 200:
            data = response.json()
            weather_data['temp'] = data.get('temp', 'No temperature data available')
            weather_data['humidity'] = data.get('humidity', 'No humidity data available')
            if 'weather' in data and isinstance(data['weather'], list) and len(data['weather']) > 0:
                weather_data['description'] = data['weather'][0]['description']
            else:
                weather_data['description'] = "No weather description available"
        else:
            weather_data['error'] = f"Error fetching data: {response.status_code}, {response.text}"

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
