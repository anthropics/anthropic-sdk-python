# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentToolset20260401GrepInput"]


class BetaManagedAgentsAgentToolset20260401GrepInput(BaseModel):
    """Input payload for the `grep` tool.

    Searches file contents for
    a regular expression, returning matching lines.
    """

    pattern: str
    """Regular expression to search for."""

    path: Optional[str] = None
    """Optional directory root to search under.

    Defaults to the runner's working directory.
    """
