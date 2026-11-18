from typing_extensions import Literal

from ...._exceptions import PermissionDeniedError
from .beta_api_key_scope_missing_error_details import BetaAPIKeyScopeMissingErrorDetails

__all__ = ["BetaAPIKeyScopeMissingError"]


class BetaAPIKeyScopeMissingError(PermissionDeniedError):
    """
    The API key lacks the scope the request needs: `read:claude_tag` for a read, `write:claude_tag` for a change.
    """

    error_code: Literal["api_key_scope_missing"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaAPIKeyScopeMissingErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
