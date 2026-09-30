from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import BetaRBACRole

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRBACRoles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        rbac_role = client.beta.organization.rbac_roles.retrieve(
            "rbac_role_id",
        )
        assert_matches_type(BetaRBACRole, rbac_role, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.rbac_roles.with_raw_response.retrieve(
            "rbac_role_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_role = response.parse()
        assert_matches_type(BetaRBACRole, rbac_role, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.rbac_roles.with_streaming_response.retrieve(
            "rbac_role_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_role = response.parse()
            assert_matches_type(BetaRBACRole, rbac_role, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rbac_role_id` but received ''"):
            client.beta.organization.rbac_roles.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        rbac_role = client.beta.organization.rbac_roles.list()
        assert_matches_type(SyncPageCursor[BetaRBACRole], rbac_role, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        rbac_role = client.beta.organization.rbac_roles.list(
            limit=1,
            page="eyJjdXJzb3IiOiAicmJhY19yb2xlXzAxIn0",
        )
        assert_matches_type(SyncPageCursor[BetaRBACRole], rbac_role, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.rbac_roles.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_role = response.parse()
        assert_matches_type(SyncPageCursor[BetaRBACRole], rbac_role, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.rbac_roles.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_role = response.parse()
            assert_matches_type(SyncPageCursor[BetaRBACRole], rbac_role, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRBACRoles:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        rbac_role = await async_client.beta.organization.rbac_roles.retrieve(
            "rbac_role_id",
        )
        assert_matches_type(BetaRBACRole, rbac_role, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.rbac_roles.with_raw_response.retrieve(
            "rbac_role_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_role = await response.parse()
        assert_matches_type(BetaRBACRole, rbac_role, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.rbac_roles.with_streaming_response.retrieve(
            "rbac_role_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_role = await response.parse()
            assert_matches_type(BetaRBACRole, rbac_role, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rbac_role_id` but received ''"):
            await async_client.beta.organization.rbac_roles.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        rbac_role = await async_client.beta.organization.rbac_roles.list()
        assert_matches_type(AsyncPageCursor[BetaRBACRole], rbac_role, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rbac_role = await async_client.beta.organization.rbac_roles.list(
            limit=1,
            page="eyJjdXJzb3IiOiAicmJhY19yb2xlXzAxIn0",
        )
        assert_matches_type(AsyncPageCursor[BetaRBACRole], rbac_role, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.rbac_roles.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_role = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaRBACRole], rbac_role, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.rbac_roles.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_role = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaRBACRole], rbac_role, path=["response"])

        assert cast(Any, response.is_closed) is True
