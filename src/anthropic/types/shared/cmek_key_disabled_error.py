from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .cmek_key_disabled_error_details import CMEKKeyDisabledErrorDetails

__all__ = ["CMEKKeyDisabledError"]


class CMEKKeyDisabledError(BadRequestError):
    """The workspace's customer-managed encryption key is disabled or revoked.

    Re-enable the key, then retry.
    """

    error_code: Literal["cmek_key_disabled"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CMEKKeyDisabledErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
