# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMemoryStoreArchivedRunError"]


class BetaManagedAgentsMemoryStoreArchivedRunError(BaseModel):
    """A memory store referenced by the deployment is archived."""

    message: str
    """Human-readable error description."""

    type: Literal["memory_store_archived_error"]
