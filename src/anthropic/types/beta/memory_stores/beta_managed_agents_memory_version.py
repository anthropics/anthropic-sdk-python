from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_actor import BetaManagedAgentsActor
from .beta_managed_agents_memory_version_operation import BetaManagedAgentsMemoryVersionOperation

__all__ = ["BetaManagedAgentsMemoryVersion"]


class BetaManagedAgentsMemoryVersion(BaseModel):
    """
    A `memory_version` object: one immutable, attributed row in a memory's append-only history. Every non-no-op mutation to a memory produces a new version. Versions belong to the store (not the individual memory) and are not deleted with the memory; each version is retained for at least the version retention period after it was written, unless the store itself is deleted. Retrieving a redacted version returns 200 with `content`, `path`, `content_size_bytes`, and `content_sha256` set to `null`; branch on `redacted_at`, not HTTP status.
    """

    id: str
    """Unique identifier for this version (a `memver_...` value)."""

    created_at: datetime
    """When this version was written, in RFC 3339 format."""

    memory_id: str
    """ID of the memory this version snapshots (a `mem_...` value).

    Remains valid after the memory is deleted; pass it as `memory_id` to
    [List memory versions](/en/api/beta/memory_stores/memory_versions/list) to
    retrieve the memory's retained versions, including the `deleted` row while the
    lineage is retained.
    """

    memory_store_id: str
    """ID of the memory store this version belongs to (a `memstore_...` value)."""

    operation: BetaManagedAgentsMemoryVersionOperation
    """The kind of mutation this version records: `created`, `modified`, or `deleted`."""

    type: Literal["memory_version"]

    content: Optional[str] = None
    """The memory's UTF-8 text content as of this version.

    `null` when `view=basic`, when `operation` is `deleted`, or when `redacted_at`
    is set.
    """

    content_sha256: Optional[str] = None
    """Lowercase hex SHA-256 digest of `content` as of this version (64 characters).

    `null` when `redacted_at` is set or `operation` is `deleted`. Populated
    regardless of `view` otherwise.
    """

    content_size_bytes: Optional[int] = None
    """Size of `content` in bytes as of this version.

    `null` when `redacted_at` is set or `operation` is `deleted`. Populated
    regardless of `view` otherwise.
    """

    created_by: Optional[BetaManagedAgentsActor] = None
    """
    Who performed this write: one of `session_actor`, `api_actor`, `user_actor`, or
    `service_account_actor`; `null` when no writer is recorded. Captured at write
    time and preserved through redaction. A `session_actor` is an agent writing
    through the store's mounted filesystem at `/mnt/memory/`. The API key that
    created that session is not recorded on agent writes, so attribution names who
    made the write, not who is ultimately responsible; look up session provenance
    via the [Sessions API](/en/api/beta/sessions/retrieve).
    """

    path: Optional[str] = None
    """The memory's path at the time of this write.

    `null` if and only if `redacted_at` is set.
    """

    redacted_at: Optional[datetime] = None
    """
    When this version was redacted, in RFC 3339 format, or `null` if it has not been
    redacted. When set, `content`, `path`, `content_size_bytes`, and
    `content_sha256` are all `null`. See
    [Redact a memory version](/en/api/beta/memory_stores/memory_versions/redact).
    """

    redacted_by: Optional[BetaManagedAgentsActor] = None
    """Who redacted this version, or `null` if it has not been redacted.

    In practice always an `api_actor`, `user_actor`, or `service_account_actor`
    (agents do not have a redact capability).
    """
