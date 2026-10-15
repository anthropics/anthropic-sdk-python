from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsWebFetchURLSourceNone"]


class BetaManagedAgentsWebFetchURLSourceNone(BaseModel):
    """This source contributes no URLs that may be fetched."""

    type: Literal["none"]
