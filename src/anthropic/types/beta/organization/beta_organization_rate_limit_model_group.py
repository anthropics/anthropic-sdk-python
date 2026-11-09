from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaOrganizationRateLimitModelGroup"]


class BetaOrganizationRateLimitModelGroup(BaseModel):
    id: str
    """
    Opaque identifier of the rate-limit group (for example,
    `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never
    changes, unlike the entry's own identifier, which differs per organization.
    """

    display_name: str
    """Human-readable name of the model group (for example, `Claude Sonnet 4.x`).

    For display only; it may change.
    """

    type: Literal["model_group"]
    """Always `model_group`: a family of models."""
