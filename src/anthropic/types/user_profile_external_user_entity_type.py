from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileExternalUserEntityType"]

UserProfileExternalUserEntityType: TypeAlias = Literal["individual", "business", "non_profit", "government"]
"""
What kind of entity the profile represents, as the platform states it: `individual`, `business`, `non_profit` or `government`.
"""
