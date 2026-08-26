# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization.federation import (
    BetaFederationRule,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRules:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        rule = client.beta.organization.federation.rules.create(
            issuer_id="issuer_id",
            match={},
            name="x",
            oauth_scope="x",
            target={
                "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
                "type": "service_account",
            },
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        rule = client.beta.organization.federation.rules.create(
            issuer_id="issuer_id",
            match={
                "audience": "audience",
                "claims": {"foo": "string"},
                "condition": "condition",
                "subject_prefix": "subject_prefix",
            },
            name="x",
            oauth_scope="x",
            target={
                "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
                "type": "service_account",
                "service_account_name": "service_account_name",
            },
            applies_to_all_workspaces=True,
            attributes={"foo": "string"},
            description="description",
            token_lifetime_seconds=60,
            workspace_id="workspace_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.federation.rules.with_raw_response.create(
            issuer_id="issuer_id",
            match={},
            name="x",
            oauth_scope="x",
            target={
                "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
                "type": "service_account",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = response.parse()
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.federation.rules.with_streaming_response.create(
            issuer_id="issuer_id",
            match={},
            name="x",
            oauth_scope="x",
            target={
                "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
                "type": "service_account",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = response.parse()
            assert_matches_type(BetaFederationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        rule = client.beta.organization.federation.rules.retrieve(
            federation_rule_id="federation_rule_id",
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        rule = client.beta.organization.federation.rules.retrieve(
            federation_rule_id="federation_rule_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.federation.rules.with_raw_response.retrieve(
            federation_rule_id="federation_rule_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = response.parse()
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.federation.rules.with_streaming_response.retrieve(
            federation_rule_id="federation_rule_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = response.parse()
            assert_matches_type(BetaFederationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_rule_id` but received ''"):
            client.beta.organization.federation.rules.with_raw_response.retrieve(
                federation_rule_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        rule = client.beta.organization.federation.rules.update(
            federation_rule_id="federation_rule_id",
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        rule = client.beta.organization.federation.rules.update(
            federation_rule_id="federation_rule_id",
            applies_to_all_workspaces=True,
            attributes={"foo": "string"},
            description="description",
            match={
                "audience": "audience",
                "claims": {"foo": "string"},
                "condition": "condition",
                "subject_prefix": "subject_prefix",
            },
            name="x",
            oauth_scope="x",
            target={
                "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
                "type": "service_account",
                "service_account_name": "service_account_name",
            },
            token_lifetime_seconds=60,
            workspace_id="workspace_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.federation.rules.with_raw_response.update(
            federation_rule_id="federation_rule_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = response.parse()
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.federation.rules.with_streaming_response.update(
            federation_rule_id="federation_rule_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = response.parse()
            assert_matches_type(BetaFederationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_rule_id` but received ''"):
            client.beta.organization.federation.rules.with_raw_response.update(
                federation_rule_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        rule = client.beta.organization.federation.rules.list()
        assert_matches_type(SyncPageCursor[BetaFederationRule], rule, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        rule = client.beta.organization.federation.rules.list(
            include_archived=True,
            issuer_id="issuer_id",
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaFederationRule], rule, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.federation.rules.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = response.parse()
        assert_matches_type(SyncPageCursor[BetaFederationRule], rule, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.federation.rules.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = response.parse()
            assert_matches_type(SyncPageCursor[BetaFederationRule], rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        rule = client.beta.organization.federation.rules.archive(
            federation_rule_id="federation_rule_id",
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        rule = client.beta.organization.federation.rules.archive(
            federation_rule_id="federation_rule_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.organization.federation.rules.with_raw_response.archive(
            federation_rule_id="federation_rule_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = response.parse()
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.organization.federation.rules.with_streaming_response.archive(
            federation_rule_id="federation_rule_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = response.parse()
            assert_matches_type(BetaFederationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_rule_id` but received ''"):
            client.beta.organization.federation.rules.with_raw_response.archive(
                federation_rule_id="",
            )


class TestAsyncRules:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        rule = await async_client.beta.organization.federation.rules.create(
            issuer_id="issuer_id",
            match={},
            name="x",
            oauth_scope="x",
            target={
                "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
                "type": "service_account",
            },
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rule = await async_client.beta.organization.federation.rules.create(
            issuer_id="issuer_id",
            match={
                "audience": "audience",
                "claims": {"foo": "string"},
                "condition": "condition",
                "subject_prefix": "subject_prefix",
            },
            name="x",
            oauth_scope="x",
            target={
                "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
                "type": "service_account",
                "service_account_name": "service_account_name",
            },
            applies_to_all_workspaces=True,
            attributes={"foo": "string"},
            description="description",
            token_lifetime_seconds=60,
            workspace_id="workspace_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.federation.rules.with_raw_response.create(
            issuer_id="issuer_id",
            match={},
            name="x",
            oauth_scope="x",
            target={
                "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
                "type": "service_account",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = await response.parse()
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.federation.rules.with_streaming_response.create(
            issuer_id="issuer_id",
            match={},
            name="x",
            oauth_scope="x",
            target={
                "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
                "type": "service_account",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = await response.parse()
            assert_matches_type(BetaFederationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        rule = await async_client.beta.organization.federation.rules.retrieve(
            federation_rule_id="federation_rule_id",
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rule = await async_client.beta.organization.federation.rules.retrieve(
            federation_rule_id="federation_rule_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.federation.rules.with_raw_response.retrieve(
            federation_rule_id="federation_rule_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = await response.parse()
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.federation.rules.with_streaming_response.retrieve(
            federation_rule_id="federation_rule_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = await response.parse()
            assert_matches_type(BetaFederationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_rule_id` but received ''"):
            await async_client.beta.organization.federation.rules.with_raw_response.retrieve(
                federation_rule_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        rule = await async_client.beta.organization.federation.rules.update(
            federation_rule_id="federation_rule_id",
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rule = await async_client.beta.organization.federation.rules.update(
            federation_rule_id="federation_rule_id",
            applies_to_all_workspaces=True,
            attributes={"foo": "string"},
            description="description",
            match={
                "audience": "audience",
                "claims": {"foo": "string"},
                "condition": "condition",
                "subject_prefix": "subject_prefix",
            },
            name="x",
            oauth_scope="x",
            target={
                "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
                "type": "service_account",
                "service_account_name": "service_account_name",
            },
            token_lifetime_seconds=60,
            workspace_id="workspace_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.federation.rules.with_raw_response.update(
            federation_rule_id="federation_rule_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = await response.parse()
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.federation.rules.with_streaming_response.update(
            federation_rule_id="federation_rule_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = await response.parse()
            assert_matches_type(BetaFederationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_rule_id` but received ''"):
            await async_client.beta.organization.federation.rules.with_raw_response.update(
                federation_rule_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        rule = await async_client.beta.organization.federation.rules.list()
        assert_matches_type(AsyncPageCursor[BetaFederationRule], rule, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rule = await async_client.beta.organization.federation.rules.list(
            include_archived=True,
            issuer_id="issuer_id",
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaFederationRule], rule, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.federation.rules.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaFederationRule], rule, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.federation.rules.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaFederationRule], rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        rule = await async_client.beta.organization.federation.rules.archive(
            federation_rule_id="federation_rule_id",
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rule = await async_client.beta.organization.federation.rules.archive(
            federation_rule_id="federation_rule_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.federation.rules.with_raw_response.archive(
            federation_rule_id="federation_rule_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = await response.parse()
        assert_matches_type(BetaFederationRule, rule, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.federation.rules.with_streaming_response.archive(
            federation_rule_id="federation_rule_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = await response.parse()
            assert_matches_type(BetaFederationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_rule_id` but received ''"):
            await async_client.beta.organization.federation.rules.with_raw_response.archive(
                federation_rule_id="",
            )
