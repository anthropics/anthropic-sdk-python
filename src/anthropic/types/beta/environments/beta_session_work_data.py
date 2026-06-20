# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSessionWorkData"]


class BetaSessionWorkData(BaseModel):
    """Work data for session work items.

    This resource type is used when work represents a session that needs to be executed
    in a self-hosted environment.
    """

    id: str
    """Session identifier (e.g., 'session\\__...')"""

    type: Literal["session"]
    """Type of work data"""
