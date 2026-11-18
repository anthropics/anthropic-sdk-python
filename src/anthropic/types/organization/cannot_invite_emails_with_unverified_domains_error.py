from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .cannot_invite_emails_with_unverified_domains_error_details import (
    CannotInviteEmailsWithUnverifiedDomainsErrorDetails,
)

__all__ = ["CannotInviteEmailsWithUnverifiedDomainsError"]


class CannotInviteEmailsWithUnverifiedDomainsError(BadRequestError):
    """
    The email address's domain is not one of the verified domains of the organization's parent organization.
    """

    error_code: Literal["cannot_invite_emails_with_unverified_domains"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CannotInviteEmailsWithUnverifiedDomainsErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
