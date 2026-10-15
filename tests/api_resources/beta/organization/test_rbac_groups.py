from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import (
    BetaRBACGroup,
    RBACGroupDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRBACGroups:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        rbac_group = client.beta.organization.rbac_groups.create(
            name="Engineering",
        )
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.rbac_groups.with_raw_response.create(
            name="Engineering",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group = response.parse()
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.rbac_groups.with_streaming_response.create(
            name="Engineering",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group = response.parse()
            assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        rbac_group = client.beta.organization.rbac_groups.retrieve(
            "rbac_group_id",
        )
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.rbac_groups.with_raw_response.retrieve(
            "rbac_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group = response.parse()
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.rbac_groups.with_streaming_response.retrieve(
            "rbac_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group = response.parse()
            assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rbac_group_id` but received ''"):
            client.beta.organization.rbac_groups.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        rbac_group = client.beta.organization.rbac_groups.update(
            rbac_group_id="rbac_group_id",
        )
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        rbac_group = client.beta.organization.rbac_groups.update(
            rbac_group_id="rbac_group_id",
            name="Engineering",
        )
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.rbac_groups.with_raw_response.update(
            rbac_group_id="rbac_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group = response.parse()
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.rbac_groups.with_streaming_response.update(
            rbac_group_id="rbac_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group = response.parse()
            assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rbac_group_id` but received ''"):
            client.beta.organization.rbac_groups.with_raw_response.update(
                rbac_group_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        rbac_group = client.beta.organization.rbac_groups.list()
        assert_matches_type(SyncPageCursor[BetaRBACGroup], rbac_group, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        rbac_group = client.beta.organization.rbac_groups.list(
            limit=1,
            page="eyJjdXJzb3IiOiAicmJhY19ncm91cF8wMSJ9",
        )
        assert_matches_type(SyncPageCursor[BetaRBACGroup], rbac_group, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.rbac_groups.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group = response.parse()
        assert_matches_type(SyncPageCursor[BetaRBACGroup], rbac_group, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.rbac_groups.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group = response.parse()
            assert_matches_type(SyncPageCursor[BetaRBACGroup], rbac_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        rbac_group = client.beta.organization.rbac_groups.delete(
            "rbac_group_id",
        )
        assert_matches_type(RBACGroupDeleteResponse, rbac_group, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.organization.rbac_groups.with_raw_response.delete(
            "rbac_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group = response.parse()
        assert_matches_type(RBACGroupDeleteResponse, rbac_group, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.organization.rbac_groups.with_streaming_response.delete(
            "rbac_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group = response.parse()
            assert_matches_type(RBACGroupDeleteResponse, rbac_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rbac_group_id` but received ''"):
            client.beta.organization.rbac_groups.with_raw_response.delete(
                "",
            )


class TestAsyncRBACGroups:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        rbac_group = await async_client.beta.organization.rbac_groups.create(
            name="Engineering",
        )
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.rbac_groups.with_raw_response.create(
            name="Engineering",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group = await response.parse()
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.rbac_groups.with_streaming_response.create(
            name="Engineering",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group = await response.parse()
            assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        rbac_group = await async_client.beta.organization.rbac_groups.retrieve(
            "rbac_group_id",
        )
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.rbac_groups.with_raw_response.retrieve(
            "rbac_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group = await response.parse()
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.rbac_groups.with_streaming_response.retrieve(
            "rbac_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group = await response.parse()
            assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rbac_group_id` but received ''"):
            await async_client.beta.organization.rbac_groups.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        rbac_group = await async_client.beta.organization.rbac_groups.update(
            rbac_group_id="rbac_group_id",
        )
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rbac_group = await async_client.beta.organization.rbac_groups.update(
            rbac_group_id="rbac_group_id",
            name="Engineering",
        )
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.rbac_groups.with_raw_response.update(
            rbac_group_id="rbac_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group = await response.parse()
        assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.rbac_groups.with_streaming_response.update(
            rbac_group_id="rbac_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group = await response.parse()
            assert_matches_type(BetaRBACGroup, rbac_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rbac_group_id` but received ''"):
            await async_client.beta.organization.rbac_groups.with_raw_response.update(
                rbac_group_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        rbac_group = await async_client.beta.organization.rbac_groups.list()
        assert_matches_type(AsyncPageCursor[BetaRBACGroup], rbac_group, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rbac_group = await async_client.beta.organization.rbac_groups.list(
            limit=1,
            page="eyJjdXJzb3IiOiAicmJhY19ncm91cF8wMSJ9",
        )
        assert_matches_type(AsyncPageCursor[BetaRBACGroup], rbac_group, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.rbac_groups.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaRBACGroup], rbac_group, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.rbac_groups.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaRBACGroup], rbac_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        rbac_group = await async_client.beta.organization.rbac_groups.delete(
            "rbac_group_id",
        )
        assert_matches_type(RBACGroupDeleteResponse, rbac_group, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.rbac_groups.with_raw_response.delete(
            "rbac_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group = await response.parse()
        assert_matches_type(RBACGroupDeleteResponse, rbac_group, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.rbac_groups.with_streaming_response.delete(
            "rbac_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group = await response.parse()
            assert_matches_type(RBACGroupDeleteResponse, rbac_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rbac_group_id` but received ''"):
            await async_client.beta.organization.rbac_groups.with_raw_response.delete(
                "",
            )
