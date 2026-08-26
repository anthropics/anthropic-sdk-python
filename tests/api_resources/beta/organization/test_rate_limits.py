# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import BetaOrganizationRateLimit

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRateLimits:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        rate_limit = client.beta.organization.rate_limits.list()
        assert_matches_type(SyncPageCursor[BetaOrganizationRateLimit], rate_limit, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        rate_limit = client.beta.organization.rate_limits.list(
            group_type="batch",
            limit=1,
            model="model",
            page="page",
        )
        assert_matches_type(SyncPageCursor[BetaOrganizationRateLimit], rate_limit, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.rate_limits.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rate_limit = response.parse()
        assert_matches_type(SyncPageCursor[BetaOrganizationRateLimit], rate_limit, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.rate_limits.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rate_limit = response.parse()
            assert_matches_type(SyncPageCursor[BetaOrganizationRateLimit], rate_limit, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRateLimits:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        rate_limit = await async_client.beta.organization.rate_limits.list()
        assert_matches_type(AsyncPageCursor[BetaOrganizationRateLimit], rate_limit, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rate_limit = await async_client.beta.organization.rate_limits.list(
            group_type="batch",
            limit=1,
            model="model",
            page="page",
        )
        assert_matches_type(AsyncPageCursor[BetaOrganizationRateLimit], rate_limit, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.rate_limits.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rate_limit = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaOrganizationRateLimit], rate_limit, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.rate_limits.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rate_limit = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaOrganizationRateLimit], rate_limit, path=["response"])

        assert cast(Any, response.is_closed) is True
