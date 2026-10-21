from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaMemoryTool20250818DeleteCommand"]


class BetaMemoryTool20250818DeleteCommand(BaseModel):
    command: Literal["delete"]
    """Command type identifier"""

    path: str
    """Path to the file or directory to delete"""
