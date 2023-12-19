import asyncio
from typing_extensions import override

from anthropic import AsyncAnthropic
from anthropic.types.beta import MessageStreamEvent
from anthropic.lib.streaming import AsyncMessageStream

client = AsyncAnthropic()


class MyStream(AsyncMessageStream):
    @override
    async def on_stream_event(self, event: MessageStreamEvent) -> None:
        print("on_event fired with:", event)


async def main() -> None:
    async with client.beta.messages.stream(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
        model="claude-2.1",
        event_handler=MyStream,
    ) as stream:
        accumulated = await stream.get_final_message()
        print("accumulated message: ", accumulated.model_dump_json(indent=2))


asyncio.run(main())
