from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPage, AsyncPage
from anthropic.types.beta.organization import (
    BetaOrganizationWebhookEndpoint,
    BetaNewOrganizationWebhookEndpoint,
    BetaDeletedOrganizationWebhookEndpoint,
    BetaOrganizationWebhookEndpointSigningSecret,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWebhooks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.create(
            enabled_events=["user_profile.enforcement_action_opened"],
            url="x",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaNewOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.create(
            enabled_events=["user_profile.enforcement_action_opened"],
            url="x",
            description="description",
            name="name",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaNewOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.webhooks.with_raw_response.create(
            enabled_events=["user_profile.enforcement_action_opened"],
            url="x",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(BetaNewOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.webhooks.with_streaming_response.create(
            enabled_events=["user_profile.enforcement_action_opened"],
            url="x",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(BetaNewOrganizationWebhookEndpoint, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.retrieve(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.retrieve(
            webhook_endpoint_id="webhook_endpoint_id",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.webhooks.with_raw_response.retrieve(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.webhooks.with_streaming_response.retrieve(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_endpoint_id` but received ''"):
            client.beta.organization.webhooks.with_raw_response.retrieve(
                webhook_endpoint_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.update(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.update(
            webhook_endpoint_id="webhook_endpoint_id",
            description="description",
            enabled_events=["user_profile.enforcement_action_opened"],
            name="name",
            state="disabled",
            url="x",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.webhooks.with_raw_response.update(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.webhooks.with_streaming_response.update(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_endpoint_id` but received ''"):
            client.beta.organization.webhooks.with_raw_response.update(
                webhook_endpoint_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPage[BetaOrganizationWebhookEndpoint], webhook, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.list(
            after_id="after_id",
            before_id="before_id",
            limit=0,
            order="asc",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPage[BetaOrganizationWebhookEndpoint], webhook, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.webhooks.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(SyncPage[BetaOrganizationWebhookEndpoint], webhook, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.webhooks.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(SyncPage[BetaOrganizationWebhookEndpoint], webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.delete(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaDeletedOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.delete(
            webhook_endpoint_id="webhook_endpoint_id",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaDeletedOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.organization.webhooks.with_raw_response.delete(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(BetaDeletedOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.organization.webhooks.with_streaming_response.delete(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(BetaDeletedOrganizationWebhookEndpoint, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_endpoint_id` but received ''"):
            client.beta.organization.webhooks.with_raw_response.delete(
                webhook_endpoint_id="",
            )

    @parametrize
    def test_method_regenerate_signing_secret(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.regenerate_signing_secret(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpointSigningSecret, webhook, path=["response"])

    @parametrize
    def test_method_regenerate_signing_secret_with_all_params(self, client: Anthropic) -> None:
        webhook = client.beta.organization.webhooks.regenerate_signing_secret(
            webhook_endpoint_id="webhook_endpoint_id",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpointSigningSecret, webhook, path=["response"])

    @parametrize
    def test_raw_response_regenerate_signing_secret(self, client: Anthropic) -> None:
        response = client.beta.organization.webhooks.with_raw_response.regenerate_signing_secret(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(BetaOrganizationWebhookEndpointSigningSecret, webhook, path=["response"])

    @parametrize
    def test_streaming_response_regenerate_signing_secret(self, client: Anthropic) -> None:
        with client.beta.organization.webhooks.with_streaming_response.regenerate_signing_secret(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(BetaOrganizationWebhookEndpointSigningSecret, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_regenerate_signing_secret(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_endpoint_id` but received ''"):
            client.beta.organization.webhooks.with_raw_response.regenerate_signing_secret(
                webhook_endpoint_id="",
            )


class TestAsyncWebhooks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.create(
            enabled_events=["user_profile.enforcement_action_opened"],
            url="x",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaNewOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.create(
            enabled_events=["user_profile.enforcement_action_opened"],
            url="x",
            description="description",
            name="name",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaNewOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.webhooks.with_raw_response.create(
            enabled_events=["user_profile.enforcement_action_opened"],
            url="x",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(BetaNewOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.webhooks.with_streaming_response.create(
            enabled_events=["user_profile.enforcement_action_opened"],
            url="x",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(BetaNewOrganizationWebhookEndpoint, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.retrieve(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.retrieve(
            webhook_endpoint_id="webhook_endpoint_id",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.webhooks.with_raw_response.retrieve(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.webhooks.with_streaming_response.retrieve(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_endpoint_id` but received ''"):
            await async_client.beta.organization.webhooks.with_raw_response.retrieve(
                webhook_endpoint_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.update(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.update(
            webhook_endpoint_id="webhook_endpoint_id",
            description="description",
            enabled_events=["user_profile.enforcement_action_opened"],
            name="name",
            state="disabled",
            url="x",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.webhooks.with_raw_response.update(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.webhooks.with_streaming_response.update(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(BetaOrganizationWebhookEndpoint, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_endpoint_id` but received ''"):
            await async_client.beta.organization.webhooks.with_raw_response.update(
                webhook_endpoint_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPage[BetaOrganizationWebhookEndpoint], webhook, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.list(
            after_id="after_id",
            before_id="before_id",
            limit=0,
            order="asc",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPage[BetaOrganizationWebhookEndpoint], webhook, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.webhooks.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(AsyncPage[BetaOrganizationWebhookEndpoint], webhook, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.webhooks.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(AsyncPage[BetaOrganizationWebhookEndpoint], webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.delete(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaDeletedOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.delete(
            webhook_endpoint_id="webhook_endpoint_id",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaDeletedOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.webhooks.with_raw_response.delete(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(BetaDeletedOrganizationWebhookEndpoint, webhook, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.webhooks.with_streaming_response.delete(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(BetaDeletedOrganizationWebhookEndpoint, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_endpoint_id` but received ''"):
            await async_client.beta.organization.webhooks.with_raw_response.delete(
                webhook_endpoint_id="",
            )

    @parametrize
    async def test_method_regenerate_signing_secret(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.regenerate_signing_secret(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpointSigningSecret, webhook, path=["response"])

    @parametrize
    async def test_method_regenerate_signing_secret_with_all_params(self, async_client: AsyncAnthropic) -> None:
        webhook = await async_client.beta.organization.webhooks.regenerate_signing_secret(
            webhook_endpoint_id="webhook_endpoint_id",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaOrganizationWebhookEndpointSigningSecret, webhook, path=["response"])

    @parametrize
    async def test_raw_response_regenerate_signing_secret(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.webhooks.with_raw_response.regenerate_signing_secret(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(BetaOrganizationWebhookEndpointSigningSecret, webhook, path=["response"])

    @parametrize
    async def test_streaming_response_regenerate_signing_secret(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.webhooks.with_streaming_response.regenerate_signing_secret(
            webhook_endpoint_id="webhook_endpoint_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(BetaOrganizationWebhookEndpointSigningSecret, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_regenerate_signing_secret(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_endpoint_id` but received ''"):
            await async_client.beta.organization.webhooks.with_raw_response.regenerate_signing_secret(
                webhook_endpoint_id="",
            )
