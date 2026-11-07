from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileEnforcementStatus"]

UserProfileEnforcementStatus: TypeAlias = Literal["unrestricted", "pending", "restricted", "banned"]
