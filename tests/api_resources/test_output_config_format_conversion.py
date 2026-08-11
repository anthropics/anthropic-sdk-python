"""Tests for Pydantic models passed through output_config.format."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
from respx import MockRouter
from pydantic import Field, BaseModel

from anthropic import Anthropic, AsyncAnthropic, _compat


class Item(BaseModel):
    code: str = Field(pattern=r"^[A-Z]{3}$", min_length=3)


def message_response() -> dict[str, object]:
    return {
        "id": "msg_123",
        "type": "message",
        "role": "assistant",
        "model": "claude-sonnet-4-5",
        "content": [{"text": '{"code": "ABC"}', "type": "text"}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 10, "output_tokens": 20},
    }


def assert_item_schema(output_format: dict[str, Any]) -> None:
    assert output_format["type"] == "json_schema"
    assert output_format["schema"]["additionalProperties"] is False
    assert output_format["schema"]["properties"]["code"] == {
        "type": "string",
        "title": "Code",
        "description": "{minLength: 3, pattern: ^[A-Z]{3}$}",
    }


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
def test_messages_create_transforms_pydantic_output_config_format(client: Anthropic, respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_response()))

    client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"effort": "high", "format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert body["output_config"]["effort"] == "high"
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
def test_messages_parse_transforms_pydantic_output_config_format(client: Anthropic, respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_response()))

    client.messages.parse(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
def test_messages_stream_transforms_pydantic_output_config_format(client: Anthropic, respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_response()))

    with client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    ):
        pass

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
def test_messages_count_tokens_transforms_pydantic_output_config_format(
    client: Anthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages/count_tokens").mock(return_value=httpx.Response(200, json={"input_tokens": 10}))

    client.messages.count_tokens(
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
async def test_beta_messages_create_transforms_pydantic_output_config_format(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages?beta=true").mock(return_value=httpx.Response(200, json=message_response()))

    await async_client.beta.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"effort": "high", "format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert body["output_config"]["effort"] == "high"
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
def test_beta_messages_parse_transforms_pydantic_output_config_format(
    client: Anthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages?beta=true").mock(return_value=httpx.Response(200, json=message_response()))

    client.beta.messages.parse(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
def test_beta_messages_stream_transforms_pydantic_output_config_format(
    client: Anthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages?beta=true").mock(return_value=httpx.Response(200, json=message_response()))

    with client.beta.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    ):
        pass

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
def test_beta_messages_count_tokens_transforms_pydantic_output_config_format(
    client: Anthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages/count_tokens?beta=true").mock(
        return_value=httpx.Response(200, json={"input_tokens": 10})
    )

    client.beta.messages.count_tokens(
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
async def test_async_messages_create_transforms_pydantic_output_config_format(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_response()))

    await async_client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
async def test_async_messages_parse_transforms_pydantic_output_config_format(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_response()))

    await async_client.messages.parse(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
async def test_async_messages_stream_transforms_pydantic_output_config_format(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_response()))

    async with async_client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    ):
        pass

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
async def test_async_messages_count_tokens_transforms_pydantic_output_config_format(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages/count_tokens").mock(return_value=httpx.Response(200, json={"input_tokens": 10}))

    await async_client.messages.count_tokens(
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
async def test_async_beta_messages_create_transforms_pydantic_output_config_format(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages?beta=true").mock(return_value=httpx.Response(200, json=message_response()))

    await async_client.beta.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"effort": "high", "format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert body["output_config"]["effort"] == "high"
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
async def test_async_beta_messages_parse_transforms_pydantic_output_config_format(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages?beta=true").mock(return_value=httpx.Response(200, json=message_response()))

    await async_client.beta.messages.parse(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
async def test_async_beta_messages_stream_transforms_pydantic_output_config_format(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages?beta=true").mock(return_value=httpx.Response(200, json=message_response()))

    async with async_client.beta.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    ):
        pass

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs require Pydantic v2")
async def test_async_beta_messages_count_tokens_transforms_pydantic_output_config_format(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages/count_tokens?beta=true").mock(
        return_value=httpx.Response(200, json={"input_tokens": 10})
    )

    await async_client.beta.messages.count_tokens(
        messages=[{"role": "user", "content": "Return an item"}],
        model="claude-sonnet-4-5",
        output_config={"format": Item},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert_item_schema(body["output_config"]["format"])
