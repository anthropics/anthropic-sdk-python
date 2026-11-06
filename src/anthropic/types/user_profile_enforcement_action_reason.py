from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileEnforcementActionReason"]

UserProfileEnforcementActionReason: TypeAlias = Literal[
    "unsupported_region", "fraud_or_abuse", "high_harm", "usage_policy_violation", "account_compromise", "unspecified"
]
