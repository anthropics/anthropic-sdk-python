from __future__ import annotations

import inspect
from typing import Any, Type, Union, Generic, TypeVar, cast
from datetime import date, datetime
from typing_extensions import final

try:
    from pydantic import v1 as pydantic
    from pydantic.v1 import generics, Extra
    from pydantic.v1.fields import ModelField
    from pydantic.v1.typing import get_args, is_union, get_origin, is_literal_type
    from pydantic.v1.datetime_parse import parse_date
except ImportError:
    import pydantic
    from pydantic import generics, Extra
    from pydantic.fields import ModelField
    from pydantic.typing import get_args, is_union, get_origin, is_literal_type
    from pydantic.datetime_parse import parse_date

from ._types import (
    Body,
    Query,
    ModelT,
    Headers,
    Timeout,
    NotGiven,
    AnyMapping,
    RequestFiles,
)
from ._utils import is_list, is_mapping, parse_datetime, strip_not_given

__all__ = ["BaseModel", "GenericModel"]

_T = TypeVar("_T")


class BaseModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        extra: Extra = Extra.allow

    def __str__(self) -> str:
        return f'{self.__repr_name__()}({self.__repr_str__(", ")})'

    # Override the 'construct' method in a way that supports recursive parsing without validation.
    # Based on https://github.com/samuelcolvin/pydantic/issues/1168#issuecomment-817742836.
    @classmethod
    def construct(
        cls: Type[ModelT],
        _fields_set: set[str] | None = None,
        **values: object,
    ) -> ModelT:
        m = cls.__new__(cls)
        fields_values: dict[str, object] = {}

        config = cls.__config__

        for name, field in cls.__fields__.items():
            key = field.alias
            if key not in values and config.allow_population_by_field_name:
                key = name

            if key in values:
                value = values[key]
                fields_values[name] = _construct_field(value=value, field=field)
            elif not field.required:
                fields_values[name] = field.get_default()

        for key, value in values.items():
            if key not in cls.__fields__:
                fields_values[key] = value

        object.__setattr__(m, "__dict__", fields_values)
        if _fields_set is None:
            _fields_set = set(fields_values.keys())
        object.__setattr__(m, "__fields_set__", _fields_set)
        m._init_private_attributes()
        return m


def _construct_field(value: object, field: ModelField) -> object:
    if value is None:
        return field.get_default()

    return construct_type(value=value, type_=field.outer_type_)


def construct_type(*, value: object, type_: type) -> object:
    """Loose coercion to the expected type with construction of nested values.

    If the given value does not match the expected type then it is returned as-is.
    """

    # we need to use the origin class for any types that are subscripted generics
    # e.g. Dict[str, object]
    origin = get_origin(type_) or type_
    args = get_args(type_)

    if is_union(origin):
        new_value, error = _create_pydantic_field(type_).validate(value, {}, loc="")
        if not error:
            return new_value

        # if the data is not valid, use the first variant that doesn't fail while deserializing
        for variant in args:
            try:
                return construct_type(value=value, type_=variant)
            except Exception:
                continue

        raise RuntimeError(f"Could not convert data into a valid instance of {type_}")

    if origin == dict:
        if not is_mapping(value):
            return value

        _, items_type = get_args(type_)  # Dict[_, items_type]
        return {key: construct_type(value=item, type_=items_type) for key, item in value.items()}

    if not is_literal_type(type_) and (issubclass(origin, BaseModel) or issubclass(origin, GenericModel)):
        if is_list(value):
            return [cast(Any, type_).construct(**entry) if is_mapping(entry) else entry for entry in value]

        if is_mapping(value):
            if issubclass(type_, BaseModel):
                return type_.construct(**value)  # type: ignore[arg-type]

            return cast(Any, type_).construct(**value)

    if origin == list:
        if not is_list(value):
            return value

        inner_type = args[0]  # List[inner_type]
        return [construct_type(value=entry, type_=inner_type) for entry in value]

    if origin == float:
        try:
            return float(cast(Any, value))
        except Exception:
            return value

    if origin == int:
        try:
            return int(cast(Any, value))
        except Exception:
            return value

    if type_ == datetime:
        try:
            return parse_datetime(value)  # type: ignore
        except Exception:
            return value

    if type_ == date:
        try:
            return parse_date(value)  # type: ignore
        except Exception:
            return value

    return value


def validate_type(*, type_: type[_T], value: object) -> _T:
    """Strict validation that the given value matches the expected type"""
    if inspect.isclass(type_) and issubclass(type_, pydantic.BaseModel):
        return cast(_T, type_.parse_obj(value))

    model = _create_pydantic_model(type_).validate(value)
    return cast(_T, model.__root__)


def _create_pydantic_model(type_: _T) -> Type[RootModel[_T]]:
    return RootModel[type_]  # type: ignore


def _create_pydantic_field(type_: type) -> ModelField:
    # TODO: benchmark this
    model_type = cast(Type[RootModel[object]], RootModel[type_])  # type: ignore
    return model_type.__fields__["__root__"]


class GenericModel(BaseModel, generics.GenericModel):
    pass


class RootModel(GenericModel, Generic[_T]):
    """Used as a placeholder to easily convert runtime types to a Pydantic format
    to provide validation.

    For example:
    ```py
    validated = RootModel[int](__root__='5').__root__
    # validated: 5
    ```
    """

    __root__: _T


@final
class FinalRequestOptions(pydantic.BaseModel):
    method: str
    url: str
    params: Query = {}
    headers: Union[Headers, NotGiven] = NotGiven()
    max_retries: Union[int, NotGiven] = NotGiven()
    timeout: Union[float, Timeout, None, NotGiven] = NotGiven()
    files: Union[RequestFiles, None] = None
    idempotency_key: Union[str, None] = None

    # It should be noted that we cannot use `json` here as that would override
    # a BaseModel method in an incompatible fashion.
    json_data: Union[Body, None] = None
    extra_json: Union[AnyMapping, None] = None

    class Config(pydantic.BaseConfig):
        arbitrary_types_allowed: bool = True

    def get_max_retries(self, max_retries: int) -> int:
        if isinstance(self.max_retries, NotGiven):
            return max_retries
        return self.max_retries

    # override the `construct` method so that we can run custom transformations.
    # this is necessary as we don't want to do any actual runtime type checking
    # (which means we can't use validators) but we do want to ensure that `NotGiven`
    # values are not present
    @classmethod
    def construct(
        cls,
        _fields_set: set[str] | None = None,
        **values: object,
    ) -> FinalRequestOptions:
        kwargs = {
            # we unconditionally call `strip_not_given` on any value
            # as it will just ignore any non-mapping types
            key: strip_not_given(value)
            for key, value in values.items()
        }
        return super().construct(_fields_set, **kwargs)
