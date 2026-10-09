import asyncio
import json
from typing_extensions import Literal

import rich

from anthropic import AsyncAnthropic, beta_tool

client = AsyncAnthropic()


@beta_tool
def get_weather(location: str, units: Literal["c", "f"]) -> str:
    """Lookup the weather for a given city in either celsius or fahrenheit

    Args:
        location: The city and state, e.g. San Francisco, CA
        units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit

    Returns:
        A dictionary containing the location, temperature, and weather condition.
    """
    # Simulate a weather API call
    print(f"Fetching weather for {location} in {units}")
    # Here you would typically make an API call to a weather service
    # For demonstration, we return a mock response
    if units == "c":
        return json.dumps(
            {
                "location": location,
                "temperature": "20\u00b0C",
                "condition": "Sunny",
            }
        )
    else:
        return json.dumps(
            {
                "location": location,
                "temperature": "68\u00b0F",
                "condition": "Sunny",
            }
        )


async def main() -> None:
    runner = client.beta.messages.tool_runner(
        max_tokens=1024,
        model="claude-opus-4-5",
        # alternatively, you can use `tools=[anthropic.beta_tool(get_weather)]`
        tools=[get_weather],
        messages=[{"role": "user", "content": "What is the weather in SF?"}],
    )
    async for message in runner:
        rich.print(message)


asyncio.run(main())
