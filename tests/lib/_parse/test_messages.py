from typing import Any, List, cast

import pytest
from pydantic import BaseModel
from inline_snapshot import external, snapshot

from anthropic import Anthropic, AsyncAnthropic, _compat


class OrderItem(BaseModel):
    product_name: str
    price: float
    quantity: int


class OrderDetails(BaseModel):
    items: List[OrderItem]
    total: float


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
class TestSyncParse:
    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:c11eefc7-fff0-4466-8453-42eef73b8876.json")),
        ],
    )
    def test_parse_with_pydantic_model(self, snapshot_client: Anthropic) -> None:
        """Test sync messages.parse() with a Pydantic model output_format."""

        response = snapshot_client.messages.parse(
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

        assert response.parsed_output is not None
        assert isinstance(response.parsed_output, OrderItem)
        assert response.parsed_output.product_name == "Green Tea"
        assert response.parsed_output.price == 5.5
        assert response.parsed_output.quantity == 2

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:bd7029d5-d8d4-4e06-be3a-2ac9c60803a6.json")),
        ],
    )
    def test_parse_with_nested_pydantic_model(self, snapshot_client: Anthropic) -> None:
        """Test sync messages.parse() with nested Pydantic models."""

        response = snapshot_client.messages.parse(
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

        assert response.parsed_output is not None
        assert isinstance(response.parsed_output, OrderDetails)
        assert len(response.parsed_output.items) == 2
        assert response.parsed_output.items[0].product_name == "Green Tea"
        assert response.parsed_output.total == 14.0


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
class TestAsyncParse:
    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:924cfccc-c863-44ed-9838-c36b37416eaf.json")),
        ],
    )
    async def test_parse_with_pydantic_model(self, async_snapshot_client: AsyncAnthropic) -> None:
        """Test async messages.parse() with a Pydantic model output_format."""

        response = await async_snapshot_client.messages.parse(
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

        assert response.parsed_output is not None
        assert isinstance(response.parsed_output, OrderItem)
        assert response.parsed_output.product_name == "Green Tea"
        assert response.parsed_output.price == 5.5
        assert response.parsed_output.quantity == 2

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:d743d628-16aa-4c9f-ae78-51deb578f746.json")),
        ],
    )
    async def test_parse_with_nested_pydantic_model(self, async_snapshot_client: AsyncAnthropic) -> None:
        """Test async messages.parse() with nested Pydantic models."""

        response = await async_snapshot_client.messages.parse(
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

        assert response.parsed_output is not None
        assert isinstance(response.parsed_output, OrderDetails)
        assert len(response.parsed_output.items) == 2
        assert response.parsed_output.items[0].product_name == "Green Tea"
        assert response.parsed_output.total == 14.0


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
class TestAsyncStream:
    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:a8b7dbb8-2321-4624-abdb-7ba2136b5c38.json")),
        ],
    )
    async def test_stream_with_raw_schema(self, async_snapshot_client: AsyncAnthropic) -> None:
        """Test async messages.stream() with raw JSON schema via output_config."""

        async with async_snapshot_client.messages.stream(
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
            response = await stream.get_final_message()

        content_block = response.content[0]
        assert content_block.type == "text"
        assert content_block.text == snapshot("[12345,67890]")
