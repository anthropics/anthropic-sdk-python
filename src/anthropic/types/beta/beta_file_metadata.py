# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_file_scope import BetaFileScope

__all__ = ["BetaFileMetadata"]


class BetaFileMetadata(BaseModel):
    id: str
    """Unique object identifier.

    The format and length of IDs may change over time.
    """

    created_at: datetime
    """RFC 3339 datetime string representing when the file was created."""

    filename: str
    """Original filename of the uploaded file."""

    mime_type: str
    """MIME type of the file."""

    size_bytes: int
    """Size of the file in bytes."""

    type: Literal["file"]
    """Object type.

    For files, this is always `"file"`.
    """

    downloadable: Optional[bool] = None
    """Whether the file can be downloaded."""

    expires_at: Optional[datetime] = None
    """
    RFC 3339 datetime string representing when the file will expire and become
    unavailable for download. Null if the file does not expire. For files uploaded
    with `expires_in_seconds`, this is the upload time plus that value.
    """

    scope: Optional[BetaFileScope] = None
    """
    The scope of this file, indicating the context in which it was created (e.g., a
    session).
    """
