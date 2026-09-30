from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from ..beta_cache_creation import BetaCacheCreation
from .beta_analytics_user_actor import BetaAnalyticsUserActor
from .beta_analytics_context_window import BetaAnalyticsContextWindow
from .beta_analytics_server_tool_use import BetaAnalyticsServerToolUse
from .beta_analytics_claude_tag_category import BetaAnalyticsClaudeTagCategory

__all__ = ["BetaAnalyticsUsageUsersItem"]


class BetaAnalyticsUsageUsersItem(BaseModel):
    actor: BetaAnalyticsUserActor
    """The user this row's usage or cost is attributed to. Always a `user_actor`."""

    cache_creation: BetaCacheCreation
    """The number of input tokens for cache creation."""

    cache_read_input_tokens: int
    """The number of input tokens read from the cache."""

    claude_tag_category: Optional[BetaAnalyticsClaudeTagCategory] = None
    """
    Claude Tag (Claude in Slack) spend category: `engaged` (a person addressed
    Claude in a channel or thread), `proactive` (Claude responded without being
    addressed), `scheduled` (a scheduled routine ran), `monitoring` (Claude watching
    a channel it was asked to monitor), or `dm` (direct messages with Claude).
    Populated only when `claude_tag_category` is in `group_by[]`; null for usage
    that is not Claude Tag. Direct-message usage is billed to the individual user
    and is reported under that user's product, not under `claude-tag`. New
    categories may be added over time.
    """

    claude_tag_user_id: Optional[str] = None
    """
    Slack user ID (for example `U0123ABCDEF`) of the member the Claude Tag (Claude
    in Slack) usage is attributed to, not a claude.ai user ID. Populated only when
    `claude_tag_user_id` is in `group_by[]`; null for usage that is not Claude Tag
    and for Claude Tag usage that is not attributed to a single user (for example
    `monitoring`, and `proactive` usage Claude initiated), so per-user rows can sum
    to less than the Claude Tag total. Cannot be combined with
    `group_by[]=rbac_group_id` or the `rbac_group_ids[]` filter.
    """

    context_window: Optional[BetaAnalyticsContextWindow] = None
    """Context-window pricing tier of the usage or cost.

    Null unless `context_window` is in `group_by[]`; it can also be null on grouped
    rows with no context-window tier, such as code execution.
    """

    ending_at: Optional[datetime] = None
    """
    End of the row's UTC time bucket (exclusive), as an RFC 3339 timestamp; equal to
    `starting_at` plus one `bucket_width`. Null unless `bucket_width` is set.
    """

    inference_geo: Optional[Literal["global", "us"]] = None
    """Inference region of the usage or cost.

    Null unless `inference_geo` is in `group_by[]`; it can also be null on grouped
    rows where the region is not set (the rows that `inference_geos[]=not_available`
    matches).
    """

    model: Optional[str] = None
    """
    Model that produced the usage or cost, as a model name in the form the
    `models[]` filter accepts (for example, `claude-opus-5`). Null unless `model` is
    in `group_by[]`; it can also be null on grouped rows whose usage or cost is not
    attributed to a specific model, such as code execution.
    """

    output_tokens: int
    """The number of output tokens generated."""

    product: Optional[str] = None
    """Product surface that produced the usage or cost.

    Null unless product is in `group_by[]`; it can also be null on grouped rows
    whose usage cannot be attributed to a known surface. Values include `chat`,
    `claude_code`, `cowork`, `office_agent`, `claude_in_chrome`, `claude_design`,
    and `claude-tag`. `claude-tag` is Claude Tag, the Claude product in Slack. Some
    unattributed usage is reported as "other".
    """

    rbac_group_id: Optional[str] = None
    """
    RBAC group (team) the usage is attributed to, in the public tagged
    `rbac_group_...` spelling — the same spelling the activity resources use for
    this key, so the same team has one id across resources and it round-trips as an
    `rbac_group_ids[]` filter value. Populated only when `rbac_group_id` is in
    `group_by[]`. Any-membership semantics: a user in several groups contributes
    their full usage to each of those groups' rows, so the named-group rows overlap
    and their sum can exceed the org total. A null value is the single unassigned
    row: users in no group on that (UTC) day. For the true org total, run the same
    query without `group_by[]`.
    """

    requests: Optional[int] = None
    """Number of API requests in this row's scope.

    For sandbox / code-execution events, this counts execution spans rather than
    HTTP requests (these rows surface with `product: null`).
    """

    server_tool_use: BetaAnalyticsServerToolUse
    """Server-side tool usage metrics."""

    slack_channel_id: Optional[str] = None
    """Slack channel the usage originated from.

    Populated only when `slack_channel_id` is in `group_by[]`; null for usage
    outside Slack (and for rows recorded before channel attribution was enabled).
    """

    speed: Optional[Literal["fast", "standard"]] = None
    """Inference speed mode of the usage or cost: `fast` or `standard`.

    Null unless `speed` is in `group_by[]`.
    """

    starting_at: Optional[datetime] = None
    """Start of the row's UTC time bucket (inclusive), as an RFC 3339 timestamp.

    Null unless `bucket_width` is set; without `bucket_width`, each row aggregates
    the full requested range.
    """

    total_tokens: int
    """Total token count across all token types.

    This is the value the default `order_by` (`total_tokens`) sorts on.
    """

    uncached_input_tokens: int
    """The number of uncached input tokens processed."""
