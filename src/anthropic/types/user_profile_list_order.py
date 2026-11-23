from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileListOrder"]

UserProfileListOrder: TypeAlias = Literal["asc", "desc"]
"""The direction that a list of user profiles is sorted in.

- `asc` - Oldest first when `order_by` is `created_at`, or names in ascending order when `order_by` is `name`.
- `desc` - Newest first when `order_by` is `created_at`, or names in descending order when `order_by` is `name`. This is the default.
"""
