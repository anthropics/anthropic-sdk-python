from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsMemory"]


class BetaManagedAgentsMemory(BaseModel):
    """A text document at a path inside a memory store.

    `content` is `null` when the response uses `view=basic`. `content_size_bytes` and `content_sha256` are always set, so you can detect changes without fetching the content. To retrieve, update, or delete a memory, pass its ID, which stays the same when its path changes.

    See the [memory guide](https://platform.claude.com/docs/en/managed-agents/memory#view-and-edit-memories) to learn more about working with memories.
    """

    id: str
    """The unique ID of the memory (`mem_...`).

    It stays the same when the memory's path changes.

    To retrieve, update, or delete the memory, pass this ID.
    """

    content_sha256: str
    """Lowercase hex SHA-256 digest of the UTF-8 `content` bytes (64 characters).

    The server applies no normalization, so clients can compute the same hash
    locally for staleness checks and as the value for a `content_sha256`
    precondition on update. Always populated, regardless of `view`.
    """

    content_size_bytes: int
    """The size of the memory's `content` in UTF-8 bytes.

    It is set regardless of `view`.
    """

    created_at: datetime
    """When this memory was created, in RFC 3339 format."""

    memory_store_id: str
    """ID of the memory store this memory belongs to (a `memstore_...` value)."""

    memory_version_id: str
    """
    The ID of the memory version that holds the memory's current content
    (`memver_...`).

    Memory versions don't have a flag that marks the latest one. Compare their IDs
    with this field instead.

    See the
    [memory guide](https://platform.claude.com/docs/en/managed-agents/memory#audit-memory-changes)
    to learn more about memory versions.
    """

    path: str
    """Hierarchical path of the memory within the store, e.g.

    `/projects/foo/notes.md`. Always starts with `/`. Paths are case-sensitive and
    unique within a store. Maximum 1,024 bytes.
    """

    type: Literal["memory"]

    updated_at: datetime
    """When the memory was last changed, in RFC 3339.

    To find out who made the change, look at `created_by` on the memory version that
    `memory_version_id` references.
    """

    content: Optional[str] = None
    """The memory's UTF-8 text content, or `null` when the response uses `view=basic`.

    The maximum size is 100 kB (102,400 bytes).
    """
