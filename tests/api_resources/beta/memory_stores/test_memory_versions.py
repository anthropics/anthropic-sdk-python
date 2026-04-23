# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.memory_stores import (
    BetaManagedAgentsMemoryVersion,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMemoryVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        memory_version = client.beta.memory_stores.memory_versions.retrieve(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        memory_version = client.beta.memory_stores.memory_versions.retrieve(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
            view="basic",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.memory_versions.with_raw_response.retrieve(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_version = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.memory_stores.memory_versions.with_streaming_response.retrieve(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_version = response.parse()
            assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.memory_versions.with_raw_response.retrieve(
                memory_version_id="memory_version_id",
                memory_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_version_id` but received ''"):
            client.beta.memory_stores.memory_versions.with_raw_response.retrieve(
                memory_version_id="",
                memory_store_id="memory_store_id",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        memory_version = client.beta.memory_stores.memory_versions.list(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryVersion], memory_version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        memory_version = client.beta.memory_stores.memory_versions.list(
            memory_store_id="memory_store_id",
            api_key_id="api_key_id",
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=0,
            memory_id="memory_id",
            operation="created",
            page="page",
            session_id="session_id",
            view="basic",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryVersion], memory_version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.memory_versions.with_raw_response.list(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_version = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryVersion], memory_version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.memory_stores.memory_versions.with_streaming_response.list(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_version = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsMemoryVersion], memory_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.memory_versions.with_raw_response.list(
                memory_store_id="",
            )

    @parametrize
    def test_method_redact(self, client: Anthropic) -> None:
        memory_version = client.beta.memory_stores.memory_versions.redact(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    def test_method_redact_with_all_params(self, client: Anthropic) -> None:
        memory_version = client.beta.memory_stores.memory_versions.redact(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    def test_raw_response_redact(self, client: Anthropic) -> None:
        response = client.beta.memory_stores.memory_versions.with_raw_response.redact(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_version = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    def test_streaming_response_redact(self, client: Anthropic) -> None:
        with client.beta.memory_stores.memory_versions.with_streaming_response.redact(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_version = response.parse()
            assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_redact(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            client.beta.memory_stores.memory_versions.with_raw_response.redact(
                memory_version_id="memory_version_id",
                memory_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_version_id` but received ''"):
            client.beta.memory_stores.memory_versions.with_raw_response.redact(
                memory_version_id="",
                memory_store_id="memory_store_id",
            )


class TestAsyncMemoryVersions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        memory_version = await async_client.beta.memory_stores.memory_versions.retrieve(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory_version = await async_client.beta.memory_stores.memory_versions.retrieve(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
            view="basic",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.memory_versions.with_raw_response.retrieve(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_version = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.memory_versions.with_streaming_response.retrieve(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_version = await response.parse()
            assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.memory_versions.with_raw_response.retrieve(
                memory_version_id="memory_version_id",
                memory_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_version_id` but received ''"):
            await async_client.beta.memory_stores.memory_versions.with_raw_response.retrieve(
                memory_version_id="",
                memory_store_id="memory_store_id",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        memory_version = await async_client.beta.memory_stores.memory_versions.list(
            memory_store_id="memory_store_id",
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryVersion], memory_version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory_version = await async_client.beta.memory_stores.memory_versions.list(
            memory_store_id="memory_store_id",
            api_key_id="api_key_id",
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=0,
            memory_id="memory_id",
            operation="created",
            page="page",
            session_id="session_id",
            view="basic",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryVersion], memory_version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.memory_versions.with_raw_response.list(
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_version = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryVersion], memory_version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.memory_versions.with_streaming_response.list(
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_version = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsMemoryVersion], memory_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.memory_versions.with_raw_response.list(
                memory_store_id="",
            )

    @parametrize
    async def test_method_redact(self, async_client: AsyncAnthropic) -> None:
        memory_version = await async_client.beta.memory_stores.memory_versions.redact(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        )
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    async def test_method_redact_with_all_params(self, async_client: AsyncAnthropic) -> None:
        memory_version = await async_client.beta.memory_stores.memory_versions.redact(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    async def test_raw_response_redact(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.memory_stores.memory_versions.with_raw_response.redact(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory_version = response.parse()
        assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

    @parametrize
    async def test_streaming_response_redact(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.memory_stores.memory_versions.with_streaming_response.redact(
            memory_version_id="memory_version_id",
            memory_store_id="memory_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory_version = await response.parse()
            assert_matches_type(BetaManagedAgentsMemoryVersion, memory_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_redact(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await async_client.beta.memory_stores.memory_versions.with_raw_response.redact(
                memory_version_id="memory_version_id",
                memory_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_version_id` but received ''"):
            await async_client.beta.memory_stores.memory_versions.with_raw_response.redact(
                memory_version_id="",
                memory_store_id="memory_store_id",
            )
