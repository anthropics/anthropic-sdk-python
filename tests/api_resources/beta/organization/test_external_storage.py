from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import (
    BetaExternalStorage,
    BetaDeletedExternalStorage,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExternalStorage:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.create(
            provider_config={
                "account_id": "111122223333",
                "bucket_name": "acme-safety-retention",
                "region": "us-east-2",
                "type": "aws",
            },
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.create(
            provider_config={
                "account_id": "111122223333",
                "bucket_name": "acme-safety-retention",
                "region": "us-east-2",
                "type": "aws",
            },
            display_name="x",
            user_profile_id="uprof_01SDCCSbTxrXDpWc1phhtcfK",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.external_storage.with_raw_response.create(
            provider_config={
                "account_id": "111122223333",
                "bucket_name": "acme-safety-retention",
                "region": "us-east-2",
                "type": "aws",
            },
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = response.parse()
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.external_storage.with_streaming_response.create(
            provider_config={
                "account_id": "111122223333",
                "bucket_name": "acme-safety-retention",
                "region": "us-east-2",
                "type": "aws",
            },
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = response.parse()
            assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.retrieve(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.retrieve(
            external_storage_id="external_storage_id",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.external_storage.with_raw_response.retrieve(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = response.parse()
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.external_storage.with_streaming_response.retrieve(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = response.parse()
            assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_storage_id` but received ''"):
            client.beta.organization.external_storage.with_raw_response.retrieve(
                external_storage_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.update(
            external_storage_id="external_storage_id",
            display_name="x",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.update(
            external_storage_id="external_storage_id",
            display_name="x",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.external_storage.with_raw_response.update(
            external_storage_id="external_storage_id",
            display_name="x",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = response.parse()
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.external_storage.with_streaming_response.update(
            external_storage_id="external_storage_id",
            display_name="x",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = response.parse()
            assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_storage_id` but received ''"):
            client.beta.organization.external_storage.with_raw_response.update(
                external_storage_id="",
                display_name="x",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaExternalStorage], external_storage, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.list(
            limit=1,
            page="page",
            user_profile_ids=["string"],
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaExternalStorage], external_storage, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.external_storage.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = response.parse()
        assert_matches_type(SyncPageCursor[BetaExternalStorage], external_storage, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.external_storage.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = response.parse()
            assert_matches_type(SyncPageCursor[BetaExternalStorage], external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.delete(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaDeletedExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.delete(
            external_storage_id="external_storage_id",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaDeletedExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.organization.external_storage.with_raw_response.delete(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = response.parse()
        assert_matches_type(BetaDeletedExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.organization.external_storage.with_streaming_response.delete(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = response.parse()
            assert_matches_type(BetaDeletedExternalStorage, external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_storage_id` but received ''"):
            client.beta.organization.external_storage.with_raw_response.delete(
                external_storage_id="",
            )

    @parametrize
    def test_method_activate(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.activate(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_method_activate_with_all_params(self, client: Anthropic) -> None:
        external_storage = client.beta.organization.external_storage.activate(
            external_storage_id="external_storage_id",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_raw_response_activate(self, client: Anthropic) -> None:
        response = client.beta.organization.external_storage.with_raw_response.activate(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = response.parse()
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    def test_streaming_response_activate(self, client: Anthropic) -> None:
        with client.beta.organization.external_storage.with_streaming_response.activate(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = response.parse()
            assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_activate(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_storage_id` but received ''"):
            client.beta.organization.external_storage.with_raw_response.activate(
                external_storage_id="",
            )


class TestAsyncExternalStorage:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.create(
            provider_config={
                "account_id": "111122223333",
                "bucket_name": "acme-safety-retention",
                "region": "us-east-2",
                "type": "aws",
            },
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.create(
            provider_config={
                "account_id": "111122223333",
                "bucket_name": "acme-safety-retention",
                "region": "us-east-2",
                "type": "aws",
            },
            display_name="x",
            user_profile_id="uprof_01SDCCSbTxrXDpWc1phhtcfK",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_storage.with_raw_response.create(
            provider_config={
                "account_id": "111122223333",
                "bucket_name": "acme-safety-retention",
                "region": "us-east-2",
                "type": "aws",
            },
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = await response.parse()
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_storage.with_streaming_response.create(
            provider_config={
                "account_id": "111122223333",
                "bucket_name": "acme-safety-retention",
                "region": "us-east-2",
                "type": "aws",
            },
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = await response.parse()
            assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.retrieve(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.retrieve(
            external_storage_id="external_storage_id",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_storage.with_raw_response.retrieve(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = await response.parse()
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_storage.with_streaming_response.retrieve(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = await response.parse()
            assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_storage_id` but received ''"):
            await async_client.beta.organization.external_storage.with_raw_response.retrieve(
                external_storage_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.update(
            external_storage_id="external_storage_id",
            display_name="x",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.update(
            external_storage_id="external_storage_id",
            display_name="x",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_storage.with_raw_response.update(
            external_storage_id="external_storage_id",
            display_name="x",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = await response.parse()
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_storage.with_streaming_response.update(
            external_storage_id="external_storage_id",
            display_name="x",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = await response.parse()
            assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_storage_id` but received ''"):
            await async_client.beta.organization.external_storage.with_raw_response.update(
                external_storage_id="",
                display_name="x",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaExternalStorage], external_storage, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.list(
            limit=1,
            page="page",
            user_profile_ids=["string"],
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaExternalStorage], external_storage, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_storage.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaExternalStorage], external_storage, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_storage.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaExternalStorage], external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.delete(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaDeletedExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.delete(
            external_storage_id="external_storage_id",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaDeletedExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_storage.with_raw_response.delete(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = await response.parse()
        assert_matches_type(BetaDeletedExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_storage.with_streaming_response.delete(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = await response.parse()
            assert_matches_type(BetaDeletedExternalStorage, external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_storage_id` but received ''"):
            await async_client.beta.organization.external_storage.with_raw_response.delete(
                external_storage_id="",
            )

    @parametrize
    async def test_method_activate(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.activate(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_method_activate_with_all_params(self, async_client: AsyncAnthropic) -> None:
        external_storage = await async_client.beta.organization.external_storage.activate(
            external_storage_id="external_storage_id",
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_raw_response_activate(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.external_storage.with_raw_response.activate(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_storage = await response.parse()
        assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

    @parametrize
    async def test_streaming_response_activate(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.external_storage.with_streaming_response.activate(
            external_storage_id="external_storage_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_storage = await response.parse()
            assert_matches_type(BetaExternalStorage, external_storage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_activate(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `external_storage_id` but received ''"):
            await async_client.beta.organization.external_storage.with_raw_response.activate(
                external_storage_id="",
            )
