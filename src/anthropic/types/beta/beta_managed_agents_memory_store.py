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
    """The unique ID of the memory store (`memstore_...`).

    Use it to attach the store to a session.
    """

    archived_at: Optional[datetime] = None
    """When the memory store was archived, in RFC 3339, or `null` if it hasn't been.

    Archiving can't be undone. An archived store can't be attached to new sessions.
    You can't create or update its memories or update the store. You can still read
    and delete its memories, redact their versions, and delete the store.

    See the
    [memory guide](https://platform.claude.com/docs/en/managed-agents/memory#archive-a-store)
    to learn more about archiving.
    """

    created_at: datetime
    """When the memory store was created, in RFC 3339."""

    description: str
    """Free-text description of what the store contains, up to 1,024 characters.

    Included in the agent's system prompt when the store is attached, so word it to
    be useful to the agent. Empty string when unset.
    """

    metadata: Dict[str, str]
    """
    Key-value pairs for your own use, such as the end user that the store belongs
    to.

    A store has at most 16 pairs. Keys are 1 to 64 characters long and values at
    most 512 characters. You can't filter lists by metadata.
    """

    name: str
    """Human-readable name for the store.

    1–255 characters. The store's mount-path slug under `/mnt/memory/` is derived
    from this name.
    """

    type: Literal["memory_store"]

    updated_at: datetime
    """When the memory store was last changed, in RFC 3339.

    Changing its `name`, `description`, or `metadata` updates it. Archiving the
    store does too. Changes to the store's memories don't.
    """
