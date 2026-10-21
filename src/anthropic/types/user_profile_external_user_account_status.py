from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileExternalUserAccountStatus"]

UserProfileExternalUserAccountStatus: TypeAlias = Literal["active", "suspended", "blocked"]
