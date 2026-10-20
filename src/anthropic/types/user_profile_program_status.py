from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileProgramStatus"]

UserProfileProgramStatus: TypeAlias = Literal["active", "pending", "rejected"]
