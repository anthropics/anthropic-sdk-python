# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import (
    BetaExternalKey,
    ExternalKeyDeleteResponse,
    ExternalKeyValidateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExternalKeys:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        external_key = client.beta.organization.external_keys.create(
            provider_config={
                "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
                "type": "aws",
            },
        )
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        external_key = client.beta.organization.external_keys.create(
            provider_config={
                "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
                "type": "aws",
                "region": "us-east-1",
                "role_arn": "arn:aws:iam::111122223333:role/anthropic-cmek",
            },
            display_name="x",
            geo="us",
        )
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.external_keys.with_raw_response.create(
            provider_config={
                "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
                "type": "aws",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = response.parse()
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.external_keys.with_streaming_response.create(
            provider_config={
                "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
                "type": "aws",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = response.parse()
            assert_matches_type(BetaExternalKey, external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        external_key = client.beta.organization.external_keys.retrieve(
            "external_key_id",
        )
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.external_keys.with_raw_response.retrieve(
            "external_key_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = response.parse()
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.external_keys.with_streaming_response.retrieve(
            "external_key_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = response.parse()
            assert_matches_type(BetaExternalKey, external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_key_id` but received ''"):
            client.beta.organization.external_keys.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        external_key = client.beta.organization.external_keys.update(
            external_key_id="external_key_id",
        )
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        external_key = client.beta.organization.external_keys.update(
            external_key_id="external_key_id",
            display_name="x",
            geo="us",
            provider_config={
                "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
                "type": "aws",
                "region": "us-east-1",
                "role_arn": "arn:aws:iam::111122223333:role/anthropic-cmek",
            },
        )
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.external_keys.with_raw_response.update(
            external_key_id="external_key_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = response.parse()
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.external_keys.with_streaming_response.update(
            external_key_id="external_key_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = response.parse()
            assert_matches_type(BetaExternalKey, external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_key_id` but received ''"):
            client.beta.organization.external_keys.with_raw_response.update(
                external_key_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        external_key = client.beta.organization.external_keys.list()
        assert_matches_type(SyncPageCursor[BetaExternalKey], external_key, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        external_key = client.beta.organization.external_keys.list(
            limit=1,
            page="page",
        )
        assert_matches_type(SyncPageCursor[BetaExternalKey], external_key, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.external_keys.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = response.parse()
        assert_matches_type(SyncPageCursor[BetaExternalKey], external_key, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.external_keys.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = response.parse()
            assert_matches_type(SyncPageCursor[BetaExternalKey], external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        external_key = client.beta.organization.external_keys.delete(
            "external_key_id",
        )
        assert_matches_type(ExternalKeyDeleteResponse, external_key, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.organization.external_keys.with_raw_response.delete(
            "external_key_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = response.parse()
        assert_matches_type(ExternalKeyDeleteResponse, external_key, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.organization.external_keys.with_streaming_response.delete(
            "external_key_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = response.parse()
            assert_matches_type(ExternalKeyDeleteResponse, external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_key_id` but received ''"):
            client.beta.organization.external_keys.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_validate(self, client: Anthropic) -> None:
        external_key = client.beta.organization.external_keys.validate(
            "external_key_id",
        )
        assert_matches_type(ExternalKeyValidateResponse, external_key, path=["response"])

    @parametrize
    def test_raw_response_validate(self, client: Anthropic) -> None:
        response = client.beta.organization.external_keys.with_raw_response.validate(
            "external_key_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = response.parse()
        assert_matches_type(ExternalKeyValidateResponse, external_key, path=["response"])

    @parametrize
    def test_streaming_response_validate(self, client: Anthropic) -> None:
        with client.beta.organization.external_keys.with_streaming_response.validate(
            "external_key_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = response.parse()
            assert_matches_type(ExternalKeyValidateResponse, external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_validate(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_key_id` but received ''"):
            client.beta.organization.external_keys.with_raw_response.validate(
                "",
            )


class TestAsyncExternalKeys:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        external_key = await async_client.beta.organization.external_keys.create(
            provider_config={
                "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
                "type": "aws",
            },
        )
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        external_key = await async_client.beta.organization.external_keys.create(
            provider_config={
                "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
                "type": "aws",
                "region": "us-east-1",
                "role_arn": "arn:aws:iam::111122223333:role/anthropic-cmek",
            },
            display_name="x",
            geo="us",
        )
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_keys.with_raw_response.create(
            provider_config={
                "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
                "type": "aws",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = await response.parse()
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_keys.with_streaming_response.create(
            provider_config={
                "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
                "type": "aws",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = await response.parse()
            assert_matches_type(BetaExternalKey, external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        external_key = await async_client.beta.organization.external_keys.retrieve(
            "external_key_id",
        )
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_keys.with_raw_response.retrieve(
            "external_key_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = await response.parse()
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_keys.with_streaming_response.retrieve(
            "external_key_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = await response.parse()
            assert_matches_type(BetaExternalKey, external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_key_id` but received ''"):
            await async_client.beta.organization.external_keys.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        external_key = await async_client.beta.organization.external_keys.update(
            external_key_id="external_key_id",
        )
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        external_key = await async_client.beta.organization.external_keys.update(
            external_key_id="external_key_id",
            display_name="x",
            geo="us",
            provider_config={
                "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
                "type": "aws",
                "region": "us-east-1",
                "role_arn": "arn:aws:iam::111122223333:role/anthropic-cmek",
            },
        )
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_keys.with_raw_response.update(
            external_key_id="external_key_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = await response.parse()
        assert_matches_type(BetaExternalKey, external_key, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_keys.with_streaming_response.update(
            external_key_id="external_key_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = await response.parse()
            assert_matches_type(BetaExternalKey, external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_key_id` but received ''"):
            await async_client.beta.organization.external_keys.with_raw_response.update(
                external_key_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        external_key = await async_client.beta.organization.external_keys.list()
        assert_matches_type(AsyncPageCursor[BetaExternalKey], external_key, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        external_key = await async_client.beta.organization.external_keys.list(
            limit=1,
            page="page",
        )
        assert_matches_type(AsyncPageCursor[BetaExternalKey], external_key, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_keys.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaExternalKey], external_key, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_keys.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaExternalKey], external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        external_key = await async_client.beta.organization.external_keys.delete(
            "external_key_id",
        )
        assert_matches_type(ExternalKeyDeleteResponse, external_key, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_keys.with_raw_response.delete(
            "external_key_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = await response.parse()
        assert_matches_type(ExternalKeyDeleteResponse, external_key, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_keys.with_streaming_response.delete(
            "external_key_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = await response.parse()
            assert_matches_type(ExternalKeyDeleteResponse, external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_key_id` but received ''"):
            await async_client.beta.organization.external_keys.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_validate(self, async_client: AsyncAnthropic) -> None:
        external_key = await async_client.beta.organization.external_keys.validate(
            "external_key_id",
        )
        assert_matches_type(ExternalKeyValidateResponse, external_key, path=["response"])

    @parametrize
    async def test_raw_response_validate(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_keys.with_raw_response.validate(
            "external_key_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_key = await response.parse()
        assert_matches_type(ExternalKeyValidateResponse, external_key, path=["response"])

    @parametrize
    async def test_streaming_response_validate(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_keys.with_streaming_response.validate(
            "external_key_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_key = await response.parse()
            assert_matches_type(ExternalKeyValidateResponse, external_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_validate(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_key_id` but received ''"):
            await async_client.beta.organization.external_keys.with_raw_response.validate(
                "",
            )
