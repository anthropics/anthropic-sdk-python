import json
from typing import Any, List
from typing_extensions import Literal

import rich

from anthropic import Anthropic, beta_tool
from anthropic.lib.tools import BetaFunctionTool, BetaFunctionToolResultType
from anthropic.types.beta import BetaToolReferenceBlockParam

client = Anthropic()


@beta_tool(defer_loading=True)
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
                "temperature": "20°C",
                "condition": "Sunny",
            }
        )
    else:
        return json.dumps(
            {
                "location": location,
                "temperature": "68°F",
                "condition": "Sunny",
            }
        )


def make_tool_searcher(tools: List[BetaFunctionTool[Any]]) -> BetaFunctionTool[Any]:
    """Returns a tool that Claude can use to search through all available tools"""

    @beta_tool
    def search_available_tools(*, keyword: str) -> BetaFunctionToolResultType:
        """Search for useful tools using a query string"""

        results: list[BetaToolReferenceBlockParam] = []
        for tool in tools:
            if keyword in json.dumps(tool.to_dict()):
                results.append({"type": "tool_reference", "tool_name": tool.name})

        return results

    return search_available_tools


def main() -> None:
    tools: list[BetaFunctionTool[Any]] = [
        get_weather,
        # ... many more tools
    ]
    runner = client.beta.messages.tool_runner(
        max_tokens=1024,
        model="claude-sonnet-4-5-20250929",
        tools=[*tools, make_tool_searcher(tools)],
        messages=[{"role": "user", "content": "What is the weather in SF?"}],
        betas=["tool-search-tool-2025-10-19"],
    )
    for message in runner:
        rich.print(message)


main()
