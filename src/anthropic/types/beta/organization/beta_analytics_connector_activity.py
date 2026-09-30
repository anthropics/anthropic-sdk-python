from typing import Optional

from ...._models import BaseModel
from .beta_analytics_connector_chat_metrics import BetaAnalyticsConnectorChatMetrics
from .beta_analytics_connector_cowork_metrics import BetaAnalyticsConnectorCoworkMetrics
from .beta_analytics_connector_office_metrics import BetaAnalyticsConnectorOfficeMetrics
from .beta_analytics_connector_claude_code_metrics import BetaAnalyticsConnectorClaudeCodeMetrics

__all__ = ["BetaAnalyticsConnectorActivity"]


class BetaAnalyticsConnectorActivity(BaseModel):
    """Per-connector activity data for a given day."""

    chat_metrics: BetaAnalyticsConnectorChatMetrics
    """Claude.ai activity metrics for a single connector on a given day."""

    claude_code_metrics: BetaAnalyticsConnectorClaudeCodeMetrics
    """Claude Code activity metrics for a single connector on a given day."""

    connector_name: str
    """Name of the connector.

    Some rows carry an opaque connector id here instead of a readable name;
    `connector_display_name` holds the resolved name for those rows.
    """

    cowork_metrics: BetaAnalyticsConnectorCoworkMetrics
    """Cowork activity metrics for a single connector on a given day."""

    distinct_user_count: int
    """
    Number of distinct users who used the connector on the requested day, or, in
    date-range mode, over the requested window — recomputed as an exact distinct
    count over the window's per-member daily rows, never a sum of per-day values.
    """

    office_metrics: BetaAnalyticsConnectorOfficeMetrics
    """
    Office Agent activity metrics for a single connector on a given day, broken out
    by Office product.
    """

    connector_display_name: Optional[str] = None
    """
    Human-readable display name for rows whose `connector_name` is an opaque
    connector id rather than a readable name, resolved at request time from the
    organization's connectors (including connectors that have since been removed).
    `connector_name` remains the row's stable key for sorting and pagination, and
    `filter[]=connector_name:{value}` also matches these rows by display name.
    Display names are not unique, and the same connector's claude.ai usage can
    appear under a separate row with a readable `connector_name`. Null when
    `connector_name` is already a readable name, when the id cannot be resolved to
    one of the organization's connectors, or when display-name resolution is not
    enabled for this organization.
    """

    individual_auth_distinct_user_count: Optional[int] = None
    """
    Number of distinct users whose use of this connector on the requested day ran on
    their own individual credential, connected through their own consent flow.
    Companion bucket to `managed_auth_distinct_user_count`, which carries the
    measurement, attribution, and null rules. Users whose requests used no stored
    credential count in neither bucket.
    """

    managed_auth_distinct_user_count: Optional[int] = None
    """
    Number of distinct users whose use of this connector on the requested day ran on
    Enterprise Managed Auth (an organization-managed credential provisioned through
    the organization's identity provider), read from the token record each request
    used. Null, never 0, when managed-auth reporting is not enabled for the
    organization, the value cannot be attributed to the row, no credentialed
    requests and no managed-token mint events (a managed credential being
    provisioned for a user's use of the connector) were observed that day, or the
    day predates 2026-07-01, the first day the backing data exists (forward-only
    data, no backfill). When credentialed requests or mint events were observed and
    attributed, both managed-auth fields populate, reporting 0 for a bucket with no
    users; the two counts are independent, not a partition — a user whose requests
    that day used both kinds of credential counts in both. Mint events carry user
    but not surface attribution, so they count as observed auth activity on
    `user_id` and `rbac_group_id` cuts — attributed to the user the credential was
    provisioned for — but never on a cut that references `product` (group or
    filter). Date-range rollup mode (`starting_date`/`ending_date`) computes both
    fields exactly over the window — distinct users with at least one qualifying day
    — when the whole window starts on or after 2026-07-01, with the null-versus-0
    and mint-event rules applying with the window in place of the day; a range
    starting earlier reports every managed-auth field as null, never a
    partial-window value.
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

    read_call_count: Optional[int] = None
    """
    Number of connector tool calls on the requested day whose trusted read-only
    annotation marked them read-only. Call count, not distinct users. Every call
    recorded on a classified surface lands in exactly one of `read_call_count`,
    `write_call_count`, or `unclassified_call_count`, so the three sum to the day's
    classified calls. Classification is forward-only per surface: claude.ai from
    2026-06-01, Claude Code from 2026-05-30, Claude in Office from 2026-05-29,
    Cowork from 2026-06-02 (Cowork clients predating annotation forwarding land in
    `unclassified_call_count`). Null, never 0, when the value cannot be stated: the
    read/write split is not enabled for this organization, or the day predates
    2026-05-29. For a date-range total, sum the per-day values, but treat a window
    that extends before 2026-05-29 as null rather than summing only its covered days
    — date-range rollup mode (`starting_date`/`ending_date`) applies both rules
    server-side.
    """

    unclassified_call_count: Optional[int] = None
    """
    Number of connector tool calls on the requested day with no trusted read-only
    annotation — the annotation is optional in the MCP spec and is discarded when
    connector access controls are active, so unclassified calls are common. This
    field shows how much of the day's classified activity the read/write split
    actually covers. Call count, not distinct users. One of the three
    call-classification buckets; see `read_call_count` for the per-surface
    data-start dates, null conditions, and date-range guidance.
    """

    user_id: Optional[str] = None
    """Tagged user identifier (e.g.

    `user_...`). Present only when the request grouped by `user_id`.
    """

    write_call_count: Optional[int] = None
    """
    Number of connector tool calls on the requested day whose trusted read-only
    annotation marked them not read-only. Call count, not distinct users. One of the
    three call-classification buckets; see `read_call_count` for the per-surface
    data-start dates, null conditions, and date-range guidance.
    """
