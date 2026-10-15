from typing import List
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_web_fetch_url_source_tool_reference import BetaManagedAgentsWebFetchURLSourceToolReference

__all__ = ["BetaManagedAgentsWebFetchURLSourceOnly"]


class BetaManagedAgentsWebFetchURLSourceOnly(BaseModel):
    """Only the named tools' results contribute URLs that may be fetched."""

    tools: List[BetaManagedAgentsWebFetchURLSourceToolReference]
    """The tools whose results contribute.

    Between 1 and 128 entries, each with a different name. An empty list is
    rejected; use "none" to allow no tool's results.
    """

    type: Literal["only"]
