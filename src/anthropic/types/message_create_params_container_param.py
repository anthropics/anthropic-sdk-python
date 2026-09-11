from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .container_params import ContainerParams

__all__ = ["MessageCreateParamsContainerParam"]

MessageCreateParamsContainerParam: TypeAlias = Union[ContainerParams, str]
