import requests
from typing import Dict

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_weather_data() -> Dict[str, any]:
    """
    Fetch the maximum temperature forecast for Tokyo using the Open-Meteo API.

    Returns:
        dict: A dictionary containing the date and the maximum temperature.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.RequestException: If there was a network error.
        KeyError: If the expected data is not in the API response.
    """
    url = ("https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917"
           "&daily=temperature_2m_max&timezone=Asia/Tokyo")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check that the request was successful

        # Parse the JSON response
        data = response.json()

        # Extract the date and maximum temperature
        date = data['daily']['time'][0]
        max_temperature = data['daily']['temperature_2m_max'][0]

        return {"date": date, "max_temperature": max_temperature}
    except requests.RequestException as e:
        raise requests.RequestException(f"Error fetching weather data: {e}")
    except KeyError as e:
        raise KeyError(f"Unexpected API response format. Missing key: {e}")


if __name__ == "__main__":
    try:
        # Fetch the weather data
        weather_data = fetch_weather_data()

        # Save the data to a JSON file
        save_to_json(weather_data, "tokyo_weather.json")

        print("Data successfully saved to tokyo_weather.json")
    except Exception as e:
        print(f"An error occurred: {e}")
