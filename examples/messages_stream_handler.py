import asyncio
from typing_extensions import override

from anthropic import AsyncAnthropic, AsyncMessageStream
from anthropic.types import MessageStreamEvent

client = AsyncAnthropic()


class MyStream(AsyncMessageStream):
    @override
    async def on_stream_event(self, event: MessageStreamEvent) -> None:
        print("on_event fired with:", event)


async def main() -> None:
    async with client.messages.stream(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
        model="claude-3-opus-20240229",
        event_handler=MyStream,
    ) as stream:
        accumulated = await stream.get_final_message()
        print("accumulated message: ", accumulated.to_json())


asyncio.run(main())
