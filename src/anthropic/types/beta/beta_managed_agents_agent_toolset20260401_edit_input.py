# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentToolset20260401EditInput"]


class BetaManagedAgentsAgentToolset20260401EditInput(BaseModel):
    """Input payload for the `edit` tool.

    Performs a string
    replacement in the named file; by default `old_string` must
    occur exactly once.
    """

    file_path: str
    """Path of the file to edit."""

    new_string: str
    """Replacement text."""

    old_string: str
    """Substring to find and replace."""

    replace_all: Optional[bool] = None
    """
    When true, replace every occurrence of `old_string` instead of requiring a
    unique match.
    """
