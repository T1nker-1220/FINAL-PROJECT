import requests

api_key = "/vTftsNwDaweVZNqQLyePw==nYcCW3NVHxLYnUNw"  

latitude = "14.599512" 
longitude = "120.984222"  


complete_url = f"https://api.api-ninjas.com/v1/weather?lon={longitude}&lat={latitude}"


headers = {
    'X-Api-Key': "/vTftsNwDaweVZNqQLyePw==nYcCW3NVHxLYnUNw"  
}


response = requests.get(complete_url, headers=headers)


if response.status_code == 200:
    data = response.json()
    
    
    print("Response Data:", data)

    temp = data.get('temp', 'No temperature data available')
    humidity = data.get('humidity', 'No humidity data available')
    
    
    if 'weather' in data and isinstance(data['weather'], list) and len(data['weather']) > 0:
        description = data['weather'][0]['description']
    else:
        description = "No weather description available"

    
    print(f"Temperature: {temp}°C")
    print(f"Humidity: {humidity}%")
    print(f"Weather: {description}")
else:
    print(f"Error fetching data: {response.status_code}, {response.text}")
