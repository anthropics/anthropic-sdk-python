from __future__ import annotations

import base64

import pytest

mcp = pytest.importorskip("mcp")

from mcp.types import (  # noqa: E402
    EmbeddedResource,
    ReadResourceResult,
    BlobResourceContents,
    TextResourceContents,
)

from anthropic.lib.tools.mcp import (  # noqa: E402
    UnsupportedMCPValueError,
    mcp_content,
    mcp_resource_to_content,
)


def _blob(data: bytes, mime_type: str | None = None) -> BlobResourceContents:
    payload = {
        "uri": "file:///binary.bin",
        "blob": base64.b64encode(data).decode(),
    }
    if mime_type is not None:
        payload["mimeType"] = mime_type
    return BlobResourceContents.model_validate(payload)


def _text(text: str, mime_type: str | None = None) -> TextResourceContents:
    payload = {"uri": "file:///text.txt", "text": text}
    if mime_type is not None:
        payload["mimeType"] = mime_type
    return TextResourceContents.model_validate(payload)


def _result(*contents: TextResourceContents | BlobResourceContents) -> ReadResourceResult:
    return ReadResourceResult.model_validate({"contents": [content.model_dump() for content in contents]})


def test_unknown_mime_blob_is_not_treated_as_text() -> None:
    with pytest.raises(UnsupportedMCPValueError, match="No supported MIME type"):
        mcp_resource_to_content(_result(_blob(b"\xff\xfe\xfd")))


def test_unknown_mime_blob_does_not_hide_later_supported_resource() -> None:
    result = mcp_resource_to_content(
        _result(
            _blob(b"\xff\xfe\xfd"),
            _text("usable text", "text/plain"),
        )
    )

    assert result["type"] == "document"
    assert result["source"]["data"] == "usable text"


def test_embedded_unknown_mime_blob_raises_sdk_error() -> None:
    resource = _blob(b"\xff\xfe\xfd")

    with pytest.raises(UnsupportedMCPValueError, match="Blob resource has no MIME type"):
        mcp_content(EmbeddedResource(type="resource", resource=resource))


def test_explicit_text_blob_remains_supported() -> None:
    result = mcp_resource_to_content(_result(_blob(b"hello", "text/plain")))

    assert result["type"] == "document"
    assert result["source"]["data"] == "hello"
