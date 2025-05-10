import requests

API_KEY = "cac2742878f46724288600b6b2c6aee2"

def get_weather(city):
    """Fetch weather data for the given city."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for 4xx/5xx errors
        data = response.json()
        
        if data["cod"] != 200:
            print(f"Error: {data.get('message', 'Unknown error')}")
            return None
        
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        return weather
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("Error: Invalid or unauthorized API key. Please verify your API key on openweathermap.org.")
        else:
            print(f"HTTP error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error parsing API response: {e}")
        return None

def display_weather(weather):
    """Display formatted weather details."""
    if weather:
        print(f"\nWeather in {weather['city']}:")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Description: {weather['description']}")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Wind Speed: {weather['wind_speed']} m/s")
    else:
        print("Failed to retrieve weather data.")

def main():
    print("Weather App")
    
    while True:
        city = input("\nEnter city name (or 'quit' to exit): ").strip()
        if city.lower() == "quit":
            print("Exiting.")
            break
        if not city:
            print("City name cannot be empty.")
            continue
        
        weather = get_weather(city)
        display_weather(weather)

if __name__ == "__main__":
    main()