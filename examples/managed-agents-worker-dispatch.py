#!/usr/bin/env python3
"""Service one already-claimed work item — the self-hosted "sandbox process" shape.

Unlike ``managed-agents-self-hosted-sandbox-worker.py`` (which creates an agent +
session and runs ``EnvironmentWorker.run()`` as a long-running poll loop), this
process does *not* create anything and does *not* poll. Something upstream — an
``ant worker poll --on-work`` script, or your own orchestrator that spawns a
sandbox per work item — already claimed a ``session`` work item and handed it to
this process. Our only job is to run that one item's tool calls to completion,
then exit.

``EnvironmentWorker.handle_item()`` with no arguments reads the work-item
identity from the environment variables that ``ant worker poll --on-work`` sets
on the process it spawns:

  ANTHROPIC_WORK_ID          the claimed work item to service
  ANTHROPIC_ENVIRONMENT_ID   the self-hosted environment it belongs to
  ANTHROPIC_SESSION_ID       the session whose tool calls we run
  ANTHROPIC_ENVIRONMENT_KEY  the environment key (the worker's single credential)

It builds the per-session workdir, downloads the session agent's skills, runs the
tools while heartbeating the work-item lease, and force-stops the item on exit.

Security model: the worker executes bash and file operations directly on the
host. Run inside a container or other isolation boundary you control.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from anthropic import AsyncAnthropic
from anthropic.lib.tools import beta_async_tool
from anthropic.lib.tools.agent_toolset import beta_agent_toolset_20260401


# A custom tool, same pattern as managed-agents-self-hosted-sandbox-worker.py:
# @beta_async_tool produces the same type the worker's tool runner accepts, so it
# runs alongside the built-in agent_toolset tools with no extra wiring.
@beta_async_tool
async def current_time() -> str:
    """Return the host's current local time as an ISO-8601 string."""
    return datetime.now().isoformat()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    client = AsyncAnthropic()

    # No agent/session creation and no polling here — an upstream poller already
    # claimed the item. Build the worker with just a `tools` factory: it is
    # invoked once per claimed session with that session's `AgentToolContext`,
    # so the built-in toolset binds to the right per-session workdir.
    # (`worker(...)` returns an `EnvironmentWorker`; you can also construct one
    # directly with `EnvironmentWorker(client, ...)` from `anthropic.lib.environments`.)
    worker = client.beta.environments.work.worker(
        workdir="/workspace",
        tools=lambda env: [*beta_agent_toolset_20260401(env), current_time],
    )

    # handle_item() with no arguments reads ANTHROPIC_WORK_ID /
    # ANTHROPIC_ENVIRONMENT_ID / ANTHROPIC_SESSION_ID / ANTHROPIC_ENVIRONMENT_KEY
    # from the environment, then runs the per-item flow: set up the workdir +
    # skills, run the session's tool calls while heartbeating the lease, and
    # force-stop the work item on exit. It returns once the item is done.
    await worker.handle_item()
    print("work item complete")


if __name__ == "__main__":
    asyncio.run(main())
