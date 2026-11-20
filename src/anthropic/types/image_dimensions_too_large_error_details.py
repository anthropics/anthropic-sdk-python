from typing import List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ImageDimensionsTooLargeErrorDetails"]


class ImageDimensionsTooLargeErrorDetails(BaseModel):
    """
    The longest side of one or more images in the request exceeds the image size limit. Scale each image in `paths` so that neither side exceeds `max_side_length_pixels`, or remove it, then retry.
    """

    error_code: Literal["image_dimensions_too_large"]

    max_side_length_pixels: int
    """
    The limit the images exceeded: the largest width or height, in pixels, that an
    image on this request may have.
    """

    paths: List[str]
    """
    The position of every image over the limit, in the order you sent them, nested
    blocks included, such as `messages.0.content.1`, or
    `messages.0.content.1.content.0` for an image in a `tool_result` block.
    """
