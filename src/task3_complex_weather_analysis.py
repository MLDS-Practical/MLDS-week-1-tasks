from typing import Dict, List, Any

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def analyze_daily_weather(day: Dict[str, Any], temp_threshold: float = 30, 
                          wind_threshold: float = 15, humidity_threshold: float = 70) -> Dict[str, Any]:
    """
    Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """
    date = day["date"]
    max_temperature = day["max_temperature"]
    min_temperature = day["min_temperature"]
    precipitation = day["precipitation"]
    wind_speed = day["wind_speed"]
    humidity = day["humidity"]
    weather_description = day["weather_description"]

    is_hot_day = max_temperature > temp_threshold
    temperature_swing = max_temperature - min_temperature
    is_windy_day = wind_speed > wind_threshold
    is_uncomfortable_day = humidity > humidity_threshold
    is_rainy_day = precipitation > 0

    analysis = {
        "date": date,
        "is_hot_day": is_hot_day,
        "max_temperature": max_temperature,
        "min_temperature": min_temperature,
        "temperature_swing": temperature_swing,
        "is_windy_day": is_windy_day,
        "wind_speed": wind_speed,
        "is_uncomfortable_day": is_uncomfortable_day,
        "humidity": humidity,
        "is_rainy_day": is_rainy_day,
        "precipitation": precipitation,
        "weather_description": weather_description
    }

    return analysis


def generate_daily_report(analysis: Dict[str, Any]) -> str:
    """
    Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A detailed report as a string.
    """
    # Core information about the day
    report_lines = [
        f"Date: {analysis['date']}",
        f"Weather: {analysis['weather_description']}",
        f"Temperature: Max {analysis['max_temperature']}°C, Min {analysis['min_temperature']}°C (Swing: {analysis['temperature_swing']}°C)"
    ]

    # Conditional messages for specific weather conditions
    conditions = {
        "is_hot_day": "It was a hot day.",
        "temperature_swing": f"The temperature swing was significant at {analysis['temperature_swing']}°C."
                             if analysis["temperature_swing"] > 10 else "",
        "is_windy_day": "It was a windy day.",
        "is_uncomfortable_day": "The humidity made the day uncomfortable.",
        "is_rainy_day": "It was a rainy day.",
    }

    # Add conditional messages to the report
    for key, message in conditions.items():
        if isinstance(analysis[key], bool) and analysis[key]:  # Add messages for boolean conditions
            report_lines.append(message)
        elif key == "temperature_swing" and message:  # Add message for temperature swing if it exists
            report_lines.append(message)

    # Add a message for no precipitation if the day was not rainy
    if not analysis["is_rainy_day"]:
        report_lines.append("There was no precipitation.")

    # Combine all lines into a single string separated by newlines
    return "\n".join(report_lines)


def summarize_weather_analysis(analyses: List[Dict[str, Any]]) -> str:
    """
    Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report as a string.
    """
    hottest_day = max(analyses, key=lambda x: x['max_temperature'])
    windiest_day = max(analyses, key=lambda x: x['wind_speed'])
    most_humid_day = max(analyses, key=lambda x: x['humidity'])
    rainiest_day = max(analyses, key=lambda x: x['precipitation'])

    summary = "Weather Summary:\n"
    summary += f"Hottest day: {hottest_day['date']} with a maximum temperature of {hottest_day['max_temperature']}°C\n"
    summary += f"Windiest day: {windiest_day['date']} with wind speeds of {windiest_day['wind_speed']} km/h\n"
    summary += f"Most humid day: {most_humid_day['date']} with a humidity level of {most_humid_day['humidity']}%\n"
    summary += f"Rainiest day: {rainiest_day['date']} with {rainiest_day['precipitation']} mm of precipitation\n"

    return summary


if __name__ == "__main__":
    try:
        # Load the JSON data
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Analyze the weather data for each day
        analyses = [analyze_daily_weather(day) for day in weather_data['daily']]

        # Generate and print daily reports
        for analysis in analyses:
            report = generate_daily_report(analysis)
            print(report)

        # Generate and print a summary report
        summary_report = summarize_weather_analysis(analyses)
        print(summary_report)
    except Exception as e:
        print(f"An error occurred: {e}")
