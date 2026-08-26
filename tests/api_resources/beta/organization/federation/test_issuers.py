# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization.federation import (
    BetaFederationIssuer,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestIssuers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        issuer = client.beta.organization.federation.issuers.create(
            issuer_url="x",
            name="x",
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        issuer = client.beta.organization.federation.issuers.create(
            issuer_url="x",
            name="x",
            check_jti=True,
            jwks={
                "type": "discovery",
                "ca_cert_pem": "ca_cert_pem",
                "discovery_base": "discovery_base",
            },
            max_jwt_lifetime_seconds=1,
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.federation.issuers.with_raw_response.create(
            issuer_url="x",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issuer = response.parse()
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.federation.issuers.with_streaming_response.create(
            issuer_url="x",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issuer = response.parse()
            assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        issuer = client.beta.organization.federation.issuers.retrieve(
            federation_issuer_id="federation_issuer_id",
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        issuer = client.beta.organization.federation.issuers.retrieve(
            federation_issuer_id="federation_issuer_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.federation.issuers.with_raw_response.retrieve(
            federation_issuer_id="federation_issuer_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issuer = response.parse()
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.federation.issuers.with_streaming_response.retrieve(
            federation_issuer_id="federation_issuer_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issuer = response.parse()
            assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_issuer_id` but received ''"):
            client.beta.organization.federation.issuers.with_raw_response.retrieve(
                federation_issuer_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        issuer = client.beta.organization.federation.issuers.update(
            federation_issuer_id="federation_issuer_id",
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        issuer = client.beta.organization.federation.issuers.update(
            federation_issuer_id="federation_issuer_id",
            check_jti=True,
            issuer_url="x",
            jwks={
                "type": "discovery",
                "ca_cert_pem": "ca_cert_pem",
                "discovery_base": "discovery_base",
            },
            jwks_polling_disabled=True,
            max_jwt_lifetime_seconds=1,
            name="x",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.federation.issuers.with_raw_response.update(
            federation_issuer_id="federation_issuer_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issuer = response.parse()
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.federation.issuers.with_streaming_response.update(
            federation_issuer_id="federation_issuer_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issuer = response.parse()
            assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_issuer_id` but received ''"):
            client.beta.organization.federation.issuers.with_raw_response.update(
                federation_issuer_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        issuer = client.beta.organization.federation.issuers.list()
        assert_matches_type(SyncPageCursor[BetaFederationIssuer], issuer, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        issuer = client.beta.organization.federation.issuers.list(
            include_archived=True,
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaFederationIssuer], issuer, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.federation.issuers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issuer = response.parse()
        assert_matches_type(SyncPageCursor[BetaFederationIssuer], issuer, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.federation.issuers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issuer = response.parse()
            assert_matches_type(SyncPageCursor[BetaFederationIssuer], issuer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        issuer = client.beta.organization.federation.issuers.archive(
            federation_issuer_id="federation_issuer_id",
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        issuer = client.beta.organization.federation.issuers.archive(
            federation_issuer_id="federation_issuer_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.organization.federation.issuers.with_raw_response.archive(
            federation_issuer_id="federation_issuer_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issuer = response.parse()
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.organization.federation.issuers.with_streaming_response.archive(
            federation_issuer_id="federation_issuer_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issuer = response.parse()
            assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_issuer_id` but received ''"):
            client.beta.organization.federation.issuers.with_raw_response.archive(
                federation_issuer_id="",
            )


class TestAsyncIssuers:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        issuer = await async_client.beta.organization.federation.issuers.create(
            issuer_url="x",
            name="x",
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        issuer = await async_client.beta.organization.federation.issuers.create(
            issuer_url="x",
            name="x",
            check_jti=True,
            jwks={
                "type": "discovery",
                "ca_cert_pem": "ca_cert_pem",
                "discovery_base": "discovery_base",
            },
            max_jwt_lifetime_seconds=1,
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.federation.issuers.with_raw_response.create(
            issuer_url="x",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issuer = await response.parse()
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.federation.issuers.with_streaming_response.create(
            issuer_url="x",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issuer = await response.parse()
            assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        issuer = await async_client.beta.organization.federation.issuers.retrieve(
            federation_issuer_id="federation_issuer_id",
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        issuer = await async_client.beta.organization.federation.issuers.retrieve(
            federation_issuer_id="federation_issuer_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.federation.issuers.with_raw_response.retrieve(
            federation_issuer_id="federation_issuer_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issuer = await response.parse()
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.federation.issuers.with_streaming_response.retrieve(
            federation_issuer_id="federation_issuer_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issuer = await response.parse()
            assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_issuer_id` but received ''"):
            await async_client.beta.organization.federation.issuers.with_raw_response.retrieve(
                federation_issuer_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        issuer = await async_client.beta.organization.federation.issuers.update(
            federation_issuer_id="federation_issuer_id",
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        issuer = await async_client.beta.organization.federation.issuers.update(
            federation_issuer_id="federation_issuer_id",
            check_jti=True,
            issuer_url="x",
            jwks={
                "type": "discovery",
                "ca_cert_pem": "ca_cert_pem",
                "discovery_base": "discovery_base",
            },
            jwks_polling_disabled=True,
            max_jwt_lifetime_seconds=1,
            name="x",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.federation.issuers.with_raw_response.update(
            federation_issuer_id="federation_issuer_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issuer = await response.parse()
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.federation.issuers.with_streaming_response.update(
            federation_issuer_id="federation_issuer_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issuer = await response.parse()
            assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_issuer_id` but received ''"):
            await async_client.beta.organization.federation.issuers.with_raw_response.update(
                federation_issuer_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        issuer = await async_client.beta.organization.federation.issuers.list()
        assert_matches_type(AsyncPageCursor[BetaFederationIssuer], issuer, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        issuer = await async_client.beta.organization.federation.issuers.list(
            include_archived=True,
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaFederationIssuer], issuer, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.federation.issuers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issuer = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaFederationIssuer], issuer, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.federation.issuers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issuer = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaFederationIssuer], issuer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        issuer = await async_client.beta.organization.federation.issuers.archive(
            federation_issuer_id="federation_issuer_id",
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        issuer = await async_client.beta.organization.federation.issuers.archive(
            federation_issuer_id="federation_issuer_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.federation.issuers.with_raw_response.archive(
            federation_issuer_id="federation_issuer_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issuer = await response.parse()
        assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.federation.issuers.with_streaming_response.archive(
            federation_issuer_id="federation_issuer_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issuer = await response.parse()
            assert_matches_type(BetaFederationIssuer, issuer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `federation_issuer_id` but received ''"):
            await async_client.beta.organization.federation.issuers.with_raw_response.archive(
                federation_issuer_id="",
            )
