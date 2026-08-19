# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import TypedDict

from .skill_params import SkillParams

__all__ = ["ContainerParams"]


class ContainerParams(TypedDict, total=False):
    """Container parameters with skills to be loaded."""

    id: Optional[str]
    """Container id"""

    skills: Optional[Iterable[SkillParams]]
    """List of skills to load in the container"""
