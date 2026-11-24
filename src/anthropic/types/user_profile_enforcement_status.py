from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileEnforcementStatus"]

UserProfileEnforcementStatus: TypeAlias = Literal["unrestricted", "pending", "restricted", "banned"]
"""
Anthropic's enforcement status of this profile: `unrestricted`, `pending`, `restricted` or `banned`. More values may be added; read a value you do not recognize as `restricted`.
"""
