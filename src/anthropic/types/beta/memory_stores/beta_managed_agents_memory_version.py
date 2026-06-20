# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_actor import BetaManagedAgentsActor
from .beta_managed_agents_memory_version_operation import BetaManagedAgentsMemoryVersionOperation

__all__ = ["BetaManagedAgentsMemoryVersion"]


class BetaManagedAgentsMemoryVersion(BaseModel):
    """
    A `memory_version` object: one immutable, attributed row in a memory's append-only history. Every non-no-op mutation to a memory produces a new version. Versions belong to the store (not the individual memory) and persist after the memory is deleted. Retrieving a redacted version returns 200 with `content`, `path`, `content_size_bytes`, and `content_sha256` set to `null`; branch on `redacted_at`, not HTTP status.
    """

    id: str
    """Unique identifier for this version (a `memver_...` value)."""

    created_at: datetime
    """A timestamp in RFC 3339 format"""

    memory_id: str
    """ID of the memory this version snapshots (a `mem_...` value).

    Remains valid after the memory is deleted; pass it as `memory_id` to
    [List memory versions](/en/api/beta/memory_stores/memory_versions/list) to
    retrieve the full lineage including the `deleted` row.
    """

    memory_store_id: str
    """ID of the memory store this version belongs to (a `memstore_...` value)."""

    operation: BetaManagedAgentsMemoryVersionOperation
    """The kind of mutation a `memory_version` records.

    Every non-no-op mutation to a memory appends exactly one version row with one of
    these values.
    """

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
    """Identifies who performed a write or redact operation.

    Captured at write time on the `memory_version` row. The API key that created a
    session is not recorded on agent writes; attribution answers who made the write,
    not who is ultimately responsible. Look up session provenance separately via the
    [Sessions API](/en/api/sessions-retrieve).
    """

    path: Optional[str] = None
    """The memory's path at the time of this write.

    `null` if and only if `redacted_at` is set.
    """

    redacted_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    redacted_by: Optional[BetaManagedAgentsActor] = None
    """Identifies who performed a write or redact operation.

    Captured at write time on the `memory_version` row. The API key that created a
    session is not recorded on agent writes; attribution answers who made the write,
    not who is ultimately responsible. Look up session provenance separately via the
    [Sessions API](/en/api/sessions-retrieve).
    """
