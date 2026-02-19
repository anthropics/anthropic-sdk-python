# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPage, AsyncPage
from anthropic.types.messages import (
    MessageBatch,
    DeletedMessageBatch,
    MessageBatchIndividualResponse,
)
from anthropic._decoders.jsonl import JSONLDecoder, AsyncJSONLDecoder

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBatches:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        batch = client.messages.batches.create(
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
                        "model": "claude-opus-4-6",
                    },
                }
            ],
        )
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.messages.batches.with_raw_response.create(
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
                        "model": "claude-opus-4-6",
                    },
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.messages.batches.with_streaming_response.create(
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
                        "model": "claude-opus-4-6",
                    },
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(MessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        batch = client.messages.batches.retrieve(
            "message_batch_id",
        )
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.messages.batches.with_raw_response.retrieve(
            "message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.messages.batches.with_streaming_response.retrieve(
            "message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(MessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            client.messages.batches.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        batch = client.messages.batches.list()
        assert_matches_type(SyncPage[MessageBatch], batch, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        batch = client.messages.batches.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
        )
        assert_matches_type(SyncPage[MessageBatch], batch, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.messages.batches.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(SyncPage[MessageBatch], batch, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.messages.batches.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(SyncPage[MessageBatch], batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        batch = client.messages.batches.delete(
            "message_batch_id",
        )
        assert_matches_type(DeletedMessageBatch, batch, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.messages.batches.with_raw_response.delete(
            "message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(DeletedMessageBatch, batch, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.messages.batches.with_streaming_response.delete(
            "message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(DeletedMessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            client.messages.batches.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_cancel(self, client: Anthropic) -> None:
        batch = client.messages.batches.cancel(
            "message_batch_id",
        )
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: Anthropic) -> None:
        response = client.messages.batches.with_raw_response.cancel(
            "message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: Anthropic) -> None:
        with client.messages.batches.with_streaming_response.cancel(
            "message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(MessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            client.messages.batches.with_raw_response.cancel(
                "",
            )

    @pytest.mark.skip(reason="Mock server doesn't support application/x-jsonl responses")
    @parametrize
    def test_method_results(self, client: Anthropic) -> None:
        batch_stream = client.messages.batches.results(
            "message_batch_id",
        )
        assert_matches_type(JSONLDecoder[MessageBatchIndividualResponse], batch_stream, path=["response"])

    @pytest.mark.skip(reason="Mock server doesn't support application/x-jsonl responses")
    @parametrize
    def test_raw_response_results(self, client: Anthropic) -> None:
        response = client.messages.batches.with_raw_response.results(
            "message_batch_id",
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @pytest.mark.skip(reason="Mock server doesn't support application/x-jsonl responses")
    @parametrize
    def test_streaming_response_results(self, client: Anthropic) -> None:
        with client.messages.batches.with_streaming_response.results(
            "message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server doesn't support application/x-jsonl responses")
    @parametrize
    def test_path_params_results(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            client.messages.batches.with_raw_response.results(
                "",
            )


class TestAsyncBatches:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.messages.batches.create(
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
                        "model": "claude-opus-4-6",
                    },
                }
            ],
        )
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.messages.batches.with_raw_response.create(
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
                        "model": "claude-opus-4-6",
                    },
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.messages.batches.with_streaming_response.create(
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
                        "model": "claude-opus-4-6",
                    },
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(MessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.messages.batches.retrieve(
            "message_batch_id",
        )
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.messages.batches.with_raw_response.retrieve(
            "message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.messages.batches.with_streaming_response.retrieve(
            "message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(MessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            await async_client.messages.batches.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.messages.batches.list()
        assert_matches_type(AsyncPage[MessageBatch], batch, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.messages.batches.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
        )
        assert_matches_type(AsyncPage[MessageBatch], batch, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.messages.batches.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(AsyncPage[MessageBatch], batch, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.messages.batches.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(AsyncPage[MessageBatch], batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.messages.batches.delete(
            "message_batch_id",
        )
        assert_matches_type(DeletedMessageBatch, batch, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.messages.batches.with_raw_response.delete(
            "message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(DeletedMessageBatch, batch, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.messages.batches.with_streaming_response.delete(
            "message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(DeletedMessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            await async_client.messages.batches.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_cancel(self, async_client: AsyncAnthropic) -> None:
        batch = await async_client.messages.batches.cancel(
            "message_batch_id",
        )
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.messages.batches.with_raw_response.cancel(
            "message_batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(MessageBatch, batch, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncAnthropic) -> None:
        async with async_client.messages.batches.with_streaming_response.cancel(
            "message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(MessageBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            await async_client.messages.batches.with_raw_response.cancel(
                "",
            )

    @pytest.mark.skip(reason="Mock server doesn't support application/x-jsonl responses")
    @parametrize
    async def test_method_results(self, async_client: AsyncAnthropic) -> None:
        batch_stream = await async_client.messages.batches.results(
            "message_batch_id",
        )
        assert_matches_type(AsyncJSONLDecoder[MessageBatchIndividualResponse], batch_stream, path=["response"])

    @pytest.mark.skip(reason="Mock server doesn't support application/x-jsonl responses")
    @parametrize
    async def test_raw_response_results(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.messages.batches.with_raw_response.results(
            "message_batch_id",
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        await stream.close()

    @pytest.mark.skip(reason="Mock server doesn't support application/x-jsonl responses")
    @parametrize
    async def test_streaming_response_results(self, async_client: AsyncAnthropic) -> None:
        async with async_client.messages.batches.with_streaming_response.results(
            "message_batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server doesn't support application/x-jsonl responses")
    @parametrize
    async def test_path_params_results(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_batch_id` but received ''"):
            await async_client.messages.batches.with_raw_response.results(
                "",
            )
