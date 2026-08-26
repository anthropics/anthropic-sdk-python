# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPage, AsyncPage
from anthropic.types.beta.organization import BetaWorkspaceMember
from anthropic.types.beta.organization.workspaces import (
    MemberRemoveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMembers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        member = client.beta.organization.workspaces.members.retrieve(
            user_id="user_id",
            workspace_id="workspace_id",
        )
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.members.with_raw_response.retrieve(
            user_id="user_id",
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = response.parse()
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.members.with_streaming_response.retrieve(
            user_id="user_id",
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = response.parse()
            assert_matches_type(BetaWorkspaceMember, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.members.with_raw_response.retrieve(
                user_id="user_id",
                workspace_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.beta.organization.workspaces.members.with_raw_response.retrieve(
                user_id="",
                workspace_id="workspace_id",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        member = client.beta.organization.workspaces.members.update(
            user_id="user_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.members.with_raw_response.update(
            user_id="user_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = response.parse()
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.members.with_streaming_response.update(
            user_id="user_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = response.parse()
            assert_matches_type(BetaWorkspaceMember, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.members.with_raw_response.update(
                user_id="user_id",
                workspace_id="",
                workspace_role="workspace_admin",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.beta.organization.workspaces.members.with_raw_response.update(
                user_id="",
                workspace_id="workspace_id",
                workspace_role="workspace_admin",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        member = client.beta.organization.workspaces.members.list(
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncPage[BetaWorkspaceMember], member, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        member = client.beta.organization.workspaces.members.list(
            workspace_id="workspace_id",
            after_id="after_id",
            before_id="before_id",
            limit=1,
        )
        assert_matches_type(SyncPage[BetaWorkspaceMember], member, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.members.with_raw_response.list(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = response.parse()
        assert_matches_type(SyncPage[BetaWorkspaceMember], member, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.members.with_streaming_response.list(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = response.parse()
            assert_matches_type(SyncPage[BetaWorkspaceMember], member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.members.with_raw_response.list(
                workspace_id="",
            )

    @parametrize
    def test_method_add(self, client: Anthropic) -> None:
        member = client.beta.organization.workspaces.members.add(
            workspace_id="workspace_id",
            user_id="user_01WCz1FkmYMm4gnmykNKUu3Q",
            workspace_role="workspace_admin",
        )
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    def test_raw_response_add(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.members.with_raw_response.add(
            workspace_id="workspace_id",
            user_id="user_01WCz1FkmYMm4gnmykNKUu3Q",
            workspace_role="workspace_admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = response.parse()
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    def test_streaming_response_add(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.members.with_streaming_response.add(
            workspace_id="workspace_id",
            user_id="user_01WCz1FkmYMm4gnmykNKUu3Q",
            workspace_role="workspace_admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = response.parse()
            assert_matches_type(BetaWorkspaceMember, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_add(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.members.with_raw_response.add(
                workspace_id="",
                user_id="user_01WCz1FkmYMm4gnmykNKUu3Q",
                workspace_role="workspace_admin",
            )

    @parametrize
    def test_method_remove(self, client: Anthropic) -> None:
        member = client.beta.organization.workspaces.members.remove(
            user_id="user_id",
            workspace_id="workspace_id",
        )
        assert_matches_type(MemberRemoveResponse, member, path=["response"])

    @parametrize
    def test_raw_response_remove(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.members.with_raw_response.remove(
            user_id="user_id",
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = response.parse()
        assert_matches_type(MemberRemoveResponse, member, path=["response"])

    @parametrize
    def test_streaming_response_remove(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.members.with_streaming_response.remove(
            user_id="user_id",
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = response.parse()
            assert_matches_type(MemberRemoveResponse, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_remove(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.members.with_raw_response.remove(
                user_id="user_id",
                workspace_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.beta.organization.workspaces.members.with_raw_response.remove(
                user_id="",
                workspace_id="workspace_id",
            )


class TestAsyncMembers:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        member = await async_client.beta.organization.workspaces.members.retrieve(
            user_id="user_id",
            workspace_id="workspace_id",
        )
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.members.with_raw_response.retrieve(
            user_id="user_id",
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = await response.parse()
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.members.with_streaming_response.retrieve(
            user_id="user_id",
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = await response.parse()
            assert_matches_type(BetaWorkspaceMember, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.members.with_raw_response.retrieve(
                user_id="user_id",
                workspace_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.beta.organization.workspaces.members.with_raw_response.retrieve(
                user_id="",
                workspace_id="workspace_id",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        member = await async_client.beta.organization.workspaces.members.update(
            user_id="user_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.members.with_raw_response.update(
            user_id="user_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = await response.parse()
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.members.with_streaming_response.update(
            user_id="user_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = await response.parse()
            assert_matches_type(BetaWorkspaceMember, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.members.with_raw_response.update(
                user_id="user_id",
                workspace_id="",
                workspace_role="workspace_admin",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.beta.organization.workspaces.members.with_raw_response.update(
                user_id="",
                workspace_id="workspace_id",
                workspace_role="workspace_admin",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        member = await async_client.beta.organization.workspaces.members.list(
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncPage[BetaWorkspaceMember], member, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        member = await async_client.beta.organization.workspaces.members.list(
            workspace_id="workspace_id",
            after_id="after_id",
            before_id="before_id",
            limit=1,
        )
        assert_matches_type(AsyncPage[BetaWorkspaceMember], member, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.members.with_raw_response.list(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = await response.parse()
        assert_matches_type(AsyncPage[BetaWorkspaceMember], member, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.members.with_streaming_response.list(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = await response.parse()
            assert_matches_type(AsyncPage[BetaWorkspaceMember], member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.members.with_raw_response.list(
                workspace_id="",
            )

    @parametrize
    async def test_method_add(self, async_client: AsyncAnthropic) -> None:
        member = await async_client.beta.organization.workspaces.members.add(
            workspace_id="workspace_id",
            user_id="user_01WCz1FkmYMm4gnmykNKUu3Q",
            workspace_role="workspace_admin",
        )
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    async def test_raw_response_add(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.members.with_raw_response.add(
            workspace_id="workspace_id",
            user_id="user_01WCz1FkmYMm4gnmykNKUu3Q",
            workspace_role="workspace_admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = await response.parse()
        assert_matches_type(BetaWorkspaceMember, member, path=["response"])

    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.members.with_streaming_response.add(
            workspace_id="workspace_id",
            user_id="user_01WCz1FkmYMm4gnmykNKUu3Q",
            workspace_role="workspace_admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = await response.parse()
            assert_matches_type(BetaWorkspaceMember, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_add(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.members.with_raw_response.add(
                workspace_id="",
                user_id="user_01WCz1FkmYMm4gnmykNKUu3Q",
                workspace_role="workspace_admin",
            )

    @parametrize
    async def test_method_remove(self, async_client: AsyncAnthropic) -> None:
        member = await async_client.beta.organization.workspaces.members.remove(
            user_id="user_id",
            workspace_id="workspace_id",
        )
        assert_matches_type(MemberRemoveResponse, member, path=["response"])

    @parametrize
    async def test_raw_response_remove(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.members.with_raw_response.remove(
            user_id="user_id",
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = await response.parse()
        assert_matches_type(MemberRemoveResponse, member, path=["response"])

    @parametrize
    async def test_streaming_response_remove(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.members.with_streaming_response.remove(
            user_id="user_id",
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = await response.parse()
            assert_matches_type(MemberRemoveResponse, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_remove(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.members.with_raw_response.remove(
                user_id="user_id",
                workspace_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.beta.organization.workspaces.members.with_raw_response.remove(
                user_id="",
                workspace_id="workspace_id",
            )
