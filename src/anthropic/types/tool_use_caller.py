from typing import Union
from typing_extensions import Annotated, TypeAlias

from .._models import UnionDiscriminator
from .direct_caller import DirectCaller
from .server_tool_caller import ServerToolCaller
from .server_tool_caller_20260120 import ServerToolCaller20260120

__all__ = ["ToolUseCaller"]

ToolUseCaller: TypeAlias = Annotated[
    Union[DirectCaller, ServerToolCaller, ServerToolCaller20260120], UnionDiscriminator("type")
]
