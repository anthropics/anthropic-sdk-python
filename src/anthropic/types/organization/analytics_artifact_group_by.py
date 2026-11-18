from typing_extensions import Literal, TypeAlias

__all__ = ["AnalyticsArtifactGroupBy"]

AnalyticsArtifactGroupBy: TypeAlias = Literal["product", "rbac_group_id", "user_id"]
