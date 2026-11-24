from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileEnforcementActionNextStep"]

UserProfileEnforcementActionNextStep: TypeAlias = Literal["verify"]
"""
The next step on this enforcement action: `verify` means the end user can clear the action by passing an identity check. More values may be added; read a value you do not recognize as `null`.
"""
