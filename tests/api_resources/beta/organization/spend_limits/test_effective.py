from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import BetaSpendSummary

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEffective:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        effective = client.beta.organization.spend_limits.effective.list()
        assert_matches_type(SyncPageCursor[BetaSpendSummary], effective, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        effective = client.beta.organization.spend_limits.effective.list(
            limit=1,
            page="page",
            period=["daily"],
            user_ids=["string"],
        )
        assert_matches_type(SyncPageCursor[BetaSpendSummary], effective, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.spend_limits.effective.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        effective = response.parse()
        assert_matches_type(SyncPageCursor[BetaSpendSummary], effective, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.spend_limits.effective.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            effective = response.parse()
            assert_matches_type(SyncPageCursor[BetaSpendSummary], effective, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEffective:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        effective = await async_client.beta.organization.spend_limits.effective.list()
        assert_matches_type(AsyncPageCursor[BetaSpendSummary], effective, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        effective = await async_client.beta.organization.spend_limits.effective.list(
            limit=1,
            page="page",
            period=["daily"],
            user_ids=["string"],
        )
        assert_matches_type(AsyncPageCursor[BetaSpendSummary], effective, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.spend_limits.effective.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        effective = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaSpendSummary], effective, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.spend_limits.effective.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            effective = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaSpendSummary], effective, path=["response"])

        assert cast(Any, response.is_closed) is True
