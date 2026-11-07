from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsServiceAccountActor"]


class BetaManagedAgentsServiceAccountActor(BaseModel):
    """
    A workload authenticated as a service account, for example via Workload Identity Federation.
    """

    service_account_id: str
    """ID of the service account (a `svac_...` value)."""

    type: Literal["service_account_actor"]
