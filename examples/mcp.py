#!/usr/bin/env -S rye run python

from anthropic import Anthropic

anthropic = Anthropic()

response = anthropic.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "Calculate 1+2",
        },
    ],
    mcp_servers=[
        {
            "type": "url",
            "url": "http://example-server.modelcontextprotocol.io/sse",
            "authorization_token": "YOUR_TOKEN",
            "name": "example",
            "tool_configuration": {  # Optional, by default all tools are enabled
                "enabled": True,
                "allowed_tools": ["echo", "add"],  # Optional
            },
        }
    ],
    extra_headers={
        "anthropic-beta": "mcp-client-2025-04-04",
    },
)
print(response.content)
