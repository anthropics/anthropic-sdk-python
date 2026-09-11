from __future__ import annotations

from typing import overload
from datetime import datetime, timezone
from typing_extensions import TypeAlias

from ..._compat import model_copy
from ..._models import build
from ..._exceptions import AnthropicError
from ...types.beta.sessions import BetaManagedAgentsAgentMessageEvent, BetaManagedAgentsStreamSessionEvents

__all__ = ["AccumulatedEvent", "accumulate_managed_agents_event"]

AccumulatedEvent: TypeAlias = BetaManagedAgentsAgentMessageEvent

# Placeholder `processed_at` (the Unix epoch) for a preview snapshot until the
# buffered final event, which carries the real timestamp, replaces it.
_UNPROCESSED = datetime(1970, 1, 1, tzinfo=timezone.utc)


@overload
def accumulate_managed_agents_event(
    accumulated: AccumulatedEvent | None,
    event: BetaManagedAgentsAgentMessageEvent,
) -> BetaManagedAgentsAgentMessageEvent: ...


@overload
def accumulate_managed_agents_event(
    accumulated: AccumulatedEvent | None,
    event: BetaManagedAgentsStreamSessionEvents,
) -> AccumulatedEvent | None: ...


def accumulate_managed_agents_event(
    accumulated: AccumulatedEvent | None,
    event: BetaManagedAgentsStreamSessionEvents,
) -> AccumulatedEvent | None:
    """Fold one preview event into an ``agent.message`` snapshot. Returns a fresh
    snapshot — the ``accumulated`` argument is never mutated.

    - ``event_start`` opens the preview: a new snapshot with empty content is
      returned (so ``accumulated`` may be ``None``). Its ``processed_at`` is an
      epoch placeholder that the buffered final event's server timestamp
      replaces. ``accumulated`` is passed through unchanged when the
      previewed event is not an ``agent.message`` — this helper only tracks
      ``agent.message`` previews.
    - ``event_delta`` is folded into ``accumulated``: a new ``delta.index``
      inserts the fragment as a fresh content entry; an existing index returns
      a copy with that entry appended to. An unrecognised fragment type on an
      existing index passes the entry through unchanged — deltas are
      best-effort and the buffered final event is canonical.
    - ``agent.message`` is the buffered final event: a copy of it is returned,
      replacing whatever the preview had accumulated.
    - Any other event, including types this SDK version does not know about,
      passes ``accumulated`` through unchanged.
    """
    if event.type == "event_start":
        if event.event.type == "agent.message":
            return build(
                BetaManagedAgentsAgentMessageEvent,
                id=event.event.id,
                type="agent.message",
                content=[],
                processed_at=_UNPROCESSED,
            )
        # This helper only tracks agent.message previews; agent.thinking
        # previews are start-only and have no deltas to fold, and unrecognised
        # preview types pass through unchanged.
        return accumulated

    elif event.type == "agent.message":
        return model_copy(event, deep=True)

    elif event.type == "event_delta":
        if accumulated is None:
            raise AnthropicError(f"event_delta for {event.event_id} received before its event_start")

        idx = event.delta.index
        if idx is None:
            idx = 0
        fragment = event.delta.content

        # Indices arrive in order — the first delta at a new index opens the slot.
        # A gap means deltas arrived out of order or were mis-routed.
        if idx > len(accumulated.content):
            raise AnthropicError(
                f"event_delta index {idx} is beyond the end of content (length {len(accumulated.content)})",
            )

        content = list(accumulated.content)
        if idx == len(content):
            # New index: pass the fragment through as a fresh block.
            content.append(model_copy(fragment))
        else:
            existing = content[idx]
            if fragment.type == "text" and existing.type == "text":
                updated = model_copy(existing)
                updated.text = existing.text + fragment.text
                content[idx] = updated

        snapshot = model_copy(accumulated)
        snapshot.content = content
        return snapshot

    # Any other event, including types newer than this SDK, leaves the snapshot unchanged.
    return accumulated
