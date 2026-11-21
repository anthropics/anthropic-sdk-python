from typing_extensions import Literal

from ..._exceptions import PaymentRequiredError
from .linked_organization_spend_limit_reached_error_details import LinkedOrganizationSpendLimitReachedErrorDetails

__all__ = ["LinkedOrganizationSpendLimitReachedError"]


class LinkedOrganizationSpendLimitReachedError(PaymentRequiredError):
    """
    The organization linked to the request's user profile has reached a spend limit that it set, or lacks credit for the request. The response does not say which applies.
    """

    error_code: Literal["linked_organization_spend_limit_reached"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: LinkedOrganizationSpendLimitReachedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
