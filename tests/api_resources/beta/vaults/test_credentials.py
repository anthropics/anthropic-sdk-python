# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.vaults import (
    BetaManagedAgentsCredential,
    BetaManagedAgentsDeletedCredential,
    BetaManagedAgentsCredentialValidation,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCredentials:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.create(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            auth={
                "token": "bearer_exampletoken",
                "mcp_server_url": "https://example-server.modelcontextprotocol.io/sse",
                "type": "static_bearer",
            },
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.create(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            auth={
                "token": "bearer_exampletoken",
                "mcp_server_url": "https://example-server.modelcontextprotocol.io/sse",
                "type": "static_bearer",
            },
            display_name="Example credential",
            metadata={"environment": "production"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.vaults.credentials.with_raw_response.create(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            auth={
                "token": "bearer_exampletoken",
                "mcp_server_url": "https://example-server.modelcontextprotocol.io/sse",
                "type": "static_bearer",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.vaults.credentials.with_streaming_response.create(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            auth={
                "token": "bearer_exampletoken",
                "mcp_server_url": "https://example-server.modelcontextprotocol.io/sse",
                "type": "static_bearer",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.create(
                vault_id="",
                auth={
                    "token": "bearer_exampletoken",
                    "mcp_server_url": "https://example-server.modelcontextprotocol.io/sse",
                    "type": "static_bearer",
                },
            )

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.retrieve(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.retrieve(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.vaults.credentials.with_raw_response.retrieve(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.vaults.credentials.with_streaming_response.retrieve(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.retrieve(
                credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
                vault_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.retrieve(
                credential_id="",
                vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.update(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.update(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            auth={
                "type": "mcp_oauth",
                "access_token": "x",
                "expires_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                "refresh": {
                    "refresh_token": "x",
                    "scope": "scope",
                    "token_endpoint_auth": {
                        "type": "client_secret_basic",
                        "client_secret": "x",
                    },
                },
            },
            display_name="Example credential",
            metadata={"environment": "production"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.vaults.credentials.with_raw_response.update(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.vaults.credentials.with_streaming_response.update(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.update(
                credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
                vault_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.update(
                credential_id="",
                vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.list(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsCredential], credential, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.list(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsCredential], credential, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.vaults.credentials.with_raw_response.list(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsCredential], credential, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.vaults.credentials.with_streaming_response.list(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsCredential], credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.list(
                vault_id="",
            )

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.delete(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsDeletedCredential, credential, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.delete(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeletedCredential, credential, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.vaults.credentials.with_raw_response.delete(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsDeletedCredential, credential, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.vaults.credentials.with_streaming_response.delete(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(BetaManagedAgentsDeletedCredential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.delete(
                credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
                vault_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.delete(
                credential_id="",
                vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            )

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.archive(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.archive(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.vaults.credentials.with_raw_response.archive(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.vaults.credentials.with_streaming_response.archive(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.archive(
                credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
                vault_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.archive(
                credential_id="",
                vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            )

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_mcp_oauth_validate(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.mcp_oauth_validate(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsCredentialValidation, credential, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_mcp_oauth_validate_with_all_params(self, client: Anthropic) -> None:
        credential = client.beta.vaults.credentials.mcp_oauth_validate(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsCredentialValidation, credential, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_raw_response_mcp_oauth_validate(self, client: Anthropic) -> None:
        response = client.beta.vaults.credentials.with_raw_response.mcp_oauth_validate(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsCredentialValidation, credential, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_streaming_response_mcp_oauth_validate(self, client: Anthropic) -> None:
        with client.beta.vaults.credentials.with_streaming_response.mcp_oauth_validate(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(BetaManagedAgentsCredentialValidation, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_path_params_mcp_oauth_validate(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.mcp_oauth_validate(
                credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
                vault_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            client.beta.vaults.credentials.with_raw_response.mcp_oauth_validate(
                credential_id="",
                vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            )


class TestAsyncCredentials:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.create(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            auth={
                "token": "bearer_exampletoken",
                "mcp_server_url": "https://example-server.modelcontextprotocol.io/sse",
                "type": "static_bearer",
            },
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.create(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            auth={
                "token": "bearer_exampletoken",
                "mcp_server_url": "https://example-server.modelcontextprotocol.io/sse",
                "type": "static_bearer",
            },
            display_name="Example credential",
            metadata={"environment": "production"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.credentials.with_raw_response.create(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            auth={
                "token": "bearer_exampletoken",
                "mcp_server_url": "https://example-server.modelcontextprotocol.io/sse",
                "type": "static_bearer",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.credentials.with_streaming_response.create(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            auth={
                "token": "bearer_exampletoken",
                "mcp_server_url": "https://example-server.modelcontextprotocol.io/sse",
                "type": "static_bearer",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.create(
                vault_id="",
                auth={
                    "token": "bearer_exampletoken",
                    "mcp_server_url": "https://example-server.modelcontextprotocol.io/sse",
                    "type": "static_bearer",
                },
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.retrieve(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.retrieve(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.credentials.with_raw_response.retrieve(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.credentials.with_streaming_response.retrieve(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.retrieve(
                credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
                vault_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.retrieve(
                credential_id="",
                vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.update(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.update(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            auth={
                "type": "mcp_oauth",
                "access_token": "x",
                "expires_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                "refresh": {
                    "refresh_token": "x",
                    "scope": "scope",
                    "token_endpoint_auth": {
                        "type": "client_secret_basic",
                        "client_secret": "x",
                    },
                },
            },
            display_name="Example credential",
            metadata={"environment": "production"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.credentials.with_raw_response.update(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.credentials.with_streaming_response.update(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.update(
                credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
                vault_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.update(
                credential_id="",
                vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.list(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsCredential], credential, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.list(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsCredential], credential, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.credentials.with_raw_response.list(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsCredential], credential, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.credentials.with_streaming_response.list(
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsCredential], credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.list(
                vault_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.delete(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsDeletedCredential, credential, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.delete(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeletedCredential, credential, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.credentials.with_raw_response.delete(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsDeletedCredential, credential, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.credentials.with_streaming_response.delete(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(BetaManagedAgentsDeletedCredential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.delete(
                credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
                vault_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.delete(
                credential_id="",
                vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            )

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.archive(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.archive(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.credentials.with_raw_response.archive(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.credentials.with_streaming_response.archive(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(BetaManagedAgentsCredential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.archive(
                credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
                vault_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.archive(
                credential_id="",
                vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            )

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_mcp_oauth_validate(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.mcp_oauth_validate(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )
        assert_matches_type(BetaManagedAgentsCredentialValidation, credential, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_mcp_oauth_validate_with_all_params(self, async_client: AsyncAnthropic) -> None:
        credential = await async_client.beta.vaults.credentials.mcp_oauth_validate(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsCredentialValidation, credential, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_raw_response_mcp_oauth_validate(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.vaults.credentials.with_raw_response.mcp_oauth_validate(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(BetaManagedAgentsCredentialValidation, credential, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_streaming_response_mcp_oauth_validate(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.vaults.credentials.with_streaming_response.mcp_oauth_validate(
            credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
            vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(BetaManagedAgentsCredentialValidation, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_path_params_mcp_oauth_validate(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.mcp_oauth_validate(
                credential_id="vcrd_011CZkZEMt8gZan2iYOQfSkw",
                vault_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            await async_client.beta.vaults.credentials.with_raw_response.mcp_oauth_validate(
                credential_id="",
                vault_id="vlt_011CZkZDLs7fYzm1hXNPeRjv",
            )
