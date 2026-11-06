from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .thread_unsupported_feature_name import ThreadUnsupportedFeatureName

__all__ = ["ThreadUnsupportedRequestErrorDetails"]


class ThreadUnsupportedRequestErrorDetails(BaseModel):
    """
    The request combines `thread` with a request field or an organization setting that Threads do not support; `unsupported`, when present, names it. Send the full conversation without `thread`, or change that field.
    """

    error_code: Literal["thread_unsupported_request"]

    unsupported: Optional[List[ThreadUnsupportedFeatureName]] = None
    """
    Each entry names a request field or an organization setting that Threads do not
    support. On a value you do not recognize, send the full conversation without
    `thread`.
    """
