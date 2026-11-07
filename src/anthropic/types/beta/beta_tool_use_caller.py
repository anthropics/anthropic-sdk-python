from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_direct_caller import BetaDirectCaller
from .beta_server_tool_caller import BetaServerToolCaller
from .beta_server_tool_caller_20260120 import BetaServerToolCaller20260120

__all__ = ["BetaToolUseCaller"]

BetaToolUseCaller: TypeAlias = Annotated[
    Union[BetaDirectCaller, BetaServerToolCaller, BetaServerToolCaller20260120], UnionDiscriminator("type")
]
