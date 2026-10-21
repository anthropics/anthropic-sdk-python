from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaWebSearchResultBlockParam"]


class BetaWebSearchResultBlockParam(TypedDict, total=False):
    encrypted_content: Required[str]

    title: Required[str]

    type: Required[Literal["web_search_result"]]

    url: Required[str]

    page_age: Optional[str]
