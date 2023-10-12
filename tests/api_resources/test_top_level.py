# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import os

import pytest

from anthropic import Anthropic, AsyncAnthropic

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"


class TestTopLevel:
    strict_client = Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)
    loose_client = Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=False)
    parametrize = pytest.mark.parametrize("client", [strict_client, loose_client], ids=["strict", "loose"])

    def test_count_tokens(self) -> None:
        tokens = self.strict_client.count_tokens("hello world!")
        assert tokens == 3


class TestAsyncTopLevel:
    strict_client = AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)
    loose_client = AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=False)
    parametrize = pytest.mark.parametrize("client", [strict_client, loose_client], ids=["strict", "loose"])

    async def test_count_tokens(self) -> None:
        tokens = await self.strict_client.count_tokens("hello world!")
        assert tokens == 3
