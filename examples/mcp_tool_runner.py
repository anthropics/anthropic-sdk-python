"""Example showing how to use MCP helpers with tool_runner().

Connects to an MCP server, converts its tools to Anthropic-compatible tools
using async_mcp_tool(), and runs them in a tool_runner() loop.

Requires: pip install anthropic[mcp]
Requires: Python 3.10+
"""

import asyncio

import rich
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from anthropic import AsyncAnthropic
from anthropic.lib.tools.mcp import async_mcp_tool

client = AsyncAnthropic()


async def main() -> None:
    # Connect to a local MCP server via stdio
    # This example uses the MCP filesystem server; replace with your own server
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_client:
            await mcp_client.initialize()

            # List available tools from the MCP server and convert them
            tools_result = await mcp_client.list_tools()
            tools = [async_mcp_tool(t, mcp_client) for t in tools_result.tools]

            print(f"Connected to MCP server with {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool.name}")
            print()

            # Run a conversation with tool_runner()
            runner = client.beta.messages.tool_runner(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                tools=tools,
                messages=[{"role": "user", "content": "List the files in /tmp"}],
            )
            async for message in runner:
                rich.print(message)


asyncio.run(main())
