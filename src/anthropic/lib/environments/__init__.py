"""Self-hosted environment runner helpers.

- :func:`anthropic.resources.beta.environments.work.AsyncWork.poller`
  (``client.beta.environments.work.poller(...)``) — control-plane only: claims
  work items, ack's each one, and hands back the work item. Async only (lives on
  ``AsyncWork``, not the sync ``Work``). The underlying generators are
  :func:`iter_work` / :func:`aiter_work`.
- :class:`SessionToolRunner` (``client.beta.sessions.events.tool_runner(...)``)
  — the sessions-side counterpart to ``client.beta.messages.tool_runner``:
  dispatches local tools against a session's ``agent.tool_use`` events.
- :class:`EnvironmentWorker`
  (``client.beta.environments.work.worker(...)``) — the full composition: poll →
  set up the workdir + download the session agent's skills → run a
  :class:`SessionToolRunner` while heartbeating the work-item lease → force-stop
  on exit → loop. Build it with ``client.beta.environments.work.worker(...)`` or
  construct it directly: ``EnvironmentWorker(client, ...)``; use
  :meth:`EnvironmentWorker.handle_item` for the per-item flow when you already
  hold a claimed work item.

The tool implementations themselves (:func:`beta_agent_toolset` and the per-tool
factories) live next to the other tool helpers — import them from
``anthropic.lib.tools.agent_toolset``.
"""

from ._poller import (
    POLL_BLOCK_MS,
    iter_work,
    aiter_work,
)
from ._worker import EnvironmentWorker, EnvironmentWorkerTools
from ..tools._skills import download_session_skills
from ..tools._beta_session_runner import (
    DEFAULT_MAX_IDLE,
    MANAGED_AGENTS_BETA,
    SessionToolRunner,
    DispatchedToolCall,
    BetaAnyRunnableTool,
    DispatchedToolUseEvent,
    DispatchedToolResultParams,
)

__all__ = [
    "iter_work",
    "aiter_work",
    "POLL_BLOCK_MS",
    "EnvironmentWorker",
    "EnvironmentWorkerTools",
    "SessionToolRunner",
    "DispatchedToolCall",
    "DispatchedToolUseEvent",
    "DispatchedToolResultParams",
    "BetaAnyRunnableTool",
    "download_session_skills",
    "MANAGED_AGENTS_BETA",
    "DEFAULT_MAX_IDLE",
]
