# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportMissingImports=false, reportUnknownParameterType=false
from __future__ import annotations

import json
import base64
from typing import Any
from unittest.mock import AsyncMock

import anyio
import pytest

mcp = pytest.importorskip("mcp")

from mcp.types import (  # noqa: E402
    Tool,
    TextContent,
    AudioContent,
    ImageContent,
    ResourceLink,
    PromptMessage,
    CallToolResult,
    EmbeddedResource,
    ReadResourceResult,
    BlobResourceContents,
    TextResourceContents,
)

from anthropic.lib.tools import ToolError
from anthropic.lib.tools.mcp import (
    UnsupportedMCPValueError,
    mcp_tool,
    mcp_content,
    mcp_message,
    async_mcp_tool,
    mcp_resource_to_file,
    mcp_resource_to_content,
)

# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------


def _text_resource(uri: str = "file:///x.txt", text: str = "hello", mime: str | None = None) -> TextResourceContents:
    return TextResourceContents.model_validate({"uri": uri, "text": text, **({"mimeType": mime} if mime else {})})


def _blob_resource(uri: str = "file:///x.bin", blob: str = "", mime: str | None = None) -> BlobResourceContents:
    return BlobResourceContents.model_validate({"uri": uri, "blob": blob, **({"mimeType": mime} if mime else {})})


def _read_result(contents: list[Any]) -> ReadResourceResult:
    return ReadResourceResult.model_validate({"contents": contents})


def _mock_client(result: CallToolResult | None = None) -> Any:
    """Return a mock that quacks like ClientSession.call_tool."""
    default = CallToolResult(content=[TextContent(type="text", text="tool output")], isError=False)
    mock = type("MockClient", (), {"call_tool": AsyncMock(return_value=result or default)})()
    return mock


# -----------------------------------------------------------------------
# Tests: mcp_content
# -----------------------------------------------------------------------


class TestMCPContent:
    def test_text_content(self) -> None:
        result = mcp_content(TextContent(type="text", text="hello world"))
        assert result["type"] == "text"
        assert result["text"] == "hello world"

    def test_text_content_with_cache_control(self) -> None:
        result = mcp_content(TextContent(type="text", text="hi"), cache_control={"type": "ephemeral"})
        assert not isinstance(result, str)
        assert result["type"] == "text"
        assert "cache_control" in result
        assert result["cache_control"] == {"type": "ephemeral"}

    def test_image_content_png(self) -> None:
        result = mcp_content(ImageContent(type="image", data="abc123", mimeType="image/png"))
        assert result["type"] == "image"
        source = result["source"]
        assert source["type"] == "base64"
        assert source["data"] == "abc123"
        assert source["media_type"] == "image/png"

    def test_image_content_jpeg(self) -> None:
        result = mcp_content(ImageContent(type="image", data="abc", mimeType="image/jpeg"))
        assert not isinstance(result, str)
        assert result["type"] == "image"
        assert "media_type" in result["source"]
        assert result["source"]["media_type"] == "image/jpeg"

    def test_image_content_gif(self) -> None:
        result = mcp_content(ImageContent(type="image", data="abc", mimeType="image/gif"))
        assert result["type"] == "image"

    def test_image_content_webp(self) -> None:
        result = mcp_content(ImageContent(type="image", data="abc", mimeType="image/webp"))
        assert result["type"] == "image"

    def test_image_unsupported_mime_type(self) -> None:
        with pytest.raises(UnsupportedMCPValueError, match="image/bmp"):
            mcp_content(ImageContent(type="image", data="abc", mimeType="image/bmp"))

    def test_embedded_resource_text(self) -> None:
        resource = _text_resource(text="doc content", mime="text/plain")
        result = mcp_content(EmbeddedResource(type="resource", resource=resource))
        assert result["type"] == "document"
        assert result["source"]["type"] == "text"
        assert result["source"]["data"] == "doc content"

    def test_embedded_resource_pdf(self) -> None:
        pdf_data = base64.b64encode(b"pdf bytes").decode()
        resource = _blob_resource(uri="file:///doc.pdf", blob=pdf_data, mime="application/pdf")
        result = mcp_content(EmbeddedResource(type="resource", resource=resource))
        assert result["type"] == "document"
        assert result["source"]["type"] == "base64"
        assert result["source"]["media_type"] == "application/pdf"

    def test_embedded_resource_image(self) -> None:
        resource = _blob_resource(uri="file:///img.png", blob="aW1nZGF0YQ==", mime="image/png")
        result = mcp_content(EmbeddedResource(type="resource", resource=resource))
        assert result["type"] == "image"
        assert "media_type" in result["source"]
        assert result["source"]["media_type"] == "image/png"

    def test_audio_unsupported(self) -> None:
        with pytest.raises(UnsupportedMCPValueError, match="audio"):
            mcp_content(AudioContent(type="audio", data="base64data", mimeType="audio/mpeg"))

    def test_resource_link_unsupported(self) -> None:
        with pytest.raises(UnsupportedMCPValueError, match="resource_link"):
            mcp_content(
                ResourceLink.model_validate({"type": "resource_link", "uri": "https://example.com", "name": "x"})
            )

    def test_embedded_resource_no_mime_defaults_to_text(self) -> None:
        resource = _text_resource(text="content")
        result = mcp_content(EmbeddedResource(type="resource", resource=resource))
        assert result["type"] == "document"
        assert result["source"]["type"] == "text"
        assert result["source"]["data"] == "content"

    def test_embedded_resource_unsupported_mime(self) -> None:
        resource = _blob_resource(blob="data", mime="application/octet-stream")
        with pytest.raises(UnsupportedMCPValueError, match="application/octet-stream"):
            mcp_content(EmbeddedResource(type="resource", resource=resource))

    def test_embedded_resource_image_requires_blob(self) -> None:
        resource = _text_resource(text="not blob", mime="image/png")
        with pytest.raises(UnsupportedMCPValueError, match="blob data"):
            mcp_content(EmbeddedResource(type="resource", resource=resource))

    def test_embedded_resource_pdf_requires_blob(self) -> None:
        resource = _text_resource(text="not blob", mime="application/pdf")
        with pytest.raises(UnsupportedMCPValueError, match="blob data"):
            mcp_content(EmbeddedResource(type="resource", resource=resource))


