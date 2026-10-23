from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization.claude_tag import BetaClaudeTagBundle

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBundles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        bundle = client.beta.organization.claude_tag.bundles.retrieve(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundle, bundle, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        bundle = client.beta.organization.claude_tag.bundles.retrieve(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundle, bundle, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.bundles.with_raw_response.retrieve(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bundle = response.parse()
        assert_matches_type(BetaClaudeTagBundle, bundle, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.bundles.with_streaming_response.retrieve(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bundle = response.parse()
            assert_matches_type(BetaClaudeTagBundle, bundle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bundle_id` but received ''"):
            client.beta.organization.claude_tag.bundles.with_raw_response.retrieve(
                bundle_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        bundle = client.beta.organization.claude_tag.bundles.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaClaudeTagBundle], bundle, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        bundle = client.beta.organization.claude_tag.bundles.list(
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaClaudeTagBundle], bundle, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.bundles.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bundle = response.parse()
        assert_matches_type(SyncPageCursor[BetaClaudeTagBundle], bundle, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.bundles.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bundle = response.parse()
            assert_matches_type(SyncPageCursor[BetaClaudeTagBundle], bundle, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBundles:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        bundle = await async_client.beta.organization.claude_tag.bundles.retrieve(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundle, bundle, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        bundle = await async_client.beta.organization.claude_tag.bundles.retrieve(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundle, bundle, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.bundles.with_raw_response.retrieve(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bundle = await response.parse()
        assert_matches_type(BetaClaudeTagBundle, bundle, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.bundles.with_streaming_response.retrieve(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bundle = await response.parse()
            assert_matches_type(BetaClaudeTagBundle, bundle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bundle_id` but received ''"):
            await async_client.beta.organization.claude_tag.bundles.with_raw_response.retrieve(
                bundle_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        bundle = await async_client.beta.organization.claude_tag.bundles.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaClaudeTagBundle], bundle, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        bundle = await async_client.beta.organization.claude_tag.bundles.list(
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaClaudeTagBundle], bundle, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.bundles.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bundle = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaClaudeTagBundle], bundle, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.bundles.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bundle = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaClaudeTagBundle], bundle, path=["response"])

        assert cast(Any, response.is_closed) is True
