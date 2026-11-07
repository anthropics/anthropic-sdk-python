from typing_extensions import Literal, TypeAlias

__all__ = ["BetaAnalyticsCostGroupBy"]

BetaAnalyticsCostGroupBy: TypeAlias = Literal[
    "actor",
    "actor_type",
    "agent_id",
    "api_key_id",
    "claude_tag_category",
    "claude_tag_user_id",
    "context_window",
    "cost_type",
    "deployment_id",
    "environment_id",
    "inference_geo",
    "model",
    "product",
    "rbac_group_id",
    "service_tier",
    "session_id",
    "slack_channel_id",
    "speed",
    "token_type",
    "user_profile_id",
    "workspace_id",
]