# -----------------------------------------------------------------------
# Tests: mcp_message
# -----------------------------------------------------------------------


class TestMCPMessage:
    def test_user_message(self) -> None:
        msg = PromptMessage(role="user", content=TextContent(type="text", text="hello"))
        result = mcp_message(msg)
        assert result["role"] == "user"
        content_list = result["content"]
        assert len(content_list) == 1
        block: Any = content_list[0]
        assert block["type"] == "text"
        assert block["text"] == "hello"

    def test_assistant_message(self) -> None:
        msg = PromptMessage(role="assistant", content=TextContent(type="text", text="hi there"))
        result = mcp_message(msg)
        assert result["role"] == "assistant"

    def test_message_with_cache_control(self) -> None:
        msg = PromptMessage(role="user", content=TextContent(type="text", text="hi"))
        result = mcp_message(msg, cache_control={"type": "ephemeral"})
        block = result["content"][0]
        assert block["cache_control"] == {"type": "ephemeral"}

    def test_list_comprehension(self) -> None:
        msgs = [
            PromptMessage(role="user", content=TextContent(type="text", text="q1")),
            PromptMessage(role="assistant", content=TextContent(type="text", text="a1")),
        ]
        result = [mcp_message(m) for m in msgs]
        assert len(result) == 2
        assert result[0]["role"] == "user"
        assert result[1]["role"] == "assistant"


# -----------------------------------------------------------------------
# Tests: mcp_resource_to_content
# -----------------------------------------------------------------------


class TestMCPResourceToContent:
    def test_text_resource(self) -> None:
        result = mcp_resource_to_content(_read_result([_text_resource(text="hello", mime="text/plain").model_dump()]))
        assert result["type"] == "document"
        assert "data" in result["source"]
        assert result["source"]["data"] == "hello"

    def test_pdf_resource(self) -> None:
        pdf_data = base64.b64encode(b"pdf content").decode()
        result = mcp_resource_to_content(
            _read_result([_blob_resource(blob=pdf_data, mime="application/pdf").model_dump()])
        )
        assert result["type"] == "document"
        assert "media_type" in result["source"]
        assert result["source"]["media_type"] == "application/pdf"

    def test_image_resource(self) -> None:
        result = mcp_resource_to_content(_read_result([_blob_resource(blob="aW1n", mime="image/png").model_dump()]))
        assert result["type"] == "image"

    def test_empty_contents_raises(self) -> None:
        with pytest.raises(UnsupportedMCPValueError, match="at least one item"):
            mcp_resource_to_content(ReadResourceResult(contents=[]))

    def test_no_supported_mime_raises(self) -> None:
        with pytest.raises(UnsupportedMCPValueError, match="No supported MIME type"):
            mcp_resource_to_content(
                _read_result([_blob_resource(blob="", mime="application/octet-stream").model_dump()])
            )

    def test_selects_first_supported(self) -> None:
        result = mcp_resource_to_content(
            _read_result(
                [
                    _blob_resource(blob="", mime="application/octet-stream").model_dump(),
                    _text_resource(text="found it", mime="text/plain").model_dump(),
                ]
            )
        )
        assert result["type"] == "document"
        assert "data" in result["source"]
        assert result["source"]["data"] == "found it"


# -----------------------------------------------------------------------
# Tests: mcp_resource_to_file
# -----------------------------------------------------------------------


