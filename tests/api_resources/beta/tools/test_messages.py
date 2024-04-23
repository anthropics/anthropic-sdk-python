# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.types.beta.tools.tools_beta_message import ToolsBetaMessage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMessages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_overload_1(self, client: Anthropic) -> None:
        message = client.beta.tools.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
        )
        assert_matches_type(ToolsBetaMessage, message, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: Anthropic) -> None:
        message = client.beta.tools.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string", "string", "string"],
            stream=False,
            system="Today's date is 2024-01-01.",
            temperature=1,
            tools=[
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
            ],
            top_k=5,
            top_p=0.7,
        )
        assert_matches_type(ToolsBetaMessage, message, path=["response"])

    @parametrize
    def test_raw_response_create_overload_1(self, client: Anthropic) -> None:
        response = client.beta.tools.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(ToolsBetaMessage, message, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_1(self, client: Anthropic) -> None:
        with client.beta.tools.messages.with_streaming_response.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = response.parse()
            assert_matches_type(ToolsBetaMessage, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_overload_2(self, client: Anthropic) -> None:
        message_stream = client.beta.tools.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
            stream=True,
        )
        message_stream.response.close()

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: Anthropic) -> None:
        message_stream = client.beta.tools.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
            stream=True,
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string", "string", "string"],
            system="Today's date is 2024-01-01.",
            temperature=1,
            tools=[
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
            ],
            top_k=5,
            top_p=0.7,
        )
        message_stream.response.close()

    @parametrize
    def test_raw_response_create_overload_2(self, client: Anthropic) -> None:
        response = client.beta.tools.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_create_overload_2(self, client: Anthropic) -> None:
        with client.beta.tools.messages.with_streaming_response.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True


class TestAsyncMessages:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncAnthropic) -> None:
        message = await async_client.beta.tools.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
        )
        assert_matches_type(ToolsBetaMessage, message, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncAnthropic) -> None:
        message = await async_client.beta.tools.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string", "string", "string"],
            stream=False,
            system="Today's date is 2024-01-01.",
            temperature=1,
            tools=[
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
            ],
            top_k=5,
            top_p=0.7,
        )
        assert_matches_type(ToolsBetaMessage, message, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tools.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(ToolsBetaMessage, message, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tools.messages.with_streaming_response.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = await response.parse()
            assert_matches_type(ToolsBetaMessage, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncAnthropic) -> None:
        message_stream = await async_client.beta.tools.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
            stream=True,
        )
        await message_stream.response.aclose()

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncAnthropic) -> None:
        message_stream = await async_client.beta.tools.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
            stream=True,
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string", "string", "string"],
            system="Today's date is 2024-01-01.",
            temperature=1,
            tools=[
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
                {
                    "description": "Get the current weather in a given location",
                    "name": "x",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                },
            ],
            top_k=5,
            top_p=0.7,
        )
        await message_stream.response.aclose()

    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tools.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tools.messages.with_streaming_response.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-opus-20240229",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True
