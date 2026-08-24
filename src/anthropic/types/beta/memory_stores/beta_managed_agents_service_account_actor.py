# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsServiceAccountActor"]


class BetaManagedAgentsServiceAccountActor(BaseModel):
    """
    Attribution for a write made by a workload authenticated as a service account, for example via Workload Identity Federation.
    """

    service_account_id: str
    """ID of the service account that performed the write (a `svac_...` value)."""

    type: Literal["service_account_actor"]
