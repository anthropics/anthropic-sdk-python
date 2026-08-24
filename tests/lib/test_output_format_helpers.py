"""The typed `output_format=` argument of the hand-written helpers on the non-beta client."""

from __future__ import annotations

import json

import httpx2 as httpx
import pytest
from respx import MockRouter
from pydantic import BaseModel

from anthropic import Anthropic, AsyncAnthropic, _compat


class Answer(BaseModel):
    text: str


def _count(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages/count_tokens").mock(return_value=httpx.Response(200, json={"input_tokens": 7}))


def _last_body(respx_mock: MockRouter) -> dict[str, object]:
    return json.loads(respx_mock.calls.last.request.content)


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="schema generation from models requires Pydantic v2")
def test_count_tokens_accepts_a_type(client: Anthropic, respx_mock: MockRouter) -> None:
    _count(respx_mock)

    client.messages.count_tokens(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": "hi"}],
        output_format=Answer,
    )

    body = _last_body(respx_mock)
    assert "output_format" not in body
    fmt = body["output_config"]["format"]  # type: ignore[index]
    assert fmt["type"] == "json_schema"
    assert fmt["schema"]["properties"]["text"]["type"] == "string"


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="schema generation from models requires Pydantic v2")
def test_count_tokens_merges_the_type_into_an_existing_output_config(client: Anthropic, respx_mock: MockRouter) -> None:
    _count(respx_mock)

    client.messages.count_tokens(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": "hi"}],
        output_config={"effort": "high"},
        output_format=Answer,
    )

    output_config = _last_body(respx_mock)["output_config"]
    assert output_config["effort"] == "high"  # type: ignore[index]
    assert output_config["format"]["type"] == "json_schema"  # type: ignore[index]


def test_count_tokens_rejects_a_schema_dict(client: Anthropic) -> None:
    with pytest.raises(TypeError, match="output_config"):
        client.messages.count_tokens(
            model="claude-sonnet-4-5",
            messages=[{"role": "user", "content": "hi"}],
            output_format={"type": "json_schema", "schema": {"type": "object"}},  # type: ignore[arg-type]
        )


def test_stream_rejects_a_schema_dict(client: Anthropic) -> None:
    with pytest.raises(TypeError, match="output_config"):
        client.messages.stream(
            max_tokens=16,
            model="claude-sonnet-4-5",
            messages=[{"role": "user", "content": "hi"}],
            output_format={"type": "json_schema", "schema": {"type": "object"}},  # type: ignore[arg-type]
        )


def test_count_tokens_output_config_dict_still_works(client: Anthropic, respx_mock: MockRouter) -> None:
    _count(respx_mock)

    client.messages.count_tokens(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": "hi"}],
        output_config={"format": {"type": "json_schema", "schema": {"type": "object"}}},
    )

    assert _last_body(respx_mock)["output_config"] == {"format": {"type": "json_schema", "schema": {"type": "object"}}}


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="schema generation from models requires Pydantic v2")
async def test_async_count_tokens_accepts_a_type(async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
    _count(respx_mock)

    await async_client.messages.count_tokens(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": "hi"}],
        output_format=Answer,
    )

    assert _last_body(respx_mock)["output_config"]["format"]["type"] == "json_schema"  # type: ignore[index]


async def test_async_count_tokens_rejects_a_schema_dict(async_client: AsyncAnthropic) -> None:
    with pytest.raises(TypeError, match="output_config"):
        await async_client.messages.count_tokens(
            model="claude-sonnet-4-5",
            messages=[{"role": "user", "content": "hi"}],
            output_format={"type": "json_schema", "schema": {"type": "object"}},  # type: ignore[arg-type]
        )
