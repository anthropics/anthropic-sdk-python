# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsFileRubricParams"]


class BetaManagedAgentsFileRubricParams(TypedDict, total=False):
    """Rubric referenced by a file uploaded via the Files API."""

    file_id: Required[str]
    """ID of the rubric file."""

    type: Required[Literal["file"]]
