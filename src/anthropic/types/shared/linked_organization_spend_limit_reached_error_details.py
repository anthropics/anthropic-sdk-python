from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["LinkedOrganizationSpendLimitReachedErrorDetails"]


class LinkedOrganizationSpendLimitReachedErrorDetails(BaseModel):
    """
    The organization linked to the request's user profile has reached a spend limit that it set, or lacks credit for the request. The response does not say which applies.
    """

    error_code: Literal["linked_organization_spend_limit_reached"]
