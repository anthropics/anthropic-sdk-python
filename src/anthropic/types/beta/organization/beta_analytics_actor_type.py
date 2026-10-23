from typing_extensions import Literal, TypeAlias

__all__ = ["BetaAnalyticsActorType"]

BetaAnalyticsActorType: TypeAlias = Literal["api_actor", "federated_actor", "service_account_actor", "user_actor"]
