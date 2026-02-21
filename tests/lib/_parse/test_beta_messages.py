import json
from typing import Any, cast

import pytest
from pydantic import BaseModel
from inline_snapshot import external, snapshot

from anthropic import AnthropicError, AsyncAnthropic, _compat
from anthropic.types.beta.parsed_beta_message import ParsedBetaMessage


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
class TestAsyncMessages:
    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:9381e2b7-7fa1-46f7-9f78-46dc8431ea9d.json")),
        ],
    )
    async def test_stream_with_raw_schema(self, async_snapshot_client: AsyncAnthropic) -> None:
        async def async_stream_parse(client: AsyncAnthropic) -> ParsedBetaMessage[None]:
            async with client.beta.messages.stream(
                model="claude-sonnet-4-5",
                messages=[
                    {
                        "role": "user",
                        "content": "Extract order IDs from the following text:\n\nOrder 12345\nOrder 67890",
                    }
                ],
                output_format={
                    "type": "json_schema",
                    "schema": {
                        "type": "array",
                        "items": {"type": "integer"},
                    },
                },
                betas=["structured-outputs-2025-12-15"],
                max_tokens=1024,
            ) as stream:
                return await stream.get_final_message()

        response = await async_stream_parse(async_snapshot_client)

        assert response.content[0].text == snapshot("[12345,67890]")  # type: ignore

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:d7092a7d-b723-4470-8fb0-da138cd103a1.json")),
        ],
    )
    async def test_parse_uses_output_config(self, async_snapshot_client: AsyncAnthropic) -> None:
        class User(BaseModel):
            name: str
            age: int

        response = await async_snapshot_client.beta.with_raw_response.messages.parse(
            model="claude-sonnet-4-5",
            messages=[
                {
                    "role": "user",
                    "content": "Extract the user's name and age from the following text:\n\nMy name is John Doe and I am 30 years old.",
                }
            ],
            output_format=User,
            max_tokens=1024,
        )

        request_json = json.loads(response.http_request.content)
        assert request_json == snapshot(
            {
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": """\
Extract the user's name and age from the following text:

My name is John Doe and I am 30 years old.\
""",
                    }
                ],
                "model": "claude-sonnet-4-5",
                "output_config": {
                    "format": {
                        "schema": {
                            "type": "object",
                            "title": "User",
                            "properties": {
                                "name": {"type": "string", "title": "Name"},
                                "age": {"type": "integer", "title": "Age"},
                            },
                            "additionalProperties": False,
                            "required": ["name", "age"],
                        },
                        "type": "json_schema",
                    }
                },
            }
        )

    async def test_rejects_both_output_format_and_config(self, async_client: AsyncAnthropic) -> None:
        class User(BaseModel):
            name: str
            age: int

        with pytest.raises(AnthropicError, match="Both output_format and output_config.format were provided"):
            await async_client.beta.messages.parse(
                model="claude-sonnet-4-5",
                messages=[
                    {
                        "role": "user",
                        "content": "Extract the user's name and age.",
                    }
                ],
                output_format=User,
                output_config={
                    "format": {
                        "type": "json_schema",
                        "schema": {"type": "object"},
                    }
                },
                max_tokens=1024,
            )
