# File generated from our OpenAPI spec by Stainless.

from .._models import BaseModel

__all__ = ["MessageDeltaUsage"]


class MessageDeltaUsage(BaseModel):
    output_tokens: int
    """The cumulative number of output tokens which were used."""
