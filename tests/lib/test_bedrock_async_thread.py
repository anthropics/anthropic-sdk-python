"""Regression test for #1770: AsyncAnthropicBedrock must not block the event loop during SigV4 auth."""

import asyncio
import time
from unittest.mock import patch

import pytest

from anthropic import AsyncAnthropicBedrock


@pytest.mark.asyncio
async def test_async_bedrock_auth_does_not_block_event_loop():
    """Slow credential resolution must not stall concurrent async tasks."""
    heartbeats: list[float] = []

    async def heartbeat():
        for _ in range(4):
            heartbeats.append(time.monotonic())
            await asyncio.sleep(0.1)

    def slow_get_auth_headers(**kwargs):
        time.sleep(0.5)
        return {"Authorization": "AWS4-HMAC-SHA256 ..."}

    client = AsyncAnthropicBedrock(aws_region="us-east-1")

    with patch("anthropic.lib.bedrock._client.get_auth_headers", side_effect=slow_get_auth_headers):
        # _prepare_request needs a real httpx.Request
        import httpx

        req = httpx.Request("POST", "https://bedrock-runtime.us-east-1.amazonaws.com/model/test/invoke", content=b"{}")

        async def call_prepare():
            await client._prepare_request(req)

        await asyncio.gather(heartbeat(), call_prepare())

    # If auth blocked the loop, heartbeats would cluster after the sleep.
    # With to_thread, heartbeats should be spread across ~0.4s.
    assert len(heartbeats) == 4
    span = heartbeats[-1] - heartbeats[0]
    assert span > 0.2, f"Heartbeats too clustered ({span:.3f}s) — event loop was blocked"
