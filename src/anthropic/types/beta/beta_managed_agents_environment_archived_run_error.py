# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsEnvironmentArchivedRunError"]


class BetaManagedAgentsEnvironmentArchivedRunError(BaseModel):
    """The deployment's environment was archived."""

    message: str
    """Human-readable error description."""

    type: Literal["environment_archived_error"]
