from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import BetaAnalyticsUsageUsersItem

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUserUsageReport:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        user_usage_report = client.beta.organization.analytics.user_usage_report.list(
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(SyncPageCursor[BetaAnalyticsUsageUsersItem], user_usage_report, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        user_usage_report = client.beta.organization.analytics.user_usage_report.list(
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            bucket_width="1d",
            claude_tag_categories=["engaged"],
            claude_tag_user_ids=["U0123ABCDEF"],
            context_windows=["0-200k"],
            ending_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            exclude_deleted_users=True,
            group_by=["claude_tag_category"],
            inference_geos=["global"],
            limit=1,
            models=["string"],
            order="asc",
            order_by="output_tokens",
            page="page",
            products=["chat"],
            rbac_group_ids=["rbac_group_012rppKaSVsmTo6NqRDXQXNF"],
            slack_channel_ids=["C0123ABCDEF"],
            speeds=["fast"],
            user_ids=["user_01AbCdEfGhIjKlMnOpQrSt"],
        )
        assert_matches_type(SyncPageCursor[BetaAnalyticsUsageUsersItem], user_usage_report, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.analytics.user_usage_report.with_raw_response.list(
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_usage_report = response.parse()
        assert_matches_type(SyncPageCursor[BetaAnalyticsUsageUsersItem], user_usage_report, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.analytics.user_usage_report.with_streaming_response.list(
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_usage_report = response.parse()
            assert_matches_type(SyncPageCursor[BetaAnalyticsUsageUsersItem], user_usage_report, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUserUsageReport:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        user_usage_report = await async_client.beta.organization.analytics.user_usage_report.list(
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(AsyncPageCursor[BetaAnalyticsUsageUsersItem], user_usage_report, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user_usage_report = await async_client.beta.organization.analytics.user_usage_report.list(
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            bucket_width="1d",
            claude_tag_categories=["engaged"],
            claude_tag_user_ids=["U0123ABCDEF"],
            context_windows=["0-200k"],
            ending_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            exclude_deleted_users=True,
            group_by=["claude_tag_category"],
            inference_geos=["global"],
            limit=1,
            models=["string"],
            order="asc",
            order_by="output_tokens",
            page="page",
            products=["chat"],
            rbac_group_ids=["rbac_group_012rppKaSVsmTo6NqRDXQXNF"],
            slack_channel_ids=["C0123ABCDEF"],
            speeds=["fast"],
            user_ids=["user_01AbCdEfGhIjKlMnOpQrSt"],
        )
        assert_matches_type(AsyncPageCursor[BetaAnalyticsUsageUsersItem], user_usage_report, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.analytics.user_usage_report.with_raw_response.list(
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_usage_report = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaAnalyticsUsageUsersItem], user_usage_report, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.analytics.user_usage_report.with_streaming_response.list(
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_usage_report = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaAnalyticsUsageUsersItem], user_usage_report, path=["response"])

        assert cast(Any, response.is_closed) is True
