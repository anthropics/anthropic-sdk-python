# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPage, AsyncPage
from anthropic._decoders.jsonl import JSONLDecoder, AsyncJSONLDecoder
from anthropic.types.beta.messages import (
    BetaMessageBatch,
    BetaDeletedMessageBatch,
    BetaMessageBatchIndividualResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBatches:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.create(
            requests=[
                {
                    "custom_id": "my-custom-id-1",
                    "params": {
                        "max_tokens": 1024,
                        "messages": [
                            {
                                "content": "Hello, world",
                                "role": "user",
                            }
                        ],
                        "model": "claude-3-5-sonnet-20241022",
                    },
                }
            ],
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.create(
            requests=[
                {
                    "custom_id": "my-custom-id-1",
                    "params": {
                        "max_tokens": 1024,
                        "messages": [
                            {
                                "content": "Hello, world",
                                "role": "user",
                            }
                        ],
                        "model": "claude-3-5-sonnet-20241022",
                        "metadata": {"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
                        "stop_sequences": ["string"],
                        "stream": True,
                        "system": [
                            {
                                "text": "Today's date is 2024-06-01.",
                                "type": "text",
                                "cache_control": {"type": "ephemeral"},
                            }
                        ],
                        "temperature": 1,
                        "tool_choice": {
                            "type": "auto",
                            "disable_parallel_tool_use": True,
                        },
                        "tools": [
                            {
                                "input_schema": {
                                    "type": "object",
                                    "properties": {
                                        "location": {
                                            "description": "The city and state, e.g. San Francisco, CA",
                                            "type": "string",
                                        },
                                        "unit": {
                                            "description": "Unit for the output - one of (celsius, fahrenheit)",
                                            "type": "string",
                                        },
                                    },
                                },
                                "name": "name",
                                "cache_control": {"type": "ephemeral"},
                                "description": "Get the current weather in a given location",
                                "type": "custom",
                            }
                        ],
                        "top_k": 5,
                        "top_p": 0.7,
                    },
                }
            ],
            betas=["string"],
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.messages.batches.with_raw_response.create(
            requests=[
                {
                    "custom_id": "my-custom-id-1",
                    "params": {
                        "max_tokens": 1024,
                        "messages": [
                            {
                                "content": "Hello, world",
                                "role": "user",
                            }
                        ],
                        "model": "claude-3-5-sonnet-20241022",
                    },
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.messages.batches.with_streaming_response.create(
            requests=[
                {
                    "custom_id": "my-custom-id-1",
                    "params": {
                        "max_tokens": 1024,
                        "messages": [
                            {
                                "content": "Hello, world",
                                "role": "user",
                            }
                        ],
                        "model": "claude-3-5-sonnet-20241022",
                    },
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(BetaMessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.retrieve(
            message_batch_id="message_batch_id",
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.retrieve(
            message_batch_id="message_batch_id",
            betas=["string"],
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.messages.batches.with_raw_response.retrieve(
            message_batch_id="message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.messages.batches.with_streaming_response.retrieve(
            message_batch_id="message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(BetaMessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            client.beta.messages.batches.with_raw_response.retrieve(
                message_batch_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.list()
        assert_matches_type(SyncPage[BetaMessageBatch], batch, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            betas=["string"],
        )
        assert_matches_type(SyncPage[BetaMessageBatch], batch, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.messages.batches.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(SyncPage[BetaMessageBatch], batch, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.messages.batches.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(SyncPage[BetaMessageBatch], batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.delete(
            message_batch_id="message_batch_id",
        )
        assert_matches_type(BetaDeletedMessageBatch, batch, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.delete(
            message_batch_id="message_batch_id",
            betas=["string"],
        )
        assert_matches_type(BetaDeletedMessageBatch, batch, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.messages.batches.with_raw_response.delete(
            message_batch_id="message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BetaDeletedMessageBatch, batch, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.messages.batches.with_streaming_response.delete(
            message_batch_id="message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(BetaDeletedMessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            client.beta.messages.batches.with_raw_response.delete(
                message_batch_id="",
            )

    @parametrize
    def test_method_cancel(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.cancel(
            message_batch_id="message_batch_id",
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    def test_method_cancel_with_all_params(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.cancel(
            message_batch_id="message_batch_id",
            betas=["string"],
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: Anthropic) -> None:
        response = client.beta.messages.batches.with_raw_response.cancel(
            message_batch_id="message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: Anthropic) -> None:
        with client.beta.messages.batches.with_streaming_response.cancel(
            message_batch_id="message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(BetaMessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            client.beta.messages.batches.with_raw_response.cancel(
                message_batch_id="",
            )

    @pytest.mark.skip(reason="Prism doesn't support JSONL responses yet")
    @parametrize
    def test_method_results(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.results(
            message_batch_id="message_batch_id",
        )
        assert_matches_type(JSONLDecoder[BetaMessageBatchIndividualResponse], batch, path=["response"])

    @pytest.mark.skip(reason="Prism doesn't support JSONL responses yet")
    @parametrize
    def test_method_results_with_all_params(self, client: Anthropic) -> None:
        batch = client.beta.messages.batches.results(
            message_batch_id="message_batch_id",
            betas=["string"],
        )
        assert_matches_type(JSONLDecoder[BetaMessageBatchIndividualResponse], batch, path=["response"])

    @pytest.mark.skip(reason="Prism doesn't support JSONL responses yet")
    @parametrize
    def test_raw_response_results(self, client: Anthropic) -> None:
        response = client.beta.messages.batches.with_raw_response.results(
            message_batch_id="message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(JSONLDecoder[BetaMessageBatchIndividualResponse], batch, path=["response"])

    @pytest.mark.skip(reason="Prism doesn't support JSONL responses yet")
    @parametrize
    def test_streaming_response_results(self, client: Anthropic) -> None:
        with client.beta.messages.batches.with_streaming_response.results(
            message_batch_id="message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(JSONLDecoder[BetaMessageBatchIndividualResponse], batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism doesn't support JSONL responses yet")
    @parametrize
    def test_path_params_results(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            client.beta.messages.batches.with_raw_response.results(
                message_batch_id="",
            )


class TestAsyncBatches:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.create(
            requests=[
                {
                    "custom_id": "my-custom-id-1",
                    "params": {
                        "max_tokens": 1024,
                        "messages": [
                            {
                                "content": "Hello, world",
                                "role": "user",
                            }
                        ],
                        "model": "claude-3-5-sonnet-20241022",
                    },
                }
            ],
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.create(
            requests=[
                {
                    "custom_id": "my-custom-id-1",
                    "params": {
                        "max_tokens": 1024,
                        "messages": [
                            {
                                "content": "Hello, world",
                                "role": "user",
                            }
                        ],
                        "model": "claude-3-5-sonnet-20241022",
                        "metadata": {"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
                        "stop_sequences": ["string"],
                        "stream": True,
                        "system": [
                            {
                                "text": "Today's date is 2024-06-01.",
                                "type": "text",
                                "cache_control": {"type": "ephemeral"},
                            }
                        ],
                        "temperature": 1,
                        "tool_choice": {
                            "type": "auto",
                            "disable_parallel_tool_use": True,
                        },
                        "tools": [
                            {
                                "input_schema": {
                                    "type": "object",
                                    "properties": {
                                        "location": {
                                            "description": "The city and state, e.g. San Francisco, CA",
                                            "type": "string",
                                        },
                                        "unit": {
                                            "description": "Unit for the output - one of (celsius, fahrenheit)",
                                            "type": "string",
                                        },
                                    },
                                },
                                "name": "name",
                                "cache_control": {"type": "ephemeral"},
                                "description": "Get the current weather in a given location",
                                "type": "custom",
                            }
                        ],
                        "top_k": 5,
                        "top_p": 0.7,
                    },
                }
            ],
            betas=["string"],
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.messages.batches.with_raw_response.create(
            requests=[
                {
                    "custom_id": "my-custom-id-1",
                    "params": {
                        "max_tokens": 1024,
                        "messages": [
                            {
                                "content": "Hello, world",
                                "role": "user",
                            }
                        ],
                        "model": "claude-3-5-sonnet-20241022",
                    },
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.messages.batches.with_streaming_response.create(
            requests=[
                {
                    "custom_id": "my-custom-id-1",
                    "params": {
                        "max_tokens": 1024,
                        "messages": [
                            {
                                "content": "Hello, world",
                                "role": "user",
                            }
                        ],
                        "model": "claude-3-5-sonnet-20241022",
                    },
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(BetaMessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.retrieve(
            message_batch_id="message_batch_id",
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.retrieve(
            message_batch_id="message_batch_id",
            betas=["string"],
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.messages.batches.with_raw_response.retrieve(
            message_batch_id="message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.messages.batches.with_streaming_response.retrieve(
            message_batch_id="message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(BetaMessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            await async_client.beta.messages.batches.with_raw_response.retrieve(
                message_batch_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.list()
        assert_matches_type(AsyncPage[BetaMessageBatch], batch, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            betas=["string"],
        )
        assert_matches_type(AsyncPage[BetaMessageBatch], batch, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.messages.batches.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(AsyncPage[BetaMessageBatch], batch, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.messages.batches.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(AsyncPage[BetaMessageBatch], batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.delete(
            message_batch_id="message_batch_id",
        )
        assert_matches_type(BetaDeletedMessageBatch, batch, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.delete(
            message_batch_id="message_batch_id",
            betas=["string"],
        )
        assert_matches_type(BetaDeletedMessageBatch, batch, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.messages.batches.with_raw_response.delete(
            message_batch_id="message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BetaDeletedMessageBatch, batch, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.messages.batches.with_streaming_response.delete(
            message_batch_id="message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(BetaDeletedMessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            await async_client.beta.messages.batches.with_raw_response.delete(
                message_batch_id="",
            )

    @parametrize
    async def test_method_cancel(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.cancel(
            message_batch_id="message_batch_id",
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    async def test_method_cancel_with_all_params(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.cancel(
            message_batch_id="message_batch_id",
            betas=["string"],
        )
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.messages.batches.with_raw_response.cancel(
            message_batch_id="message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BetaMessageBatch, batch, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.messages.batches.with_streaming_response.cancel(
            message_batch_id="message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(BetaMessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            await async_client.beta.messages.batches.with_raw_response.cancel(
                message_batch_id="",
            )

    @pytest.mark.skip(reason="Prism doesn't support JSONL responses yet")
    @parametrize
    async def test_method_results(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.results(
            message_batch_id="message_batch_id",
        )
        assert_matches_type(AsyncJSONLDecoder[BetaMessageBatchIndividualResponse], batch, path=["response"])

    @pytest.mark.skip(reason="Prism doesn't support JSONL responses yet")
    @parametrize
    async def test_method_results_with_all_params(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.beta.messages.batches.results(
            message_batch_id="message_batch_id",
            betas=["string"],
        )
        assert_matches_type(AsyncJSONLDecoder[BetaMessageBatchIndividualResponse], batch, path=["response"])

    @pytest.mark.skip(reason="Prism doesn't support JSONL responses yet")
    @parametrize
    async def test_raw_response_results(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.messages.batches.with_raw_response.results(
            message_batch_id="message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(AsyncJSONLDecoder[BetaMessageBatchIndividualResponse], batch, path=["response"])

    @pytest.mark.skip(reason="Prism doesn't support JSONL responses yet")
    @parametrize
    async def test_streaming_response_results(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.messages.batches.with_streaming_response.results(
            message_batch_id="message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(AsyncJSONLDecoder[BetaMessageBatchIndividualResponse], batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism doesn't support JSONL responses yet")
    @parametrize
    async def test_path_params_results(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            await async_client.beta.messages.batches.with_raw_response.results(
                message_batch_id="",
            )
