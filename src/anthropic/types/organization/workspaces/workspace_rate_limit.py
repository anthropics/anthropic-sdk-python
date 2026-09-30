from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .workspace_rate_limit_value import WorkspaceRateLimitValue
from ..organization_rate_limit_batch_group import OrganizationRateLimitBatchGroup
from ..organization_rate_limit_files_group import OrganizationRateLimitFilesGroup
from ..organization_rate_limit_model_group import OrganizationRateLimitModelGroup
from ..organization_rate_limit_skills_group import OrganizationRateLimitSkillsGroup
from ..organization_rate_limit_web_search_group import OrganizationRateLimitWebSearchGroup
from ..organization_rate_limit_token_count_group import OrganizationRateLimitTokenCountGroup

__all__ = ["WorkspaceRateLimit", "Group"]

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


class WorkspaceRateLimit(BaseModel):
    group: Group
    """The rate-limit group this entry's limits apply to.

    Its `type` equals `group_type`.
    """

    limits: List[WorkspaceRateLimitValue]
    """The workspace's limiter values for this group.

    By default only the limiter types with a workspace-level override are listed.
    With `include_inherited` set to `true`, the limiter types the workspace inherits
    from the organization are listed too, each marked by `source`.
    """

    models: Optional[List[str]] = None
    """Model names this entry's limits apply to, including aliases.

    `null` when `group_type` is not `"model_group"`.
    """

    rate_limit_id: str
    """The `id` of the organization's RateLimit entry this entry applies to."""

    type: Literal["workspace_rate_limit"]
    """Object type. Always `workspace_rate_limit` for workspace rate-limit entries."""

    workspace_id: str
    """ID of the Workspace this entry applies to."""
