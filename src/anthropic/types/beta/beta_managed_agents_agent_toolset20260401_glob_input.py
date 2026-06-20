# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentToolset20260401GlobInput"]


class BetaManagedAgentsAgentToolset20260401GlobInput(BaseModel):
    """Input payload for the `glob` tool.

    Returns paths matching a
    doublestar glob pattern, newest first.
    """

    pattern: str
    """Doublestar glob pattern (e.g.

    `**/*.go`). Absolute patterns are only permitted when the runner is configured
    to allow them.
    """

    path: Optional[str] = None
    """Optional directory root to search under.

    Defaults to the runner's working directory.
    """
