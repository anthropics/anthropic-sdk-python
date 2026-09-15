from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .web_fetch_url_source_tool_reference_param import WebFetchURLSourceToolReferenceParam

__all__ = ["WebFetchURLSourceOnlyParam"]


class WebFetchURLSourceOnlyParam(TypedDict, total=False):
    """
    The tool filter variant under which only the named tools' results
    contribute.
    """

    tools: Required[Iterable[WebFetchURLSourceToolReferenceParam]]

    type: Required[Literal["only"]]
