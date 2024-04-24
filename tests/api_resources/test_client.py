# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os

import pytest

from anthropic import Anthropic, AsyncAnthropic

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTopLevel:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    def test_count_tokens(self, client: Anthropic) -> None:
        tokens = client.count_tokens("hello world!")
        assert tokens == 3


class TestAsyncTopLevel:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    async def test_count_tokens(self, async_client: AsyncAnthropic) -> None:
        tokens = await async_client.count_tokens("hello world!")
        assert tokens == 3
