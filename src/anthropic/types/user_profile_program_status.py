from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileProgramStatus"]

UserProfileProgramStatus: TypeAlias = Literal["active", "pending", "rejected"]
"""A user profile's status in a program.

Each program's `status` field says what the values mean there.

- `active` - The profile is in the program.
- `pending` - The profile is not in the program yet, and something is still awaited.
- `rejected` - The profile is not in the program and nothing is awaited: Anthropic has declined, or has withdrawn an earlier approval.
"""
