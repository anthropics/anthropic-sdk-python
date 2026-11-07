from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebFetchURLSourceNone"]


class BetaWebFetchURLSourceNone(BaseModel):
    """
    The ``url_sources`` variant under which a source contributes nothing:
    no result of the tool filter's source, or no user input.
    """

    type: Literal["none"]
