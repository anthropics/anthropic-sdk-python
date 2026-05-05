# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr
from .beta_managed_agents_multiagent_roster_entry_params import BetaManagedAgentsMultiagentRosterEntryParams

__all__ = ["BetaManagedAgentsMultiagentParams"]


class BetaManagedAgentsMultiagentParams(TypedDict, total=False):
    """
    A coordinator topology: the session's primary thread orchestrates work by spawning session threads, each running an agent drawn from the `agents` roster.
    """

    agents: Required[SequenceNotStr[BetaManagedAgentsMultiagentRosterEntryParams]]
    """Agents the coordinator may spawn as session threads.

    1–20 entries. Each entry is an agent ID string, a versioned
    `{"type":"agent","id","version"}` reference, or `{"type":"self"}` to allow
    recursive self-invocation. Entries must reference distinct agents (after
    resolving `self` and string forms); at most one `self`. Referenced agents must
    exist, must not be archived, and must not themselves have `multiagent` set
    (depth limit 1).
    """

    type: Required[Literal["coordinator"]]
