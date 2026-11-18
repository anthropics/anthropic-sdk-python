from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMemoryStoreArchivedDeploymentPausedReasonErrorObject"]


class BetaManagedAgentsMemoryStoreArchivedDeploymentPausedReasonErrorObject(BaseModel):
    """A memory store referenced by the deployment is archived."""

    type: Literal["memory_store_archived_error"]
