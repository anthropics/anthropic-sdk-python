from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .email_domain_not_allowed_error_details import EmailDomainNotAllowedErrorDetails

__all__ = ["EmailDomainNotAllowedError"]


class EmailDomainNotAllowedError(BadRequestError):
    """
    The organization restricts invites to an allowed list of email domains, and the list is empty or does not include the email address's domain.
    """

    error_code: Literal["email_domain_not_allowed"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: EmailDomainNotAllowedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
