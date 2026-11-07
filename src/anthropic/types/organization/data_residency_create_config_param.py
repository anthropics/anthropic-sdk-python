from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Literal, TypedDict

from .allowed_inference_geo import AllowedInferenceGeo

__all__ = ["DataResidencyCreateConfigParam"]


class DataResidencyCreateConfigParam(TypedDict, total=False):
    allowed_inference_geos: Union[List[AllowedInferenceGeo], Literal["unrestricted"], None]
    """Permitted inference geo values.

    Defaults to 'unrestricted' if omitted, which allows all geos. Use the string
    'unrestricted' to allow all geos, or a list of specific geos.
    """

    default_inference_geo: Optional[Literal["global", "us"]]
    """Default inference geo applied when requests omit the parameter.

    Defaults to 'global' if omitted. Must be a member of `allowed_inference_geos`
    unless `allowed_inference_geos` is `"unrestricted"`.
    """

    workspace_geo: Optional[Literal["us"]]
    """Geographic region for workspace data storage.

    Immutable after creation. Defaults to 'us' if omitted.
    """
