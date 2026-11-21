from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsVaultArchivedRunErrorObject"]


class BetaManagedAgentsVaultArchivedRunErrorObject(BaseModel):
    """A vault referenced by the deployment is archived."""

    message: str
    """Human-readable error description."""

    type: Literal["vault_archived_error"]
