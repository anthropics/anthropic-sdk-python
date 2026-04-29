# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsMemory"]


class BetaManagedAgentsMemory(BaseModel):
    """
    A `memory` object: a single text document at a hierarchical path inside a memory store. The `content` field is populated when `view=full` and `null` when `view=basic`; the `content_size_bytes` and `content_sha256` fields are always populated so sync clients can diff without fetching content. Memories are addressed by their `mem_...` ID; the path is the create key and can be changed via update.
    """

    id: str
    """Unique identifier for this memory (a `mem_...` value).

    Stable across renames; use this ID, not the path, to read, update, or delete the
    memory.
    """

    content_sha256: str
    """Lowercase hex SHA-256 digest of the UTF-8 `content` bytes (64 characters).

    The server applies no normalization, so clients can compute the same hash
    locally for staleness checks and as the value for a `content_sha256`
    precondition on update. Always populated, regardless of `view`.
    """

    content_size_bytes: int
    """Size of `content` in bytes (the UTF-8 plaintext length).

    Always populated, regardless of `view`.
    """

    created_at: datetime
    """A timestamp in RFC 3339 format"""

    memory_store_id: str
    """ID of the memory store this memory belongs to (a `memstore_...` value)."""

    memory_version_id: str
    """
    ID of the `memory_version` representing this memory's current content (a
    `memver_...` value). This is the authoritative head pointer; `memory_version`
    objects do not carry an `is_latest` flag, so compare against this field instead.
    Enumerate the full history via
    [List memory versions](/en/api/beta/memory_stores/memory_versions/list).
    """

    path: str
    """Hierarchical path of the memory within the store, e.g.

    `/projects/foo/notes.md`. Always starts with `/`. Paths are case-sensitive and
    unique within a store. Maximum 1,024 bytes.
    """

    type: Literal["memory"]

    updated_at: datetime
    """A timestamp in RFC 3339 format"""

    content: Optional[str] = None
    """The memory's UTF-8 text content.

    Populated when `view=full`; `null` when `view=basic`. Maximum 100 kB (102,400
    bytes).
    """
