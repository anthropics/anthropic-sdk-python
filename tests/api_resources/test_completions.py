# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import os

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.types import Completion

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"


class TestCompletions:
    strict_client = Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)
    loose_client = Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=False)
    parametrize = pytest.mark.parametrize("client", [strict_client, loose_client], ids=["strict", "loose"])

    @parametrize
    def test_method_create_overload_1(self, client: Anthropic) -> None:
        completion = client.completions.create(
            max_tokens_to_sample=256,
            model="claude-2",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
        )
        assert_matches_type(Completion, completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: Anthropic) -> None:
        completion = client.completions.create(
            max_tokens_to_sample=256,
            model="claude-2",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string", "string", "string"],
            stream=False,
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        assert_matches_type(Completion, completion, path=["response"])

    @parametrize
    def test_method_create_overload_2(self, client: Anthropic) -> None:
        client.completions.create(
            max_tokens_to_sample=256,
            model="claude-2",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
        )

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: Anthropic) -> None:
        client.completions.create(
            max_tokens_to_sample=256,
            model="claude-2",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string", "string", "string"],
            temperature=1,
            top_k=5,
            top_p=0.7,
        )


class TestAsyncCompletions:
    strict_client = AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)
    loose_client = AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=False)
    parametrize = pytest.mark.parametrize("client", [strict_client, loose_client], ids=["strict", "loose"])

    @parametrize
    async def test_method_create_overload_1(self, client: AsyncAnthropic) -> None:
        completion = await client.completions.create(
            max_tokens_to_sample=256,
            model="claude-2",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
        )
        assert_matches_type(Completion, completion, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, client: AsyncAnthropic) -> None:
        completion = await client.completions.create(
            max_tokens_to_sample=256,
            model="claude-2",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string", "string", "string"],
            stream=False,
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        assert_matches_type(Completion, completion, path=["response"])

    @parametrize
    async def test_method_create_overload_2(self, client: AsyncAnthropic) -> None:
        await client.completions.create(
            max_tokens_to_sample=256,
            model="claude-2",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
        )

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, client: AsyncAnthropic) -> None:
        await client.completions.create(
            max_tokens_to_sample=256,
            model="claude-2",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string", "string", "string"],
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
