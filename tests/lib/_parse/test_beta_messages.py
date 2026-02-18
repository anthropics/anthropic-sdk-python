import json

import pytest
from respx import MockRouter
from pydantic import BaseModel
from inline_snapshot import external, snapshot

from anthropic import AnthropicError, AsyncAnthropic, _compat
from anthropic._legacy_response import LegacyAPIResponse
from anthropic.types.beta.parsed_beta_message import ParsedBetaMessage

from ..snapshots import make_async_stream_snapshot_request


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
class TestAsyncMessages:
    async def test_stream_with_raw_schema(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
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

        response = await make_async_stream_snapshot_request(
            async_stream_parse,
            content_snapshot=external("uuid:48aac7c3-f271-47b3-854b-af4ed31e10bb.json"),
            respx_mock=respx_mock,
            mock_client=async_client,
            path="/v1/messages?beta=true",
        )

        assert response.content[0].text == snapshot("[12345,67890]")

    async def test_parse_uses_output_config(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        class User(BaseModel):
            name: str
            age: int

        async def simple_parse(client: AsyncAnthropic) -> LegacyAPIResponse[ParsedBetaMessage[User]]:
            return await client.beta.with_raw_response.messages.parse(
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

        response = await make_async_stream_snapshot_request(
            simple_parse,
            content_snapshot=external("uuid:044ce19d-3e9c-42d2-90e7-759c978cd94b.json"),
            respx_mock=respx_mock,
            mock_client=async_client,
            path="/v1/messages?beta=true",
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

    async def test_rejects_invalid_output_format_types(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(
            TypeError,
            match="Invalid `output_format` type. Please pass a Pydantic model or valid Python type. To use a raw JSON schema, use the `.create\\(\\)` method instead.",
        ):
            await async_client.beta.messages.parse(
                model="claude-sonnet-4-5",
                messages=[
                    {
                        "role": "user",
                        "content": "Extract data.",
                    }
                ],
                output_format={},  # type: ignore
                max_tokens=1024,
            )
