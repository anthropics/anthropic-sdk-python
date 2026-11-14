from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaBundleAttachmentNotSupportedErrorDetails"]


class BetaBundleAttachmentNotSupportedErrorDetails(BaseModel):
    """
    The Bundle has an attachment this API does not support editing, so its instructions can be changed only in claude.ai.
    """

    error_code: Literal["bundle_attachment_not_supported"]
