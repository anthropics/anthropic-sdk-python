# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["ImageTransformationsParam"]


class ImageTransformationsParam(TypedDict, total=False):
    """
    Configures the transformations the server applies to this image before the model observes it. Each key names a condition the server transforms images for; its value selects the transformation applied. Omitted keys keep their default behavior, and an empty object is equivalent to omitting the field.
    """

    oversized_image: Literal["downsize", "error"]
    """What the server does when this image exceeds the model's maximum image size.

    `"downsize"` (the default) scales the image down to fit, which changes the
    dimensions the model observes without telling you. `"error"` instead rejects the
    request with a 400 error naming the image's dimensions and the largest
    dimensions that fit, so you can scale the image deliberately — your image is
    never silently scaled down.
    """
