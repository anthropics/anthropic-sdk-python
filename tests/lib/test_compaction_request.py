from __future__ import annotations

import json
from typing import Any, TypeVar, cast

import httpx
import respx
import pytest

from anthropic import Anthropic, AsyncAnthropic
from anthropic._utils import transform as _transform, async_transform as _async_transform
from anthropic.types.beta import BetaCompactionBlock
from anthropic.lib._compaction import omit_compaction_encrypted_content
from anthropic._utils._transform import _transform_recursive
from anthropic.types.beta.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.beta.messages.batch_create_params import BatchCreateParams

from ..conftest import base_url

_T = TypeVar("_T")

COMPACTION_PAYLOAD = "EpwBCioIDxgCEAEYASJALd_opaque_compaction_payload"


parametrize = pytest.mark.parametrize("use_async", [False, True], ids=["sync", "async"])


async def transform(data: _T, expected_type: object, use_async: bool) -> _T:
    if use_async:
        return await _async_transform(data, expected_type=expected_type)
    return _transform(data, expected_type=expected_type)


def _message_json() -> dict[str, object]:
    return {
        "id": "msg_abc123",
        "type": "message",
        "role": "assistant",
        "model": "claude-sonnet-4-5",
        "content": [{"type": "text", "text": "hi"}],
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {"input_tokens": 1, "output_tokens": 1},
    }


def _compaction_dict() -> dict[str, str]:
    return {
        "type": "compaction",
        "content": "Earlier conversation summarized.",
        "encrypted_content": COMPACTION_PAYLOAD,
    }


def test_omit_compaction_encrypted_content_leaves_other_blocks() -> None:
    web_search = {
        "type": "web_search_result",
        "title": "Example",
        "url": "https://example.com",
        "encrypted_content": "keep-web-search",
    }
    advisor = {
        "type": "advisor_redacted_result",
        "encrypted_content": "keep-advisor",
    }
    assert omit_compaction_encrypted_content(web_search) is web_search
    assert omit_compaction_encrypted_content(advisor) is advisor
    ints = [1, 2, 3]
    assert omit_compaction_encrypted_content(ints) is ints


def test_omit_compaction_encrypted_content_strips_only_compaction() -> None:
    payload = {
        "messages": [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": [_compaction_dict()]},
        ]
    }
    stripped = omit_compaction_encrypted_content(payload)
    block = stripped["messages"][1]["content"][0]
    assert block == {"type": "compaction", "content": "Earlier conversation summarized."}
    assert payload["messages"][1]["content"][0]["encrypted_content"] == COMPACTION_PAYLOAD


@parametrize
@pytest.mark.asyncio
async def test_transform_strips_compaction_dict_on_create_params(use_async: bool) -> None:
    payload = {
        "max_tokens": 16,
        "model": "claude-sonnet-4-5",
        "messages": [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": [_compaction_dict()]},
        ],
    }
    # Stainless TypedDict transform still copies encrypted_content; the request
    # wrapper is what drops it so documented response.content round-trips work.
    raw = _transform_recursive(payload, annotation=MessageCreateParamsNonStreaming)
    assert raw["messages"][1]["content"][0]["encrypted_content"] == COMPACTION_PAYLOAD

    body = await transform(payload, MessageCreateParamsNonStreaming, use_async)
    block = body["messages"][1]["content"][0]
    assert block == {"type": "compaction", "content": "Earlier conversation summarized."}


@parametrize
@pytest.mark.asyncio
async def test_transform_strips_compaction_model_round_trip(use_async: bool) -> None:
    block = BetaCompactionBlock(
        type="compaction",
        content="Earlier conversation summarized.",
        encrypted_content=COMPACTION_PAYLOAD,
    )
    assert block.encrypted_content == COMPACTION_PAYLOAD

    body = await transform(
        {
            "max_tokens": 16,
            "model": "claude-sonnet-4-5",
            "messages": [
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": [block]},
            ],
        },
        MessageCreateParamsNonStreaming,
        use_async,
    )
    sent = body["messages"][1]["content"][0]
    assert sent == {"type": "compaction", "content": "Earlier conversation summarized."}
    assert block.encrypted_content == COMPACTION_PAYLOAD


