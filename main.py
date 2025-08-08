import requests    # To make HTTP requests to the Weather API
import json        # To handle JSON data (converting string to python dictionary)
from dotenv import load_dotenv
import os

load_dotenv()    # Load environment variables from .env file

weather_api = os.getenv("WEATHER_API_KEY")    # Replace with your API key  

# Function to get weather data from WeatherAPI
def get_weather_forecast(city, api_key):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"

    try:
        response = requests.get(url)
        response.raise_for_status()    # Raise an exception if the response contains an HTTP error (like 404 or 401)
        return response.json()         # Convert the JSON response into a Python dictionary and return it
    
    # Handles HTTP errors (like city not found or invalid API key)
    except requests.exceptions.HTTPError as e:    
        print(f"❌ Error: {e}")

    # Handles general request issues like network failure or connection problems
    except requests.exceptions.RequestException:  
        print("❌ Network error. Please check your connection.")

    return None


# Function to display weather data
def display_current_weather(data):
    # If there is no data (error occurred), exit the function
    if not data:
        return
    
    # Extracting useful parts of the data from JSON file or API into variables
    current = data["current"]
    location = data["location"]
    condition = current["condition"]
    
    print(f"\n📍 Location: {location['name']}, {location['country']}")
    print(f"🕐 Last Updated: {current['last_updated']}")
    print(f"🌡️  Temperature: {current['temp_c']} °C")
    print(f"🤔 Feels Like: {current['feelslike_c']} °C")
    print(f"🌤️  Condition: {condition['text']}")
    print(f"💧 Humidity: {current['humidity']}%")
    print(f"💨 Wind: {current['wind_kph']} km/h {current['wind_dir']}")
    print(f"☁️  Cloud Cover: {current['cloud']}%")
    print(f"🌞 UV Index: {current['uv']}")
    print(f"🖼️  Icon URL: https:{condition['icon']}")  # Prepend 'https:' to icon path


# Function to display the 3-day weather forecast
def display_forecast(data):
    # Get the list of forecasted days from the API response
    forecast_days = data["forecast"]["forecastday"]

    print("\n📅 3-Day Forecast:\n")

    # Loop through each day in the forecast
    for day in forecast_days:
        date = day["date"]                         
        day_info = day["day"]                       
        condition = day_info["condition"]["text"]   
        max_temp = day_info["maxtemp_c"]             
        min_temp = day_info["mintemp_c"]            
        chance_of_rain = day_info["daily_chance_of_rain"] 

        # Print the forecast details for each day using f-strings
        print(f"📆 Date: {date}")
        print(f"🌤️  Condition: {condition}")
        print(f"🔼 Max Temp: {max_temp} °C")
        print(f"🔽 Min Temp: {min_temp} °C")
        print(f"🌧️  Chance of Rain: {chance_of_rain}%")
        print("—" * 32)


# The main function (which consists other functions)
def main():  
    city = input("Enter the name of the city: ")

    # Get both current and 3-day forecast weather data
    weather_data = get_weather_forecast(city, weather_api)

    if weather_data:
        display_current_weather(weather_data)
        display_forecast(weather_data)


# Ensures that the script runs only when executed directly and not when imported
if __name__ == "__main__":
    main()


