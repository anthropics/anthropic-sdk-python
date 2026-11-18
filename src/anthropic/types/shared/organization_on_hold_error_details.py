from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["OrganizationOnHoldErrorDetails"]


class OrganizationOnHoldErrorDetails(BaseModel):
    """Anthropic has disabled the organization for trust and safety reasons.

    An organization disabled for any other reason, such as billing, does not get this code. `appeal_url`, when present, is where the organization can appeal.
    """

    error_code: Literal["organization_on_hold"]

    appeal_url: Optional[str] = None
