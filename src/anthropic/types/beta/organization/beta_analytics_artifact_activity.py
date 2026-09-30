from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsArtifactActivity"]


class BetaAnalyticsArtifactActivity(BaseModel):
    """
    Artifact-creation activity for one (`artifact_type`, `is_shared`) bucket
    on a given day.

    Artifacts form a small finite cube — the canonical MIME type (8 values incl.
    `other`) crossed with shared-vs-private — so the response is the full set of
    non-empty buckets, not a ranked/paginated list. Claude Code and Cowork
    artifacts report under `text/html` and are counted from 2026-08-17
    onward; earlier days contain claude.ai chat artifacts only. With
    `group_by[]=product` / `user_id` / `rbac_group_id` each row is further
    split by the flat group keys and counts are scoped to that cut.
    """

    artifact_type: str
    """Canonical artifact MIME type (e.g.

    `text/markdown`, `application/vnd.ant.react`, `image/svg+xml`), or `other`.
    Claude Code and Cowork artifacts report as `text/html`.
    """

    artifacts_created_count: int
    """Number of artifacts created in this bucket on the requested day"""

    distinct_user_count: int
    """
    Number of distinct users who created artifacts in this bucket on the requested
    day
    """

    is_shared: bool
    """
    Whether the artifacts in this bucket have ever been shared (a Claude Code /
    Cowork artifact is shared once anyone beyond its creator may open it: named
    members, the whole organization, or anyone with the link).
    """

    published_artifacts_created_count: int
    """
    Number of those artifacts that have been published (for Claude Code / Cowork
    artifacts: open to anyone with the link); never exceeds
    `artifacts_created_count`
    """

    product: Optional[str] = None
    """
    Product that produced this row's activity: one of `chat`, `claude_code`,
    `cowork`, or `office_agent` (the canonical Cost & Usage product naming; an
    `office_agent` row's per-surface breakdown is in its `office_metrics`). On
    `/plugins` only `cowork` and `claude_code` occur (the only surfaces with plugin
    attribution); on `/artifacts` only `chat`, `claude_code`, and `cowork` occur
    (the surfaces that create artifacts); `/apps/chat/projects` does not support the
    product dimension (a `product` entry in `group_by[]` or `filter[]` there is
    rejected). Present only when the request grouped by `product`.
    """

    rbac_group_id: Optional[str] = None
    """
    Tagged RBAC group identifier (`rbac_group_...`), matching the spend-limits API
    spelling. Present only when the request grouped by `rbac_group_id`.
    """

    rbac_group_name: Optional[str] = None
    """
    Resolved RBAC group display name, alongside `rbac_group_id` when name resolution
    is available. Null if the group has been deleted or its name could not be
    resolved; `rbac_group_id` remains the stable key.
    """

    user_id: Optional[str] = None
    """Tagged user identifier (e.g.

    `user_...`). Present only when the request grouped by `user_id`.
    """
