from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["LinkedOrganizationBillingUnavailableErrorDetails"]


class LinkedOrganizationBillingUnavailableErrorDetails(BaseModel):
    """
    Anthropic cannot currently bill the organization linked to the request's user profile, for a reason that lies with that organization's own account. The response does not say what the reason is.
    """

    error_code: Literal["linked_organization_billing_unavailable"]
