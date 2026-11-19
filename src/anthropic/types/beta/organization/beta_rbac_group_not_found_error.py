from typing_extensions import Literal

from ...._exceptions import NotFoundError
from .beta_rbac_group_not_found_error_details import BetaRBACGroupNotFoundErrorDetails

__all__ = ["BetaRBACGroupNotFoundError"]


class BetaRBACGroupNotFoundError(NotFoundError):
    """The RBAC Group is not one of the organization's groups."""

    error_code: Literal["rbac_group_not_found"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaRBACGroupNotFoundErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
