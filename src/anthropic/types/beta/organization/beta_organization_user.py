# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from ..beta_organization_role import BetaOrganizationRole

__all__ = ["BetaOrganizationUser"]


class BetaOrganizationUser(BaseModel):
    id: str
    """ID of the User."""

    added_at: datetime
    """RFC 3339 datetime string indicating when the User joined the Organization."""

    email: str
    """Email of the User."""

    name: str
    """Name of the User."""

    role: BetaOrganizationRole
    """Organization role of the User."""

    type: Literal["user"]
    """Object type.

    For Users, this is always `"user"`.
    """
