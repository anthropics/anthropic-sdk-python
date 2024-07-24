# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.types import Completion

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCompletions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_overload_1(self, client: Anthropic) -> None:
        completion = client.completions.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
        )
        assert_matches_type(Completion, completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: Anthropic) -> None:
        completion = client.completions.create(
            max_tokens_to_sample=256,
            model="string",
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
    def test_raw_response_create_overload_1(self, client: Anthropic) -> None:
        response = client.completions.with_raw_response.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        completion = response.parse()
        assert_matches_type(Completion, completion, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_1(self, client: Anthropic) -> None:
        with client.completions.with_streaming_response.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            completion = response.parse()
            assert_matches_type(Completion, completion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_overload_2(self, client: Anthropic) -> None:
        completion_stream = client.completions.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
        )
        completion_stream.response.close()

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: Anthropic) -> None:
        completion_stream = client.completions.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string", "string", "string"],
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        completion_stream.response.close()

    @parametrize
    def test_raw_response_create_overload_2(self, client: Anthropic) -> None:
        response = client.completions.with_raw_response.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_create_overload_2(self, client: Anthropic) -> None:
        with client.completions.with_streaming_response.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True


class TestAsyncCompletions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncAnthropic) -> None:
        completion = await async_client.completions.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
        )
        assert_matches_type(Completion, completion, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncAnthropic) -> None:
        completion = await async_client.completions.create(
            max_tokens_to_sample=256,
            model="string",
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
    async def test_raw_response_create_overload_1(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.completions.with_raw_response.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        completion = response.parse()
        assert_matches_type(Completion, completion, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncAnthropic) -> None:
        async with async_client.completions.with_streaming_response.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            completion = await response.parse()
            assert_matches_type(Completion, completion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncAnthropic) -> None:
        completion_stream = await async_client.completions.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
        )
        await completion_stream.response.aclose()

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncAnthropic) -> None:
        completion_stream = await async_client.completions.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string", "string", "string"],
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        await completion_stream.response.aclose()

    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.completions.with_raw_response.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncAnthropic) -> None:
        async with async_client.completions.with_streaming_response.create(
            max_tokens_to_sample=256,
            model="string",
            prompt="\n\nHuman: Hello, world!\n\nAssistant:",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True
