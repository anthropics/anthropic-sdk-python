from __future__ import annotations

from typing import Literal

import pytest
from respx import MockRouter
from pydantic import BaseModel
from inline_snapshot import snapshot

from anthropic import AsyncAnthropic, _compat

from ..utils import print_obj
from ..snapshots import make_async_snapshot_request


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
class TestAsyncMessages:
    async def test_simple_parse(
        self, async_client: AsyncAnthropic, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        class ContactInfo(BaseModel):
            name: str
            email: str
            plan_interest: str
            demo_requested: bool

        resp = await make_async_snapshot_request(
            lambda cl: cl.beta.messages.parse(
                model="claude-sonnet-4-5",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Extract the key information from this email: John Smith (john@example.com) is "
                            "interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
                        ),
                    }
                ],
                max_tokens=1024,
                output_format=ContactInfo,
            ),
            content_snapshot=snapshot(
                '{"model": "claude-sonnet-4-5-20250929", "id": "msg_01PpBVKyHCmDmjk57fYhRsMk", "type": "message", "role": "assistant", "content": [{"type": "text", "text": "{\\"name\\": \\"John Smith\\", \\"email\\": \\"john@example.com\\", \\"plan_interest\\": \\"Enterprise\\", \\"demo_requested\\": true}"}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 303, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 35, "service_tier": "standard"}}'
            ),
            respx_mock=respx_mock,
            mock_client=async_client,
            path="/v1/messages?beta=true",
        )
        assert print_obj(resp, monkeypatch) == snapshot(
            "ParsedBetaMessage(container=None, content=[ParsedBetaTextBlock(citations=None, parsed_output=ContactInfo(demo_requested=True, email='john@example.com', name='John Smith', plan_interest='Enterprise'), text='{\"name\": \"John Smith\", \"email\": \"john@example.com\", \"plan_interest\": \"Enterprise\", \"demo_requested\": true}', type='text')], context_management=None, id='msg_01PpBVKyHCmDmjk57fYhRsMk', model='claude-sonnet-4-5-20250929', role='assistant', stop_reason='end_turn', stop_sequence=None, type='message', usage=BetaUsage(cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=303, output_tokens=35, server_tool_use=None, service_tier='standard'))\n"
        )

    async def test_special_types(
        self, async_client: AsyncAnthropic, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        resp = await make_async_snapshot_request(
            lambda cl: cl.beta.messages.parse(
                model="claude-sonnet-4-5",
                messages=[
                    {
                        "role": "user",
                        "content": "Which programming language is better for data science, Python or JavaScript?",
                    }
                ],
                max_tokens=1024,
                output_format=Literal["Python", "Typescript"],
            ),
            content_snapshot=snapshot(
                '{"model": "claude-sonnet-4-5-20250929", "id": "msg_015CQWZ6XgLgvZpALgDXQQR5", "type": "message", "role": "assistant", "content": [{"type": "text", "text": "\\"Python\\""}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 129, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 6, "service_tier": "standard"}}'
            ),
            respx_mock=respx_mock,
            mock_client=async_client,
            path="/v1/messages?beta=true",
        )
        assert print_obj(resp, monkeypatch) == snapshot(
            "ParsedBetaMessage(container=None, content=[ParsedBetaTextBlock(citations=None, parsed_output='Python', text='\"Python\"', type='text')], context_management=None, id='msg_015CQWZ6XgLgvZpALgDXQQR5', model='claude-sonnet-4-5-20250929', role='assistant', stop_reason='end_turn', stop_sequence=None, type='message', usage=BetaUsage(cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=129, output_tokens=6, server_tool_use=None, service_tier='standard'))\n"
        )
