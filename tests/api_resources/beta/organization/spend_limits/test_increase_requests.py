from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization.spend_limits import (
    BetaSpendLimitIncreaseRequest,
    IncreaseRequestApproveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestIncreaseRequests:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        increase_request = client.beta.organization.spend_limits.increase_requests.retrieve(
            "spend_limit_increase_request_id",
        )
        assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.spend_limits.increase_requests.with_raw_response.retrieve(
            "spend_limit_increase_request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        increase_request = response.parse()
        assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.spend_limits.increase_requests.with_streaming_response.retrieve(
            "spend_limit_increase_request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            increase_request = response.parse()
            assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `spend_limit_increase_request_id` but received ''"
        ):
            client.beta.organization.spend_limits.increase_requests.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        increase_request = client.beta.organization.spend_limits.increase_requests.list()
        assert_matches_type(SyncPageCursor[BetaSpendLimitIncreaseRequest], increase_request, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        increase_request = client.beta.organization.spend_limits.increase_requests.list(
            actor_ids=["string"],
            limit=1,
            page="page",
            status=["approved"],
        )
        assert_matches_type(SyncPageCursor[BetaSpendLimitIncreaseRequest], increase_request, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.spend_limits.increase_requests.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        increase_request = response.parse()
        assert_matches_type(SyncPageCursor[BetaSpendLimitIncreaseRequest], increase_request, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.spend_limits.increase_requests.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            increase_request = response.parse()
            assert_matches_type(SyncPageCursor[BetaSpendLimitIncreaseRequest], increase_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_approve(self, client: Anthropic) -> None:
        increase_request = client.beta.organization.spend_limits.increase_requests.approve(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
            amount="50000",
        )
        assert_matches_type(IncreaseRequestApproveResponse, increase_request, path=["response"])

    @parametrize
    def test_method_approve_with_all_params(self, client: Anthropic) -> None:
        increase_request = client.beta.organization.spend_limits.increase_requests.approve(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
            amount="50000",
            period="monthly",
            suppress_notification=True,
        )
        assert_matches_type(IncreaseRequestApproveResponse, increase_request, path=["response"])

    @parametrize
    def test_raw_response_approve(self, client: Anthropic) -> None:
        response = client.beta.organization.spend_limits.increase_requests.with_raw_response.approve(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
            amount="50000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        increase_request = response.parse()
        assert_matches_type(IncreaseRequestApproveResponse, increase_request, path=["response"])

    @parametrize
    def test_streaming_response_approve(self, client: Anthropic) -> None:
        with client.beta.organization.spend_limits.increase_requests.with_streaming_response.approve(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
            amount="50000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            increase_request = response.parse()
            assert_matches_type(IncreaseRequestApproveResponse, increase_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_approve(self, client: Anthropic) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `spend_limit_increase_request_id` but received ''"
        ):
            client.beta.organization.spend_limits.increase_requests.with_raw_response.approve(
                spend_limit_increase_request_id="",
                amount="50000",
            )

    @parametrize
    def test_method_deny(self, client: Anthropic) -> None:
        increase_request = client.beta.organization.spend_limits.increase_requests.deny(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
        )
        assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

    @parametrize
    def test_method_deny_with_all_params(self, client: Anthropic) -> None:
        increase_request = client.beta.organization.spend_limits.increase_requests.deny(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
            suppress_notification=True,
        )
        assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

    @parametrize
    def test_raw_response_deny(self, client: Anthropic) -> None:
        response = client.beta.organization.spend_limits.increase_requests.with_raw_response.deny(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        increase_request = response.parse()
        assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

    @parametrize
    def test_streaming_response_deny(self, client: Anthropic) -> None:
        with client.beta.organization.spend_limits.increase_requests.with_streaming_response.deny(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            increase_request = response.parse()
            assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_deny(self, client: Anthropic) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `spend_limit_increase_request_id` but received ''"
        ):
            client.beta.organization.spend_limits.increase_requests.with_raw_response.deny(
                spend_limit_increase_request_id="",
            )


class TestAsyncIncreaseRequests:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        increase_request = await async_client.beta.organization.spend_limits.increase_requests.retrieve(
            "spend_limit_increase_request_id",
        )
        assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.spend_limits.increase_requests.with_raw_response.retrieve(
            "spend_limit_increase_request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        increase_request = await response.parse()
        assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.spend_limits.increase_requests.with_streaming_response.retrieve(
            "spend_limit_increase_request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            increase_request = await response.parse()
            assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `spend_limit_increase_request_id` but received ''"
        ):
            await async_client.beta.organization.spend_limits.increase_requests.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        increase_request = await async_client.beta.organization.spend_limits.increase_requests.list()
        assert_matches_type(AsyncPageCursor[BetaSpendLimitIncreaseRequest], increase_request, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        increase_request = await async_client.beta.organization.spend_limits.increase_requests.list(
            actor_ids=["string"],
            limit=1,
            page="page",
            status=["approved"],
        )
        assert_matches_type(AsyncPageCursor[BetaSpendLimitIncreaseRequest], increase_request, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.spend_limits.increase_requests.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        increase_request = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaSpendLimitIncreaseRequest], increase_request, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with (
            async_client.beta.organization.spend_limits.increase_requests.with_streaming_response.list() as response
        ):
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            increase_request = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaSpendLimitIncreaseRequest], increase_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_approve(self, async_client: AsyncAnthropic) -> None:
        increase_request = await async_client.beta.organization.spend_limits.increase_requests.approve(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
            amount="50000",
        )
        assert_matches_type(IncreaseRequestApproveResponse, increase_request, path=["response"])

    @parametrize
    async def test_method_approve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        increase_request = await async_client.beta.organization.spend_limits.increase_requests.approve(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
            amount="50000",
            period="monthly",
            suppress_notification=True,
        )
        assert_matches_type(IncreaseRequestApproveResponse, increase_request, path=["response"])

    @parametrize
    async def test_raw_response_approve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.spend_limits.increase_requests.with_raw_response.approve(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
            amount="50000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        increase_request = await response.parse()
        assert_matches_type(IncreaseRequestApproveResponse, increase_request, path=["response"])

    @parametrize
    async def test_streaming_response_approve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.spend_limits.increase_requests.with_streaming_response.approve(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
            amount="50000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            increase_request = await response.parse()
            assert_matches_type(IncreaseRequestApproveResponse, increase_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_approve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `spend_limit_increase_request_id` but received ''"
        ):
            await async_client.beta.organization.spend_limits.increase_requests.with_raw_response.approve(
                spend_limit_increase_request_id="",
                amount="50000",
            )

    @parametrize
    async def test_method_deny(self, async_client: AsyncAnthropic) -> None:
        increase_request = await async_client.beta.organization.spend_limits.increase_requests.deny(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
        )
        assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

    @parametrize
    async def test_method_deny_with_all_params(self, async_client: AsyncAnthropic) -> None:
        increase_request = await async_client.beta.organization.spend_limits.increase_requests.deny(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
            suppress_notification=True,
        )
        assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

    @parametrize
    async def test_raw_response_deny(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.spend_limits.increase_requests.with_raw_response.deny(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        increase_request = await response.parse()
        assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

    @parametrize
    async def test_streaming_response_deny(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.spend_limits.increase_requests.with_streaming_response.deny(
            spend_limit_increase_request_id="spend_limit_increase_request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            increase_request = await response.parse()
            assert_matches_type(BetaSpendLimitIncreaseRequest, increase_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_deny(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `spend_limit_increase_request_id` but received ''"
        ):
            await async_client.beta.organization.spend_limits.increase_requests.with_raw_response.deny(
                spend_limit_increase_request_id="",
            )
