from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_actor import BetaManagedAgentsActor
from .beta_managed_agents_memory_version_operation import BetaManagedAgentsMemoryVersionOperation

__all__ = ["BetaManagedAgentsMemoryVersion"]


class BetaManagedAgentsMemoryVersion(BaseModel):
    """One entry in a memory's history, recording a single change and who made it.

    Every change to a memory adds one version. Only redaction can change a version after that. Versions belong to the memory store and stay after the memory is deleted. Each version is retained for at least the version retention period after it was written, unless the store itself is deleted.

    Retrieving a redacted version succeeds, with `content`, `path`, `content_size_bytes`, and `content_sha256` set to `null`. Check `redacted_at` to find out whether a version was redacted.

    See the [memory guide](https://platform.claude.com/docs/en/managed-agents/memory#audit-memory-changes) to learn more about memory versions.
    """

    id: str
    """Unique identifier for this version (a `memver_...` value)."""

    created_at: datetime
    """When this version was written, in RFC 3339 format."""

    memory_id: str
    """The ID of the memory that this version belongs to (`mem_...`).

    The ID stays valid after the memory is deleted. Pass it as `memory_id` to
    [List Memory Versions](https://platform.claude.com/docs/en/api/beta/memory_stores/memory_versions/list)
    to get the memory's retained versions, including its `deleted` version while the
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
    """Who made this change to the memory, or `null` if the author wasn't recorded.

    Redacting the version doesn't change this field. A `session_actor` here is an
    agent that wrote through the store's mounted filesystem at `/mnt/memory/`. The
    version doesn't record the API key that created that session. So the author in
    `created_by` is who made the change, not who is ultimately responsible for it.

    You can
    [retrieve the session](https://platform.claude.com/docs/en/api/beta/sessions/retrieve)
    to learn more about where the change came from.
    """

    path: Optional[str] = None
    """The memory's path at the time of this write.

    `null` if and only if `redacted_at` is set.
    """

    redacted_at: Optional[datetime] = None
    """When the version was redacted, in RFC 3339, or `null` if it hasn't been.

    When set, `content`, `path`, `content_size_bytes`, and `content_sha256` are
    `null`.

    See the
    [memory guide](https://platform.claude.com/docs/en/managed-agents/memory#redact-a-version)
    to learn more about redaction.
    """

    redacted_by: Optional[BetaManagedAgentsActor] = None
    """Who redacted this version, or `null` if it has not been redacted.

    In practice always an `api_actor`, `user_actor`, or `service_account_actor`
    (agents do not have a redact capability).
    """
