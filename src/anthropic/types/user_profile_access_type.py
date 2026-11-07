from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileAccessType"]

UserProfileAccessType: TypeAlias = Literal["application", "passthrough"]
