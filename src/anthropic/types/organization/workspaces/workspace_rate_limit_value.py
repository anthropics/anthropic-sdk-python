from typing import Union, Optional
from typing_extensions import Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .workspace_rate_limit_workspace_source import WorkspaceRateLimitWorkspaceSource
from .workspace_rate_limit_organization_source import WorkspaceRateLimitOrganizationSource

__all__ = ["WorkspaceRateLimitValue", "Source"]

Source: TypeAlias = Annotated[
    Union[WorkspaceRateLimitWorkspaceSource, WorkspaceRateLimitOrganizationSource], UnionDiscriminator("type")
]


class WorkspaceRateLimitValue(BaseModel):
    org_limit: Optional[int] = None
    """The organization-level value for the same limiter type, for reference.

    `null` when the organization has no limit configured for this limiter type.
    """

    source: Source
    """Where `value` comes from.

    `organization` values are listed only when `include_inherited` is `true`, and
    then `value` equals `org_limit`.
    """

    type: str
    """
    The limiter type (for example, `requests_per_minute` or
    `input_tokens_per_minute`).
    """

    value: int
    """
    The workspace's value for this limiter type: the workspace-level override when
    `source.type` is `workspace`, otherwise the organization's value.
    """
