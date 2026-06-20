# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentToolset20260401WriteInput"]


class BetaManagedAgentsAgentToolset20260401WriteInput(BaseModel):
    """Input payload for the `write` tool.

    Writes (overwriting) the
    entire file contents.
    """

    content: str
    """Full file contents to write."""

    file_path: str
    """Path of the file to write."""
