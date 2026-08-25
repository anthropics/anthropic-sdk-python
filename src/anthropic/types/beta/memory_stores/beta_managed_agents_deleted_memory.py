# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsDeletedMemory"]


class BetaManagedAgentsDeletedMemory(BaseModel):
    """
    Tombstone returned by [Delete a memory](/en/api/beta/memory_stores/memories/delete). Deleting a memory does not erase its version history: its versions remain listable via [List memory versions](/en/api/beta/memory_stores/memory_versions/list) while they are retained (each version is kept for at least the version retention period after it was written, unless the store itself is deleted).
    """

    id: str
    """ID of the deleted memory (a `mem_...` value)."""

    type: Literal["memory_deleted"]
