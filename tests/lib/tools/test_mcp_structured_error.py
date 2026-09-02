from __future__ import annotations

import json
from typing import Any

import anyio
import pytest

mcp = pytest.importorskip("mcp")

from mcp.types import Tool, TextContent, CallToolResult  # noqa: E402

from anthropic.lib.tools import ToolError  # noqa: E402
from anthropic.lib.tools.mcp import async_mcp_tool  # noqa: E402


class _Client:
    def __init__(self, result: CallToolResult) -> None:
        self.result = result

    async def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> CallToolResult:  # noqa: ARG002
        return self.result


def test_structured_only_mcp_error_preserves_payload() -> None:
    async def run() -> None:
        payload = {"code": "invalid_input", "details": {"field": "query"}}
        result = CallToolResult(content=[], structuredContent=payload, isError=True)
        tool = async_mcp_tool(Tool(name="lookup", inputSchema={"type": "object"}), _Client(result))

        with pytest.raises(ToolError) as exc_info:
            await tool.call({})

        assert exc_info.value.content == json.dumps(payload)
        assert str(exc_info.value) == json.dumps(payload)

    anyio.run(run)


def test_mcp_error_prefers_explicit_content_over_structured_fallback() -> None:
    async def run() -> None:
        result = CallToolResult(
            content=[TextContent(type="text", text="explicit failure")],
            structuredContent={"code": "fallback"},
            isError=True,
        )
        tool = async_mcp_tool(Tool(name="lookup", inputSchema={"type": "object"}), _Client(result))

        with pytest.raises(ToolError) as exc_info:
            await tool.call({})

        content = list(exc_info.value.content)
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "explicit failure"

    anyio.run(run)


def test_structured_only_mcp_success_remains_json_string() -> None:
    async def run() -> None:
        payload = {"status": "ok"}
        result = CallToolResult(content=[], structuredContent=payload, isError=False)
        tool = async_mcp_tool(Tool(name="lookup", inputSchema={"type": "object"}), _Client(result))

        assert await tool.call({}) == json.dumps(payload)

    anyio.run(run)
