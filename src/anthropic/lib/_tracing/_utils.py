from __future__ import annotations

import json
from typing import Any, cast

import pydantic

from ..._utils import is_dict
from ..._models import BaseModel
from ...types.message_create_params import MessageCreateParamsBase
from ...types.beta.message_create_params import MessageCreateParamsBase as BetaMessageCreateParamsBase

__all__ = ["MessageCreateBody", "get", "as_dict", "to_json"]

# A body is a plain dict by the time it is sent, so it is read as its params type, whose every key is optional here.
MessageCreateBody = MessageCreateParamsBase | BetaMessageCreateParamsBase


def get(value: object, key: str) -> Any:
    """`value[key]` for a dict, `value.key` for a model, and `None` when there is no such entry."""
    if is_dict(value):
        return value.get(key)
    if isinstance(value, pydantic.BaseModel):
        return getattr(value, key, None)
    return None


def as_dict(value: object) -> dict[str, object] | None:
    if is_dict(value):
        return cast("dict[str, object]", value)
    if isinstance(value, BaseModel):
        return value.to_dict()
    return None


def to_json(value: object) -> str:
    """Compact JSON for a content attribute. Values that JSON cannot hold become their `str()`."""
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False, default=str)
