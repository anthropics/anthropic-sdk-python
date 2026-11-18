from typing_extensions import Literal

from ..._exceptions import PaymentRequiredError
from .linked_organization_billing_unavailable_error_details import LinkedOrganizationBillingUnavailableErrorDetails

__all__ = ["LinkedOrganizationBillingUnavailableError"]


class LinkedOrganizationBillingUnavailableError(PaymentRequiredError):
    """
    Anthropic cannot currently bill the organization linked to the request's user profile, for a reason that lies with that organization's own account. The response does not say what the reason is.
    """

    error_code: Literal["linked_organization_billing_unavailable"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: LinkedOrganizationBillingUnavailableErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
