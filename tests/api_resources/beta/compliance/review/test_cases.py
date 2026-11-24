from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.compliance.review import (
    BetaComplianceReviewCase,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCases:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        case = client.beta.compliance.review.cases.retrieve(
            case_id="case_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        case = client.beta.compliance.review.cases.retrieve(
            case_id="case_id",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.compliance.review.cases.with_raw_response.retrieve(
            case_id="case_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        case = response.parse()
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.compliance.review.cases.with_streaming_response.retrieve(
            case_id="case_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            case = response.parse()
            assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `case_id` but received ''"):
            client.beta.compliance.review.cases.with_raw_response.retrieve(
                case_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        case = client.beta.compliance.review.cases.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaComplianceReviewCase], case, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        case = client.beta.compliance.review.cases.list(
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=0,
            order="asc",
            order_by="created_at",
            page="page",
            status="open",
            updated_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            updated_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            updated_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            updated_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            user_profile_id="user_profile_id",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaComplianceReviewCase], case, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.compliance.review.cases.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        case = response.parse()
        assert_matches_type(SyncPageCursor[BetaComplianceReviewCase], case, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.compliance.review.cases.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            case = response.parse()
            assert_matches_type(SyncPageCursor[BetaComplianceReviewCase], case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_respond(self, client: Anthropic) -> None:
        case = client.beta.compliance.review.cases.respond(
            case_id="case_id",
            determination="no_violation",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    def test_method_respond_with_all_params(self, client: Anthropic) -> None:
        case = client.beta.compliance.review.cases.respond(
            case_id="case_id",
            determination="no_violation",
            policy_categories=["cyber"],
            verdicts=[
                {
                    "determination": "violation",
                    "item_id": "item_id",
                    "policy_category": "cyber",
                }
            ],
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    def test_raw_response_respond(self, client: Anthropic) -> None:
        response = client.beta.compliance.review.cases.with_raw_response.respond(
            case_id="case_id",
            determination="no_violation",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        case = response.parse()
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    def test_streaming_response_respond(self, client: Anthropic) -> None:
        with client.beta.compliance.review.cases.with_streaming_response.respond(
            case_id="case_id",
            determination="no_violation",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            case = response.parse()
            assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_respond(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `case_id` but received ''"):
            client.beta.compliance.review.cases.with_raw_response.respond(
                case_id="",
                determination="no_violation",
            )


class TestAsyncCases:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        case = await async_client.beta.compliance.review.cases.retrieve(
            case_id="case_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        case = await async_client.beta.compliance.review.cases.retrieve(
            case_id="case_id",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.compliance.review.cases.with_raw_response.retrieve(
            case_id="case_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        case = await response.parse()
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.compliance.review.cases.with_streaming_response.retrieve(
            case_id="case_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            case = await response.parse()
            assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `case_id` but received ''"):
            await async_client.beta.compliance.review.cases.with_raw_response.retrieve(
                case_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        case = await async_client.beta.compliance.review.cases.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaComplianceReviewCase], case, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        case = await async_client.beta.compliance.review.cases.list(
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=0,
            order="asc",
            order_by="created_at",
            page="page",
            status="open",
            updated_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            updated_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            updated_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            updated_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            user_profile_id="user_profile_id",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaComplianceReviewCase], case, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.compliance.review.cases.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        case = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaComplianceReviewCase], case, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.compliance.review.cases.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            case = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaComplianceReviewCase], case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_respond(self, async_client: AsyncAnthropic) -> None:
        case = await async_client.beta.compliance.review.cases.respond(
            case_id="case_id",
            determination="no_violation",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    async def test_method_respond_with_all_params(self, async_client: AsyncAnthropic) -> None:
        case = await async_client.beta.compliance.review.cases.respond(
            case_id="case_id",
            determination="no_violation",
            policy_categories=["cyber"],
            verdicts=[
                {
                    "determination": "violation",
                    "item_id": "item_id",
                    "policy_category": "cyber",
                }
            ],
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    async def test_raw_response_respond(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.compliance.review.cases.with_raw_response.respond(
            case_id="case_id",
            determination="no_violation",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        case = await response.parse()
        assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

    @parametrize
    async def test_streaming_response_respond(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.compliance.review.cases.with_streaming_response.respond(
            case_id="case_id",
            determination="no_violation",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            case = await response.parse()
            assert_matches_type(BetaComplianceReviewCase, case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_respond(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `case_id` but received ''"):
            await async_client.beta.compliance.review.cases.with_raw_response.respond(
                case_id="",
                determination="no_violation",
            )
