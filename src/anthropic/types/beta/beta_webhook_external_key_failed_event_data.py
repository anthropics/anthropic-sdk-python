from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookExternalKeyFailedEventData"]


class BetaWebhookExternalKeyFailedEventData(BaseModel):
    id: str
    """ID (`ekey_...`) of the external key that stopped working or works again."""

    organization_id: str

    type: Literal["external_key.failed"]
