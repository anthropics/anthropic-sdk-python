# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from ..._types import FileTypes
from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["FileUploadParams"]


class FileUploadParams(TypedDict, total=False):
    file: Required[FileTypes]
    """The file to upload"""

    expires_in_seconds: int
    """
    Seconds from upload until the file expires and its bytes become permanently
    unavailable. Must be between 3600 (one hour) and 7776000 (ninety days).
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
