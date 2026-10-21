from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookUserProfileEnforcementActionOpenedEventData"]


class BetaWebhookUserProfileEnforcementActionOpenedEventData(BaseModel):
    id: str
    """ID of the user profile the enforcement action is on."""

    enforcement_action_id: str
    """ID (`enac_...`) of the enforcement action that was opened or resolved."""

    organization_id: str

    type: Literal["user_profile.enforcement_action_opened"]
