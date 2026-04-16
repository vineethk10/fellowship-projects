import requests

class WeatherClient:
    GEOCODING_API_URL = "http://geocoding-api.open-meteo.com/v1/search"
    WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
    WEATHER_CODE_DESCRIPTIONS = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    def __init__(self, timeout=10):
        self.timeout = timeout
    
    def geocode(self, city_name):
        try:
            params = {
                'name': city_name,
                'count': 1,
                'language': 'en',
                'format': 'json'
            }
            response = requests.get(self.GEOCODING_API_URL, params=params, timeout=self.timeout)
            response.raise_for_status()

            results = response.json().get('results')
            if not results:
                print(f"[WeatherClient] No geocoding results found for '{city_name}'")
                return None
            r = results[0]
            return {
                'city': r['name'],
                'country': r.get('country', 'Unknown'),
                'longitude': r['longitude'],
                'latitude': r['latitude'],
            }
        except requests.RequestException as e:
            print(f"[WeatherClient] Network error while Geocoding API request failed: {e}")
    
    def get_current_weather(self, latitude, longitude):
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current_weather': True,
                'timezone': 'auto',
            }
            response = requests.get(self.WEATHER_API_URL, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json().get('current_weather', {})
        except requests.RequestException as e:
            print(f"[WeatherClient] Network error while fetching weather: {e}")
            return {}

    def get_weather_description(self, weather_code):
        if weather_code is None:
            return "Unknown"
        return self.WEATHER_CODE_DESCRIPTIONS.get(weather_code, "Unknown weather")

    def fetch(self, city_name):
        location = self.geocode(city_name.strip())
        if not location:
            print(f"[WeatherClient] Unable to fetch weather for '{city_name}' due to geocoding failure.")
            return None, {}
        weather = self.get_current_weather(location['latitude'], location['longitude'])
        if not weather:
            print(f"[WeatherClient] Unable to fetch weather for '{city_name}' due to weather API failure.")
            return None, {}
        weather_code = weather.get('weathercode')
        return location, {
            'city': location['city'],
            'country': location['country'],
            'temperature': weather.get('temperature'),
            'weather_code': weather_code,
            'description': self.get_weather_description(weather_code),
            'wind_speed': weather.get('windspeed'),
            'wind_direction': weather.get('winddirection'),
        }


if __name__ == "__main__":
    client = WeatherClient()
    location, weather = client.fetch("London")
    if location:
        print(f"Weather for {location['city']}, {location['country']}:")
        print(f"  Temperature: {weather['temperature']}°C")
        print(f"  Weather Code: {weather['weather_code']}")
        print(f"  Wind Speed: {weather['wind_speed']} km/h")
        print(f"  Wind Direction: {weather['wind_direction']}°")
    else:
        print("Failed to fetch weather data.")