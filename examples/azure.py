# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "anthropic",
# ]
#
# [tool.uv.sources]
# anthropic = { path = "../", editable = true }
# ///

from anthropic import AnthropicFoundry

cl = AnthropicFoundry(
    resource="your-resource-name",
    api_key="your-foundry-anthropic-api-key",
)

response = cl.messages.create(
    model="claude-haiku-4-5",
    messages=[
        {"role": "user", "content": "Hello!"},
    ],
    max_tokens=1024,
)

print(response)
