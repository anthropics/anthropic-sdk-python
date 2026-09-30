from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_date
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import BetaAnalyticsArtifactActivity

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestArtifacts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        artifact = client.beta.organization.analytics.artifacts.list(
            date=parse_date("2019-12-27"),
        )
        assert_matches_type(SyncPageCursor[BetaAnalyticsArtifactActivity], artifact, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        artifact = client.beta.organization.analytics.artifacts.list(
            date=parse_date("2019-12-27"),
            filter=["string"],
            group_by=["product"],
            limit=1,
            page="page",
        )
        assert_matches_type(SyncPageCursor[BetaAnalyticsArtifactActivity], artifact, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.analytics.artifacts.with_raw_response.list(
            date=parse_date("2019-12-27"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = response.parse()
        assert_matches_type(SyncPageCursor[BetaAnalyticsArtifactActivity], artifact, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.analytics.artifacts.with_streaming_response.list(
            date=parse_date("2019-12-27"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = response.parse()
            assert_matches_type(SyncPageCursor[BetaAnalyticsArtifactActivity], artifact, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncArtifacts:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        artifact = await async_client.beta.organization.analytics.artifacts.list(
            date=parse_date("2019-12-27"),
        )
        assert_matches_type(AsyncPageCursor[BetaAnalyticsArtifactActivity], artifact, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        artifact = await async_client.beta.organization.analytics.artifacts.list(
            date=parse_date("2019-12-27"),
            filter=["string"],
            group_by=["product"],
            limit=1,
            page="page",
        )
        assert_matches_type(AsyncPageCursor[BetaAnalyticsArtifactActivity], artifact, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.analytics.artifacts.with_raw_response.list(
            date=parse_date("2019-12-27"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaAnalyticsArtifactActivity], artifact, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.analytics.artifacts.with_streaming_response.list(
            date=parse_date("2019-12-27"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaAnalyticsArtifactActivity], artifact, path=["response"])

        assert cast(Any, response.is_closed) is True
