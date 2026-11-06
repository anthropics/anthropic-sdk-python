from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["SandboxEgressRestrictedErrorDetails"]


class SandboxEgressRestrictedErrorDetails(BaseModel):
    """
    The request came from a Claude sandbox with restricted network access, which is not allowed to make this change. Send it from outside the sandbox, or from a sandbox with unrestricted network access.
    """

    error_code: Literal["sandbox_egress_restricted"]
