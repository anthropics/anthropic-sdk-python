# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsDeletedMemoryStore"]


class BetaManagedAgentsDeletedMemoryStore(BaseModel):
    """Confirmation that a `memory_store` was deleted."""

    id: str
    """ID of the deleted memory store (a `memstore_...` identifier).

    The store and all its memories and versions are no longer retrievable.
    """

    type: Literal["memory_store_deleted"]
