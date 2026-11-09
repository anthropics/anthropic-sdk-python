from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["EmailDomainNotAllowedErrorDetails"]


class EmailDomainNotAllowedErrorDetails(BaseModel):
    """
    The organization restricts invites to an allowed list of email domains, and the list is empty or does not include the email address's domain.
    """

    error_code: Literal["email_domain_not_allowed"]
