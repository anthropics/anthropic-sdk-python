# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .url_image_source_param import URLImageSourceParam
from .file_image_source_param import FileImageSourceParam
from .base64_image_source_param import Base64ImageSourceParam
from .image_transformations_param import ImageTransformationsParam
from .cache_control_ephemeral_param import CacheControlEphemeralParam

__all__ = ["ImageBlockParam", "Source"]

Source: TypeAlias = Union[Base64ImageSourceParam, URLImageSourceParam, FileImageSourceParam]


class ImageBlockParam(TypedDict, total=False):
    source: Required[Source]

    type: Required[Literal["image"]]

    cache_control: Optional[CacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    transformations: Optional[ImageTransformationsParam]
    """
    Configures the transformations the server applies to this image before the model
    observes it. Each key names a condition the server transforms images for; its
    value selects the transformation applied. Omitted keys keep their default
    behavior, and an empty object is equivalent to omitting the field.
    """
