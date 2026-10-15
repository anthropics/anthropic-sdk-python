from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsFileRubric"]


class BetaManagedAgentsFileRubric(BaseModel):
    """Rubric referenced by a file uploaded via the Files API."""

    file_id: str
    """ID of the rubric file."""

    type: Literal["file"]
