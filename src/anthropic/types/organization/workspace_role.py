from typing_extensions import Literal, TypeAlias

__all__ = ["WorkspaceRole"]

WorkspaceRole: TypeAlias = Literal[
    "workspace_admin", "workspace_billing", "workspace_developer", "workspace_restricted_developer", "workspace_user"
]
