# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsDeletedMemory"]


class BetaManagedAgentsDeletedMemory(BaseModel):
    """
    Tombstone returned by [Delete a memory](/en/api/beta/memory_stores/memories/delete). The memory's version history persists and remains listable via [List memory versions](/en/api/beta/memory_stores/memory_versions/list) until the store itself is deleted.
    """

    id: str
    """ID of the deleted memory (a `mem_...` value)."""

    type: Literal["memory_deleted"]
