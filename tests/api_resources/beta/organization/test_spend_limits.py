from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import (
    BetaSpendLimit,
    SpendLimitDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSpendLimits:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        spend_limit = client.beta.organization.spend_limits.retrieve(
            "spend_limit_id",
        )
        assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.spend_limits.with_raw_response.retrieve(
            "spend_limit_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spend_limit = response.parse()
        assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.spend_limits.with_streaming_response.retrieve(
            "spend_limit_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spend_limit = response.parse()
            assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `spend_limit_id` but received ''"):
            client.beta.organization.spend_limits.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        spend_limit = client.beta.organization.spend_limits.list()
        assert_matches_type(SyncPageCursor[BetaSpendLimit], spend_limit, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        spend_limit = client.beta.organization.spend_limits.list(
            limit=1,
            page="page",
            scope_type=["organization"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaSpendLimit], spend_limit, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.spend_limits.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spend_limit = response.parse()
        assert_matches_type(SyncPageCursor[BetaSpendLimit], spend_limit, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.spend_limits.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spend_limit = response.parse()
            assert_matches_type(SyncPageCursor[BetaSpendLimit], spend_limit, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        spend_limit = client.beta.organization.spend_limits.delete(
            "spend_limit_id",
        )
        assert_matches_type(SpendLimitDeleteResponse, spend_limit, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.organization.spend_limits.with_raw_response.delete(
            "spend_limit_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spend_limit = response.parse()
        assert_matches_type(SpendLimitDeleteResponse, spend_limit, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.organization.spend_limits.with_streaming_response.delete(
            "spend_limit_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spend_limit = response.parse()
            assert_matches_type(SpendLimitDeleteResponse, spend_limit, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `spend_limit_id` but received ''"):
            client.beta.organization.spend_limits.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_set(self, client: Anthropic) -> None:
        spend_limit = client.beta.organization.spend_limits.set(
            amount="50000",
            scope={
                "type": "user",
                "user_id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
            },
        )
        assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

    @parametrize
    def test_method_set_with_all_params(self, client: Anthropic) -> None:
        spend_limit = client.beta.organization.spend_limits.set(
            amount="50000",
            scope={
                "type": "user",
                "user_id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
            },
            period="monthly",
        )
        assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

    @parametrize
    def test_raw_response_set(self, client: Anthropic) -> None:
        response = client.beta.organization.spend_limits.with_raw_response.set(
            amount="50000",
            scope={
                "type": "user",
                "user_id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spend_limit = response.parse()
        assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

    @parametrize
    def test_streaming_response_set(self, client: Anthropic) -> None:
        with client.beta.organization.spend_limits.with_streaming_response.set(
            amount="50000",
            scope={
                "type": "user",
                "user_id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spend_limit = response.parse()
            assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSpendLimits:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        spend_limit = await async_client.beta.organization.spend_limits.retrieve(
            "spend_limit_id",
        )
        assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.spend_limits.with_raw_response.retrieve(
            "spend_limit_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spend_limit = await response.parse()
        assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.spend_limits.with_streaming_response.retrieve(
            "spend_limit_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spend_limit = await response.parse()
            assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `spend_limit_id` but received ''"):
            await async_client.beta.organization.spend_limits.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        spend_limit = await async_client.beta.organization.spend_limits.list()
        assert_matches_type(AsyncPageCursor[BetaSpendLimit], spend_limit, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        spend_limit = await async_client.beta.organization.spend_limits.list(
            limit=1,
            page="page",
            scope_type=["organization"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaSpendLimit], spend_limit, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.spend_limits.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spend_limit = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaSpendLimit], spend_limit, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.spend_limits.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spend_limit = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaSpendLimit], spend_limit, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        spend_limit = await async_client.beta.organization.spend_limits.delete(
            "spend_limit_id",
        )
        assert_matches_type(SpendLimitDeleteResponse, spend_limit, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.spend_limits.with_raw_response.delete(
            "spend_limit_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spend_limit = await response.parse()
        assert_matches_type(SpendLimitDeleteResponse, spend_limit, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.spend_limits.with_streaming_response.delete(
            "spend_limit_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spend_limit = await response.parse()
            assert_matches_type(SpendLimitDeleteResponse, spend_limit, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `spend_limit_id` but received ''"):
            await async_client.beta.organization.spend_limits.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_set(self, async_client: AsyncAnthropic) -> None:
        spend_limit = await async_client.beta.organization.spend_limits.set(
            amount="50000",
            scope={
                "type": "user",
                "user_id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
            },
        )
        assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

    @parametrize
    async def test_method_set_with_all_params(self, async_client: AsyncAnthropic) -> None:
        spend_limit = await async_client.beta.organization.spend_limits.set(
            amount="50000",
            scope={
                "type": "user",
                "user_id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
            },
            period="monthly",
        )
        assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

    @parametrize
    async def test_raw_response_set(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.spend_limits.with_raw_response.set(
            amount="50000",
            scope={
                "type": "user",
                "user_id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spend_limit = await response.parse()
        assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

    @parametrize
    async def test_streaming_response_set(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.spend_limits.with_streaming_response.set(
            amount="50000",
            scope={
                "type": "user",
                "user_id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spend_limit = await response.parse()
            assert_matches_type(BetaSpendLimit, spend_limit, path=["response"])

        assert cast(Any, response.is_closed) is True
