from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypedDict

from .._types import Base64FileInput
from .._models import set_pydantic_config

__all__ = ["Base64ImageSourceParam"]


class Base64ImageSourceParam(TypedDict, total=False):
    data: Required[Union[str, Base64FileInput]]

    media_type: Required[Literal["image/jpeg", "image/png", "image/gif", "image/webp"]]

    type: Required[Literal["base64"]]


set_pydantic_config(Base64ImageSourceParam, {"arbitrary_types_allowed": True})
