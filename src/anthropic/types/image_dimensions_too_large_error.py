from typing_extensions import Literal

from .._exceptions import BadRequestError
from .image_dimensions_too_large_error_details import ImageDimensionsTooLargeErrorDetails

__all__ = ["ImageDimensionsTooLargeError"]


class ImageDimensionsTooLargeError(BadRequestError):
    """
    The longest side of one or more images in the request exceeds the image size limit. Scale each image in `paths` so that neither side exceeds `max_side_length_pixels`, or remove it, then retry.
    """

    error_code: Literal["image_dimensions_too_large"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ImageDimensionsTooLargeErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
