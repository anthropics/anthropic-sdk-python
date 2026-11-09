from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsDeletedVault"]


class BetaManagedAgentsDeletedVault(BaseModel):
    """Confirmation of a deleted vault."""

    id: str
    """The unique ID of the deleted vault (`vlt_...`)."""

    type: Literal["vault_deleted"]
