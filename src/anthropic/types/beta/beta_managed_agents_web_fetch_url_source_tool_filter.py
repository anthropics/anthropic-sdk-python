from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_managed_agents_web_fetch_url_source_all import BetaManagedAgentsWebFetchURLSourceAll
from .beta_managed_agents_web_fetch_url_source_none import BetaManagedAgentsWebFetchURLSourceNone
from .beta_managed_agents_web_fetch_url_source_only import BetaManagedAgentsWebFetchURLSourceOnly
from .beta_managed_agents_web_fetch_url_source_except import BetaManagedAgentsWebFetchURLSourceExcept

__all__ = ["BetaManagedAgentsWebFetchURLSourceToolFilter"]

BetaManagedAgentsWebFetchURLSourceToolFilter: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsWebFetchURLSourceAll,
        BetaManagedAgentsWebFetchURLSourceNone,
        BetaManagedAgentsWebFetchURLSourceOnly,
        BetaManagedAgentsWebFetchURLSourceExcept,
    ],
    UnionDiscriminator("type"),
]
