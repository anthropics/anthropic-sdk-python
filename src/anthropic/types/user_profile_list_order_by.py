from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileListOrderBy"]

UserProfileListOrderBy: TypeAlias = Literal["created_at", "name"]
"""
Sort field for listing user profiles: `created_at` (default) or `name` (case-insensitive; profiles without a name sort last).

- `created_at` - Sort by when each user profile was created. This is the default.
- `name` - Sort by `name`, ignoring the case of ASCII letters. Profiles without a name come last in either direction.
"""
