# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import (
    BetaServiceAccount,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestServiceAccounts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        service_account = client.beta.organization.service_accounts.create(
            name="ci-deploy-bot",
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        service_account = client.beta.organization.service_accounts.create(
            name="ci-deploy-bot",
            description="description",
            organization_role="admin",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.service_accounts.with_raw_response.create(
            name="ci-deploy-bot",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.service_accounts.with_streaming_response.create(
            name="ci-deploy-bot",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(BetaServiceAccount, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        service_account = client.beta.organization.service_accounts.retrieve(
            service_account_id="service_account_id",
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        service_account = client.beta.organization.service_accounts.retrieve(
            service_account_id="service_account_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.service_accounts.with_raw_response.retrieve(
            service_account_id="service_account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.service_accounts.with_streaming_response.retrieve(
            service_account_id="service_account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(BetaServiceAccount, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            client.beta.organization.service_accounts.with_raw_response.retrieve(
                service_account_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        service_account = client.beta.organization.service_accounts.update(
            service_account_id="service_account_id",
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        service_account = client.beta.organization.service_accounts.update(
            service_account_id="service_account_id",
            description="description",
            organization_role="admin",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.service_accounts.with_raw_response.update(
            service_account_id="service_account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.service_accounts.with_streaming_response.update(
            service_account_id="service_account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(BetaServiceAccount, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            client.beta.organization.service_accounts.with_raw_response.update(
                service_account_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        service_account = client.beta.organization.service_accounts.list()
        assert_matches_type(SyncPageCursor[BetaServiceAccount], service_account, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        service_account = client.beta.organization.service_accounts.list(
            include_archived=True,
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaServiceAccount], service_account, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.service_accounts.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(SyncPageCursor[BetaServiceAccount], service_account, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.service_accounts.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(SyncPageCursor[BetaServiceAccount], service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        service_account = client.beta.organization.service_accounts.archive(
            service_account_id="service_account_id",
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        service_account = client.beta.organization.service_accounts.archive(
            service_account_id="service_account_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.organization.service_accounts.with_raw_response.archive(
            service_account_id="service_account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.organization.service_accounts.with_streaming_response.archive(
            service_account_id="service_account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(BetaServiceAccount, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            client.beta.organization.service_accounts.with_raw_response.archive(
                service_account_id="",
            )


class TestAsyncServiceAccounts:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.service_accounts.create(
            name="ci-deploy-bot",
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.service_accounts.create(
            name="ci-deploy-bot",
            description="description",
            organization_role="admin",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.service_accounts.with_raw_response.create(
            name="ci-deploy-bot",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.service_accounts.with_streaming_response.create(
            name="ci-deploy-bot",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(BetaServiceAccount, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.service_accounts.retrieve(
            service_account_id="service_account_id",
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.service_accounts.retrieve(
            service_account_id="service_account_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.service_accounts.with_raw_response.retrieve(
            service_account_id="service_account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.service_accounts.with_streaming_response.retrieve(
            service_account_id="service_account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(BetaServiceAccount, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            await async_client.beta.organization.service_accounts.with_raw_response.retrieve(
                service_account_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.service_accounts.update(
            service_account_id="service_account_id",
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.service_accounts.update(
            service_account_id="service_account_id",
            description="description",
            organization_role="admin",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.service_accounts.with_raw_response.update(
            service_account_id="service_account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.service_accounts.with_streaming_response.update(
            service_account_id="service_account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(BetaServiceAccount, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            await async_client.beta.organization.service_accounts.with_raw_response.update(
                service_account_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.service_accounts.list()
        assert_matches_type(AsyncPageCursor[BetaServiceAccount], service_account, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.service_accounts.list(
            include_archived=True,
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaServiceAccount], service_account, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.service_accounts.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaServiceAccount], service_account, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.service_accounts.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaServiceAccount], service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.service_accounts.archive(
            service_account_id="service_account_id",
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        service_account = await async_client.beta.organization.service_accounts.archive(
            service_account_id="service_account_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.service_accounts.with_raw_response.archive(
            service_account_id="service_account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(BetaServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.service_accounts.with_streaming_response.archive(
            service_account_id="service_account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(BetaServiceAccount, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            await async_client.beta.organization.service_accounts.with_raw_response.archive(
                service_account_id="",
            )
