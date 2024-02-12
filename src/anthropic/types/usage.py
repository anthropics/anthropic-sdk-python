# File generated from our OpenAPI spec by Stainless.

from .._models import BaseModel

__all__ = ["Usage"]


class Usage(BaseModel):
    input_tokens: int
    """The number of input tokens which were used."""

    output_tokens: int
    """The number of output tokens which were used."""
