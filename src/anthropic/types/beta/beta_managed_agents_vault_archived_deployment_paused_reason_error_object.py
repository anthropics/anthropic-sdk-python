from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsVaultArchivedDeploymentPausedReasonErrorObject"]


class BetaManagedAgentsVaultArchivedDeploymentPausedReasonErrorObject(BaseModel):
    """A vault referenced by the deployment is archived."""

    type: Literal["vault_archived_error"]
