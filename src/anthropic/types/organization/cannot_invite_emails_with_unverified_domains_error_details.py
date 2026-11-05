from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["CannotInviteEmailsWithUnverifiedDomainsErrorDetails"]


class CannotInviteEmailsWithUnverifiedDomainsErrorDetails(BaseModel):
    """
    The email address's domain is not one of the verified domains of the organization's parent organization.
    """

    error_code: Literal["cannot_invite_emails_with_unverified_domains"]
