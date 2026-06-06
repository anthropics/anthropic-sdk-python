#!/usr/bin/env -S uv run python
"""
Example: Verifying AI agent trust via TWZRD Agent Intel MCP server.

TWZRD Agent Intel (https://intel.twzrd.xyz) scores autonomous agents on Solana
based on on-chain transaction history. Use it to gate x402 micropayment flows
or any agent-to-agent trust decision.

This example connects to the TWZRD MCP server over streamable-http (no stdio
process required), converts its tools using async_mcp_tool(), and runs them
through a tool_runner() loop to score an agent wallet.

Requires: pip install anthropic[mcp]
Requires: Python 3.10+
"""
# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic[mcp]"]
# ///

import asyncio

import rich
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from anthropic import AsyncAnthropic
from anthropic.lib.tools.mcp import async_mcp_tool

client = AsyncAnthropic()

TWZRD_MCP_URL = "https://intel.twzrd.xyz/mcp"


async def main() -> None:
    # Connect to the TWZRD Agent Intel MCP server via streamable-http.
    # No API key is needed — score_agent, resolve_agent, and preflight_check are free.
    async with streamablehttp_client(TWZRD_MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as mcp_client:
            await mcp_client.initialize()

            tools_result = await mcp_client.list_tools()
            tools = [async_mcp_tool(t, mcp_client) for t in tools_result.tools]

            print(f"Connected to TWZRD Agent Intel with {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool.name}")
            print()

            # Ask Claude to score an agent wallet and explain the result.
            # score_agent returns a 0-100 trust score derived from on-chain history.
            runner = client.beta.messages.tool_runner(
                model="claude-opus-4-5",
                max_tokens=512,
                tools=tools,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Use score_agent to check wallet "
                            "D1QkbFJKiPsymJ65RKHhF6DFB8sPMfpBaFBzuHKfJGWi "
                            "and summarise whether it is safe to route a payment through."
                        ),
                    }
                ],
            )
            async for message in runner:
                rich.print(message)


asyncio.run(main())
