# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["BetaDreamSessionsInputParam"]


class BetaDreamSessionsInputParam(TypedDict, total=False):
    """Input session transcripts the dream reads."""

    session_ids: Required[SequenceNotStr[str]]

    type: Required[Literal["sessions"]]
