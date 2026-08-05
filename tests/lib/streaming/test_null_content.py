from typing import Any, cast

import httpx

from anthropic.lib.streaming._messages import accumulate_event
from anthropic.lib.streaming._beta_messages import accumulate_event as beta_accumulate_event

START_EVENT = cast(Any, {"type": "message_start", "message": {"content": None}})
BLOCK_EVENT = cast(Any, {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}})


def test_accumulate_event_normalizes_null_content() -> None:
    snapshot = accumulate_event(event=START_EVENT, current_snapshot=None)

    snapshot = accumulate_event(event=BLOCK_EVENT, current_snapshot=snapshot)

    assert len(snapshot.content) == 1


def test_beta_accumulate_event_normalizes_null_content() -> None:
    snapshot = beta_accumulate_event(event=START_EVENT, current_snapshot=None, request_headers=httpx.Headers())

    snapshot = beta_accumulate_event(event=BLOCK_EVENT, current_snapshot=snapshot, request_headers=httpx.Headers())

    assert len(snapshot.content) == 1
