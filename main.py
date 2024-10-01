import requests

# Your API Ninjas API key (without leading slashes)
api_key = "vTftsNwDaweVZNqQLyePw==nYcCW3NVHxLYnUNw"

# Latitude and longitude for the request
latitude = "14.599512" 
longitude = "120.984222"  

# Complete URL with latitude and longitude
complete_url = f"https://api.api-ninjas.com/v1/weather?lon={longitude}&lat={latitude}"

# Headers with API key
headers = {
    'X-Api-Key': api_key 
}

# Make the request
response = requests.get(complete_url, headers=headers)

# Check response status and process data
if response.status_code == 200:
    data = response.json()
    
    print("Response Data:", data)

    temp = data.get('temp', 'No temperature data available')
    humidity = data.get('humidity', 'No humidity data available')
    
    # Check for weather description
    if 'weather' in data and isinstance(data['weather'], list) and len(data['weather']) > 0:
        description = data['weather'][0]['description']
    else:
        description = "No weather description available"

    # Print the weather information
    print(f"Temperature: {temp}°C")
    print(f"Humidity: {humidity}%")
    print(f"Weather: {description}")
else:
    print(f"Error fetching data: {response.status_code}, {response.text}")
