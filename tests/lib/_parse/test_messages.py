from typing import List

import pytest
from respx import MockRouter
from pydantic import BaseModel
from inline_snapshot import external, snapshot

from anthropic import Anthropic, AsyncAnthropic, _compat
from anthropic.types.message import Message
from anthropic.types.parsed_message import ParsedMessage

from ..snapshots import make_snapshot_request, make_async_snapshot_request, make_async_stream_snapshot_request


class OrderItem(BaseModel):
    product_name: str
    price: float
    quantity: int


class OrderDetails(BaseModel):
    items: List[OrderItem]
    total: float


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
class TestSyncParse:
    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    def test_parse_with_pydantic_model(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Test sync messages.parse() with a Pydantic model output_format."""

        def parse_message(c: Anthropic) -> ParsedMessage[OrderItem]:
            return c.messages.parse(
                model="claude-sonnet-4-5",
                messages=[
                    {
                        "role": "user",
                        "content": "Extract: I want to order 2 Green Tea at $5.50 each",
                    }
                ],
                output_format=OrderItem,
                max_tokens=1024,
            )

        response = make_snapshot_request(
            parse_message,
            content_snapshot=snapshot(
                '{"model":"claude-sonnet-4-5","id":"msg_01ParseTest001","type":"message","role":"assistant","content":[{"type":"text","text":"{\\"product_name\\":\\"Green Tea\\",\\"price\\":5.5,\\"quantity\\":2}"}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":50,"output_tokens":20}}'
            ),
            respx_mock=respx_mock,
            mock_client=client,
            path="/v1/messages",
        )

        assert response.parsed_output is not None
        assert isinstance(response.parsed_output, OrderItem)
        assert response.parsed_output.product_name == "Green Tea"
        assert response.parsed_output.price == 5.5
        assert response.parsed_output.quantity == 2

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    def test_parse_with_nested_pydantic_model(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Test sync messages.parse() with nested Pydantic models."""

        def parse_message(c: Anthropic) -> ParsedMessage[OrderDetails]:
            return c.messages.parse(
                model="claude-sonnet-4-5",
                messages=[
                    {
                        "role": "user",
                        "content": "Extract order: 2 Green Tea at $5.50 and 1 Coffee at $3.00. Total $14.",
                    }
                ],
                output_format=OrderDetails,
                max_tokens=1024,
            )

        response = make_snapshot_request(
            parse_message,
            content_snapshot=snapshot(
                '{"model":"claude-sonnet-4-5","id":"msg_01ParseTest002","type":"message","role":"assistant","content":[{"type":"text","text":"{\\"items\\":[{\\"product_name\\":\\"Green Tea\\",\\"price\\":5.5,\\"quantity\\":2},{\\"product_name\\":\\"Coffee\\",\\"price\\":3.0,\\"quantity\\":1}],\\"total\\":14.0}"}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":60,"output_tokens":40}}'
            ),
            respx_mock=respx_mock,
            mock_client=client,
            path="/v1/messages",
        )

        assert response.parsed_output is not None
        assert isinstance(response.parsed_output, OrderDetails)
        assert len(response.parsed_output.items) == 2
        assert response.parsed_output.items[0].product_name == "Green Tea"
        assert response.parsed_output.total == 14.0


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
class TestAsyncParse:
    async def test_parse_with_pydantic_model(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        """Test async messages.parse() with a Pydantic model output_format."""

        async def parse_message(c: AsyncAnthropic) -> ParsedMessage[OrderItem]:
            return await c.messages.parse(
                model="claude-sonnet-4-5",
                messages=[
                    {
                        "role": "user",
                        "content": "Extract: I want to order 2 Green Tea at $5.50 each",
                    }
                ],
                output_format=OrderItem,
                max_tokens=1024,
            )

        response = await make_async_snapshot_request(
            parse_message,
            content_snapshot=snapshot(
                '{"model":"claude-sonnet-4-5","id":"msg_01AsyncParseTest001","type":"message","role":"assistant","content":[{"type":"text","text":"{\\"product_name\\":\\"Green Tea\\",\\"price\\":5.5,\\"quantity\\":2}"}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":50,"output_tokens":20}}'
            ),
            respx_mock=respx_mock,
            mock_client=async_client,
            path="/v1/messages",
        )

        assert response.parsed_output is not None
        assert isinstance(response.parsed_output, OrderItem)
        assert response.parsed_output.product_name == "Green Tea"
        assert response.parsed_output.price == 5.5
        assert response.parsed_output.quantity == 2

    async def test_parse_with_nested_pydantic_model(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        """Test async messages.parse() with nested Pydantic models."""

        async def parse_message(c: AsyncAnthropic) -> ParsedMessage[OrderDetails]:
            return await c.messages.parse(
                model="claude-sonnet-4-5",
                messages=[
                    {
                        "role": "user",
                        "content": "Extract order: 2 Green Tea at $5.50 and 1 Coffee at $3.00. Total $14.",
                    }
                ],
                output_format=OrderDetails,
                max_tokens=1024,
            )

        response = await make_async_snapshot_request(
            parse_message,
            content_snapshot=snapshot(
                '{"model":"claude-sonnet-4-5","id":"msg_01AsyncParseTest002","type":"message","role":"assistant","content":[{"type":"text","text":"{\\"items\\":[{\\"product_name\\":\\"Green Tea\\",\\"price\\":5.5,\\"quantity\\":2},{\\"product_name\\":\\"Coffee\\",\\"price\\":3.0,\\"quantity\\":1}],\\"total\\":14.0}"}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":60,"output_tokens":40}}'
            ),
            respx_mock=respx_mock,
            mock_client=async_client,
            path="/v1/messages",
        )

        assert response.parsed_output is not None
        assert isinstance(response.parsed_output, OrderDetails)
        assert len(response.parsed_output.items) == 2
        assert response.parsed_output.items[0].product_name == "Green Tea"
        assert response.parsed_output.total == 14.0


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
class TestAsyncStream:
    async def test_stream_with_raw_schema(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        """Test async messages.stream() with raw JSON schema via output_config."""

        async def async_stream_parse(client: AsyncAnthropic) -> Message:
            async with client.messages.stream(
                model="claude-sonnet-4-5",
                messages=[
                    {
                        "role": "user",
                        "content": "Extract order IDs from the following text:\n\nOrder 12345\nOrder 67890",
                    }
                ],
                output_config={
                    "format": {
                        "type": "json_schema",
                        "schema": {
                            "type": "array",
                            "items": {"type": "integer"},
                        },
                    },
                },
                max_tokens=1024,
            ) as stream:
                return await stream.get_final_message()

        response = await make_async_stream_snapshot_request(
            async_stream_parse,
            content_snapshot=external("uuid:b2c4d6e8-f012-4a56-8b90-1234567890ab.json"),
            respx_mock=respx_mock,
            mock_client=async_client,
            path="/v1/messages",
        )

        content_block = response.content[0]
        assert content_block.type == "text"
        assert content_block.text == snapshot("[12345,67890]")
