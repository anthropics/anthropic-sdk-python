#!/usr/bin/env -S uv run python

"""Example demonstrating tool use (function calling) with the Anthropic SDK.

This example shows how to:
1. Define tools with JSON Schema input descriptions
2. Send a message that triggers tool use
3. Process the tool call and return results
4. Get Claude's final response incorporating the tool results

Usage:
    export ANTHROPIC_API_KEY="your-api-key"
    python examples/tool_use.py
"""

import json

from anthropic import Anthropic

client = Anthropic()

# Define tools that Claude can use
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and country, e.g. 'London, UK'",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit (default: celsius)",
                },
            },
            "required": ["location"],
        },
    }
]


def get_weather(location: str, unit: str = "celsius") -> dict:
    """Simulate a weather API call.

    In a real application, this would call an actual weather API.
    """
    # Simulated weather data
    weather_data = {
        "London, UK": {"temp": 12, "condition": "Cloudy", "humidity": 78},
        "New York, US": {"temp": 22, "condition": "Sunny", "humidity": 45},
        "Tokyo, JP": {"temp": 18, "condition": "Partly cloudy", "humidity": 60},
    }

    data = weather_data.get(location, {"temp": 20, "condition": "Unknown", "humidity": 50})

    if unit == "fahrenheit":
        data["temp"] = round(data["temp"] * 9 / 5 + 32)

    return {
        "location": location,
        "temperature": data["temp"],
        "unit": unit,
        "condition": data["condition"],
        "humidity": data["humidity"],
    }


def process_tool_call(tool_name: str, tool_input: dict) -> str:
    """Route tool calls to the appropriate function."""
    if tool_name == "get_weather":
        result = get_weather(**tool_input)
        return json.dumps(result)

    return json.dumps({"error": f"Unknown tool: {tool_name}"})


def main() -> None:
    print("=== Tool Use Example ===\n")

    # Step 1: Send a message that will trigger tool use
    user_message = "What's the weather like in London and Tokyo?"
    print(f"User: {user_message}\n")

    messages = [{"role": "user", "content": user_message}]

    # Step 2: Get Claude's response (may include tool use requests)
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

    # Step 3: Process tool calls in a loop until Claude gives a final response
    while response.stop_reason == "tool_use":
        # Collect all tool use blocks from the response
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"Tool call: {block.name}({json.dumps(block.input)})")
                result = process_tool_call(block.name, block.input)
                print(f"Tool result: {result}\n")

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )

        # Step 4: Send tool results back to Claude
        messages = [
            *messages,
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": tool_results},
        ]

        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )

    # Step 5: Print Claude's final response
    for block in response.content:
        if hasattr(block, "text"):
            print(f"Claude: {block.text}")


if __name__ == "__main__":
    main()
