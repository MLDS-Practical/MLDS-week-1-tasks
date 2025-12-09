import csv
from typing import Dict, List, Union, TextIO

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def summarize_weather_data(data: List[Dict[str, any]]) -> Dict[str, float]:
    """
    Summarize the weather data across all days.

    Args:
        data (list of dict): The daily weather data.

    Returns:
        dict: A summary of the key metrics across all days.
    """
    # Calculate aggregate values using list comprehensions
    total_max_temp = sum(day["max_temperature"] for day in data)
    total_min_temp = sum(day["min_temperature"] for day in data)
    total_precipitation = sum(day["precipitation"] for day in data)
    total_wind_speed = sum(day["wind_speed"] for day in data)
    total_humidity = sum(day["humidity"] for day in data)

    # Count specific conditions using list comprehensions
    hot_days = sum(1 for day in data if day["max_temperature"] > 30)
    windy_days = sum(1 for day in data if day["wind_speed"] > 15)
    rainy_days = sum(1 for day in data if day["precipitation"] > 0)

    # Calculate the number of days
    count = len(data)

    # Prepare the summary dictionary
    summary = {
        "average_max_temp": total_max_temp / count,
        "average_min_temp": total_min_temp / count,
        "total_precipitation": total_precipitation,
        "average_wind_speed": total_wind_speed / count,
        "average_humidity": total_humidity / count,
        "hot_days": hot_days,
        "windy_days": windy_days,
        "rainy_days": rainy_days,
    }

    return summary


def export_to_csv(data: List[Dict[str, any]], file: Union[str, TextIO]) -> None:
    """
    Export the summarized weather data to a CSV file or file-like object.

    Args:
        data (list of dict): The daily weather data to export.
        file (str or file-like object): The name of the CSV file to save the data in, or a file-like object.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Precipitation", "Wind Speed", "Humidity",
               "Weather Description", "Is Hot Day", "Is Windy Day", "Is Rainy Day"]

    def write_data(writer: csv.DictWriter) -> None:
        """Helper function to write rows to the CSV.
        
        Args:
            writer (csv.DictWriter): The CSV writer object.
        """
        for day in data:
            writer.writerow({
                "Date": day["date"],
                "Max Temperature": day["max_temperature"],
                "Min Temperature": day["min_temperature"],
                "Precipitation": day["precipitation"],
                "Wind Speed": day["wind_speed"],
                "Humidity": day["humidity"],
                "Weather Description": day["weather_description"],
                "Is Hot Day": day["max_temperature"] > 30,
                "Is Windy Day": day["wind_speed"] > 15,
                "Is Rainy Day": day["precipitation"] > 0
            })

    # Determine whether 'file' is a filename or a file-like object
    if isinstance(file, str):
        with open(file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            write_data(writer)
    else:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        write_data(writer)


if __name__ == "__main__":
    try:
        # Load the JSON data
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Summarize the weather data
        summary = summarize_weather_data(weather_data['daily'])

        # Print the summary for verification
        print("Weather Data Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

        # Export the summarized data to a CSV file
        export_to_csv(weather_data['daily'], "tokyo_weather_summary.csv")

        print("Data successfully exported to tokyo_weather_summary.csv")
    except Exception as e:
        print(f"An error occurred: {e}")
