# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization.workspaces import BetaWorkspaceRateLimit

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRateLimits:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        rate_limit = client.beta.organization.workspaces.rate_limits.list(
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncPageCursor[BetaWorkspaceRateLimit], rate_limit, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        rate_limit = client.beta.organization.workspaces.rate_limits.list(
            workspace_id="workspace_id",
            group_type="batch",
            limit=1,
            page="page",
        )
        assert_matches_type(SyncPageCursor[BetaWorkspaceRateLimit], rate_limit, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.rate_limits.with_raw_response.list(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rate_limit = response.parse()
        assert_matches_type(SyncPageCursor[BetaWorkspaceRateLimit], rate_limit, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.rate_limits.with_streaming_response.list(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rate_limit = response.parse()
            assert_matches_type(SyncPageCursor[BetaWorkspaceRateLimit], rate_limit, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.rate_limits.with_raw_response.list(
                workspace_id="",
            )


class TestAsyncRateLimits:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        rate_limit = await async_client.beta.organization.workspaces.rate_limits.list(
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncPageCursor[BetaWorkspaceRateLimit], rate_limit, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rate_limit = await async_client.beta.organization.workspaces.rate_limits.list(
            workspace_id="workspace_id",
            group_type="batch",
            limit=1,
            page="page",
        )
        assert_matches_type(AsyncPageCursor[BetaWorkspaceRateLimit], rate_limit, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.rate_limits.with_raw_response.list(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rate_limit = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaWorkspaceRateLimit], rate_limit, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.rate_limits.with_streaming_response.list(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rate_limit = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaWorkspaceRateLimit], rate_limit, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.rate_limits.with_raw_response.list(
                workspace_id="",
            )
