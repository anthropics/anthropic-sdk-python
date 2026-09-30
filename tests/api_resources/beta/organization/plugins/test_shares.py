from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization.plugins import BetaPluginShare

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestShares:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        share = client.beta.organization.plugins.shares.list(
            plugin_id="plugin_id",
        )
        assert_matches_type(SyncPageCursor[BetaPluginShare], share, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        share = client.beta.organization.plugins.shares.list(
            plugin_id="plugin_id",
            limit=1,
            organization_id="organization_id",
            page="page",
            target_type="organization",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaPluginShare], share, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.shares.with_raw_response.list(
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share = response.parse()
        assert_matches_type(SyncPageCursor[BetaPluginShare], share, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.shares.with_streaming_response.list(
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share = response.parse()
            assert_matches_type(SyncPageCursor[BetaPluginShare], share, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            client.beta.organization.plugins.shares.with_raw_response.list(
                plugin_id="",
            )


class TestAsyncShares:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        share = await async_client.beta.organization.plugins.shares.list(
            plugin_id="plugin_id",
        )
        assert_matches_type(AsyncPageCursor[BetaPluginShare], share, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        share = await async_client.beta.organization.plugins.shares.list(
            plugin_id="plugin_id",
            limit=1,
            organization_id="organization_id",
            page="page",
            target_type="organization",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaPluginShare], share, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.shares.with_raw_response.list(
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaPluginShare], share, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.shares.with_streaming_response.list(
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaPluginShare], share, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            await async_client.beta.organization.plugins.shares.with_raw_response.list(
                plugin_id="",
            )
