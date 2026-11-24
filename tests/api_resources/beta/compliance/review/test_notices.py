from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.compliance.review import BetaComplianceReviewNotice

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestNotices:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        notice = client.beta.compliance.review.notices.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaComplianceReviewNotice], notice, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        notice = client.beta.compliance.review.notices.list(
            case_id="case_id",
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=0,
            order="asc",
            page="page",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaComplianceReviewNotice], notice, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.compliance.review.notices.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        notice = response.parse()
        assert_matches_type(SyncPageCursor[BetaComplianceReviewNotice], notice, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.compliance.review.notices.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            notice = response.parse()
            assert_matches_type(SyncPageCursor[BetaComplianceReviewNotice], notice, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncNotices:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        notice = await async_client.beta.compliance.review.notices.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaComplianceReviewNotice], notice, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        notice = await async_client.beta.compliance.review.notices.list(
            case_id="case_id",
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=0,
            order="asc",
            page="page",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaComplianceReviewNotice], notice, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.compliance.review.notices.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        notice = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaComplianceReviewNotice], notice, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.compliance.review.notices.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            notice = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaComplianceReviewNotice], notice, path=["response"])

        assert cast(Any, response.is_closed) is True
