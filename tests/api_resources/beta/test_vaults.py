# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta import (
    BetaManagedAgentsVault,
    BetaManagedAgentsDeletedVault,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVaults:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        vault = client.beta.vaults.create(
            display_name="Example vault",
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        vault = client.beta.vaults.create(
            display_name="Example vault",
            metadata={"environment": "production"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.vaults.with_raw_response.create(
            display_name="Example vault",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.vaults.with_streaming_response.create(
            display_name="Example vault",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        vault = client.beta.vaults.retrieve(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        vault = client.beta.vaults.retrieve(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.vaults.with_raw_response.retrieve(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.vaults.with_streaming_response.retrieve(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.beta.vaults.with_raw_response.retrieve(
                vault_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        vault = client.beta.vaults.update(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        vault = client.beta.vaults.update(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            display_name="Example vault",
            metadata={"environment": "production"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.vaults.with_raw_response.update(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.vaults.with_streaming_response.update(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.beta.vaults.with_raw_response.update(
                vault_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        vault = client.beta.vaults.list()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsVault], vault, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        vault = client.beta.vaults.list(
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsVault], vault, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.vaults.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsVault], vault, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.vaults.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsVault], vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        vault = client.beta.vaults.delete(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsDeletedVault, vault, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        vault = client.beta.vaults.delete(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeletedVault, vault, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.vaults.with_raw_response.delete(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(BetaManagedAgentsDeletedVault, vault, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.vaults.with_streaming_response.delete(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert_matches_type(BetaManagedAgentsDeletedVault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.beta.vaults.with_raw_response.delete(
                vault_id="",
            )

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        vault = client.beta.vaults.archive(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        vault = client.beta.vaults.archive(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.vaults.with_raw_response.archive(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.vaults.with_streaming_response.archive(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = response.parse()
            assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.beta.vaults.with_raw_response.archive(
                vault_id="",
            )


class TestAsyncVaults:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.create(
            display_name="Example vault",
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.create(
            display_name="Example vault",
            metadata={"environment": "production"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.with_raw_response.create(
            display_name="Example vault",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.with_streaming_response.create(
            display_name="Example vault",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.retrieve(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.retrieve(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.with_raw_response.retrieve(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.with_streaming_response.retrieve(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.beta.vaults.with_raw_response.retrieve(
                vault_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.update(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.update(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            display_name="Example vault",
            metadata={"environment": "production"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.with_raw_response.update(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.with_streaming_response.update(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.beta.vaults.with_raw_response.update(
                vault_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.list()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsVault], vault, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.list(
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsVault], vault, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsVault], vault, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsVault], vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.delete(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsDeletedVault, vault, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.delete(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeletedVault, vault, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.with_raw_response.delete(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(BetaManagedAgentsDeletedVault, vault, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.with_streaming_response.delete(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(BetaManagedAgentsDeletedVault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.beta.vaults.with_raw_response.delete(
                vault_id="",
            )

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.archive(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        vault = await async_client.beta.vaults.archive(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.with_raw_response.archive(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vault = response.parse()
        assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.with_streaming_response.archive(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(BetaManagedAgentsVault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.beta.vaults.with_raw_response.archive(
                vault_id="",
            )
