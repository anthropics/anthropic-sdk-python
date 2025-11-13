"""Tests for accumulating extra fields in streaming responses.

This tests that pydantic extra fields (fields not in the schema) are properly
accumulated during streaming, without exposing specific field names in the SDK.
"""

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic

from .helpers import get_response, to_async_iter

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"

sync_client = Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)
async_client = AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)


def assert_extra_fields_accumulated(message: Any) -> None:
    """Verify that extra fields are properly accumulated from streaming events.

    This test is intentionally generic - it doesn't know the specific field names,
    just that extra fields should be deep-merged correctly.
    """
    # Extra fields should be accessible via attribute access (pydantic's extra="allow")
    assert hasattr(message, '__pydantic_extra__'), "Message should have __pydantic_extra__"

    extra = message.__pydantic_extra__
    assert 'private_field' in extra, "Extra fields should be accumulated"

    # Verify deep merging: nested dicts should be merged, lists should be extended
    private_field = extra['private_field']
    assert isinstance(private_field, dict), "Extra field should be a dict"
    assert 'nested' in private_field, "Nested structure should be present"

    nested = private_field['nested']
    assert isinstance(nested, dict), "Nested field should be a dict"
    assert 'values' in nested, "Nested values should be present"

    # The 'values' list should have been extended across all streaming events:
    # message_start: [1, 2]
    # content_block_delta 1: [3]
    # content_block_delta 2: [4, 5]
    # message_delta: [6]
    # Expected: [1, 2, 3, 4, 5, 6]
    values = nested['values']
    assert isinstance(values, list), "Nested values should be a list"
    assert values == [1, 2, 3, 4, 5, 6], "Lists should be extended, not replaced"

    # Last value from dict merge should be present
    assert nested.get('metadata') == 'chunk2', "Dict values should be merged"


class TestSyncExtraFields:
    @pytest.mark.respx(base_url=base_url)
    def test_extra_fields_accumulation(self, respx_mock: MockRouter) -> None:
        """Test that extra fields are accumulated during streaming."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("extra_fields_response.txt"))
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello!",
                }
            ],
            model="claude-3-opus-latest",
        ) as stream:
            # Consume the stream
            for _ in stream:
                pass

            message = stream.get_final_message()
            assert_extra_fields_accumulated(message)


class TestAsyncExtraFields:
    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_extra_fields_accumulation(self, respx_mock: MockRouter) -> None:
        """Test that extra fields are accumulated during async streaming."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(get_response("extra_fields_response.txt")))
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello!",
                }
            ],
            model="claude-3-opus-latest",
        ) as stream:
            # Consume the stream
            async for _ in stream:
                pass

            message = await stream.get_final_message()
            assert_extra_fields_accumulated(message)


def test_deep_merge_extra_fields_function() -> None:
    """Test the _deep_merge_extra_fields helper function directly."""
    from anthropic.lib.streaming._messages import _deep_merge_extra_fields

    # Test dict merging
    existing = {"a": 1, "b": {"c": 2}}
    new = {"b": {"d": 3}, "e": 4}
    result = _deep_merge_extra_fields(existing, new)
    assert result == {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}
    assert result is existing, "Should mutate in place"

    # Test list extending
    existing_list = [1, 2, 3]
    new_list = [4, 5]
    result_list = _deep_merge_extra_fields(existing_list, new_list)
    assert result_list == [1, 2, 3, 4, 5]
    assert result_list is existing_list, "Should mutate in place"

    # Test nested dict with lists
    existing_nested = {"data": {"values": [1, 2]}}
    new_nested = {"data": {"values": [3, 4], "count": 4}}
    result_nested = _deep_merge_extra_fields(existing_nested, new_nested)
    assert result_nested == {"data": {"values": [1, 2, 3, 4], "count": 4}}
    assert result_nested is existing_nested, "Should mutate in place"

    # Test scalar replacement
    assert _deep_merge_extra_fields(1, 2) == 2
    assert _deep_merge_extra_fields("old", "new") == "new"
    assert _deep_merge_extra_fields(None, {"a": 1}) == {"a": 1}
