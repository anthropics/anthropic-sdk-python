# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

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

    created_at: datetime
    """A timestamp in RFC 3339 format"""

    name: str
    """Human-readable name for the store.

    1–255 characters. The store's mount-path slug under `/mnt/memory/` is derived
    from this name.
    """

    type: Literal["memory_store"]

    updated_at: datetime
    """A timestamp in RFC 3339 format"""

    archived_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    description: Optional[str] = None
    """Free-text description of what the store contains, up to 1024 characters.

    Included in the agent's system prompt when the store is attached, so word it to
    be useful to the agent. Empty string when unset.
    """

    metadata: Optional[Dict[str, str]] = None
    """
    Arbitrary key-value tags for your own bookkeeping (such as the end user a store
    belongs to). Up to 16 pairs; keys 1–64 characters; values up to 512 characters.
    Returned on retrieve/list but not filterable.
    """
