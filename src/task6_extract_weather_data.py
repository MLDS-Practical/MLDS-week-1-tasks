import csv
import re
from typing import List, Dict


def clean_text(line: str) -> str:
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    # Replace non-breaking spaces and other non-ASCII characters
    line = line.replace("Â", "")
    return line


def extract_weather_data(text_file: str) -> List[Dict[str, any]]:
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str): Path to the text file.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.

    Raises:
        FileNotFoundError: If the text file does not exist.
    """
    try:
        with open(text_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"The text file '{text_file}' was not found.")

    pattern = r"Date: (\d{4}-\d{2}-\d{2}), Max Temp: ([\d.]+)°C, Min Temp: ([\d.]+)°C, Humidity: (\d+)%?, Precipitation: ([\d.]+)mm"

    extracted_data = []
    for line in lines:
        cleaned_line = clean_text(line)  # Clean the line before processing
        match = re.search(pattern, cleaned_line)
        if match:
            date, max_temp, min_temp, humidity, precipitation = match.groups()
            extracted_data.append({
                "date": date,
                "max_temperature": float(max_temp),
                "min_temperature": float(min_temp),
                "humidity": int(humidity),
                "precipitation": float(precipitation)
            })
        else:
            print(f"No match found for line: {line.strip()}")  # Debugging line

    return extracted_data


def save_to_csv(data: List[Dict[str, any]], filename: str = "extracted_weather_data.csv") -> None:
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Humidity", "Precipitation"]
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for entry in data:
                writer.writerow({
                    "Date": entry["date"],
                    "Max Temperature": entry["max_temperature"],
                    "Min Temperature": entry["min_temperature"],
                    "Humidity": entry["humidity"],
                    "Precipitation": entry["precipitation"]
                })
    except IOError as e:
        raise IOError(f"Error writing to file '{filename}': {e}")


if __name__ == "__main__":
    try:
        # Extract data from the text file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.join(script_dir, "weather_report.txt")
        weather_data = extract_weather_data(txt_path)

        # Save the extracted data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully extracted and saved to extracted_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")
