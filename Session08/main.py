"""
main.py — Weather app CLI
Session 08: APIs, HTTP Requests + Environment Variables

This script creates a WeatherClient and displays the current weather
for a user-provided city.
"""

from weather_client import WeatherClient


def main():
    print("Welcome to the Weather App!")
    city_name = input("Enter a city name to get the current weather: ").strip()
    if not city_name:
        print("Please enter a valid city name.")
        return

    client = WeatherClient()
    location, weather = client.fetch(city_name)
    if location and weather:
        print(f"Weather for {location['city']}, {location['country']}:" )
        print(f"  Temperature: {weather['temperature']}°C")
        print(f"  Condition: {weather['description']}")
        print(f"  Weather Code: {weather['weather_code']}")
        print(f"  Wind Speed: {weather['wind_speed']} km/h")
        print(f"  Wind Direction: {weather['wind_direction']}°")
    else:
        print(f"Sorry, could not retrieve weather information for '{city_name}'.")


if __name__ == "__main__":
    main()
