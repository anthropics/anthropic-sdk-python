from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsDeletedCredential"]


class BetaManagedAgentsDeletedCredential(BaseModel):
    """Confirmation of a deleted credential."""

    id: str
    """The unique ID of the deleted credential (`vcrd_...`)."""

    type: Literal["vault_credential_deleted"]
