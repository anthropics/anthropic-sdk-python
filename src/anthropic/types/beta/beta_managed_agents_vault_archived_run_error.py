# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsVaultArchivedRunError"]


class BetaManagedAgentsVaultArchivedRunError(BaseModel):
    """A vault referenced by the deployment is archived."""

    message: str
    """Human-readable error description."""

    type: Literal["vault_archived_error"]
