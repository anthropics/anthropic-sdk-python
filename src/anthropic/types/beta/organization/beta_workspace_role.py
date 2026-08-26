# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["BetaWorkspaceRole"]

BetaWorkspaceRole: TypeAlias = Literal[
    "workspace_admin", "workspace_billing", "workspace_developer", "workspace_restricted_developer", "workspace_user"
]
