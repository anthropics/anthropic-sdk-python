# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaFallbackCreditRedeemed"]


class BetaFallbackCreditRedeemed(BaseModel):
    """
    The reprice was applied: the retry is billed as if the conversation
    had been on the retry model all along.
    """

    type: Literal["redeemed"]
