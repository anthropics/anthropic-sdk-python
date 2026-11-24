from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileExternalUserAccountStatus"]

UserProfileExternalUserAccountStatus: TypeAlias = Literal["active", "suspended", "blocked"]
"""
The status of the entity's account on the platform, as the platform states it: `active`; `suspended`, when the platform has restricted the account and may restore it; or `blocked`, when the platform has barred it. It records the platform's decision only. The statuses that Anthropic itself reports for the profile, such as its status in a program, are Anthropic's decisions and do not change with it.

- `active` - The platform has neither restricted nor barred the account of the entity that the user profile represents.
- `suspended` - The platform has restricted the account of the entity that the user profile represents and may restore it.
- `blocked` - The platform has barred the account of the entity that the user profile represents.
"""
