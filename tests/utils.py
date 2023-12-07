from __future__ import annotations

import os
import traceback
import contextlib
from typing import Any, TypeVar, Iterator, cast
from datetime import date, datetime
from typing_extensions import Literal, get_args, get_origin, assert_type

from anthropic._types import NoneType
from anthropic._utils import is_dict, is_list, is_list_type, is_union_type
from anthropic._compat import PYDANTIC_V2, field_outer_type, get_model_fields
from anthropic._models import BaseModel

BaseModelT = TypeVar("BaseModelT", bound=BaseModel)


def assert_matches_model(model: type[BaseModelT], value: BaseModelT, *, path: list[str]) -> bool:
    for name, field in get_model_fields(model).items():
        field_value = getattr(value, name)
        if PYDANTIC_V2:
            allow_none = False
        else:
            # in v1 nullability was structured differently
            # https://docs.pydantic.dev/2.0/migration/#required-optional-and-nullable-fields
            allow_none = getattr(field, "allow_none", False)

        assert_matches_type(
            field_outer_type(field),
            field_value,
            path=[*path, name],
            allow_none=allow_none,
        )

    return True


# Note: the `path` argument is only used to improve error messages when `--showlocals` is used
def assert_matches_type(
    type_: Any,
    value: object,
    *,
    path: list[str],
    allow_none: bool = False,
) -> None:
    if allow_none and value is None:
        return

    if type_ is None or type_ is NoneType:
        assert value is None
        return

    origin = get_origin(type_) or type_

    if is_list_type(type_):
        return _assert_list_type(type_, value)

    if origin == str:
        assert isinstance(value, str)
    elif origin == int:
        assert isinstance(value, int)
    elif origin == bool:
        assert isinstance(value, bool)
    elif origin == float:
        assert isinstance(value, float)
    elif origin == datetime:
        assert isinstance(value, datetime)
    elif origin == date:
        assert isinstance(value, date)
    elif origin == object:
        # nothing to do here, the expected type is unknown
        pass
    elif origin == Literal:
        assert value in get_args(type_)
    elif origin == dict:
        assert is_dict(value)

        args = get_args(type_)
        key_type = args[0]
        items_type = args[1]

        for key, item in value.items():
            assert_matches_type(key_type, key, path=[*path, "<dict key>"])
            assert_matches_type(items_type, item, path=[*path, "<dict item>"])
    elif is_union_type(type_):
        for i, variant in enumerate(get_args(type_)):
            try:
                assert_matches_type(variant, value, path=[*path, f"variant {i}"])
                return
            except AssertionError:
                traceback.print_exc()
                continue

        assert False, "Did not match any variants"
    elif issubclass(origin, BaseModel):
        assert isinstance(value, type_)
        assert assert_matches_model(type_, cast(Any, value), path=path)
    else:
        assert None, f"Unhandled field type: {type_}"


def _assert_list_type(type_: type[object], value: object) -> None:
    assert is_list(value)

    inner_type = get_args(type_)[0]
    for entry in value:
        assert_type(inner_type, entry)  # type: ignore


@contextlib.contextmanager
def update_env(**new_env: str) -> Iterator[None]:
    old = os.environ.copy()

    try:
        os.environ.update(new_env)

        yield None
    finally:
        os.environ.clear()
        os.environ.update(old)