class TestMCPResourceToFile:
    def test_text_resource(self) -> None:
        name, data, _ = mcp_resource_to_file(
            _read_result([_text_resource(uri="file:///path/to/doc.txt", text="hello").model_dump()])
        )
        assert name == "doc.txt"
        assert data == b"hello"

    def test_blob_resource(self) -> None:
        blob = base64.b64encode(b"binary data").decode()
        name, data, mime = mcp_resource_to_file(
            _read_result([_blob_resource(uri="file:///img.png", blob=blob, mime="image/png").model_dump()])
        )
        assert name == "img.png"
        assert data == b"binary data"
        assert mime == "image/png"

    def test_empty_contents_raises(self) -> None:
        with pytest.raises(UnsupportedMCPValueError):
            mcp_resource_to_file(ReadResourceResult(contents=[]))


# -----------------------------------------------------------------------
# Tests: tool wrappers
# -----------------------------------------------------------------------


class TestMCPToolFactory:
    def test_mcp_tool_to_dict(self) -> None:
        tool = Tool(
            name="my_tool",
            description="Does stuff",
            inputSchema={"type": "object", "properties": {"x": {"type": "integer"}}},
        )
        d: Any = mcp_tool(tool, _mock_client()).to_dict()
        assert d["name"] == "my_tool"
        assert d["description"] == "Does stuff"
        assert d["input_schema"]["type"] == "object"

    def test_mcp_tool_name(self) -> None:
        tool = Tool(name="my_tool", inputSchema={"type": "object"})
        runnable = mcp_tool(tool, _mock_client())
        assert runnable.name == "my_tool"

    def test_mcp_tool_no_description(self) -> None:
        tool = Tool(name="t", inputSchema={"type": "object"})
        d: Any = mcp_tool(tool, _mock_client()).to_dict()
        assert d.get("description", "") == ""

    def test_mcp_tool_with_cache_control(self) -> None:
        tool = Tool(name="t", inputSchema={"type": "object"})
        d: Any = mcp_tool(tool, _mock_client(), cache_control={"type": "ephemeral"}).to_dict()
        assert d["cache_control"] == {"type": "ephemeral"}

    def test_list_comprehension(self) -> None:
        tools = [Tool(name="t1", inputSchema={"type": "object"}), Tool(name="t2", inputSchema={"type": "object"})]
        client = _mock_client()
        result = [mcp_tool(t, client) for t in tools]
        assert len(result) == 2
        assert result[0].name == "t1"
        assert result[1].name == "t2"


class TestAsyncMCPToolFactory:
    def test_async_mcp_tool_to_dict(self) -> None:
        tool = Tool(name="async_tool", inputSchema={"type": "object"})
        d: Any = async_mcp_tool(tool, _mock_client()).to_dict()
        assert d["name"] == "async_tool"


class TestAsyncMCPToolCall:
    def test_call_success(self) -> None:
        async def _test() -> None:
            tool = Tool(name="calc", inputSchema={"type": "object"})
            call_result = CallToolResult(content=[TextContent(type="text", text="42")], isError=False)
            client = _mock_client(result=call_result)
            runnable = async_mcp_tool(tool, client)

            result = await runnable.call({"x": 1})
            assert isinstance(result, list)
            block = result[0]
            assert block["type"] == "text"
            assert block["text"] == "42"

            client.call_tool.assert_awaited_once_with(name="calc", arguments={"x": 1})

        anyio.run(_test)

    def test_call_error(self) -> None:
        async def _test() -> None:
            tool = Tool(name="fail_tool", inputSchema={"type": "object"})
            call_result = CallToolResult(
                content=[TextContent(type="text", text="something went wrong")],
                isError=True,
            )
            client = _mock_client(result=call_result)
            runnable = async_mcp_tool(tool, client)

            with pytest.raises(ToolError, match="something went wrong") as exc_info:
                await runnable.call({})
            # ToolError carries structured content blocks
            content = list(exc_info.value.content)
            block: Any = content[0]
            assert block["type"] == "text"
            assert block["text"] == "something went wrong"

        anyio.run(_test)

    def test_call_structured_content_fallback(self) -> None:
        async def _test() -> None:
            tool = Tool(name="structured", inputSchema={"type": "object"})
            call_result = CallToolResult(content=[], structuredContent={"key": "value"}, isError=False)
            client = _mock_client(result=call_result)
            runnable = async_mcp_tool(tool, client)

            result = await runnable.call({})
            assert result == json.dumps({"key": "value"})

        anyio.run(_test)

    def test_call_empty_content_returns_empty_list(self) -> None:
        async def _test() -> None:
            tool = Tool(name="empty", inputSchema={"type": "object"})
            call_result = CallToolResult(content=[], isError=False)
            client = _mock_client(result=call_result)
            runnable = async_mcp_tool(tool, client)

            result = await runnable.call({})
            assert result == []

        anyio.run(_test)
