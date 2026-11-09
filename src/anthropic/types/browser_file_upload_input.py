from typing import List, Optional

from .._models import BaseModel
from .browser_ref_target import BrowserRefTarget

__all__ = ["BrowserFileUploadInput"]


class BrowserFileUploadInput(BaseModel):
    """Set the value of a file-input element to one or more files.

    The target must be an
    element reference; at least one of paths or document_ids is required.
    """

    target: BrowserRefTarget
    """
    An element on the page, identified by a reference from a prior `read_page` or
    `find` result. References are scoped to the tab that produced them and become
    stale after navigation or a major re-render.
    """

    document_ids: Optional[List[str]] = None
    """
    References to files the harness has staged, for deployments where the browser
    executor cannot read the caller's filesystem.
    """

    paths: Optional[List[str]] = None
    """File paths on the browser executor's filesystem."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
