from typing import List, Union
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_allowed_inference_geo import BetaAllowedInferenceGeo

__all__ = ["BetaDataResidency"]


class BetaDataResidency(BaseModel):
    allowed_inference_geos: Union[List[BetaAllowedInferenceGeo], Literal["unrestricted"]]
    """Permitted inference geo values. 'unrestricted' means all geos are allowed."""

    default_inference_geo: Literal["global", "us"]
    """Default inference geo applied when requests omit the parameter."""

    workspace_geo: Literal["us"]
    """Geographic region for workspace data storage. Immutable after creation."""
