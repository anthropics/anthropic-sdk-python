from typing_extensions import Literal, TypeAlias

__all__ = ["AnalyticsConnectorGroupBy"]

AnalyticsConnectorGroupBy: TypeAlias = Literal["product", "rbac_group_id", "user_id"]
