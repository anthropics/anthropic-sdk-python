from __future__ import annotations

from anthropic import Anthropic

client = Anthropic()

# Create a message with web search enabled
message = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What's the weather in New York?"}],
    tools=[
        {
            "name": "web_search",
            "type": "web_search_20250305",
        }
    ],
)

# Print the full response
print("\nFull response:")
print(message.model_dump_json(indent=2))

# Extract and print the content
print("\nResponse content:")
for content_block in message.content:
    if content_block.type == "text":
        print(content_block.text)

# Print usage information
print("\nUsage statistics:")
print(f"Input tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")
if message.usage.server_tool_use:
    print(f"Web search requests: {message.usage.server_tool_use.web_search_requests}")
