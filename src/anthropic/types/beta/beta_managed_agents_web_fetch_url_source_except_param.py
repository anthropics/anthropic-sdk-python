from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .beta_managed_agents_web_fetch_url_source_tool_reference_param import (
    BetaManagedAgentsWebFetchURLSourceToolReferenceParam,
)

__all__ = ["BetaManagedAgentsWebFetchURLSourceExceptParam"]


class BetaManagedAgentsWebFetchURLSourceExceptParam(TypedDict, total=False):
    """
    Every tool's results contribute URLs that may be fetched, except the named tools' results.
    """

    tools: Required[Iterable[BetaManagedAgentsWebFetchURLSourceToolReferenceParam]]
    """The tools whose results do not contribute.

    Between 1 and 128 entries, each with a different name. An empty list is
    rejected; use "all" to leave out no tool's results.
    """

    type: Required[Literal["except"]]
