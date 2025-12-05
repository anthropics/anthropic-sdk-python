from typing import Any, cast

import pytest
from inline_snapshot import external, snapshot

from anthropic import AsyncAnthropic, _compat
from anthropic.types.beta.parsed_beta_message import ParsedBetaMessage


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
class TestAsyncMessages:
    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:606342ef-f614-4bc1-b5e7-2c3305a48bf3.json")),
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
                betas=["structured-outputs-2025-11-13"],
                max_tokens=1024,
            ) as stream:
                return await stream.get_final_message()

        response = await async_stream_parse(async_snapshot_client)

        assert response.content[0].text == snapshot("[12345,67890]")  # type: ignore
