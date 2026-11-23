from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookExternalStorageFailedEventData"]


class BetaWebhookExternalStorageFailedEventData(BaseModel):
    id: str
    """
    ID (`estrg_...`) of the External Storage whose bucket failed Anthropic's check
    or passes it again.
    """

    organization_id: str

    type: Literal["external_storage.failed"]
