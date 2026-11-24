from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileEnforcementActionReason"]

UserProfileEnforcementActionReason: TypeAlias = Literal[
    "unsupported_region", "fraud_or_abuse", "high_harm", "usage_policy_violation", "account_compromise", "unspecified"
]
"""
Why Anthropic placed this enforcement action: `unsupported_region`, `fraud_or_abuse`, `high_harm`, `usage_policy_violation`, `account_compromise` or `unspecified`. More values may be added; read a value you do not recognize as `unspecified`.
"""
