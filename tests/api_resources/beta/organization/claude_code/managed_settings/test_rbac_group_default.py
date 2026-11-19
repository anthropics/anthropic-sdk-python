from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.types.beta.organization.claude_code.managed_settings import (
    BetaClaudeCodeRBACGroupDefaultManagedSettings,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRBACGroupDefault:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        rbac_group_default = client.beta.organization.claude_code.managed_settings.rbac_group_default.retrieve(
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        rbac_group_default = client.beta.organization.claude_code.managed_settings.rbac_group_default.retrieve(
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_code.managed_settings.rbac_group_default.with_raw_response.retrieve(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group_default = response.parse()
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.claude_code.managed_settings.rbac_group_default.with_streaming_response.retrieve(
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group_default = response.parse()
            assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        rbac_group_default = client.beta.organization.claude_code.managed_settings.rbac_group_default.update(
            settings={"foo": "bar"},
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        rbac_group_default = client.beta.organization.claude_code.managed_settings.rbac_group_default.update(
            settings={"foo": "bar"},
            betas=["computer-use-2024-10-22"],
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.claude_code.managed_settings.rbac_group_default.with_raw_response.update(
            settings={"foo": "bar"},
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group_default = response.parse()
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.claude_code.managed_settings.rbac_group_default.with_streaming_response.update(
            settings={"foo": "bar"},
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group_default = response.parse()
            assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRBACGroupDefault:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        rbac_group_default = (
            await async_client.beta.organization.claude_code.managed_settings.rbac_group_default.retrieve(
                extra_query={"beta": "true"},
            )
        )
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rbac_group_default = (
            await async_client.beta.organization.claude_code.managed_settings.rbac_group_default.retrieve(
                betas=["computer-use-2024-10-22"],
                extra_query={"beta": "true"},
            )
        )
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_code.managed_settings.rbac_group_default.with_raw_response.retrieve(
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group_default = await response.parse()
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with (
            async_client.beta.organization.claude_code.managed_settings.rbac_group_default.with_streaming_response.retrieve(
                extra_query={"beta": "true"},
            ) as response
        ):
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group_default = await response.parse()
            assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        rbac_group_default = (
            await async_client.beta.organization.claude_code.managed_settings.rbac_group_default.update(
                settings={"foo": "bar"},
                extra_query={"beta": "true"},
            )
        )
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        rbac_group_default = (
            await async_client.beta.organization.claude_code.managed_settings.rbac_group_default.update(
                settings={"foo": "bar"},
                betas=["computer-use-2024-10-22"],
                extra_query={"beta": "true"},
            )
        )
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.claude_code.managed_settings.rbac_group_default.with_raw_response.update(
            settings={"foo": "bar"},
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rbac_group_default = await response.parse()
        assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with (
            async_client.beta.organization.claude_code.managed_settings.rbac_group_default.with_streaming_response.update(
                settings={"foo": "bar"},
                extra_query={"beta": "true"},
            ) as response
        ):
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rbac_group_default = await response.parse()
            assert_matches_type(BetaClaudeCodeRBACGroupDefaultManagedSettings, rbac_group_default, path=["response"])

        assert cast(Any, response.is_closed) is True
