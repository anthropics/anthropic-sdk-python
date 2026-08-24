"""Deprecated-parameter checks shared by the agent toolset and the environment worker.

Kept free of host-only imports so ``anthropic.lib.environments`` can use it at
module level without pulling in :mod:`anthropic.lib.tools.agent_toolset`.
"""

from __future__ import annotations

from ..._types import NotGiven

__all__ = ["UNRESTRICTED_PATHS_DEPRECATION", "reject_unrestricted_paths"]

UNRESTRICTED_PATHS_DEPRECATION = (
    "unrestricted_paths is no longer supported. The file tools are now always confined to the "
    "working directory plus any allowed_roots (the environment worker adds the session's memory "
    "folders there itself), which is neither of the behaviors this flag used to choose between. "
    "Remove the unrestricted_paths argument; to let the file tools reach another directory, add it "
    "to AgentToolContext.allowed_roots."
)


def reject_unrestricted_paths(value: bool | NotGiven) -> None:
    """Raise :class:`TypeError` if the deprecated ``unrestricted_paths`` was passed at all."""
    if isinstance(value, NotGiven):
        return
    raise TypeError(UNRESTRICTED_PATHS_DEPRECATION)
