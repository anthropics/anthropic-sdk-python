# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta import (
    BetaManagedAgentsAgent,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAgents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        agent = client.beta.agents.create(
            model="claude-sonnet-4-6",
            name="My First Agent",
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        agent = client.beta.agents.create(
            model="claude-sonnet-4-6",
            name="My First Agent",
            description="A general-purpose starter agent.",
            mcp_servers=[
                {
                    "name": "example-mcp",
                    "type": "url",
                    "url": "https://example-server.modelcontextprotocol.io/sse",
                }
            ],
            metadata={"foo": "bar"},
            multiagent={
                "agents": ["agent_011CZkYqphY8vELVzwCUpqiQ", {"type": "self"}],
                "type": "coordinator",
            },
            skills=[
                {
                    "skill_id": "xlsx",
                    "type": "anthropic",
                    "version": "1",
                }
            ],
            system="You are a general-purpose agent that can research, write code, run commands, and use connected tools to complete the user's task end to end.",
            tools=[
                {
                    "type": "agent_toolset_20260401",
                    "configs": [
                        {
                            "name": "bash",
                            "enabled": True,
                            "permission_policy": {"type": "always_allow"},
                        }
                    ],
                    "default_config": {
                        "enabled": True,
                        "permission_policy": {"type": "always_allow"},
                    },
                }
            ],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.agents.with_raw_response.create(
            model="claude-sonnet-4-6",
            name="My First Agent",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.agents.with_streaming_response.create(
            model="claude-sonnet-4-6",
            name="My First Agent",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        agent = client.beta.agents.retrieve(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        agent = client.beta.agents.retrieve(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            version=0,
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.agents.with_raw_response.retrieve(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.agents.with_streaming_response.retrieve(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.beta.agents.with_raw_response.retrieve(
                agent_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        agent = client.beta.agents.update(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            version=1,
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        agent = client.beta.agents.update(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            version=1,
            description="description",
            mcp_servers=[
                {
                    "name": "example-mcp",
                    "type": "url",
                    "url": "https://example-server.modelcontextprotocol.io/sse",
                }
            ],
            metadata={"foo": "string"},
            model={
                "id": "claude-opus-4-6",
                "speed": "standard",
            },
            multiagent={
                "agents": ["agent_011CZkYqphY8vELVzwCUpqiQ", {"type": "self"}],
                "type": "coordinator",
            },
            name="name",
            skills=[
                {
                    "skill_id": "xlsx",
                    "type": "anthropic",
                    "version": "1",
                }
            ],
            system="You are a general-purpose agent that can research, write code, run commands, and use connected tools to complete the user's task end to end.",
            tools=[
                {
                    "type": "agent_toolset_20260401",
                    "configs": [
                        {
                            "name": "bash",
                            "enabled": True,
                            "permission_policy": {"type": "always_allow"},
                        }
                    ],
                    "default_config": {
                        "enabled": True,
                        "permission_policy": {"type": "always_allow"},
                    },
                }
            ],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.agents.with_raw_response.update(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            version=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.agents.with_streaming_response.update(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            version=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.beta.agents.with_raw_response.update(
                agent_id="",
                version=1,
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        agent = client.beta.agents.list()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsAgent], agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        agent = client.beta.agents.list(
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsAgent], agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.agents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsAgent], agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.agents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsAgent], agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        agent = client.beta.agents.archive(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        agent = client.beta.agents.archive(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.agents.with_raw_response.archive(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.agents.with_streaming_response.archive(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.beta.agents.with_raw_response.archive(
                agent_id="",
            )


class TestAsyncAgents:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        agent = await async_client.beta.agents.create(
            model="claude-sonnet-4-6",
            name="My First Agent",
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        agent = await async_client.beta.agents.create(
            model="claude-sonnet-4-6",
            name="My First Agent",
            description="A general-purpose starter agent.",
            mcp_servers=[
                {
                    "name": "example-mcp",
                    "type": "url",
                    "url": "https://example-server.modelcontextprotocol.io/sse",
                }
            ],
            metadata={"foo": "bar"},
            multiagent={
                "agents": ["agent_011CZkYqphY8vELVzwCUpqiQ", {"type": "self"}],
                "type": "coordinator",
            },
            skills=[
                {
                    "skill_id": "xlsx",
                    "type": "anthropic",
                    "version": "1",
                }
            ],
            system="You are a general-purpose agent that can research, write code, run commands, and use connected tools to complete the user's task end to end.",
            tools=[
                {
                    "type": "agent_toolset_20260401",
                    "configs": [
                        {
                            "name": "bash",
                            "enabled": True,
                            "permission_policy": {"type": "always_allow"},
                        }
                    ],
                    "default_config": {
                        "enabled": True,
                        "permission_policy": {"type": "always_allow"},
                    },
                }
            ],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.agents.with_raw_response.create(
            model="claude-sonnet-4-6",
            name="My First Agent",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.agents.with_streaming_response.create(
            model="claude-sonnet-4-6",
            name="My First Agent",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        agent = await async_client.beta.agents.retrieve(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        agent = await async_client.beta.agents.retrieve(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            version=0,
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.agents.with_raw_response.retrieve(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.agents.with_streaming_response.retrieve(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.beta.agents.with_raw_response.retrieve(
                agent_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        agent = await async_client.beta.agents.update(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            version=1,
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        agent = await async_client.beta.agents.update(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            version=1,
            description="description",
            mcp_servers=[
                {
                    "name": "example-mcp",
                    "type": "url",
                    "url": "https://example-server.modelcontextprotocol.io/sse",
                }
            ],
            metadata={"foo": "string"},
            model={
                "id": "claude-opus-4-6",
                "speed": "standard",
            },
            multiagent={
                "agents": ["agent_011CZkYqphY8vELVzwCUpqiQ", {"type": "self"}],
                "type": "coordinator",
            },
            name="name",
            skills=[
                {
                    "skill_id": "xlsx",
                    "type": "anthropic",
                    "version": "1",
                }
            ],
            system="You are a general-purpose agent that can research, write code, run commands, and use connected tools to complete the user's task end to end.",
            tools=[
                {
                    "type": "agent_toolset_20260401",
                    "configs": [
                        {
                            "name": "bash",
                            "enabled": True,
                            "permission_policy": {"type": "always_allow"},
                        }
                    ],
                    "default_config": {
                        "enabled": True,
                        "permission_policy": {"type": "always_allow"},
                    },
                }
            ],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.agents.with_raw_response.update(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            version=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.agents.with_streaming_response.update(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            version=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.beta.agents.with_raw_response.update(
                agent_id="",
                version=1,
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        agent = await async_client.beta.agents.list()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsAgent], agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        agent = await async_client.beta.agents.list(
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsAgent], agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.agents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsAgent], agent, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.agents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsAgent], agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        agent = await async_client.beta.agents.archive(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        agent = await async_client.beta.agents.archive(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.agents.with_raw_response.archive(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.agents.with_streaming_response.archive(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(BetaManagedAgentsAgent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.beta.agents.with_raw_response.archive(
                agent_id="",
            )
