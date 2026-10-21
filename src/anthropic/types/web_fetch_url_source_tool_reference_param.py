from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["WebFetchURLSourceToolReferenceParam"]


class WebFetchURLSourceToolReferenceParam(TypedDict, total=False):
    """
    One entry of a tool filter's ``tools``: it must name a tool declared
    in this request's ``tools[]``.
    """

    name: Required[str]

    type: Required[Literal["tool_reference"]]
