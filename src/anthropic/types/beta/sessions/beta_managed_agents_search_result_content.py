# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSearchResultContent"]


class BetaManagedAgentsSearchResultContent(BaseModel):
    """Text content within a search result."""

    text: str
    """The text content."""

    type: Literal["text"]
