# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["BetaNoBillingWorkspaceRole"]

BetaNoBillingWorkspaceRole: TypeAlias = Literal[
    "workspace_admin", "workspace_developer", "workspace_restricted_developer", "workspace_user"
]
