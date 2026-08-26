# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import BetaServiceAccountWorkspaceMember
from anthropic.types.beta.organization.service_accounts import (
    WorkspaceRemoveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWorkspaces:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        workspace = client.beta.organization.service_accounts.workspaces.list(
            service_account_id="service_account_id",
        )
        assert_matches_type(SyncPageCursor[BetaServiceAccountWorkspaceMember], workspace, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        workspace = client.beta.organization.service_accounts.workspaces.list(
            service_account_id="service_account_id",
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaServiceAccountWorkspaceMember], workspace, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.service_accounts.workspaces.with_raw_response.list(
            service_account_id="service_account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(SyncPageCursor[BetaServiceAccountWorkspaceMember], workspace, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.service_accounts.workspaces.with_streaming_response.list(
            service_account_id="service_account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(SyncPageCursor[BetaServiceAccountWorkspaceMember], workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            client.beta.organization.service_accounts.workspaces.with_raw_response.list(
                service_account_id="",
            )

    @parametrize
    def test_method_add(self, client: Anthropic) -> None:
        workspace = client.beta.organization.service_accounts.workspaces.add(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, workspace, path=["response"])

    @parametrize
    def test_method_add_with_all_params(self, client: Anthropic) -> None:
        workspace = client.beta.organization.service_accounts.workspaces.add(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, workspace, path=["response"])

    @parametrize
    def test_raw_response_add(self, client: Anthropic) -> None:
        response = client.beta.organization.service_accounts.workspaces.with_raw_response.add(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(BetaServiceAccountWorkspaceMember, workspace, path=["response"])

    @parametrize
    def test_streaming_response_add(self, client: Anthropic) -> None:
        with client.beta.organization.service_accounts.workspaces.with_streaming_response.add(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(BetaServiceAccountWorkspaceMember, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_add(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            client.beta.organization.service_accounts.workspaces.with_raw_response.add(
                service_account_id="",
                workspace_id="workspace_id",
                workspace_role="workspace_admin",
            )

    @parametrize
    def test_method_remove(self, client: Anthropic) -> None:
        workspace = client.beta.organization.service_accounts.workspaces.remove(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
        )
        assert_matches_type(WorkspaceRemoveResponse, workspace, path=["response"])

    @parametrize
    def test_method_remove_with_all_params(self, client: Anthropic) -> None:
        workspace = client.beta.organization.service_accounts.workspaces.remove(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(WorkspaceRemoveResponse, workspace, path=["response"])

    @parametrize
    def test_raw_response_remove(self, client: Anthropic) -> None:
        response = client.beta.organization.service_accounts.workspaces.with_raw_response.remove(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(WorkspaceRemoveResponse, workspace, path=["response"])

    @parametrize
    def test_streaming_response_remove(self, client: Anthropic) -> None:
        with client.beta.organization.service_accounts.workspaces.with_streaming_response.remove(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(WorkspaceRemoveResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_remove(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            client.beta.organization.service_accounts.workspaces.with_raw_response.remove(
                workspace_id="workspace_id",
                service_account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.service_accounts.workspaces.with_raw_response.remove(
                workspace_id="",
                service_account_id="service_account_id",
            )


class TestAsyncWorkspaces:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.service_accounts.workspaces.list(
            service_account_id="service_account_id",
        )
        assert_matches_type(AsyncPageCursor[BetaServiceAccountWorkspaceMember], workspace, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.service_accounts.workspaces.list(
            service_account_id="service_account_id",
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaServiceAccountWorkspaceMember], workspace, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.service_accounts.workspaces.with_raw_response.list(
            service_account_id="service_account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaServiceAccountWorkspaceMember], workspace, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.service_accounts.workspaces.with_streaming_response.list(
            service_account_id="service_account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaServiceAccountWorkspaceMember], workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            await async_client.beta.organization.service_accounts.workspaces.with_raw_response.list(
                service_account_id="",
            )

    @parametrize
    async def test_method_add(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.service_accounts.workspaces.add(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, workspace, path=["response"])

    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.service_accounts.workspaces.add(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, workspace, path=["response"])

    @parametrize
    async def test_raw_response_add(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.service_accounts.workspaces.with_raw_response.add(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(BetaServiceAccountWorkspaceMember, workspace, path=["response"])

    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.service_accounts.workspaces.with_streaming_response.add(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(BetaServiceAccountWorkspaceMember, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_add(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            await async_client.beta.organization.service_accounts.workspaces.with_raw_response.add(
                service_account_id="",
                workspace_id="workspace_id",
                workspace_role="workspace_admin",
            )

    @parametrize
    async def test_method_remove(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.service_accounts.workspaces.remove(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
        )
        assert_matches_type(WorkspaceRemoveResponse, workspace, path=["response"])

    @parametrize
    async def test_method_remove_with_all_params(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.service_accounts.workspaces.remove(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(WorkspaceRemoveResponse, workspace, path=["response"])

    @parametrize
    async def test_raw_response_remove(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.service_accounts.workspaces.with_raw_response.remove(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(WorkspaceRemoveResponse, workspace, path=["response"])

    @parametrize
    async def test_streaming_response_remove(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.service_accounts.workspaces.with_streaming_response.remove(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(WorkspaceRemoveResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_remove(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            await async_client.beta.organization.service_accounts.workspaces.with_raw_response.remove(
                workspace_id="workspace_id",
                service_account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.service_accounts.workspaces.with_raw_response.remove(
                workspace_id="",
                service_account_id="service_account_id",
            )
