from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization.claude_tag import (
    BetaClaudeTagSlackWorkspace,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSlackWorkspaces:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        slack_workspace = client.beta.organization.claude_tag.slack_workspaces.retrieve(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        slack_workspace = client.beta.organization.claude_tag.slack_workspaces.retrieve(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            include_inherited=True,
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.slack_workspaces.with_raw_response.retrieve(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_workspace = response.parse()
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.slack_workspaces.with_streaming_response.retrieve(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_workspace = response.parse()
            assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.beta.organization.claude_tag.slack_workspaces.with_raw_response.retrieve(
                id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        slack_workspace = client.beta.organization.claude_tag.slack_workspaces.update(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            settings={},
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        slack_workspace = client.beta.organization.claude_tag.slack_workspaces.update(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
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
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.slack_workspaces.with_raw_response.update(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            settings={},
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_workspace = response.parse()
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.slack_workspaces.with_streaming_response.update(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            settings={},
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_workspace = response.parse()
            assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.beta.organization.claude_tag.slack_workspaces.with_raw_response.update(
                id="",
                settings={},
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        slack_workspace = client.beta.organization.claude_tag.slack_workspaces.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaClaudeTagSlackWorkspace], slack_workspace, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        slack_workspace = client.beta.organization.claude_tag.slack_workspaces.list(
            include_inherited=True,
            limit=0,
            page="page",
            slack_workspace_id="slack_workspace_id",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(SyncPageCursor[BetaClaudeTagSlackWorkspace], slack_workspace, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_tag.slack_workspaces.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_workspace = response.parse()
        assert_matches_type(SyncPageCursor[BetaClaudeTagSlackWorkspace], slack_workspace, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.claude_tag.slack_workspaces.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_workspace = response.parse()
            assert_matches_type(SyncPageCursor[BetaClaudeTagSlackWorkspace], slack_workspace, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSlackWorkspaces:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        slack_workspace = await async_client.beta.organization.claude_tag.slack_workspaces.retrieve(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        slack_workspace = await async_client.beta.organization.claude_tag.slack_workspaces.retrieve(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            include_inherited=True,
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.slack_workspaces.with_raw_response.retrieve(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_workspace = await response.parse()
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.slack_workspaces.with_streaming_response.retrieve(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_workspace = await response.parse()
            assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.beta.organization.claude_tag.slack_workspaces.with_raw_response.retrieve(
                id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        slack_workspace = await async_client.beta.organization.claude_tag.slack_workspaces.update(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            settings={},
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        slack_workspace = await async_client.beta.organization.claude_tag.slack_workspaces.update(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
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
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.slack_workspaces.with_raw_response.update(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            settings={},
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_workspace = await response.parse()
        assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.slack_workspaces.with_streaming_response.update(
            id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
            settings={},
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_workspace = await response.parse()
            assert_matches_type(BetaClaudeTagSlackWorkspace, slack_workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.beta.organization.claude_tag.slack_workspaces.with_raw_response.update(
                id="",
                settings={},
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        slack_workspace = await async_client.beta.organization.claude_tag.slack_workspaces.list(
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaClaudeTagSlackWorkspace], slack_workspace, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        slack_workspace = await async_client.beta.organization.claude_tag.slack_workspaces.list(
            include_inherited=True,
            limit=0,
            page="page",
            slack_workspace_id="slack_workspace_id",
            betas=["message-batches-2024-09-24"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(AsyncPageCursor[BetaClaudeTagSlackWorkspace], slack_workspace, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_tag.slack_workspaces.with_raw_response.list(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        slack_workspace = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaClaudeTagSlackWorkspace], slack_workspace, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.claude_tag.slack_workspaces.with_streaming_response.list(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            slack_workspace = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaClaudeTagSlackWorkspace], slack_workspace, path=["response"])

        assert cast(Any, response.is_closed) is True
