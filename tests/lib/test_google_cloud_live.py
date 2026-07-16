"""Live integration tests against the real gateway.

Gated on ``ANTHROPIC_LIVE=1``; the regular suite never hits the network. Expects
``ANTHROPIC_GOOGLE_CLOUD_{PROJECT,WORKSPACE_ID}`` (or ``..._BASE_URL``) and
Application Default Credentials in the environment.
"""

from __future__ import annotations

import os
from typing import Iterator, AsyncIterator

import httpx
import pytest

from anthropic import APIStatusError
from anthropic.lib.google_cloud import AnthropicGoogleCloud, AsyncAnthropicGoogleCloud

pytestmark = [
    pytest.mark.skipif(os.environ.get("ANTHROPIC_LIVE") != "1", reason="Set ANTHROPIC_LIVE=1 to run live tests"),
    # google-auth emits a Python-EOL FutureWarning on import; the repo runs with
    # filterwarnings=error, so silence it for this live-test module.
    pytest.mark.filterwarnings("ignore::FutureWarning"),
    pytest.mark.filterwarnings("ignore::DeprecationWarning"),
]

MODEL = "claude-haiku-4-5"
LOCATION = os.environ.get("ANTHROPIC_GOOGLE_CLOUD_LOCATION", "us-central1")


@pytest.fixture
def sync_client() -> Iterator[AnthropicGoogleCloud]:
    client = AnthropicGoogleCloud(
        location=LOCATION,
        max_retries=1,
        http_client=httpx.Client(timeout=60.0),
    )
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
async def async_client() -> AsyncIterator[AsyncAnthropicGoogleCloud]:
    client = AsyncAnthropicGoogleCloud(
        location=LOCATION,
        max_retries=1,
        http_client=httpx.AsyncClient(timeout=60.0),
    )
    try:
        yield client
    finally:
        await client.close()


class TestSyncLive:
    def test_non_streaming(self, sync_client: AnthropicGoogleCloud) -> None:
        message = sync_client.messages.create(
            model=MODEL,
            max_tokens=32,
            messages=[{"role": "user", "content": "Say hello in one word."}],
        )
        assert message.role == "assistant"
        assert message.content[0].type == "text"
        assert message.usage.output_tokens > 0

    def test_streaming(self, sync_client: AnthropicGoogleCloud) -> None:
        events: list[str] = []
        with sync_client.messages.stream(
            model=MODEL,
            max_tokens=32,
            messages=[{"role": "user", "content": "Say hello in one word."}],
        ) as stream:
            for event in stream:
                events.append(event.type)
            final = stream.get_final_message()

        assert events[0] == "message_start"
        assert "content_block_delta" in events
        assert events[-1] == "message_stop"
        assert final.role == "assistant"
        assert final.content[0].type == "text"

    def test_bad_model_surfaces_typed_error(self, sync_client: AnthropicGoogleCloud) -> None:
        with pytest.raises(APIStatusError):
            sync_client.messages.create(
                model="not-a-real-model",
                max_tokens=16,
                messages=[{"role": "user", "content": "hi"}],
            )


class TestAsyncLive:
    async def test_non_streaming(self, async_client: AsyncAnthropicGoogleCloud) -> None:
        message = await async_client.messages.create(
            model=MODEL,
            max_tokens=32,
            messages=[{"role": "user", "content": "Say hello in one word."}],
        )
        assert message.role == "assistant"
        assert message.content[0].type == "text"

    async def test_streaming(self, async_client: AsyncAnthropicGoogleCloud) -> None:
        events: list[str] = []
        async with async_client.messages.stream(
            model=MODEL,
            max_tokens=32,
            messages=[{"role": "user", "content": "Say hello in one word."}],
        ) as stream:
            async for event in stream:
                events.append(event.type)
            final = await stream.get_final_message()

        assert events[0] == "message_start"
        assert "content_block_delta" in events
        assert events[-1] == "message_stop"
        assert final.content[0].type == "text"

    async def test_bad_model_surfaces_typed_error(self, async_client: AsyncAnthropicGoogleCloud) -> None:
        with pytest.raises(APIStatusError):
            await async_client.messages.create(
                model="not-a-real-model",
                max_tokens=16,
                messages=[{"role": "user", "content": "hi"}],
            )
