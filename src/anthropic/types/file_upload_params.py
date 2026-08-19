# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import FileTypes

__all__ = ["FileUploadParams"]


class FileUploadParams(TypedDict, total=False):
    file: Required[FileTypes]
    """The file to upload"""

    expires_in_seconds: int
    """
    Seconds from upload until the file expires and its bytes become permanently
    unavailable. Must be between 3600 (one hour) and 7776000 (ninety days).
    """