@parametrize
@pytest.mark.asyncio
async def test_transform_keeps_web_search_and_advisor_encrypted_content(use_async: bool) -> None:
    body = await transform(
        {
            "max_tokens": 16,
            "model": "claude-sonnet-4-5",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "web_search_tool_result",
                            "tool_use_id": "srvtoolu_1",
                            "content": [
                                {
                                    "type": "web_search_result",
                                    "title": "Example",
                                    "url": "https://example.com",
                                    "encrypted_content": "keep-web-search",
                                }
                            ],
                        },
                        {
                            "type": "advisor_tool_result",
                            "tool_use_id": "toolu_1",
                            "content": {
                                "type": "advisor_redacted_result",
                                "encrypted_content": "keep-advisor",
                            },
                        },
                    ],
                }
            ],
        },
        MessageCreateParamsNonStreaming,
        use_async,
    )
    content = body["messages"][0]["content"]
    assert content[0]["content"][0]["encrypted_content"] == "keep-web-search"
    assert content[1]["content"]["encrypted_content"] == "keep-advisor"


@parametrize
@pytest.mark.asyncio
async def test_transform_strips_compaction_inside_batch_params(use_async: bool) -> None:
    body = await transform(
        {
            "requests": [
                {
                    "custom_id": "req-1",
                    "params": {
                        "max_tokens": 16,
                        "model": "claude-sonnet-4-5",
                        "messages": [
                            {
                                "role": "assistant",
                                "content": [_compaction_dict()],
                            }
                        ],
                    },
                }
            ]
        },
        BatchCreateParams,
        use_async,
    )
    block = body["requests"][0]["params"]["messages"][0]["content"][0]
    assert "encrypted_content" not in block
    assert block["type"] == "compaction"


@parametrize
@pytest.mark.asyncio
async def test_transform_preserves_compaction_cache_control_and_null_content(use_async: bool) -> None:
    body = await transform(
        {
            "max_tokens": 16,
            "model": "claude-sonnet-4-5",
            "messages": [
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "compaction",
                            "content": None,
                            "encrypted_content": COMPACTION_PAYLOAD,
                            "cache_control": {"type": "ephemeral"},
                        }
                    ],
                }
            ],
        },
        MessageCreateParamsNonStreaming,
        use_async,
    )
    block = body["messages"][0]["content"][0]
    assert block["type"] == "compaction"
    assert block["content"] is None
    assert block["cache_control"] == {"type": "ephemeral"}
    assert "encrypted_content" not in block


def _request_body(respx_mock: respx.MockRouter) -> dict[str, Any]:
    return cast("dict[str, Any]", json.loads(respx_mock.calls.last.request.content))


@pytest.mark.respx(base_url=base_url)
class TestCreateOmitsCompactionEncryptedContent:
    def test_create_omits_field_when_round_tripping_response_block(
        self, client: Anthropic, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=_message_json()))
        block = BetaCompactionBlock(
            type="compaction",
            content="Earlier conversation summarized.",
            encrypted_content=COMPACTION_PAYLOAD,
        )

        client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=16,
            messages=[
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": [block]},
            ],
        )

        sent = _request_body(respx_mock)["messages"][1]["content"][0]
        assert sent == {"type": "compaction", "content": "Earlier conversation summarized."}
        assert block.encrypted_content == COMPACTION_PAYLOAD

    def test_create_omits_field_from_dict_history(self, client: Anthropic, respx_mock: respx.MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=_message_json()))

        client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=16,
            messages=[
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": [_compaction_dict()]},
            ],
        )

        sent = _request_body(respx_mock)["messages"][1]["content"][0]
        assert "encrypted_content" not in sent
        assert sent["type"] == "compaction"


@pytest.mark.respx(base_url=base_url)
class TestAsyncCreateOmitsCompactionEncryptedContent:
    async def test_async_create_omits_field_when_round_tripping_response_block(
        self, async_client: AsyncAnthropic, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=_message_json()))
        block = BetaCompactionBlock(
            type="compaction",
            content="Earlier conversation summarized.",
            encrypted_content=COMPACTION_PAYLOAD,
        )

        await async_client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=16,
            messages=[
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": [block]},
            ],
        )

        sent = _request_body(respx_mock)["messages"][1]["content"][0]
        assert sent == {"type": "compaction", "content": "Earlier conversation summarized."}
