# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta import (
    BetaManagedAgentsMemoryStore,
    BetaManagedAgentsDeletedMemoryStore,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMemoryStores:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.create(
            name="x",
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.create(
            name="x",
            description="description",
            metadata={"foo": "string"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.with_raw_response.create(
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.memory_stores.with_streaming_response.create(
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = response.parse()
            assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.retrieve(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.retrieve(
            memory_store_id="memory_store_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.with_raw_response.retrieve(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.memory_stores.with_streaming_response.retrieve(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = response.parse()
            assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.with_raw_response.retrieve(
                memory_store_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.update(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.update(
            memory_store_id="memory_store_id",
            description="description",
            metadata={"foo": "string"},
            name="x",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.with_raw_response.update(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.memory_stores.with_streaming_response.update(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = response.parse()
            assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.with_raw_response.update(
                memory_store_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.list()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryStore], memory_store, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.list(
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryStore], memory_store, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryStore], memory_store, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.memory_stores.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryStore], memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.delete(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsDeletedMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.delete(
            memory_store_id="memory_store_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeletedMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.with_raw_response.delete(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(BetaManagedAgentsDeletedMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.memory_stores.with_streaming_response.delete(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = response.parse()
            assert_matches_type(BetaManagedAgentsDeletedMemoryStore, memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.with_raw_response.delete(
                memory_store_id="",
            )

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.archive(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        memory_store = client.beta.memory_stores.archive(
            memory_store_id="memory_store_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.with_raw_response.archive(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.memory_stores.with_streaming_response.archive(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = response.parse()
            assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.with_raw_response.archive(
                memory_store_id="",
            )


class TestAsyncMemoryStores:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.create(
            name="x",
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.create(
            name="x",
            description="description",
            metadata={"foo": "string"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.with_raw_response.create(
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.with_streaming_response.create(
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = await response.parse()
            assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.retrieve(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.retrieve(
            memory_store_id="memory_store_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.with_raw_response.retrieve(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.with_streaming_response.retrieve(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = await response.parse()
            assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.with_raw_response.retrieve(
                memory_store_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.update(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.update(
            memory_store_id="memory_store_id",
            description="description",
            metadata={"foo": "string"},
            name="x",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.with_raw_response.update(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.with_streaming_response.update(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = await response.parse()
            assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.with_raw_response.update(
                memory_store_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.list()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryStore], memory_store, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.list(
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryStore], memory_store, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryStore], memory_store, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryStore], memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.delete(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsDeletedMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.delete(
            memory_store_id="memory_store_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeletedMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.with_raw_response.delete(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(BetaManagedAgentsDeletedMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.with_streaming_response.delete(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = await response.parse()
            assert_matches_type(BetaManagedAgentsDeletedMemoryStore, memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.with_raw_response.delete(
                memory_store_id="",
            )

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.archive(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory_store = await async_client.beta.memory_stores.archive(
            memory_store_id="memory_store_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.with_raw_response.archive(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_store = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.with_streaming_response.archive(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_store = await response.parse()
            assert_matches_type(BetaManagedAgentsMemoryStore, memory_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.with_raw_response.archive(
                memory_store_id="",
            )
