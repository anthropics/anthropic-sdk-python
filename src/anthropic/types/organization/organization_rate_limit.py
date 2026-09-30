from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .organization_rate_limit_value import OrganizationRateLimitValue
from .organization_rate_limit_batch_group import OrganizationRateLimitBatchGroup
from .organization_rate_limit_files_group import OrganizationRateLimitFilesGroup
from .organization_rate_limit_model_group import OrganizationRateLimitModelGroup
from .organization_rate_limit_skills_group import OrganizationRateLimitSkillsGroup
from .organization_rate_limit_web_search_group import OrganizationRateLimitWebSearchGroup
from .organization_rate_limit_token_count_group import OrganizationRateLimitTokenCountGroup

__all__ = ["OrganizationRateLimit", "Group"]

Group: TypeAlias = Annotated[
    Union[
        OrganizationRateLimitModelGroup,
        OrganizationRateLimitBatchGroup,
        OrganizationRateLimitTokenCountGroup,
        OrganizationRateLimitFilesGroup,
        OrganizationRateLimitSkillsGroup,
        OrganizationRateLimitWebSearchGroup,
    ],
    UnionDiscriminator("type"),
]


class OrganizationRateLimit(BaseModel):
    id: str
    """Identifier of this rate-limit entry.

    It is stable within the organization and differs between organizations; the
    group's own identifier is `group.id`.
    """

    group: Group
    """The rate-limit group this entry's limits apply to.

    Its `type` equals `group_type`.
    """

    limits: List[OrganizationRateLimitValue]
    """The limiter values that apply to this group."""

    models: Optional[List[str]] = None
    """Model names this entry's limits apply to, including aliases.

    `null` when `group_type` is not `"model_group"`.
    """

    type: Literal["rate_limit"]
    """Object type. Always `rate_limit` for organization rate-limit entries."""
