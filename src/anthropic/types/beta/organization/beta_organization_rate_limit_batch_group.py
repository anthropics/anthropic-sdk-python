from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaOrganizationRateLimitBatchGroup"]


class BetaOrganizationRateLimitBatchGroup(BaseModel):
    id: str
    """
    Opaque identifier of the rate-limit group (for example,
    `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never
    changes, unlike the entry's own identifier, which differs per organization.
    """

    type: Literal["batch"]
    """Always `batch`: the Message Batches API."""
