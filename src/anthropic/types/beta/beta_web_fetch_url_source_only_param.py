from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .beta_web_fetch_url_source_tool_reference_param import BetaWebFetchURLSourceToolReferenceParam

__all__ = ["BetaWebFetchURLSourceOnlyParam"]


class BetaWebFetchURLSourceOnlyParam(TypedDict, total=False):
    """
    The tool filter variant under which only the named tools' results
    contribute.
    """

    tools: Required[Iterable[BetaWebFetchURLSourceToolReferenceParam]]

    type: Required[Literal["only"]]
