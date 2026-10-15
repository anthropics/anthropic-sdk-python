from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_managed_agents_web_fetch_url_source_shorthand import BetaManagedAgentsWebFetchURLSourceShorthand
from .beta_managed_agents_web_fetch_url_source_tool_filter_param import (
    BetaManagedAgentsWebFetchURLSourceToolFilterParam,
)

__all__ = ["BetaManagedAgentsWebFetchURLSourceToolFilterParams"]

BetaManagedAgentsWebFetchURLSourceToolFilterParams: TypeAlias = Union[
    BetaManagedAgentsWebFetchURLSourceShorthand, BetaManagedAgentsWebFetchURLSourceToolFilterParam
]
