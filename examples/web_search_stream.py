import asyncio

from anthropic import AsyncAnthropic


async def main() -> None:
    client = AsyncAnthropic()

    print("Claude with Web Search (Streaming)")
    print("==================================")

    # Create an async stream with web search enabled
    async with client.beta.messages.stream(
        model="claude-3-5-sonnet-latest",
        max_tokens=1024,
        messages=[{"role": "user", "content": "What's the weather in New York?"}],
        tools=[
            {
                "name": "web_search",
                "type": "web_search_20250305",
            }
        ],
    ) as stream:
        # Process streaming events
        async for chunk in stream:
            # Print text deltas as they arrive
            if chunk.type == "content_block_delta" and chunk.delta.type == "text_delta":
                print(chunk.delta.text, end="", flush=True)

            # Track when web search is being used
            elif chunk.type == "content_block_start" and chunk.content_block.type == "web_search_tool_result":
                print("\n[Web search started...]", end="", flush=True)

            elif chunk.type == "content_block_stop" and chunk.content_block.type == "web_search_tool_result":
                print("[Web search completed]", end="\n\n", flush=True)

        # Get the final complete message
        message = await stream.get_final_message()

    print("\n\nFinal usage statistics:")
    print(f"Input tokens: {message.usage.input_tokens}")
    print(f"Output tokens: {message.usage.output_tokens}")

    if message.usage.server_tool_use:
        print(f"Web search requests: {message.usage.server_tool_use.web_search_requests}")
    else:
        print("No web search requests recorded in usage")

    # Rather than parsing the web search results structure (which varies),
    # we'll just show the complete message structure for debugging
    print("\nMessage Content Types:")
    for i, block in enumerate(message.content):
        print(f"Content Block {i + 1}: Type = {block.type}")

    # Show the entire message structure as JSON for debugging
    print("\nComplete message structure (JSON):")
    print(message.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
