from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization.claude_tag.bundles import (
    BetaClaudeTagBundleTarget,
    BetaClaudeTagDeletedBundleTarget,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTargets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        target = client.beta.organization.claude_tag.bundles.targets.create(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            target={
                "slack_channel_id": "xxxxxxxx",
                "type": "slack_channel",
            },
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        target = client.beta.organization.claude_tag.bundles.targets.create(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            target={
                "slack_channel_id": "xxxxxxxx",
                "type": "slack_channel",
            },
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.bundles.targets.with_raw_response.create(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            target={
                "slack_channel_id": "xxxxxxxx",
                "type": "slack_channel",
            },
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        target = response.parse()
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.bundles.targets.with_streaming_response.create(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            target={
                "slack_channel_id": "xxxxxxxx",
                "type": "slack_channel",
            },
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            target = response.parse()
            assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bundle_id` but received ''"):
            client.beta.organization.claude_tag.bundles.targets.with_raw_response.create(
                bundle_id="",
                target={
                    "slack_channel_id": "xxxxxxxx",
                    "type": "slack_channel",
                },
            )

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        target = client.beta.organization.claude_tag.bundles.targets.retrieve(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        target = client.beta.organization.claude_tag.bundles.targets.retrieve(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.bundles.targets.with_raw_response.retrieve(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        target = response.parse()
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.bundles.targets.with_streaming_response.retrieve(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            target = response.parse()
            assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bundle_id` but received ''"):
            client.beta.organization.claude_tag.bundles.targets.with_raw_response.retrieve(
                target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
                bundle_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `target_id` but received ''"):
            client.beta.organization.claude_tag.bundles.targets.with_raw_response.retrieve(
                target_id="",
                bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        target = client.beta.organization.claude_tag.bundles.targets.list(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaClaudeTagBundleTarget], target, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        target = client.beta.organization.claude_tag.bundles.targets.list(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaClaudeTagBundleTarget], target, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.bundles.targets.with_raw_response.list(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        target = response.parse()
        assert_matches_type(SyncPageCursor[BetaClaudeTagBundleTarget], target, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.bundles.targets.with_streaming_response.list(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            target = response.parse()
            assert_matches_type(SyncPageCursor[BetaClaudeTagBundleTarget], target, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bundle_id` but received ''"):
            client.beta.organization.claude_tag.bundles.targets.with_raw_response.list(
                bundle_id="",
            )

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        target = client.beta.organization.claude_tag.bundles.targets.delete(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagDeletedBundleTarget, target, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        target = client.beta.organization.claude_tag.bundles.targets.delete(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagDeletedBundleTarget, target, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.bundles.targets.with_raw_response.delete(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        target = response.parse()
        assert_matches_type(BetaClaudeTagDeletedBundleTarget, target, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.bundles.targets.with_streaming_response.delete(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            target = response.parse()
            assert_matches_type(BetaClaudeTagDeletedBundleTarget, target, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bundle_id` but received ''"):
            client.beta.organization.claude_tag.bundles.targets.with_raw_response.delete(
                target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
                bundle_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `target_id` but received ''"):
            client.beta.organization.claude_tag.bundles.targets.with_raw_response.delete(
                target_id="",
                bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            )


class TestAsyncTargets:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        target = await async_client.beta.organization.claude_tag.bundles.targets.create(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            target={
                "slack_channel_id": "xxxxxxxx",
                "type": "slack_channel",
            },
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        target = await async_client.beta.organization.claude_tag.bundles.targets.create(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            target={
                "slack_channel_id": "xxxxxxxx",
                "type": "slack_channel",
            },
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.bundles.targets.with_raw_response.create(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            target={
                "slack_channel_id": "xxxxxxxx",
                "type": "slack_channel",
            },
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        target = await response.parse()
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.bundles.targets.with_streaming_response.create(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            target={
                "slack_channel_id": "xxxxxxxx",
                "type": "slack_channel",
            },
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            target = await response.parse()
            assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bundle_id` but received ''"):
            await async_client.beta.organization.claude_tag.bundles.targets.with_raw_response.create(
                bundle_id="",
                target={
                    "slack_channel_id": "xxxxxxxx",
                    "type": "slack_channel",
                },
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        target = await async_client.beta.organization.claude_tag.bundles.targets.retrieve(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        target = await async_client.beta.organization.claude_tag.bundles.targets.retrieve(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.bundles.targets.with_raw_response.retrieve(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        target = await response.parse()
        assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.bundles.targets.with_streaming_response.retrieve(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            target = await response.parse()
            assert_matches_type(BetaClaudeTagBundleTarget, target, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bundle_id` but received ''"):
            await async_client.beta.organization.claude_tag.bundles.targets.with_raw_response.retrieve(
                target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
                bundle_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `target_id` but received ''"):
            await async_client.beta.organization.claude_tag.bundles.targets.with_raw_response.retrieve(
                target_id="",
                bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        target = await async_client.beta.organization.claude_tag.bundles.targets.list(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaClaudeTagBundleTarget], target, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        target = await async_client.beta.organization.claude_tag.bundles.targets.list(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaClaudeTagBundleTarget], target, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.bundles.targets.with_raw_response.list(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        target = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaClaudeTagBundleTarget], target, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.bundles.targets.with_streaming_response.list(
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            target = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaClaudeTagBundleTarget], target, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bundle_id` but received ''"):
            await async_client.beta.organization.claude_tag.bundles.targets.with_raw_response.list(
                bundle_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        target = await async_client.beta.organization.claude_tag.bundles.targets.delete(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagDeletedBundleTarget, target, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        target = await async_client.beta.organization.claude_tag.bundles.targets.delete(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagDeletedBundleTarget, target, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.bundles.targets.with_raw_response.delete(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        target = await response.parse()
        assert_matches_type(BetaClaudeTagDeletedBundleTarget, target, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.bundles.targets.with_streaming_response.delete(
            target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
            bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            target = await response.parse()
            assert_matches_type(BetaClaudeTagDeletedBundleTarget, target, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bundle_id` but received ''"):
            await async_client.beta.organization.claude_tag.bundles.targets.with_raw_response.delete(
                target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
                bundle_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `target_id` but received ''"):
            await async_client.beta.organization.claude_tag.bundles.targets.with_raw_response.delete(
                target_id="",
                bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
            )
