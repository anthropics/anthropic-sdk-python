from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["WebFetchURLSourceNoneParam"]


class WebFetchURLSourceNoneParam(TypedDict, total=False):
    """
    The ``url_sources`` variant under which a source contributes nothing:
    no result of the tool filter's source, or no user input.
    """

    type: Required[Literal["none"]]
