from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Literal, TypedDict

from .allowed_inference_geo import AllowedInferenceGeo

__all__ = ["DataResidencyUpdateConfigParam"]


class DataResidencyUpdateConfigParam(TypedDict, total=False):
    allowed_inference_geos: Union[List[AllowedInferenceGeo], Literal["unrestricted"], None]
    """Permitted inference geo values.

    Use 'unrestricted' to allow all geos, or a list of specific geos.
    """

    default_inference_geo: Optional[Literal["global", "us"]]
    """Default inference geo applied when requests omit the parameter.

    Must be a member of `allowed_inference_geos` unless `allowed_inference_geos` is
    `"unrestricted"`.
    """
