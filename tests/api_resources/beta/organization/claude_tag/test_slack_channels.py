from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization.claude_tag import (
    BetaClaudeTagSlackChannel,
    BetaClaudeTagDeletedSlackChannel,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSlackChannels:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        slack_channel = client.beta.organization.claude_tag.slack_channels.create(
            slack={
                "channel_id": "xx",
                "workspace_id": "xx",
            },
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        slack_channel = client.beta.organization.claude_tag.slack_channels.create(
            slack={
                "channel_id": "xx",
                "workspace_id": "xx",
            },
            settings={
                "enabled": True,
                "environment_id": "x",
                "guest_policy": {"type": "allow"},
                "instructions": "instructions",
                "model": "x",
            },
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.slack_channels.with_raw_response.create(
            slack={
                "channel_id": "xx",
                "workspace_id": "xx",
            },
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_channel = response.parse()
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.slack_channels.with_streaming_response.create(
            slack={
                "channel_id": "xx",
                "workspace_id": "xx",
            },
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_channel = response.parse()
            assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        slack_channel = client.beta.organization.claude_tag.slack_channels.retrieve(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        slack_channel = client.beta.organization.claude_tag.slack_channels.retrieve(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            include_inherited=True,
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.slack_channels.with_raw_response.retrieve(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_channel = response.parse()
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.slack_channels.with_streaming_response.retrieve(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_channel = response.parse()
            assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.beta.organization.claude_tag.slack_channels.with_raw_response.retrieve(
                id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        slack_channel = client.beta.organization.claude_tag.slack_channels.update(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            settings={},
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        slack_channel = client.beta.organization.claude_tag.slack_channels.update(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            settings={
                "enabled": True,
                "environment_id": "x",
                "guest_policy": {"type": "allow"},
                "instructions": "instructions",
                "model": "x",
            },
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.slack_channels.with_raw_response.update(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            settings={},
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_channel = response.parse()
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.slack_channels.with_streaming_response.update(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            settings={},
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_channel = response.parse()
            assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.beta.organization.claude_tag.slack_channels.with_raw_response.update(
                id="",
                settings={},
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        slack_channel = client.beta.organization.claude_tag.slack_channels.list(
            slack_workspace_id="slack_workspace_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaClaudeTagSlackChannel], slack_channel, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        slack_channel = client.beta.organization.claude_tag.slack_channels.list(
            slack_workspace_id="slack_workspace_id",
            include_inherited=True,
            limit=0,
            page="page",
            slack_channel_id="slack_channel_id",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaClaudeTagSlackChannel], slack_channel, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.slack_channels.with_raw_response.list(
            slack_workspace_id="slack_workspace_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_channel = response.parse()
        assert_matches_type(SyncPageCursor[BetaClaudeTagSlackChannel], slack_channel, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.slack_channels.with_streaming_response.list(
            slack_workspace_id="slack_workspace_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_channel = response.parse()
            assert_matches_type(SyncPageCursor[BetaClaudeTagSlackChannel], slack_channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        slack_channel = client.beta.organization.claude_tag.slack_channels.delete(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagDeletedSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        slack_channel = client.beta.organization.claude_tag.slack_channels.delete(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagDeletedSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.slack_channels.with_raw_response.delete(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_channel = response.parse()
        assert_matches_type(BetaClaudeTagDeletedSlackChannel, slack_channel, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.slack_channels.with_streaming_response.delete(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_channel = response.parse()
            assert_matches_type(BetaClaudeTagDeletedSlackChannel, slack_channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.beta.organization.claude_tag.slack_channels.with_raw_response.delete(
                id="",
            )


class TestAsyncSlackChannels:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        slack_channel = await async_client.beta.organization.claude_tag.slack_channels.create(
            slack={
                "channel_id": "xx",
                "workspace_id": "xx",
            },
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        slack_channel = await async_client.beta.organization.claude_tag.slack_channels.create(
            slack={
                "channel_id": "xx",
                "workspace_id": "xx",
            },
            settings={
                "enabled": True,
                "environment_id": "x",
                "guest_policy": {"type": "allow"},
                "instructions": "instructions",
                "model": "x",
            },
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.slack_channels.with_raw_response.create(
            slack={
                "channel_id": "xx",
                "workspace_id": "xx",
            },
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_channel = await response.parse()
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.slack_channels.with_streaming_response.create(
            slack={
                "channel_id": "xx",
                "workspace_id": "xx",
            },
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_channel = await response.parse()
            assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        slack_channel = await async_client.beta.organization.claude_tag.slack_channels.retrieve(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        slack_channel = await async_client.beta.organization.claude_tag.slack_channels.retrieve(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            include_inherited=True,
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.slack_channels.with_raw_response.retrieve(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_channel = await response.parse()
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.slack_channels.with_streaming_response.retrieve(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_channel = await response.parse()
            assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.beta.organization.claude_tag.slack_channels.with_raw_response.retrieve(
                id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        slack_channel = await async_client.beta.organization.claude_tag.slack_channels.update(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            settings={},
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        slack_channel = await async_client.beta.organization.claude_tag.slack_channels.update(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            settings={
                "enabled": True,
                "environment_id": "x",
                "guest_policy": {"type": "allow"},
                "instructions": "instructions",
                "model": "x",
            },
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.slack_channels.with_raw_response.update(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            settings={},
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_channel = await response.parse()
        assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.slack_channels.with_streaming_response.update(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            settings={},
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_channel = await response.parse()
            assert_matches_type(BetaClaudeTagSlackChannel, slack_channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.beta.organization.claude_tag.slack_channels.with_raw_response.update(
                id="",
                settings={},
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        slack_channel = await async_client.beta.organization.claude_tag.slack_channels.list(
            slack_workspace_id="slack_workspace_id",
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaClaudeTagSlackChannel], slack_channel, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        slack_channel = await async_client.beta.organization.claude_tag.slack_channels.list(
            slack_workspace_id="slack_workspace_id",
            include_inherited=True,
            limit=0,
            page="page",
            slack_channel_id="slack_channel_id",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaClaudeTagSlackChannel], slack_channel, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.slack_channels.with_raw_response.list(
            slack_workspace_id="slack_workspace_id",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_channel = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaClaudeTagSlackChannel], slack_channel, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.slack_channels.with_streaming_response.list(
            slack_workspace_id="slack_workspace_id",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_channel = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaClaudeTagSlackChannel], slack_channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        slack_channel = await async_client.beta.organization.claude_tag.slack_channels.delete(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagDeletedSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        slack_channel = await async_client.beta.organization.claude_tag.slack_channels.delete(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagDeletedSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.slack_channels.with_raw_response.delete(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_channel = await response.parse()
        assert_matches_type(BetaClaudeTagDeletedSlackChannel, slack_channel, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.slack_channels.with_streaming_response.delete(
            id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_channel = await response.parse()
            assert_matches_type(BetaClaudeTagDeletedSlackChannel, slack_channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.beta.organization.claude_tag.slack_channels.with_raw_response.delete(
                id="",
            )
