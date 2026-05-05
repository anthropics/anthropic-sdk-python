# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsTextRubric"]


class BetaManagedAgentsTextRubric(BaseModel):
    """Rubric content provided inline as text."""

    content: str
    """Rubric content. Plain text or markdown — the grader treats it as freeform text."""

    type: Literal["text"]
