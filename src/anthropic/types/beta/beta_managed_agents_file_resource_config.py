# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsFileResourceConfig"]


class BetaManagedAgentsFileResourceConfig(BaseModel):
    """A file mounted into each session's container."""

    file_id: str
    """ID of a previously uploaded file."""

    type: Literal["file"]

    mount_path: Optional[str] = None
    """Mount path in the container. Defaults to `/mnt/session/uploads/<file_id>`."""
