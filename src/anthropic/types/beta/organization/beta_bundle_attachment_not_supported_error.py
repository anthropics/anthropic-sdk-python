from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_bundle_attachment_not_supported_error_details import BetaBundleAttachmentNotSupportedErrorDetails

__all__ = ["BetaBundleAttachmentNotSupportedError"]


class BetaBundleAttachmentNotSupportedError(BadRequestError):
    """
    The Bundle has an attachment this API does not support editing, so its instructions can be changed only in claude.ai.
    """

    error_code: Literal["bundle_attachment_not_supported"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaBundleAttachmentNotSupportedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
