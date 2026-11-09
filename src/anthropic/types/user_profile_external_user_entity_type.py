from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileExternalUserEntityType"]

UserProfileExternalUserEntityType: TypeAlias = Literal["individual", "business", "non_profit", "government"]
