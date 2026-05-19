# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentToolset20260401BashInput"]


class BetaManagedAgentsAgentToolset20260401BashInput(BaseModel):
    """Input payload for the `bash` tool of the
    `agent_toolset_20260401` toolset.

    All fields are optional;
    a normal invocation supplies `command`, while `restart=true`
    (with no `command`) reboots the runner-side bash session.
    """

    command: Optional[str] = None
    """Shell command to execute. Omit only when `restart` is true."""

    restart: Optional[bool] = None
    """When true, restart the persistent bash session instead of running a command.

    Subsequent calls without `restart` will run against the fresh session.
    """

    timeout_ms: Optional[int] = None
    """Per-call timeout in milliseconds.

    Defaults to the runner-wide tool timeout when omitted or zero.
    """
