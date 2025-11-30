"""
Weather Tool Schema Examples for Anthropic SDK

This file demonstrates both manual and decorator-based approaches
for defining a weather tool with proper JSON schema.
"""

from typing_extensions import Literal
from anthropic import Anthropic, beta_tool
from anthropic.types import ToolParam
import json


# ============================================================================
# Approach 1: Manual Dictionary-Based Tool Definition
# ============================================================================

weather_tool_manual: ToolParam = {
    "name": "get_weather",
    "description": "Get current weather information for a specified location. Returns temperature, conditions, humidity, and wind speed.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, country, or coordinates (e.g., 'San Francisco, CA', 'London, UK', '40.7128,-74.0060')"
            },
            "units": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit for the response. Defaults to celsius if not specified.",
                "default": "celsius"
            },
            "include_forecast": {
                "type": "boolean",
                "description": "Whether to include a 5-day forecast in addition to current weather",
                "default": False
            },
            "details": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["temperature", "humidity", "wind", "precipitation", "uv_index", "air_quality"]
                },
                "description": "Specific weather details to include. If not provided, returns all available data.",
                "default": ["temperature", "humidity", "wind"]
            }
        },
        "required": ["location"],
        "additionalProperties": False
    }
}


# ============================================================================
# Approach 2: Decorator-Based Tool Definition (Auto-Generated Schema)
# ============================================================================

@beta_tool
def get_weather(
    location: str,
    units: Literal["celsius", "fahrenheit"] = "celsius",
    include_forecast: bool = False
) -> str:
    """Get current weather information for a specified location.

    Returns temperature, conditions, humidity, and wind speed.

    Args:
        location: The city and state, country, or coordinates
                 (e.g., 'San Francisco, CA', 'London, UK', '40.7128,-74.0060')
        units: Temperature unit for the response
        include_forecast: Whether to include a 5-day forecast in addition to current weather

    Returns:
        JSON string containing weather information
    """
    # Mock implementation - replace with actual weather API call
    weather_data = {
        "location": location,
        "current": {
            "temperature": 72 if units == "fahrenheit" else 22,
            "units": units,
            "conditions": "Partly cloudy",
            "humidity": 65,
            "wind_speed": 10,
            "wind_direction": "NW"
        }
    }

    if include_forecast:
        weather_data["forecast"] = [
            {"day": "Tomorrow", "high": 75 if units == "fahrenheit" else 24, "low": 60 if units == "fahrenheit" else 16},
            {"day": "Day 2", "high": 73 if units == "fahrenheit" else 23, "low": 58 if units == "fahrenheit" else 14},
        ]

    return json.dumps(weather_data)


# ============================================================================
# Example Usage
# ============================================================================

def example_manual_tool():
    """Example using manual tool definition"""
    client = Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=[weather_tool_manual],
        messages=[
            {"role": "user", "content": "What's the weather in Tokyo?"}
        ]
    )

    print("Manual tool response:", response)


def example_decorator_tool():
    """Example using decorator-based tool"""
    client = Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=[get_weather],  # Decorator allows passing function directly
        messages=[
            {"role": "user", "content": "What's the weather in Paris in celsius?"}
        ]
    )

    print("Decorator tool response:", response)


# ============================================================================
# Advanced: Weather Tool with Complex Schema
# ============================================================================

advanced_weather_tool: ToolParam = {
    "name": "get_detailed_weather",
    "description": "Get comprehensive weather information including current conditions, forecasts, and alerts for a specified location.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "state": {"type": "string", "description": "State or province code (optional)"},
                    "country": {"type": "string", "description": "Country code (ISO 3166-1 alpha-2)"}
                },
                "required": ["city", "country"],
                "description": "Location details as a structured object"
            },
            "preferences": {
                "type": "object",
                "properties": {
                    "units": {
                        "type": "string",
                        "enum": ["metric", "imperial"],
                        "default": "metric"
                    },
                    "language": {
                        "type": "string",
                        "description": "Language code for weather descriptions (e.g., 'en', 'es', 'fr')",
                        "default": "en"
                    }
                }
            },
            "data_points": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "current_conditions",
                        "hourly_forecast",
                        "daily_forecast",
                        "severe_alerts",
                        "air_quality",
                        "pollen_count",
                        "moon_phase",
                        "sunrise_sunset"
                    ]
                },
                "minItems": 1,
                "description": "Specific data points to retrieve"
            }
        },
        "required": ["location", "data_points"],
        "additionalProperties": False
    }
}


if __name__ == "__main__":
    # Print the auto-generated schema from the decorator
    print("Auto-generated schema from @beta_tool decorator:")
    print(json.dumps(get_weather.to_params(), indent=2))

    print("\n" + "="*80 + "\n")

    print("Manual weather tool schema:")
    print(json.dumps(weather_tool_manual, indent=2))
