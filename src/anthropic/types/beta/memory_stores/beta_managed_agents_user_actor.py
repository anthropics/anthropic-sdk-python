# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsUserActor"]


class BetaManagedAgentsUserActor(BaseModel):
    """Attribution for a write made by a human user through the Anthropic Console."""

    type: Literal["user_actor"]

    user_id: str
    """ID of the user who performed the write (a `user_...` value)."""
