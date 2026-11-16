from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsVaultNotFoundDeploymentPausedReasonErrorObject"]


class BetaManagedAgentsVaultNotFoundDeploymentPausedReasonErrorObject(BaseModel):
    """A vault referenced by the deployment no longer exists."""

    type: Literal["vault_not_found_error"]
