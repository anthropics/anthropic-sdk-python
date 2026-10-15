from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookSessionBudgetReachedEventData"]


class BetaWebhookSessionBudgetReachedEventData(BaseModel):
    id: str
    """ID of the session that triggered the event."""

    organization_id: str

    type: Literal["session.budget_reached"]

    workspace_id: str
