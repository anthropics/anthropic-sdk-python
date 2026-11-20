#!/usr/bin/env -S uv run python
"""Use Parallel Search MCP over Streamable HTTP with the Claude tool runner.

Install: pip install 'anthropic[mcp]' 'mcp>=1.26,<2'
Run: ANTHROPIC_API_KEY=... python examples/parallel_search_mcp.py
Optional: set ANTHROPIC_MODEL to choose a different Claude model.

Parallel search and page fetching need no Parallel account or API key. Anonymous
search uses Fast mode and is rate limited; the Claude API requires its own key.
See https://docs.parallel.ai/integrations/mcp/search-mcp.
"""

import os
import uuid

import anyio
from mcp.client.session_group import ClientSessionGroup, StreamableHttpParameters

from anthropic import AsyncAnthropic
from anthropic.lib.tools.mcp import async_mcp_tool


async def main() -> None:
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5")
    session_id = str(uuid.uuid4())

    server_params = StreamableHttpParameters(
        url="https://search.parallel.ai/mcp",
        headers={"User-Agent": "anthropic-sdk-python/parallel-search-example"},
    )
    async with AsyncAnthropic() as client, ClientSessionGroup() as group:
        mcp_client = await group.connect_to_server(server_params)
        tools = [async_mcp_tool(tool, mcp_client) for tool in group.tools.values()]

        runner = client.beta.messages.tool_runner(
            model=model,
            max_tokens=2048,
            tools=tools,
            system=f"Use session_id={session_id} and model_name={model} on every search and fetch call.",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Search for the Claude Python SDK documentation, then fetch "
                        "https://platform.claude.com/docs/en/api/sdks/python and summarize "
                        "how to install the SDK. Include the source URL."
                    ),
                }
            ],
        )
        async for message in runner:
            print(message)


if __name__ == "__main__":
    anyio.run(main)
