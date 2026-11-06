from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookUserProfileProgramStatusUpdatedEventData"]


class BetaWebhookUserProfileProgramStatusUpdatedEventData(BaseModel):
    id: str
    """ID of the user profile that triggered the event."""

    organization_id: str

    type: Literal["user_profile.program_status_updated"]
