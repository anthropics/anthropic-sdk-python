from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.types.beta.compliance.review import BetaComplianceReviewItem

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestItems:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        item = client.beta.compliance.review.items.retrieve(
            item_id="item_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewItem, item, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        item = client.beta.compliance.review.items.retrieve(
            item_id="item_id",
            betas=["computer-use-2024-10-22"],
            user_profile_id="anthropic-user-profile-id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewItem, item, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.compliance.review.items.with_raw_response.retrieve(
            item_id="item_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        item = response.parse()
        assert_matches_type(BetaComplianceReviewItem, item, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.compliance.review.items.with_streaming_response.retrieve(
            item_id="item_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            item = response.parse()
            assert_matches_type(BetaComplianceReviewItem, item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `item_id` but received ''"):
            client.beta.compliance.review.items.with_raw_response.retrieve(
                item_id="",
            )


class TestAsyncItems:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        item = await async_client.beta.compliance.review.items.retrieve(
            item_id="item_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewItem, item, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        item = await async_client.beta.compliance.review.items.retrieve(
            item_id="item_id",
            betas=["computer-use-2024-10-22"],
            user_profile_id="anthropic-user-profile-id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaComplianceReviewItem, item, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.compliance.review.items.with_raw_response.retrieve(
            item_id="item_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        item = await response.parse()
        assert_matches_type(BetaComplianceReviewItem, item, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.compliance.review.items.with_streaming_response.retrieve(
            item_id="item_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            item = await response.parse()
            assert_matches_type(BetaComplianceReviewItem, item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `item_id` but received ''"):
            await async_client.beta.compliance.review.items.with_raw_response.retrieve(
                item_id="",
            )
