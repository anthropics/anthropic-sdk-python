from typing import List
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_web_fetch_url_source_tool_reference import BetaManagedAgentsWebFetchURLSourceToolReference

__all__ = ["BetaManagedAgentsWebFetchURLSourceExcept"]


class BetaManagedAgentsWebFetchURLSourceExcept(BaseModel):
    """
    Every tool's results contribute URLs that may be fetched, except the named tools' results.
    """

    tools: List[BetaManagedAgentsWebFetchURLSourceToolReference]
    """The tools whose results do not contribute.

    Between 1 and 128 entries, each with a different name. An empty list is
    rejected; use "all" to leave out no tool's results.
    """

    type: Literal["except"]
