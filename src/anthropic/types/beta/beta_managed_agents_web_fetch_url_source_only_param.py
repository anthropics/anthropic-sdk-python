from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .beta_managed_agents_web_fetch_url_source_tool_reference_param import (
    BetaManagedAgentsWebFetchURLSourceToolReferenceParam,
)

__all__ = ["BetaManagedAgentsWebFetchURLSourceOnlyParam"]


class BetaManagedAgentsWebFetchURLSourceOnlyParam(TypedDict, total=False):
    """Only the named tools' results contribute URLs that may be fetched."""

    tools: Required[Iterable[BetaManagedAgentsWebFetchURLSourceToolReferenceParam]]
    """The tools whose results contribute.

    Between 1 and 128 entries, each with a different name. An empty list is
    rejected; use "none" to allow no tool's results.
    """

    type: Required[Literal["only"]]
