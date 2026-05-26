#!/usr/bin/env python3
"""End-to-end self-hosted environment worker demo.

Creates an agent with the built-in agent_toolset_20260401 plus a custom
``current_time`` tool, opens a session against your self-hosted environment,
sends a prompt, runs an ``EnvironmentWorker`` in-process to service the tool
calls locally, then prints the resulting transcript and cleans up.

Required env vars:
  ANTHROPIC_API_KEY          your standard API key (used for agent/session calls)
  ANTHROPIC_ENVIRONMENT_ID   the self-hosted environment to poll
  ANTHROPIC_ENVIRONMENT_KEY  the environment key (the worker's single credential)

Security model: the worker executes bash and file operations directly on the
host. Run inside a container or other isolation boundary you control.
"""

from __future__ import annotations

import os
import sys
import asyncio
import logging
import contextlib
from typing import Any, cast
from datetime import datetime

from anthropic import AsyncAnthropic
from anthropic.lib.tools import beta_async_tool
from anthropic.types.beta import BetaManagedAgentsCustomToolParams
from anthropic.lib.environments import MANAGED_AGENTS_BETA
from anthropic.lib.tools.agent_toolset import beta_agent_toolset_20260401

POLL_TIMEOUT_S = 60
MODEL_ID = "claude-haiku-4-5"


# A custom tool. Because @beta_async_tool produces the same type that
# client.beta.messages.tool_runner accepts, the worker can run it alongside the
# built-in agent_toolset tools with no extra wiring.
@beta_async_tool
async def current_time() -> str:
    """Return the host's current local time as an ISO-8601 string."""
    return datetime.now().isoformat()


def _require_env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        sys.exit(f"error: environment variable {name} is required")
    return val


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    client = AsyncAnthropic()

    environment_id = _require_env("ANTHROPIC_ENVIRONMENT_ID")
    environment_key = _require_env("ANTHROPIC_ENVIRONMENT_KEY")
    workdir = os.environ.get("ANTHROPIC_WORKDIR", ".")

    # 1. Create an agent that has both the built-in toolset and our custom tool.
    #    The Agents API uses its own custom-tool TypedDict and rejects
    #    `additionalProperties` (which pydantic emits), so derive a clean schema.
    schema = {k: v for k, v in dict(current_time.input_schema).items() if k != "additionalProperties"}
    custom_tool_param: BetaManagedAgentsCustomToolParams = {
        "type": "custom",
        "name": current_time.name,
        "description": current_time.description or "Return the host's current local time.",
        "input_schema": cast("Any", schema),
    }
    agent = await client.beta.agents.create(
        name="self-hosted-runner-example",
        model={"id": MODEL_ID},
        system="You are a test agent running in a self-hosted sandbox. Use the available tools.",
        tools=[{"type": "agent_toolset_20260401"}, custom_tool_param],
    )
    print(f"created agent {agent.id}")

    # 2. Create a session bound to the self-hosted environment. The
    #    MANAGED_AGENTS_BETA header is required for the server to accept a
    #    self-hosted environment_id on Sessions endpoints.
    session = await client.beta.sessions.create(
        agent=agent.id,
        environment_id=environment_id,
        title="self-hosted-runner-example",
        betas=[MANAGED_AGENTS_BETA],
    )
    print(f"created session {session.id}")

    try:
        # 3. Send the user prompt that will trigger both a built-in tool (bash)
        #    and the custom tool (current_time).
        await client.beta.sessions.events.send(
            session.id,
            events=[
                {
                    "type": "user.message",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is the current time? Also run pwd to show me the working directory.",
                        }
                    ],
                }
            ],
            betas=[MANAGED_AGENTS_BETA],
        )

        # 4. Service the work locally: the worker polls for work, and for each
        #    claimed session sets up the workdir + downloads the agent's skills,
        #    runs the local tools against the session's tool calls while
        #    heartbeating the work-item lease, then force-stops the work. The
        #    `tools` factory binds the built-in toolset to the per-session
        #    `AgentToolContext` and adds our custom tool. (Use
        #    `client.beta.sessions.events.tool_runner(...)` directly if you want
        #    to observe each dispatched tool call.)
        #
        #    `client.beta.environments.work.worker(...)` builds an
        #    `EnvironmentWorker`; you can also construct one directly with
        #    `EnvironmentWorker(client, ...)` from `anthropic.lib.environments`.
        #
        #    If you already hold a single claimed work item — e.g. an
        #    `ant worker poll --on-work` script spawned this process for one
        #    item — use `handle_item()` instead of `run()`. With no arguments it
        #    serves the item described by the `ANTHROPIC_WORK_ID` /
        #    `ANTHROPIC_ENVIRONMENT_ID` / `ANTHROPIC_SESSION_ID` /
        #    `ANTHROPIC_ENVIRONMENT_KEY` env vars that command sets, and
        #    `environment_id` isn't needed:
        #      await client.beta.environments.work.worker(workdir=workdir, tools=...).handle_item()
        worker = client.beta.environments.work.worker(
            environment_id=environment_id,
            environment_key=environment_key,
            workdir=workdir,
            tools=lambda env: [*beta_agent_toolset_20260401(env), current_time],
        )

        # The worker runs forever; bound it for the demo so the script exits
        # after the model has finished responding.
        with contextlib.suppress(asyncio.TimeoutError):
            await asyncio.wait_for(worker.run(), timeout=POLL_TIMEOUT_S)

        # 5. Print the resulting transcript.
        print("\n--- transcript ---")
        async for ev in client.beta.sessions.events.list(session.id, limit=100, betas=[MANAGED_AGENTS_BETA]):
            print(_summarise_event(ev))

    finally:
        # 6. Clean up the session so the environment's work queue stays empty.
        await client.beta.sessions.delete(session.id, betas=[MANAGED_AGENTS_BETA])
        print(f"\ndeleted session {session.id}")


def _summarise_event(ev: Any) -> str:
    ev_type: str = getattr(ev, "type", "?")
    if ev_type == "agent.tool_use":
        return f"{ev_type}: name={getattr(ev, 'name', '?')} input={getattr(ev, 'input', {})!r}"
    content: Any = getattr(ev, "content", None)
    if not content:
        return ev_type
    first = content[0]
    text: str | None = getattr(first, "text", None)
    if text is None and hasattr(first, "get"):
        text = first.get("text")
    if not text:
        return ev_type
    snippet = text[:120] + ("..." if len(text) > 120 else "")
    return f"{ev_type}: {snippet}"


if __name__ == "__main__":
    asyncio.run(main())
