from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_organization_rate_limit_value import BetaOrganizationRateLimitValue
from .beta_organization_rate_limit_batch_group import BetaOrganizationRateLimitBatchGroup
from .beta_organization_rate_limit_files_group import BetaOrganizationRateLimitFilesGroup
from .beta_organization_rate_limit_model_group import BetaOrganizationRateLimitModelGroup
from .beta_organization_rate_limit_skills_group import BetaOrganizationRateLimitSkillsGroup
from .beta_organization_rate_limit_web_search_group import BetaOrganizationRateLimitWebSearchGroup
from .beta_organization_rate_limit_token_count_group import BetaOrganizationRateLimitTokenCountGroup

__all__ = ["BetaOrganizationRateLimit", "Group"]

Group: TypeAlias = Annotated[
    Union[
        BetaOrganizationRateLimitModelGroup,
        BetaOrganizationRateLimitBatchGroup,
        BetaOrganizationRateLimitTokenCountGroup,
        BetaOrganizationRateLimitFilesGroup,
        BetaOrganizationRateLimitSkillsGroup,
        BetaOrganizationRateLimitWebSearchGroup,
    ],
    UnionDiscriminator("type"),
]


class BetaOrganizationRateLimit(BaseModel):
    id: str
    """Identifier of this rate-limit entry.

    It is stable within the organization and differs between organizations; the
    group's own identifier is `group.id`. Pass it as `rate_limit_id` to set a
    workspace's overrides for this group.
    """

    group: Group
    """The rate-limit group this entry's limits apply to."""

    limits: List[BetaOrganizationRateLimitValue]
    """The limiter values that apply to this group."""

    models: Optional[List[str]] = None
    """Model names this entry's limits apply to, including aliases.

    `null` when `group.type` is not `"model_group"`. The list covers the models your
    organization has access to, so it can differ between organizations.
    """

    type: Literal["rate_limit"]
    """Object type. Always `rate_limit` for organization rate-limit entries."""
