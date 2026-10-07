from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaBrowserRefTarget"]


class BetaBrowserRefTarget(BaseModel):
    """
    An element on the page, identified by a reference from a prior `read_page` or
    `find` result. References are scoped to the tab that produced them and become
    stale after navigation or a major re-render.
    """

    ref: str
    """An element reference (e.g.

    "ref_7") returned by a prior `read_page` or `find` result.
    """

    type: Literal["ref"]
