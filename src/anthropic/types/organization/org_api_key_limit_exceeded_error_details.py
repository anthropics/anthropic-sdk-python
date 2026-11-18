from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["OrgAPIKeyLimitExceededErrorDetails"]


class OrgAPIKeyLimitExceededErrorDetails(BaseModel):
    """The organization has reached its limit of active API keys."""

    error_code: Literal["org_api_key_limit_exceeded"]
