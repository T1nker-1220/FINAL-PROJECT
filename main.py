import requests

# Your OpenWeatherMap API key
api_key = "50109a24ba32ed4b775a064f1fb11237"

# Latitude and longitude for the request
latitude = "14.6042" 
longitude = "120.984222"  

# Complete URL with latitude and longitude for OpenWeatherMap
complete_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

# Make the request
response = requests.get(complete_url)

# Check response status and process data
if response.status_code == 200:
    data = response.json()
    
    print("Response Data:", data)

    temp = data.get('main', {}).get('temp', 'No temperature data available')
    humidity = data.get('main', {}).get('humidity', 'No humidity data available')
    
    # Check for weather description
    description = data.get('weather', [{}])[0].get('description', "No weather description available")

    # Print the weather information
    print(f"Temperature: {temp}°C")
    print(f"Humidity: {humidity}%")
    print(f"Weather: {description}")
else:
    print(f"Error fetching data: {response.status_code}, {response.text}")
