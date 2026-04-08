# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta import BetaManagedAgentsAgent

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        version = client.beta.agents.versions.list(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsAgent], version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        version = client.beta.agents.versions.list(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            limit=0,
            page="page",
            betas=["string"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsAgent], version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.agents.versions.with_raw_response.list(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsAgent], version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.agents.versions.with_streaming_response.list(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsAgent], version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.beta.agents.versions.with_raw_response.list(
                agent_id="",
            )


class TestAsyncVersions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.agents.versions.list(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsAgent], version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.agents.versions.list(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
            limit=0,
            page="page",
            betas=["string"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsAgent], version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.agents.versions.with_raw_response.list(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsAgent], version, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.agents.versions.with_streaming_response.list(
            agent_id="agent_011CZkYpogX7uDKUyvBTophP",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsAgent], version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.beta.agents.versions.with_raw_response.list(
                agent_id="",
            )
