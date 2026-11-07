from typing_extensions import Literal, TypeAlias

__all__ = ["NoBillingWorkspaceRole"]

NoBillingWorkspaceRole: TypeAlias = Literal[
    "workspace_admin", "workspace_developer", "workspace_restricted_developer", "workspace_user"
]
