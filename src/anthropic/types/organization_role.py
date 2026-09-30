from typing_extensions import Literal, TypeAlias

__all__ = ["OrganizationRole"]

OrganizationRole: TypeAlias = Literal[
    "admin", "billing", "claude_code_user", "developer", "managed", "membership_admin", "owner", "primary_owner", "user"
]
