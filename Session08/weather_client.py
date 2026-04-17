"""
weather_client.py — WeatherClient class
Session 08: APIs, HTTP Requests + Environment Variables

This module contains one class, WeatherClient, which handles geocoding
and current weather fetching from Open-Meteo.
"""

import requests


WEATHER_CODES = {
    0:  "Clear sky",
    1:  "Mainly clear",
    2:  "Partly cloudy",
    3:  "Overcast",
    45: "Fog",
    48: "Icy fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


class WeatherClient:
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, timeout=10):
        self.timeout = timeout

    def geocode(self, city_name):
        params = {
            "name": city_name,
            "count": 1,
            "language": "en",
            "format": "json",
        }
        try:
            response = requests.get(self.GEOCODING_URL, params=params, timeout=self.timeout)
            response.raise_for_status()
            results = response.json().get("results")
            if not results:
                return None
            first = results[0]
            return {
                "city": first.get("name", city_name),
                "country": first.get("country", "Unknown"),
                "latitude": first["latitude"],
                "longitude": first["longitude"],
            }
        except requests.RequestException as error:
            print(f"[WeatherClient] Geocoding error: {error}")
            return None

    def get_current_weather(self, latitude, longitude):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
            "timezone": "auto",
        }
        try:
            response = requests.get(self.WEATHER_URL, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json().get("current_weather", {})
        except requests.RequestException as error:
            print(f"[WeatherClient] Weather fetch error: {error}")
            return {}

    def get_weather_description(self, weather_code):
        if weather_code is None:
            return "Unknown"
        return WEATHER_CODES.get(weather_code, "Unknown weather")

    def fetch(self, city_name):
        if not city_name or not city_name.strip():
            print("[WeatherClient] City name cannot be empty.")
            return None, {}

        location = self.geocode(city_name.strip())
        if not location:
            print(f"[WeatherClient] City not found: '{city_name}'.")
            return None, {}

        weather = self.get_current_weather(location["latitude"], location["longitude"])
        if not weather:
            print("[WeatherClient] Could not retrieve weather data.")
            return location, {}

        code = weather.get("weathercode")
        return location, {
            "city": location["city"],
            "country": location["country"],
            "temperature": weather.get("temperature"),
            "weather_code": code,
            "description": self.get_weather_description(code),
            "wind_speed": weather.get("windspeed"),
            "wind_direction": weather.get("winddirection"),
        }
