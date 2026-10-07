from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_managed_agents_web_fetch_url_source_all import BetaManagedAgentsWebFetchURLSourceAll
from .beta_managed_agents_web_fetch_url_source_none import BetaManagedAgentsWebFetchURLSourceNone

__all__ = ["BetaManagedAgentsWebFetchURLSourceUserInput"]

BetaManagedAgentsWebFetchURLSourceUserInput: TypeAlias = Annotated[
    Union[BetaManagedAgentsWebFetchURLSourceAll, BetaManagedAgentsWebFetchURLSourceNone], UnionDiscriminator("type")
]
