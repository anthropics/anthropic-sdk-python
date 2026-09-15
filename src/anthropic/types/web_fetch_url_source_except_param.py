from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .web_fetch_url_source_tool_reference_param import WebFetchURLSourceToolReferenceParam

__all__ = ["WebFetchURLSourceExceptParam"]


class WebFetchURLSourceExceptParam(TypedDict, total=False):
    """
    The tool filter variant under which every result but the named
    tools' contributes.
    """

    tools: Required[Iterable[WebFetchURLSourceToolReferenceParam]]

    type: Required[Literal["except"]]
