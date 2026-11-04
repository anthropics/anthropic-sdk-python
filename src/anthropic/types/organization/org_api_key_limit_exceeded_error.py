from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .org_api_key_limit_exceeded_error_details import OrgAPIKeyLimitExceededErrorDetails

__all__ = ["OrgAPIKeyLimitExceededError"]


class OrgAPIKeyLimitExceededError(BadRequestError):
    """The organization has reached its limit of active API keys."""

    error_code: Literal["org_api_key_limit_exceeded"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: OrgAPIKeyLimitExceededErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
