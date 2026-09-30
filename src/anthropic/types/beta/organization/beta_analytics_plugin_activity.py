from typing import Optional

from ...._models import BaseModel
from .beta_analytics_plugin_cowork_metrics import BetaAnalyticsPluginCoworkMetrics
from .beta_analytics_plugin_claude_code_metrics import BetaAnalyticsPluginClaudeCodeMetrics

__all__ = ["BetaAnalyticsPluginActivity"]


class BetaAnalyticsPluginActivity(BaseModel):
    """Per-plugin install + invocation activity for a given day.

    With `group_by[]=user_id` / `rbac_group_id` / `product` (`cowork` /
    `claude_code` only on this endpoint) each row is one (plugin, user),
    (plugin, group), or (plugin, product) cut: the flat `user_id` /
    `rbac_group_id` / `product` keys carry the cut and the counts are
    scoped to it.
    """

    claude_code_metrics: BetaAnalyticsPluginClaudeCodeMetrics
    """Claude Code activity metrics for a single plugin on a given day."""

    cowork_metrics: BetaAnalyticsPluginCoworkMetrics
    """Cowork activity metrics for a single plugin on a given day."""

    distinct_user_count: int
    """
    Number of distinct users with recorded install or invocation activity for the
    plugin on the requested day (install-only users count), or, in date-range mode,
    over the requested window — recomputed as an exact distinct count over the
    window's per-member daily rows, never a sum of per-day values.
    """

    install_count: Optional[int] = None
    """
    Number of distinct users who installed the plugin on the requested day, or, in
    date-range mode, over the requested window — recomputed as an exact distinct
    count over the window's per-member daily rows, never a sum of per-day values.
    """

    invocation_count: int
    """Number of plugin invocations on the requested day"""

    plugin_name: str
    """Name of the plugin"""

    plugin_id: Optional[str] = None
    """Stable plugin identifier when available (e.g.

    `serena@claude-plugins-official`). Null for third-party Claude Code plugins
    (redacted at the source) and Cowork slash commands that carry only a hashed id.
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
