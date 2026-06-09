# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsUnknownRunError"]


class BetaManagedAgentsUnknownRunError(BaseModel):
    """An unknown or unexpected error caused the run to fail.

    A fallback variant; clients that do not recognize a new error type can match on message alone.
    """

    message: str
    """Human-readable error description."""

    type: Literal["unknown_error"]
