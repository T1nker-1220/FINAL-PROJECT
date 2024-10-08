import requests

# Your OpenWeatherMap API key
api_key = "50109a24ba32ed4b775a064f1fb11237"

# Latitude and longitude for the request
latitude = "14.6042"  # Example coordinates for Manila, Philippines
longitude = "120.9842"  

# Construct the API request URL using latitude and longitude
complete_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

# Send a GET request to the API
response = requests.get(complete_url)

# If the response is successful (status code 200), process the weather data
if response.status_code == 200:
    data = response.json()  # Parse the JSON response
    
    # Extract the temperature, humidity, and weather description
    temp = data.get('main', {}).get('temp', 'No temperature data available')
    humidity = data.get('main', {}).get('humidity', 'No humidity data available')
    description = data.get('weather', [{}])[0].get('description', 'No weather description available')

    # Print the weather details
    print(f"Temperature: {temp}°C")
    print(f"Humidity: {humidity}%")
    print(f"Weather: {description}")
else:
    # If there is an error, print the error code and response text
    print(f"Error fetching data: {response.status_code}, {response.text}")
