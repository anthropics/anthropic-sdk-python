from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMemoryStoreArchivedRunErrorObject"]


class BetaManagedAgentsMemoryStoreArchivedRunErrorObject(BaseModel):
    """A memory store referenced by the deployment is archived."""

    message: str
    """Human-readable error description."""

    type: Literal["memory_store_archived_error"]
