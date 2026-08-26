# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaDataResidency"]


class BetaDataResidency(BaseModel):
    allowed_inference_geos: Union[List[str], Literal["unrestricted"]]
    """Permitted inference geo values. 'unrestricted' means all geos are allowed."""

    default_inference_geo: str
    """Default inference geo applied when requests omit the parameter."""

    workspace_geo: str
    """Geographic region for workspace data storage. Immutable after creation."""
