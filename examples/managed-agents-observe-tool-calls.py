#!/usr/bin/env python3
"""Observe every tool call with the low-level session tool runner.

``client.beta.sessions.events.tool_runner(...)`` is the "observe every call"
path: an async iterable that attaches to a session's event stream, runs the
matching local tool for each tool-call event, posts the result back, and yields
one ``DispatchedToolCall`` per completed call. It does NOT manage a work-item
lease — ``EnvironmentWorker`` is what does that.

This file has two scenarios:

  main()  — the primary entry point. A session you created and drive yourself:
            no work queue, no lease, not necessarily self-hosted. Create an
            agent + session, send a prompt, then iterate tool_runner and print
            each dispatched tool call. Reach for this when you just want to see
            (or audit, or react to) each tool call on a session you own.

  observe_as_self_hosted_worker()  — a second scenario, NOT called by default.
            The shape to use when you *are* a self-hosted worker: it composes
            the work poller + the agent tool context + your OWN heartbeat task
            running in parallel with the tool_runner loop. Reach for this only
            when you need per-call visibility AND lease management together —
            otherwise ``EnvironmentWorker`` already does both for you.

Security model: the tools execute bash and file operations directly on the host.
Run inside a container or other isolation boundary you control.
"""

from __future__ import annotations

import os
import sys
import asyncio
import logging

import anyio

from anthropic import AsyncAnthropic
from anthropic.lib.environments import MANAGED_AGENTS_BETA
from anthropic.lib.tools.agent_toolset import AgentToolContext, beta_agent_toolset_20260401

MODEL_ID = "claude-haiku-4-5"


def _require_env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        sys.exit(f"error: environment variable {name} is required")
    return val


async def main() -> None:
    """Primary scenario: drive a session yourself and watch each tool call.

    No work queue and no lease are involved — we create the session, send a
    prompt, and consume ``tool_runner`` directly. tool_runner is passed no
    ``environment_key``, so it authenticates with the client's own credentials;
    that makes this scenario work against a non-self-hosted environment too.
    """
    logging.basicConfig(level=logging.INFO)
    client = AsyncAnthropic()

    environment_id = _require_env("ANTHROPIC_ENVIRONMENT_ID")
    workdir = os.environ.get("ANTHROPIC_WORKDIR", ".")

    # 1. Create an agent with the built-in agent toolset.
    agent = await client.beta.agents.create(
        name="observe-tool-calls-example",
        model={"id": MODEL_ID},
        system="You are a test agent. Use the available tools to answer.",
        tools=[{"type": "agent_toolset_20260401"}],
    )
    print(f"created agent {agent.id}")

    # 2. Create a session. A session always lives in an environment, but here we
    #    just create it and drive its tool calls ourselves — there is no work
    #    item and no lease to manage.
    session = await client.beta.sessions.create(
        agent=agent.id,
        environment_id=environment_id,
        title="observe-tool-calls-example",
        betas=[MANAGED_AGENTS_BETA],
    )
    print(f"created session {session.id}")

    try:
        # 3. Send a prompt that will make the agent call a tool or two.
        await client.beta.sessions.events.send(
            session.id,
            events=[
                {
                    "type": "user.message",
                    "content": [{"type": "text", "text": "Run pwd and then ls to show me the working directory."}],
                }
            ],
            betas=[MANAGED_AGENTS_BETA],
        )

        # 4. Observe every dispatched tool call. tool_runner attaches to the
        #    session's event stream, runs the matching local tool for each
        #    tool-call event, posts the result back, and yields one
        #    DispatchedToolCall per completed call. AgentToolContext gives the
        #    tools their workdir; passing client + session_id also downloads the
        #    session agent's skills into the workdir before the first tool runs.
        print("\n--- dispatched tool calls ---")
        async with AgentToolContext(workdir=workdir, client=client, session_id=session.id) as env:
            async for call in client.beta.sessions.events.tool_runner(
                session.id,
                tools=beta_agent_toolset_20260401(env),
            ):
                print(f"  {call.name} {call.event.input} is_error={call.is_error} posted={call.posted}")

    finally:
        # 5. Clean up the session.
        await client.beta.sessions.delete(session.id, betas=[MANAGED_AGENTS_BETA])
        print(f"\ndeleted session {session.id}")


