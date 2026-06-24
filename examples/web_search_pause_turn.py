from __future__ import annotations

from anthropic import Anthropic
from anthropic.types import Message, MessageParam

client = Anthropic()


def assistant_turn_from_message(message: Message) -> MessageParam:
    """Preserve paused server-tool blocks exactly as the SDK returned them."""
    return {"role": "assistant", "content": message.content}


messages: list[MessageParam] = [
    {"role": "user", "content": "Search for the latest Claude web search documentation."}
]

while True:
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=messages,
        tools=[
            {
                "name": "web_search",
                "type": "web_search_20250305",
            }
        ],
    )

    if message.stop_reason != "pause_turn":
        break

    # Keep the full assistant turn intact. Splitting, filtering, or rewriting
    # individual server_tool_use blocks can orphan tool state on the next request.
    messages.append(assistant_turn_from_message(message))


print(message.model_dump_json(indent=2))
