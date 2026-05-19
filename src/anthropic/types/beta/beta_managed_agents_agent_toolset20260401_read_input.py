# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentToolset20260401ReadInput"]


class BetaManagedAgentsAgentToolset20260401ReadInput(BaseModel):
    """Input payload for the `read` tool.

    Reads file contents
    relative to the runner's working directory (or absolute when
    the runner permits).
    """

    file_path: str
    """Path of the file to read."""

    view_range: Optional[List[int]] = None
    """Optional `[start_line, end_line]` 1-indexed inclusive range.

    When omitted the entire file is returned. `end_line` of 0 or negative means "to
    end of file".
    """
