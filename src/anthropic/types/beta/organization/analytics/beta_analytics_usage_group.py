from typing import Optional

from ....._models import BaseModel
from ..beta_analytics_actor import BetaAnalyticsActor
from ..beta_analytics_speed import BetaAnalyticsSpeed
from ..beta_analytics_actor_type import BetaAnalyticsActorType
from ..beta_analytics_service_tier import BetaAnalyticsServiceTier
from ..beta_analytics_context_window import BetaAnalyticsContextWindow
from ..beta_analytics_claude_tag_category import BetaAnalyticsClaudeTagCategory
from ..beta_analytics_usage_cost_inference_geo import BetaAnalyticsUsageCostInferenceGeo

__all__ = ["BetaAnalyticsUsageGroup"]


class BetaAnalyticsUsageGroup(BaseModel):
    """
    The dimension values one usage row is broken out by; each is null
    unless its dimension is in `group_by[]`.
    """

    actor: Optional[BetaAnalyticsActor] = None
    """
    The identity the usage is attributed to: the user if one is attributed, else the
    service account, else the federated (cloud-platform) identity, else the API key.
    Populated only when `actor` is in `group_by[]`; null for usage with no
    attributable identity, and for users' and federated identities' usage when the
    reader is a member who can see only some workspaces. Distinct identities the
    server cannot render also read null, each as its own row.
    """

    actor_type: Optional[BetaAnalyticsActorType] = None
    """
    Kind of identity the usage is attributed to; matches `actor.type` when `actor`
    is set. Populated only when `actor_type` is in `group_by[]`.
    """

    agent_id: Optional[str] = None
    """Claude Managed Agents agent whose session incurred the usage.

    Populated only when `agent_id` is in `group_by[]`; null for usage outside a
    managed session.
    """

    api_key_id: Optional[str] = None
    """
    API key that authenticated the requests, as a tagged API key ID, whichever
    identity `actor` resolves to. Populated only when `api_key_id` is in
    `group_by[]`; null for usage not authenticated by an API key.
    """

    claude_tag_category: Optional[BetaAnalyticsClaudeTagCategory] = None
    """
    Claude Tag (Claude in Slack) spend category: `engaged` (a person addressed
    Claude in a channel or thread), `proactive` (Claude responded without being
    addressed), `scheduled` (a scheduled routine ran), `monitoring` (Claude watching
    a channel it was asked to monitor), or `dm` (direct messages with Claude).
    Populated only when `claude_tag_category` is in `group_by[]`; null for usage
    that is not Claude Tag. Direct-message usage is billed to the individual user
    and is reported under that user's product, not under `claude_tag`. New
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

    deployment_id: Optional[str] = None
    """Deployment that started the Claude Managed Agents session.

    Populated only when `deployment_id` is in `group_by[]`; null for usage outside a
    managed session and for sessions no deployment started.
    """

    environment_id: Optional[str] = None
    """Claude Managed Agents environment the session ran in.

    Populated only when `environment_id` is in `group_by[]`; null for usage outside
    a managed session.
    """

    inference_geo: Optional[BetaAnalyticsUsageCostInferenceGeo] = None
    """Inference region of the usage or cost.

    Null unless `inference_geo` is in `group_by[]`; it can also be null on grouped
    rows where the region is not set (the rows that `inference_geos[]=not_available`
    matches).
    """

    model: Optional[str] = None
    """
    Model that produced the usage or cost, as a model name in the form the
    `models[]` filter accepts (for example, `claude-opus-5-5`). Null unless `model`
    is in `group_by[]`; it can also be null on grouped rows whose usage or cost is
    not attributed to a specific model, such as code execution.
    """

    product: Optional[str] = None
    """Product surface that produced the usage or cost.

    Null unless product is in `group_by[]`; it can also be null on grouped rows
    whose usage cannot be attributed to a known surface. Values include `chat`,
    `claude_code`, `cowork`, `office_agent`, `claude_in_chrome`, `claude_design`,
    `claude_tag`, and `chat_cowork_unified`. `claude_tag` is Claude Tag, the Claude
    product in Slack. `chat_cowork_unified` is Chat and Cowork unified, Cowork's
    features inside claude.ai chat: chat and Cowork usage by a member who has it
    turned on is reported under this value instead of `chat` or `cowork`. It is
    accepted as a filter only on deployments that offer Chat and Cowork unified.
    Some unattributed usage is reported as "other".
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

    service_tier: Optional[BetaAnalyticsServiceTier] = None
    """Service tier the usage was served at.

    Populated only when `service_tier` is in `group_by[]`; null for usage with no
    service tier (for example, code execution) and for Claude Enterprise usage.
    """

    session_id: Optional[str] = None
    """Claude Managed Agents session that incurred the usage.

    Populated only when `session_id` is in `group_by[]`; null for usage outside a
    managed session.
    """

    slack_channel_id: Optional[str] = None
    """Slack channel the usage originated from.

    Populated only when `slack_channel_id` is in `group_by[]`; null for usage
    outside Slack (and for rows recorded before channel attribution was enabled).
    """

    speed: Optional[BetaAnalyticsSpeed] = None
    """Inference speed mode of the usage or cost: `fast` or `standard`.

    Null unless `speed` is in `group_by[]`.
    """

    user_profile_id: Optional[str] = None
    """User profile the usage was attributed to, as a tagged `uprof_` ID.

    Populated only when `user_profile_id` is in `group_by[]`; null for usage that
    named no profile and for Claude Enterprise usage.
    """

    workspace_id: Optional[str] = None
    """
    Workspace the usage occurred in, as a tagged workspace ID, including the
    organization's default workspace. Populated only when `workspace_id` is in
    `group_by[]`; null for Claude Enterprise usage.
    """
