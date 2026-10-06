from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsWebFetchURLSourceAll"]


class BetaManagedAgentsWebFetchURLSourceAll(BaseModel):
    """Every URL from this source may be fetched. This is the default."""

    type: Literal["all"]