async def observe_as_self_hosted_worker() -> None:
    """Secondary scenario — NOT called by main(); shown for reference.

    Use this shape when you *are* a self-hosted worker (you poll a work queue and
    hold a work-item lease) but you also want per-call visibility into every
    dispatched tool call.

    tool_runner does NOT manage the work-item lease — EnvironmentWorker does.
    EnvironmentWorker.run() / .handle_item() already run a tool_runner internally
    while heartbeating the lease and force-stopping the work on exit, so reach
    for them unless you specifically need to see each call. Rolling your own
    heartbeat, as below, is the cost of getting per-call visibility AND lease
    management together.

    NOTE: the heartbeat loop here is a deliberately simplified shape — just
    enough to keep the lease warm while the session runs. EnvironmentWorker's
    internal heartbeat is the careful reference: it bounds each request,
    distinguishes transient from fatal failures, and assumes the lease lost after
    a TTL of failed beats so two workers never end up serving the same item.
    """
    logging.basicConfig(level=logging.INFO)
    client = AsyncAnthropic()

    environment_id = _require_env("ANTHROPIC_ENVIRONMENT_ID")
    environment_key = _require_env("ANTHROPIC_ENVIRONMENT_KEY")

    async def heartbeat(work_id: str, env_id: str, stop: anyio.Event) -> None:
        # Scope the environment key onto a sub-client so each request carries
        # `Authorization: Bearer <env_key>` and no `X-Api-Key`, inheriting the
        # parent's timeout / retries / http_client / default_headers. This is
        # what `EnvironmentWorker` does internally for its heartbeat.
        scoped = client.copy(auth_token=environment_key, credentials=None)
        scoped.api_key = None
        # The first beat claims the lease with NO_HEARTBEAT; later beats echo
        # the server's last value back.
        last = "NO_HEARTBEAT"
        while not stop.is_set():
            resp = await scoped.beta.environments.work.heartbeat(
                work_id,
                environment_id=env_id,
                expected_last_heartbeat=last,
            )
            last = resp.last_heartbeat
            if resp.state in ("stopping", "stopped") or not resp.lease_extended:
                stop.set()
                return
            # Beat at roughly half the lease TTL; wake immediately if we stop.
            interval = resp.ttl_seconds / 2 if resp.ttl_seconds > 0 else 30.0
            with anyio.move_on_after(interval):
                await stop.wait()

    # The poller claims + acks each work item; with auto_stop=True (the default)
    # it also calls work.stop when our loop body returns. The lease heartbeat is
    # the part tool_runner does not do, so we run it ourselves alongside the loop.
    async for work in client.beta.environments.work.poller(
        environment_id=environment_id,
        environment_key=environment_key,
    ):
        session_id = work.data.id

        # Passing client + session_id makes AgentToolContext fetch the session's
        # resolved agent on enter and download each skill into the workdir.
        async with AgentToolContext(workdir="/workspace", client=client, session_id=session_id) as env:
            async with anyio.create_task_group() as tg:
                stop = anyio.Event()
                tg.start_soon(heartbeat, work.id, work.environment_id, stop)
                try:
                    # Pass environment_key so the event stream / list / send
                    # calls authenticate as the environment, like the worker does.
                    async for call in client.beta.sessions.events.tool_runner(
                        session_id,
                        tools=beta_agent_toolset_20260401(env),
                        environment_key=environment_key,
                    ):
                        print(f"  {call.name} {call.event.input} is_error={call.is_error} posted={call.posted}")
                finally:
                    # Stop the heartbeat and tear the task group down once the
                    # session's tool calls are done (or the loop raised).
                    stop.set()
                    tg.cancel_scope.cancel()


if __name__ == "__main__":
    asyncio.run(main())
