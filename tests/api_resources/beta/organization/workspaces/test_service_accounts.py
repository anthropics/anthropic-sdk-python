# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import BetaServiceAccountWorkspaceMember
from anthropic.types.beta.organization.workspaces import (
    ServiceAccountRemoveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestServiceAccounts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        service_account = client.beta.organization.workspaces.service_accounts.retrieve(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        service_account = client.beta.organization.workspaces.service_accounts.retrieve(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.service_accounts.with_raw_response.retrieve(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.service_accounts.with_streaming_response.retrieve(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.service_accounts.with_raw_response.retrieve(
                service_account_id="service_account_id",
                workspace_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            client.beta.organization.workspaces.service_accounts.with_raw_response.retrieve(
                service_account_id="",
                workspace_id="workspace_id",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        service_account = client.beta.organization.workspaces.service_accounts.update(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        service_account = client.beta.organization.workspaces.service_accounts.update(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.service_accounts.with_raw_response.update(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.service_accounts.with_streaming_response.update(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.service_accounts.with_raw_response.update(
                service_account_id="service_account_id",
                workspace_id="",
                workspace_role="workspace_admin",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            client.beta.organization.workspaces.service_accounts.with_raw_response.update(
                service_account_id="",
                workspace_id="workspace_id",
                workspace_role="workspace_admin",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        service_account = client.beta.organization.workspaces.service_accounts.list(
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncPageCursor[BetaServiceAccountWorkspaceMember], service_account, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        service_account = client.beta.organization.workspaces.service_accounts.list(
            workspace_id="workspace_id",
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaServiceAccountWorkspaceMember], service_account, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.service_accounts.with_raw_response.list(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(SyncPageCursor[BetaServiceAccountWorkspaceMember], service_account, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.service_accounts.with_streaming_response.list(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(SyncPageCursor[BetaServiceAccountWorkspaceMember], service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.service_accounts.with_raw_response.list(
                workspace_id="",
            )

    @parametrize
    def test_method_add(self, client: Anthropic) -> None:
        service_account = client.beta.organization.workspaces.service_accounts.add(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
            workspace_role="workspace_admin",
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    def test_method_add_with_all_params(self, client: Anthropic) -> None:
        service_account = client.beta.organization.workspaces.service_accounts.add(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
            workspace_role="workspace_admin",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    def test_raw_response_add(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.service_accounts.with_raw_response.add(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
            workspace_role="workspace_admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    def test_streaming_response_add(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.service_accounts.with_streaming_response.add(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
            workspace_role="workspace_admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_add(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.service_accounts.with_raw_response.add(
                workspace_id="",
                service_account_id="service_account_id",
                workspace_role="workspace_admin",
            )

    @parametrize
    def test_method_remove(self, client: Anthropic) -> None:
        service_account = client.beta.organization.workspaces.service_accounts.remove(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        )
        assert_matches_type(ServiceAccountRemoveResponse, service_account, path=["response"])

    @parametrize
    def test_method_remove_with_all_params(self, client: Anthropic) -> None:
        service_account = client.beta.organization.workspaces.service_accounts.remove(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(ServiceAccountRemoveResponse, service_account, path=["response"])

    @parametrize
    def test_raw_response_remove(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.service_accounts.with_raw_response.remove(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(ServiceAccountRemoveResponse, service_account, path=["response"])

    @parametrize
    def test_streaming_response_remove(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.service_accounts.with_streaming_response.remove(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(ServiceAccountRemoveResponse, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_remove(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.service_accounts.with_raw_response.remove(
                service_account_id="service_account_id",
                workspace_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            client.beta.organization.workspaces.service_accounts.with_raw_response.remove(
                service_account_id="",
                workspace_id="workspace_id",
            )


class TestAsyncServiceAccounts:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.workspaces.service_accounts.retrieve(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.workspaces.service_accounts.retrieve(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.service_accounts.with_raw_response.retrieve(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.service_accounts.with_streaming_response.retrieve(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.service_accounts.with_raw_response.retrieve(
                service_account_id="service_account_id",
                workspace_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            await async_client.beta.organization.workspaces.service_accounts.with_raw_response.retrieve(
                service_account_id="",
                workspace_id="workspace_id",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.workspaces.service_accounts.update(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.workspaces.service_accounts.update(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.service_accounts.with_raw_response.update(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.service_accounts.with_streaming_response.update(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            workspace_role="workspace_admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.service_accounts.with_raw_response.update(
                service_account_id="service_account_id",
                workspace_id="",
                workspace_role="workspace_admin",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            await async_client.beta.organization.workspaces.service_accounts.with_raw_response.update(
                service_account_id="",
                workspace_id="workspace_id",
                workspace_role="workspace_admin",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.workspaces.service_accounts.list(
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncPageCursor[BetaServiceAccountWorkspaceMember], service_account, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.workspaces.service_accounts.list(
            workspace_id="workspace_id",
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaServiceAccountWorkspaceMember], service_account, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.service_accounts.with_raw_response.list(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaServiceAccountWorkspaceMember], service_account, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.service_accounts.with_streaming_response.list(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaServiceAccountWorkspaceMember], service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.service_accounts.with_raw_response.list(
                workspace_id="",
            )

    @parametrize
    async def test_method_add(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.workspaces.service_accounts.add(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
            workspace_role="workspace_admin",
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.workspaces.service_accounts.add(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
            workspace_role="workspace_admin",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    async def test_raw_response_add(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.service_accounts.with_raw_response.add(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
            workspace_role="workspace_admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.service_accounts.with_streaming_response.add(
            workspace_id="workspace_id",
            service_account_id="service_account_id",
            workspace_role="workspace_admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(BetaServiceAccountWorkspaceMember, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_add(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.service_accounts.with_raw_response.add(
                workspace_id="",
                service_account_id="service_account_id",
                workspace_role="workspace_admin",
            )

    @parametrize
    async def test_method_remove(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.workspaces.service_accounts.remove(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        )
        assert_matches_type(ServiceAccountRemoveResponse, service_account, path=["response"])

    @parametrize
    async def test_method_remove_with_all_params(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.workspaces.service_accounts.remove(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(ServiceAccountRemoveResponse, service_account, path=["response"])

    @parametrize
    async def test_raw_response_remove(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.service_accounts.with_raw_response.remove(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(ServiceAccountRemoveResponse, service_account, path=["response"])

    @parametrize
    async def test_streaming_response_remove(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.service_accounts.with_streaming_response.remove(
            service_account_id="service_account_id",
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(ServiceAccountRemoveResponse, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_remove(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.service_accounts.with_raw_response.remove(
                service_account_id="service_account_id",
                workspace_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            await async_client.beta.organization.workspaces.service_accounts.with_raw_response.remove(
                service_account_id="",
                workspace_id="workspace_id",
            )
