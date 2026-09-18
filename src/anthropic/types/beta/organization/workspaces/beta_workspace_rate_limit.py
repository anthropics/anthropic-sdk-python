from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ....._models import BaseModel, UnionDiscriminator
from .beta_workspace_rate_limit_value import BetaWorkspaceRateLimitValue
from ..beta_organization_rate_limit_batch_group import BetaOrganizationRateLimitBatchGroup
from ..beta_organization_rate_limit_files_group import BetaOrganizationRateLimitFilesGroup
from ..beta_organization_rate_limit_model_group import BetaOrganizationRateLimitModelGroup
from ..beta_organization_rate_limit_skills_group import BetaOrganizationRateLimitSkillsGroup
from ..beta_organization_rate_limit_web_search_group import BetaOrganizationRateLimitWebSearchGroup
from ..beta_organization_rate_limit_token_count_group import BetaOrganizationRateLimitTokenCountGroup

__all__ = ["BetaWorkspaceRateLimit", "Group"]

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


class BetaWorkspaceRateLimit(BaseModel):
    group: Group
    """The rate-limit group this entry's limits apply to.

    Its `type` equals `group_type`.
    """

    group_type: Literal["batch", "files", "model_group", "skills", "token_count", "web_search"]
    """Deprecated: use `group.type` instead.

    The kind of rate-limit group this entry represents. `model_group` entries apply
    to a family of models (listed in `models`); other values apply to an API-surface
    category and have `models` set to `null`. Always equal to `group.type`.
    """

    limits: List[BetaWorkspaceRateLimitValue]
    """The limiter values overridden for this group in this workspace.

    Limiter types without a workspace override are omitted and inherit the
    organization value.
    """

    models: Optional[List[str]] = None
    """Model names this entry's limits apply to, including aliases.

    `null` when `group_type` is not `"model_group"`.
    """

    rate_limit_id: str
    """The `id` of the organization's RateLimit entry this override applies to."""

    type: Literal["workspace_rate_limit"]
    """Object type. Always `workspace_rate_limit` for workspace rate-limit entries."""

    workspace_id: str
    """ID of the Workspace this override applies to."""
