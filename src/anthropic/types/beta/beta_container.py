# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ..._models import BaseModel
from .beta_container_skill import BetaContainerSkill

__all__ = ["BetaContainer"]


class BetaContainer(BaseModel):
    """
    Information about the container used in the request (for the code execution tool)
    """

    id: str
    """Identifier for the container used in this request"""

    expires_at: datetime
    """The time at which the container will expire."""

    skills: Optional[List[BetaContainerSkill]] = None
    """Skills loaded in the container"""
