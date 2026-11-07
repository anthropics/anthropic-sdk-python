from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaWebFetchURLSourceAllParam"]


class BetaWebFetchURLSourceAllParam(TypedDict, total=False):
    """
    The ``url_sources`` variant under which a source contributes in
    full: every result of the tool filter's source, or all user input.
    """

    type: Required[Literal["all"]]
