from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaUserProfileEnrollmentURL"]


class BetaUserProfileEnrollmentURL(BaseModel):
    """
    A URL to give to the entity that a user profile represents, so that the entity can enroll in a program.
    """

    expires_at: datetime
    """When this enrollment URL expires, in RFC 3339 format."""

    type: Literal["enrollment_url"]
    """Object type. Always `enrollment_url`."""

    url: str
    """Enrollment URL to send to the end user. Valid until `expires_at`."""
