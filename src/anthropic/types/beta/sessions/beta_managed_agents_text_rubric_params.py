# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsTextRubricParams"]


class BetaManagedAgentsTextRubricParams(TypedDict, total=False):
    """Rubric content provided inline as text."""

    content: Required[str]
    """Rubric content.

    Plain text or markdown — the grader treats it as freeform text. Maximum 262144
    characters.
    """

    type: Required[Literal["text"]]
