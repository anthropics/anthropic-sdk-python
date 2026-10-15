from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_date
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import BetaAnalyticsUserActivity

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        user = client.beta.organization.analytics.users.list()
        assert_matches_type(SyncPageCursor[BetaAnalyticsUserActivity], user, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        user = client.beta.organization.analytics.users.list(
            date=parse_date("2019-12-27"),
            ending_date=parse_date("2019-12-27"),
            filter=["string"],
            group_by=["rbac_group_id"],
            limit=1,
            order="asc",
            order_by="order_by",
            page="page",
            starting_date=parse_date("2019-12-27"),
        )
        assert_matches_type(SyncPageCursor[BetaAnalyticsUserActivity], user, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.analytics.users.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(SyncPageCursor[BetaAnalyticsUserActivity], user, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.analytics.users.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(SyncPageCursor[BetaAnalyticsUserActivity], user, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUsers:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        user = await async_client.beta.organization.analytics.users.list()
        assert_matches_type(AsyncPageCursor[BetaAnalyticsUserActivity], user, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user = await async_client.beta.organization.analytics.users.list(
            date=parse_date("2019-12-27"),
            ending_date=parse_date("2019-12-27"),
            filter=["string"],
            group_by=["rbac_group_id"],
            limit=1,
            order="asc",
            order_by="order_by",
            page="page",
            starting_date=parse_date("2019-12-27"),
        )
        assert_matches_type(AsyncPageCursor[BetaAnalyticsUserActivity], user, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.analytics.users.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaAnalyticsUserActivity], user, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.analytics.users.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaAnalyticsUserActivity], user, path=["response"])

        assert cast(Any, response.is_closed) is True
