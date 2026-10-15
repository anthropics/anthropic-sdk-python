from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAgentAutoEvaluatedPermissionAllow"]


class BetaManagedAgentsAgentAutoEvaluatedPermissionAllow(BaseModel):
    """The server judged the invocation safe to execute without client approval."""

    type: Literal["allow"]
