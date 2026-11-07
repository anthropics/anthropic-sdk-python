from ...._models import BaseModel

__all__ = ["BetaOrganizationWebhookEndpointSigningSecret"]


class BetaOrganizationWebhookEndpointSigningSecret(BaseModel):
    """An organization webhook endpoint's new signing secret."""

    signing_secret: str
    """The new signing secret.

    Deliveries are signed with it from now on, and no other response returns it.
    """
