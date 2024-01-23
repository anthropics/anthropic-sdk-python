import asyncio

from anthropic import AnthropicVertex, AsyncAnthropicVertex


def sync_client() -> None:
    print("------ Sync Vertex ------")

    client = AnthropicVertex()

    message = client.beta.messages.create(
        model="claude-instant-1p2",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
    )
    print(message.model_dump_json(indent=2))


async def async_client() -> None:
    print("------ Async Vertex ------")

    client = AsyncAnthropicVertex()

    message = await client.beta.messages.create(
        model="claude-instant-1p2",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
    )
    print(message.model_dump_json(indent=2))


sync_client()
asyncio.run(async_client())
