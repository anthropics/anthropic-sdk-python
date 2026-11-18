from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaRegistrationPendingErrorDetails"]


class BetaRegistrationPendingErrorDetails(BaseModel):
    """The Plugin version was stored but is not yet usable in claude.ai.

    `plugin_id` and `plugin_version_id` identify what was stored.
    """

    error_code: Literal["registration_pending"]

    plugin_id: str

    plugin_version_id: str
