import asyncio
from typing_extensions import override

from anthropic import AsyncAnthropic
from anthropic.lib.streaming.beta import AsyncToolsBetaMessageStream

client = AsyncAnthropic()


class MyHandler(AsyncToolsBetaMessageStream):
    @override
    async def on_input_json(self, delta: str, snapshot: object) -> None:
        print(f"delta: {repr(delta)}")
        print(f"snapshot: {snapshot}")
        print()


async def main() -> None:
    async with client.beta.tools.messages.stream(
        max_tokens=1024,
        model="claude-3-haiku-20240307",
        tools=[
            {
                "name": "get_weather",
                "description": "Get the weather at a specific location",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "Unit for the output",
                        },
                    },
                    "required": ["location"],
                },
            }
        ],
        messages=[{"role": "user", "content": "What is the weather in SF?"}],
        event_handler=MyHandler,
    ) as stream:
        async for event in stream:
            if event.type == "input_json":
                print(f"delta: {repr(event.partial_json)}")
                print(f"snapshot: {event.snapshot}")

    print()


asyncio.run(main())
