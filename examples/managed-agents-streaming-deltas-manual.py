#!/usr/bin/env python3
"""Streams a session with ``event_deltas`` enabled and folds the ``event_start``
/ ``event_delta`` previews into ``agent.message`` snapshots with
``accumulate_managed_agents_event`` — for callers who want to own the preview
lifecycle themselves.
"""

from __future__ import annotations

import sys

from anthropic import Anthropic
from anthropic.lib.sessions import accumulate_managed_agents_event
from anthropic.types.beta.sessions import BetaManagedAgentsAgentMessageEvent

client = Anthropic()


def main() -> None:
    # Create an environment, agent and session.
    environment = client.beta.environments.create(
        name="streaming-deltas-manual-example",
    )
    print("Created environment:", environment.id)

    agent = client.beta.agents.create(
        name="streaming-deltas-manual-example",
        model="claude-sonnet-4-6",
    )
    print("Created agent:", agent.id)

    session = client.beta.sessions.create(
        environment_id=environment.id,
        agent={"type": "agent", "id": agent.id},
    )
    print("Created session:", session.id)

    # Send a user message.
    client.beta.sessions.events.send(
        session.id,
        events=[
            {
                "type": "user.message",
                "content": [{"type": "text", "text": "Write a short haiku about the ocean."}],
            }
        ],
    )

    # Open the event stream with ``event_deltas`` enabled so ``agent.message``
    # text arrives incrementally as ``event_start`` / ``event_delta`` previews
    # before the buffered final event.
    print("\nStreaming:")
    with client.beta.sessions.events.stream(
        session.id,
        event_deltas=["agent.message"],
    ) as stream:
        # One snapshot per previewed event id.
        previews: dict[str, BetaManagedAgentsAgentMessageEvent] = {}

        for ev in stream:
            event_id = (
                ev.event_id
                if ev.type == "event_delta"
                else ev.event.id
                if ev.type == "event_start"
                else getattr(ev, "id", None)
            )

            prev = previews.get(event_id) if event_id is not None else None
            if ev.type == "event_delta" and prev is None:
                # The preview was already closed (e.g. dropped below at
                # ``span.model_request_end``) — ignore the stray delta.
                continue
            preview = accumulate_managed_agents_event(prev, ev)
            if event_id is not None and preview is not None:
                previews[event_id] = preview

            if ev.type == "event_delta":
                if preview is not None and preview.type == "agent.message":
                    text = "".join(b.text for b in preview.content)
                    sys.stdout.write(f"\r{text}")
                    sys.stdout.flush()

            elif ev.type == "agent.message":
                assert event_id is not None
                previews.pop(event_id, None)
                sys.stdout.write("\n")
                print("[final]", "".join(b.text for b in ev.content))

            elif ev.type == "span.model_request_end":
                # The model request ended — any open preview will not get a buffered
                # event, so drop it.
                previews.clear()

            elif ev.type == "session.status_idle":
                # The session is no longer doing work (whatever the stop reason)
                # and the stream stays open, so stop reading.
                break

            elif ev.type == "session.error":
                print("[error]", ev.error.type, ev.error.message, file=sys.stderr)
                break


main()
