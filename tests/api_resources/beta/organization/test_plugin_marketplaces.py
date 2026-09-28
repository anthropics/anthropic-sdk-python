from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import (
    BetaPluginMarketplace,
    BetaPluginMarketplaceValidationReport,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPluginMarketplaces:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        plugin_marketplace = client.beta.organization.plugin_marketplaces.retrieve(
            marketplace_id="marketplace_id",
        )
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        plugin_marketplace = client.beta.organization.plugin_marketplaces.retrieve(
            marketplace_id="marketplace_id",
            organization_id="organization_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.plugin_marketplaces.with_raw_response.retrieve(
            marketplace_id="marketplace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin_marketplace = response.parse()
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.plugin_marketplaces.with_streaming_response.retrieve(
            marketplace_id="marketplace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin_marketplace = response.parse()
            assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `marketplace_id` but received ''"):
            client.beta.organization.plugin_marketplaces.with_raw_response.retrieve(
                marketplace_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        plugin_marketplace = client.beta.organization.plugin_marketplaces.update(
            marketplace_id="marketplace_id",
            default_installation_preference="available",
        )
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        plugin_marketplace = client.beta.organization.plugin_marketplaces.update(
            marketplace_id="marketplace_id",
            default_installation_preference="available",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.plugin_marketplaces.with_raw_response.update(
            marketplace_id="marketplace_id",
            default_installation_preference="available",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin_marketplace = response.parse()
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.plugin_marketplaces.with_streaming_response.update(
            marketplace_id="marketplace_id",
            default_installation_preference="available",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin_marketplace = response.parse()
            assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `marketplace_id` but received ''"):
            client.beta.organization.plugin_marketplaces.with_raw_response.update(
                marketplace_id="",
                default_installation_preference="available",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        plugin_marketplace = client.beta.organization.plugin_marketplaces.list()
        assert_matches_type(SyncPageCursor[BetaPluginMarketplace], plugin_marketplace, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        plugin_marketplace = client.beta.organization.plugin_marketplaces.list(
            limit=1,
            organization_id="organization_id",
            owner_type="organization",
            page="page",
            source="directory",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaPluginMarketplace], plugin_marketplace, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.plugin_marketplaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin_marketplace = response.parse()
        assert_matches_type(SyncPageCursor[BetaPluginMarketplace], plugin_marketplace, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.plugin_marketplaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin_marketplace = response.parse()
            assert_matches_type(SyncPageCursor[BetaPluginMarketplace], plugin_marketplace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_validate_archive(self, client: Anthropic) -> None:
        plugin_marketplace = client.beta.organization.plugin_marketplaces.validate_archive(
            archive=b"Example data",
        )
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    def test_method_validate_archive_with_all_params(self, client: Anthropic) -> None:
        plugin_marketplace = client.beta.organization.plugin_marketplaces.validate_archive(
            archive=b"Example data",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    def test_raw_response_validate_archive(self, client: Anthropic) -> None:
        response = client.beta.organization.plugin_marketplaces.with_raw_response.validate_archive(
            archive=b"Example data",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin_marketplace = response.parse()
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    def test_streaming_response_validate_archive(self, client: Anthropic) -> None:
        with client.beta.organization.plugin_marketplaces.with_streaming_response.validate_archive(
            archive=b"Example data",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin_marketplace = response.parse()
            assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_validate_repository(self, client: Anthropic) -> None:
        plugin_marketplace = client.beta.organization.plugin_marketplaces.validate_repository(
            repository_url="https://github.com/example-org/example-marketplace",
        )
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    def test_method_validate_repository_with_all_params(self, client: Anthropic) -> None:
        plugin_marketplace = client.beta.organization.plugin_marketplaces.validate_repository(
            repository_url="https://github.com/example-org/example-marketplace",
            ref="main",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    def test_raw_response_validate_repository(self, client: Anthropic) -> None:
        response = client.beta.organization.plugin_marketplaces.with_raw_response.validate_repository(
            repository_url="https://github.com/example-org/example-marketplace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin_marketplace = response.parse()
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    def test_streaming_response_validate_repository(self, client: Anthropic) -> None:
        with client.beta.organization.plugin_marketplaces.with_streaming_response.validate_repository(
            repository_url="https://github.com/example-org/example-marketplace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin_marketplace = response.parse()
            assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPluginMarketplaces:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        plugin_marketplace = await async_client.beta.organization.plugin_marketplaces.retrieve(
            marketplace_id="marketplace_id",
        )
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        plugin_marketplace = await async_client.beta.organization.plugin_marketplaces.retrieve(
            marketplace_id="marketplace_id",
            organization_id="organization_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugin_marketplaces.with_raw_response.retrieve(
            marketplace_id="marketplace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin_marketplace = await response.parse()
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugin_marketplaces.with_streaming_response.retrieve(
            marketplace_id="marketplace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin_marketplace = await response.parse()
            assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `marketplace_id` but received ''"):
            await async_client.beta.organization.plugin_marketplaces.with_raw_response.retrieve(
                marketplace_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        plugin_marketplace = await async_client.beta.organization.plugin_marketplaces.update(
            marketplace_id="marketplace_id",
            default_installation_preference="available",
        )
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        plugin_marketplace = await async_client.beta.organization.plugin_marketplaces.update(
            marketplace_id="marketplace_id",
            default_installation_preference="available",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugin_marketplaces.with_raw_response.update(
            marketplace_id="marketplace_id",
            default_installation_preference="available",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin_marketplace = await response.parse()
        assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugin_marketplaces.with_streaming_response.update(
            marketplace_id="marketplace_id",
            default_installation_preference="available",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin_marketplace = await response.parse()
            assert_matches_type(BetaPluginMarketplace, plugin_marketplace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `marketplace_id` but received ''"):
            await async_client.beta.organization.plugin_marketplaces.with_raw_response.update(
                marketplace_id="",
                default_installation_preference="available",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        plugin_marketplace = await async_client.beta.organization.plugin_marketplaces.list()
        assert_matches_type(AsyncPageCursor[BetaPluginMarketplace], plugin_marketplace, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        plugin_marketplace = await async_client.beta.organization.plugin_marketplaces.list(
            limit=1,
            organization_id="organization_id",
            owner_type="organization",
            page="page",
            source="directory",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaPluginMarketplace], plugin_marketplace, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugin_marketplaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin_marketplace = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaPluginMarketplace], plugin_marketplace, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugin_marketplaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin_marketplace = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaPluginMarketplace], plugin_marketplace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_validate_archive(self, async_client: AsyncAnthropic) -> None:
        plugin_marketplace = await async_client.beta.organization.plugin_marketplaces.validate_archive(
            archive=b"Example data",
        )
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    async def test_method_validate_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        plugin_marketplace = await async_client.beta.organization.plugin_marketplaces.validate_archive(
            archive=b"Example data",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    async def test_raw_response_validate_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugin_marketplaces.with_raw_response.validate_archive(
            archive=b"Example data",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin_marketplace = await response.parse()
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    async def test_streaming_response_validate_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugin_marketplaces.with_streaming_response.validate_archive(
            archive=b"Example data",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin_marketplace = await response.parse()
            assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_validate_repository(self, async_client: AsyncAnthropic) -> None:
        plugin_marketplace = await async_client.beta.organization.plugin_marketplaces.validate_repository(
            repository_url="https://github.com/example-org/example-marketplace",
        )
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    async def test_method_validate_repository_with_all_params(self, async_client: AsyncAnthropic) -> None:
        plugin_marketplace = await async_client.beta.organization.plugin_marketplaces.validate_repository(
            repository_url="https://github.com/example-org/example-marketplace",
            ref="main",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    async def test_raw_response_validate_repository(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugin_marketplaces.with_raw_response.validate_repository(
            repository_url="https://github.com/example-org/example-marketplace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin_marketplace = await response.parse()
        assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

    @parametrize
    async def test_streaming_response_validate_repository(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugin_marketplaces.with_streaming_response.validate_repository(
            repository_url="https://github.com/example-org/example-marketplace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin_marketplace = await response.parse()
            assert_matches_type(BetaPluginMarketplaceValidationReport, plugin_marketplace, path=["response"])

        assert cast(Any, response.is_closed) is True
