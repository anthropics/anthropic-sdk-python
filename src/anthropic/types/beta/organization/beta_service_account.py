# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaServiceAccount"]


class BetaServiceAccount(BaseModel):
    """Named non-human identity within the caller's organization.

    A service account is a pure identity: name + org. Authorization lives on
    whatever references it (federation rules).
    """

    id: str
    """Tagged ID of the service account."""

    archived_at: Optional[datetime] = None
    """If set, this service account is archived."""

    archived_by_actor_id: Optional[str] = None
    """Tagged ID (`user_`/`svac_`) of the actor that archived this service account."""

    created_at: datetime
    """When this service account was created."""

    created_by_actor_id: Optional[str] = None
    """Tagged ID (`user_`/`svac_`) of the actor that created this service account."""

    description: Optional[str] = None
    """Optional free-text description."""

    name: str
    """Admin-chosen slug identifier."""

    organization_role: Literal["admin", "developer"]
    """Org-level role.

    A federation rule may only be created or retargeted to grant `org:admin` scope
    when this is `admin`. A rule granting `org:admin` whose target is later demoted
    to `developer` is rejected at token exchange. Rules granting `org:admin` are
    managed in the Console.
    """

    type: Literal["service_account"]

    updated_at: datetime
    """When this service account was last updated."""

    updated_by_actor_id: Optional[str] = None
    """
    Tagged ID (`user_`/`svac_`) of the actor that last updated this service account.
    """
