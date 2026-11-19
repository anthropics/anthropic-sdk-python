from typing import Union
from typing_extensions import Annotated, TypeAlias

from ......_models import UnionDiscriminator
from .beta_claude_code_rbac_group_status_active import BetaClaudeCodeRBACGroupStatusActive
from .beta_claude_code_rbac_group_status_deleted import BetaClaudeCodeRBACGroupStatusDeleted
from .beta_claude_code_rbac_group_status_unknown import BetaClaudeCodeRBACGroupStatusUnknown

__all__ = ["BetaClaudeCodeRBACGroupStatus"]

BetaClaudeCodeRBACGroupStatus: TypeAlias = Annotated[
    Union[
        BetaClaudeCodeRBACGroupStatusActive, BetaClaudeCodeRBACGroupStatusDeleted, BetaClaudeCodeRBACGroupStatusUnknown
    ],
    UnionDiscriminator("type"),
]
