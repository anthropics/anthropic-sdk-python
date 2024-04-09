import asyncio

from anthropic import AnthropicVertex, AsyncAnthropicVertex


def sync_client() -> None:
    print("------ Sync Vertex ------")

    client = AnthropicVertex()

    message = client.messages.create(
        model="claude-3-sonnet@20240229",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": "Hello!",
            }
        ],
    )
    print(message.to_json())


async def async_client() -> None:
    print("------ Async Vertex ------")

    client = AsyncAnthropicVertex()

    message = await client.messages.create(
        model="claude-3-sonnet@20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello!",
            }
        ],
    )
    print(message.to_json())


sync_client()
asyncio.run(async_client())
