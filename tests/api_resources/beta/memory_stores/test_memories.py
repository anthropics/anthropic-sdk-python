# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.memory_stores import (
    BetaManagedAgentsMemory,
    BetaManagedAgentsDeletedMemory,
    BetaManagedAgentsMemoryListItem,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMemories:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        memory = client.beta.memory_stores.memories.create(
            memory_store_id="memory_store_id",
            content="content",
            path="xx",
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        memory = client.beta.memory_stores.memories.create(
            memory_store_id="memory_store_id",
            content="content",
            path="xx",
            view="basic",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.memories.with_raw_response.create(
            memory_store_id="memory_store_id",
            content="content",
            path="xx",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.memory_stores.memories.with_streaming_response.create(
            memory_store_id="memory_store_id",
            content="content",
            path="xx",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.memories.with_raw_response.create(
                memory_store_id="",
                content="content",
                path="xx",
            )

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        memory = client.beta.memory_stores.memories.retrieve(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        memory = client.beta.memory_stores.memories.retrieve(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
            view="basic",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.memories.with_raw_response.retrieve(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.memory_stores.memories.with_streaming_response.retrieve(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.memories.with_raw_response.retrieve(
                memory_id="memory_id",
                memory_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_id` but received ''"):
            client.beta.memory_stores.memories.with_raw_response.retrieve(
                memory_id="",
                memory_store_id="memory_store_id",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        memory = client.beta.memory_stores.memories.update(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        memory = client.beta.memory_stores.memories.update(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
            view="basic",
            content="content",
            path="xx",
            precondition={
                "type": "content_sha256",
                "content_sha256": "content_sha256",
            },
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.memories.with_raw_response.update(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.memory_stores.memories.with_streaming_response.update(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.memories.with_raw_response.update(
                memory_id="memory_id",
                memory_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_id` but received ''"):
            client.beta.memory_stores.memories.with_raw_response.update(
                memory_id="",
                memory_store_id="memory_store_id",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        memory = client.beta.memory_stores.memories.list(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryListItem], memory, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        memory = client.beta.memory_stores.memories.list(
            memory_store_id="memory_store_id",
            depth=0,
            limit=0,
            order="asc",
            order_by="order_by",
            page="page",
            path_prefix="path_prefix",
            view="basic",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryListItem], memory, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.memories.with_raw_response.list(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryListItem], memory, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.memory_stores.memories.with_streaming_response.list(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryListItem], memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.memories.with_raw_response.list(
                memory_store_id="",
            )

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        memory = client.beta.memory_stores.memories.delete(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsDeletedMemory, memory, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        memory = client.beta.memory_stores.memories.delete(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
            expected_content_sha256="expected_content_sha256",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeletedMemory, memory, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.memories.with_raw_response.delete(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(BetaManagedAgentsDeletedMemory, memory, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.memory_stores.memories.with_streaming_response.delete(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(BetaManagedAgentsDeletedMemory, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.memories.with_raw_response.delete(
                memory_id="memory_id",
                memory_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_id` but received ''"):
            client.beta.memory_stores.memories.with_raw_response.delete(
                memory_id="",
                memory_store_id="memory_store_id",
            )


class TestAsyncMemories:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        memory = await async_client.beta.memory_stores.memories.create(
            memory_store_id="memory_store_id",
            content="content",
            path="xx",
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory = await async_client.beta.memory_stores.memories.create(
            memory_store_id="memory_store_id",
            content="content",
            path="xx",
            view="basic",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.memories.with_raw_response.create(
            memory_store_id="memory_store_id",
            content="content",
            path="xx",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.memories.with_streaming_response.create(
            memory_store_id="memory_store_id",
            content="content",
            path="xx",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.memories.with_raw_response.create(
                memory_store_id="",
                content="content",
                path="xx",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        memory = await async_client.beta.memory_stores.memories.retrieve(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory = await async_client.beta.memory_stores.memories.retrieve(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
            view="basic",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.memories.with_raw_response.retrieve(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.memories.with_streaming_response.retrieve(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.memories.with_raw_response.retrieve(
                memory_id="memory_id",
                memory_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_id` but received ''"):
            await async_client.beta.memory_stores.memories.with_raw_response.retrieve(
                memory_id="",
                memory_store_id="memory_store_id",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        memory = await async_client.beta.memory_stores.memories.update(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory = await async_client.beta.memory_stores.memories.update(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
            view="basic",
            content="content",
            path="xx",
            precondition={
                "type": "content_sha256",
                "content_sha256": "content_sha256",
            },
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.memories.with_raw_response.update(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.memories.with_streaming_response.update(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(BetaManagedAgentsMemory, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.memories.with_raw_response.update(
                memory_id="memory_id",
                memory_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_id` but received ''"):
            await async_client.beta.memory_stores.memories.with_raw_response.update(
                memory_id="",
                memory_store_id="memory_store_id",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        memory = await async_client.beta.memory_stores.memories.list(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryListItem], memory, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory = await async_client.beta.memory_stores.memories.list(
            memory_store_id="memory_store_id",
            depth=0,
            limit=0,
            order="asc",
            order_by="order_by",
            page="page",
            path_prefix="path_prefix",
            view="basic",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryListItem], memory, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.memories.with_raw_response.list(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryListItem], memory, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.memories.with_streaming_response.list(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryListItem], memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.memories.with_raw_response.list(
                memory_store_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        memory = await async_client.beta.memory_stores.memories.delete(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsDeletedMemory, memory, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory = await async_client.beta.memory_stores.memories.delete(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
            expected_content_sha256="expected_content_sha256",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeletedMemory, memory, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.memories.with_raw_response.delete(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(BetaManagedAgentsDeletedMemory, memory, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.memories.with_streaming_response.delete(
            memory_id="memory_id",
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(BetaManagedAgentsDeletedMemory, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.memories.with_raw_response.delete(
                memory_id="memory_id",
                memory_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_id` but received ''"):
            await async_client.beta.memory_stores.memories.with_raw_response.delete(
                memory_id="",
                memory_store_id="memory_store_id",
            )
