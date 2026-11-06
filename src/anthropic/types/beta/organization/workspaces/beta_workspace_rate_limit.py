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
    """The rate-limit group this entry's limits apply to."""

    limits: List[BetaWorkspaceRateLimitValue]
    """The workspace's limiter values for this group.

    By default only the limiter types with a workspace-level override are listed.
    With `include_inherited` set to `true`, the limiter types the workspace inherits
    from the organization are listed too, each marked by `source`.
    """

    models: Optional[List[str]] = None
    """Model names this entry's limits apply to, including aliases.

    `null` when `group.type` is not `"model_group"`. The list covers the models this
    workspace has access to, so it can differ between workspaces.
    """

    rate_limit_id: str
    """The `id` of the organization's RateLimit entry this entry applies to."""

    type: Literal["workspace_rate_limit"]
    """Object type. Always `workspace_rate_limit` for workspace rate-limit entries."""

    workspace_id: str
    """ID of the Workspace this entry applies to."""
