# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["DeletedSkill"]


class DeletedSkill(BaseModel):
    id: str
    """Unique identifier for the skill.

    The format and length of IDs may change over time.
    """

    type: Literal["skill_deleted"]
    """Deleted object type.

    For Skills, this is always `"skill_deleted"`.
    """
