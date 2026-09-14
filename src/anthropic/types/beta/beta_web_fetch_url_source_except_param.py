from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .beta_web_fetch_url_source_tool_reference_param import BetaWebFetchURLSourceToolReferenceParam

__all__ = ["BetaWebFetchURLSourceExceptParam"]


class BetaWebFetchURLSourceExceptParam(TypedDict, total=False):
    """
    The tool filter variant under which every result but the named
    tools' contributes.
    """

    tools: Required[Iterable[BetaWebFetchURLSourceToolReferenceParam]]

    type: Required[Literal["except"]]
