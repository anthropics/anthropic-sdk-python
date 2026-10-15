from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMemoryStore"]


class BetaManagedAgentsMemoryStore(BaseModel):
    """A `memory_store`: a named container for agent memories, scoped to a workspace.

    Attach a store to a session via `resources[]` to mount it as a directory the agent can read and write.
    """

    id: str
    """Unique identifier for the memory store (a `memstore_...` tagged ID).

    Use this when attaching the store to a session, or in the `{memory_store_id}`
    path parameter of subsequent calls.
    """

    archived_at: Optional[datetime] = None
    """Timestamp when the store was archived, or `null` if active.

    Set once and never cleared; archiving is one-way. Archived stores are read-only
    and cannot be attached to new sessions.
    """

    created_at: datetime
    """Timestamp when the store was created."""

    description: str
    """Free-text description of what the store contains, up to 1024 characters.

    Included in the agent's system prompt when the store is attached, so word it to
    be useful to the agent. Empty string when unset.
    """

    metadata: Dict[str, str]
    """
    Arbitrary key-value tags for your own bookkeeping (such as the end user a store
    belongs to). Up to 16 pairs; keys 1–64 characters; values up to 512 characters.
    Returned on retrieve/list but not filterable.
    """

    name: str
    """Human-readable name for the store.

    1–255 characters. The store's mount-path slug under `/mnt/memory/` is derived
    from this name.
    """

    type: Literal["memory_store"]

    updated_at: datetime
    """
    Timestamp when the store's `name`, `description`, or `metadata` was last
    modified. Memory writes inside the store do not advance this.
    """
