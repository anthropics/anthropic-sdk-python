import pytest
from respx import MockRouter
from inline_snapshot import external, snapshot

from anthropic import AsyncAnthropic, _compat
from anthropic.types.beta.parsed_beta_message import ParsedBetaMessage

from ..snapshots import make_async_stream_snapshot_request


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
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
                betas=["structured-outputs-2025-11-13"],
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
