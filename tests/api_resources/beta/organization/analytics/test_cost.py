from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncReportPageCursor, AsyncReportPageCursor
from anthropic.types.beta.organization.analytics import (
    BetaAnalyticsCostItem,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCost:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        cost = client.beta.organization.analytics.cost.list(
            starting_at=parse_datetime("2026-09-01T00:00:00Z"),
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncReportPageCursor[BetaAnalyticsCostItem], cost, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        cost = client.beta.organization.analytics.cost.list(
            starting_at=parse_datetime("2026-09-01T00:00:00Z"),
            actor_ids=["user_01WCz1FkmYMm4gnmykNKUu3Q"],
            actor_types=["service_account_actor"],
            agent_ids=["agent_01VHd3EAGJ6PLkP9LM7DDu3f"],
            api_key_ids=["apikey_01Rj2N8SVvo6BePZj99NhmiT"],
            claude_tag_categories=["engaged"],
            claude_tag_user_ids=["U0123ABCDEF"],
            context_windows=["0-200k"],
            deployment_ids=["depl_01JFC6ihzZHtAuyHsaENdJhY"],
            ending_at=parse_datetime("2026-10-01T00:00:00Z"),
            environment_ids=["env_017oTjuGedHtjhJauVC5xGJD"],
            exclude_deleted_users=True,
            group_by=["actor"],
            inference_geos=["global"],
            limit=1,
            models=["string"],
            order="asc",
            order_by="amount",
            page="page",
            products=["chat"],
            rbac_group_ids=["rbac_group_012rppKaSVsmTo6NqRDXQXNF"],
            service_tiers=["batch"],
            session_ids=["sesn_0187kPDyNCwibNNvfaPEApCJ"],
            slack_channel_ids=["C0123ABCDEF"],
            speeds=["fast"],
            time_bucket_width="1d",
            user_profile_ids=["uprof_01M33NeYUQK2WV9PpYcsPHLi"],
            workspace_ids=["wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"],
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncReportPageCursor[BetaAnalyticsCostItem], cost, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.analytics.cost.with_raw_response.list(
            starting_at=parse_datetime("2026-09-01T00:00:00Z"),
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        cost = response.parse()
        assert_matches_type(SyncReportPageCursor[BetaAnalyticsCostItem], cost, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.analytics.cost.with_streaming_response.list(
            starting_at=parse_datetime("2026-09-01T00:00:00Z"),
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            cost = response.parse()
            assert_matches_type(SyncReportPageCursor[BetaAnalyticsCostItem], cost, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCost:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        cost = await async_client.beta.organization.analytics.cost.list(
            starting_at=parse_datetime("2026-09-01T00:00:00Z"),
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncReportPageCursor[BetaAnalyticsCostItem], cost, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        cost = await async_client.beta.organization.analytics.cost.list(
            starting_at=parse_datetime("2026-09-01T00:00:00Z"),
            actor_ids=["user_01WCz1FkmYMm4gnmykNKUu3Q"],
            actor_types=["service_account_actor"],
            agent_ids=["agent_01VHd3EAGJ6PLkP9LM7DDu3f"],
            api_key_ids=["apikey_01Rj2N8SVvo6BePZj99NhmiT"],
            claude_tag_categories=["engaged"],
            claude_tag_user_ids=["U0123ABCDEF"],
            context_windows=["0-200k"],
            deployment_ids=["depl_01JFC6ihzZHtAuyHsaENdJhY"],
            ending_at=parse_datetime("2026-10-01T00:00:00Z"),
            environment_ids=["env_017oTjuGedHtjhJauVC5xGJD"],
            exclude_deleted_users=True,
            group_by=["actor"],
            inference_geos=["global"],
            limit=1,
            models=["string"],
            order="asc",
            order_by="amount",
            page="page",
            products=["chat"],
            rbac_group_ids=["rbac_group_012rppKaSVsmTo6NqRDXQXNF"],
            service_tiers=["batch"],
            session_ids=["sesn_0187kPDyNCwibNNvfaPEApCJ"],
            slack_channel_ids=["C0123ABCDEF"],
            speeds=["fast"],
            time_bucket_width="1d",
            user_profile_ids=["uprof_01M33NeYUQK2WV9PpYcsPHLi"],
            workspace_ids=["wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"],
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncReportPageCursor[BetaAnalyticsCostItem], cost, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.analytics.cost.with_raw_response.list(
            starting_at=parse_datetime("2026-09-01T00:00:00Z"),
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        cost = await response.parse()
        assert_matches_type(AsyncReportPageCursor[BetaAnalyticsCostItem], cost, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.analytics.cost.with_streaming_response.list(
            starting_at=parse_datetime("2026-09-01T00:00:00Z"),
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            cost = await response.parse()
            assert_matches_type(AsyncReportPageCursor[BetaAnalyticsCostItem], cost, path=["response"])

        assert cast(Any, response.is_closed) is True
