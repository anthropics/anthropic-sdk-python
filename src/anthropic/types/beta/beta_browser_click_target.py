from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_browser_ref_target import BetaBrowserRefTarget
from .beta_browser_coordinate_target import BetaBrowserCoordinateTarget

__all__ = ["BetaBrowserClickTarget"]

BetaBrowserClickTarget: TypeAlias = Annotated[
    Union[BetaBrowserCoordinateTarget, BetaBrowserRefTarget], UnionDiscriminator("type")
]
