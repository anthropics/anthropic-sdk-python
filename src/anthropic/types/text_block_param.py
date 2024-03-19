# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["TextBlockParam"]


class TextBlockParam(TypedDict, total=False):
    text: Required[str]

    type: Literal["text"]
