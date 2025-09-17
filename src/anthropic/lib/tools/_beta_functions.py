from __future__ import annotations

import logging
from typing import Any, Union, Generic, TypeVar, Callable, Iterable, Coroutine, cast, overload
from inspect import iscoroutinefunction
from typing_extensions import TypeAlias, override

import pydantic
import docstring_parser
from pydantic import BaseModel

from ... import _compat
from ..._utils import is_dict
from ..._compat import cached_property
from ..._models import TypeAdapter
from ..._utils._utils import CallableT
from ...types.tool_param import ToolParam, InputSchema
from ...types.beta.beta_tool_result_block_param import Content as BetaContent

log = logging.getLogger(__name__)

BetaFunctionToolResultType: TypeAlias = Union[str, Iterable[BetaContent]]

Function = Callable[..., BetaFunctionToolResultType]
FunctionT = TypeVar("FunctionT", bound=Function)

AsyncFunction = Callable[..., Coroutine[Any, Any, BetaFunctionToolResultType]]
AsyncFunctionT = TypeVar("AsyncFunctionT", bound=AsyncFunction)


class BaseFunctionTool(Generic[CallableT]):
    func: CallableT
    """The function this tool is wrapping"""

    name: str
    """The name of the tool that will be sent to the API"""

    description: str

    input_schema: InputSchema

    def __init__(
        self,
        func: CallableT,
        *,
        name: str | None = None,
        description: str | None = None,
        input_schema: InputSchema | type[BaseModel] | None = None,
    ) -> None:
        if _compat.PYDANTIC_V1:
            raise RuntimeError("Tool functions are only supported with Pydantic v2")

        self.func = func
        self._func_with_validate = pydantic.validate_call(func)
        self.name = name or func.__name__

        self.description = description or self._get_description_from_docstring()

        if input_schema is not None:
            if isinstance(input_schema, type):
                self.input_schema: InputSchema = input_schema.model_json_schema()
            else:
                self.input_schema = input_schema
        else:
            self.input_schema = self._create_schema_from_function()

    @property
    def __call__(self) -> CallableT:
        return self.func

    def to_dict(self) -> ToolParam:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }

    @cached_property
    def _parsed_docstring(self) -> docstring_parser.Docstring:
        return docstring_parser.parse(self.func.__doc__ or "")

    def _get_description_from_docstring(self) -> str:
        """Extract description from parsed docstring."""
        if self._parsed_docstring.short_description:
            description = self._parsed_docstring.short_description
            if self._parsed_docstring.long_description:
                description += f"\n\n{self._parsed_docstring.long_description}"
            return description
        return ""

    def _create_schema_from_function(self) -> InputSchema:
        """Create JSON schema from function signature using pydantic."""

        from pydantic_core import CoreSchema
        from pydantic.json_schema import JsonSchemaValue, GenerateJsonSchema
        from pydantic_core.core_schema import ArgumentsParameter

        class CustomGenerateJsonSchema(GenerateJsonSchema):
            def __init__(self, *, func: Callable[..., Any], parsed_docstring: Any) -> None:
                super().__init__()
                self._func = func
                self._parsed_docstring = parsed_docstring

            def __call__(self, *_args: Any, **_kwds: Any) -> "CustomGenerateJsonSchema":  # noqa: ARG002
                return self

            @override
            def kw_arguments_schema(
                self,
                arguments: "list[ArgumentsParameter]",
                var_kwargs_schema: CoreSchema | None,
            ) -> JsonSchemaValue:
                schema = super().kw_arguments_schema(arguments, var_kwargs_schema)
                if schema.get("type") != "object":
                    return schema

                properties = schema.get("properties")
                if not properties or not is_dict(properties):
                    return schema

                # Add parameter descriptions from docstring
                for param in self._parsed_docstring.params:
                    prop_schema = properties.get(param.arg_name)
                    if not prop_schema or not is_dict(prop_schema):
                        continue

                    if param.description and "description" not in prop_schema:
                        prop_schema["description"] = param.description

                return schema

        schema_generator = CustomGenerateJsonSchema(func=self.func, parsed_docstring=self._parsed_docstring)
        return self._adapter.json_schema(schema_generator=schema_generator)  # type: ignore

    @cached_property
    def _adapter(self) -> TypeAdapter[Any]:
        return TypeAdapter(self._func_with_validate)


class BetaFunctionTool(BaseFunctionTool[FunctionT]):
    def call(self, input: object) -> BetaFunctionToolResultType:
        if iscoroutinefunction(self.func):
            raise RuntimeError("Cannot call a coroutine function synchronously. Use `@async_tool` instead.")

        if not is_dict(input):
            raise TypeError(f"Input must be a dictionary, got {type(input).__name__}")

        try:
            return self._func_with_validate(**cast(Any, input))
        except pydantic.ValidationError as e:
            raise ValueError(f"Invalid arguments for function {self.name}") from e


class BetaAsyncFunctionTool(BaseFunctionTool[AsyncFunctionT]):
    async def call(self, input: object) -> BetaFunctionToolResultType:
        if not iscoroutinefunction(self.func):
            raise RuntimeError("Cannot call a synchronous function asynchronously. Use `@tool` instead.")

        if not is_dict(input):
            raise TypeError(f"Input must be a dictionary, got {type(input).__name__}")

        try:
            return await self._func_with_validate(**cast(Any, input))
        except pydantic.ValidationError as e:
            raise ValueError(f"Invalid arguments for function {self.name}") from e


@overload
def beta_tool(func: FunctionT) -> BetaFunctionTool[FunctionT]: ...


@overload
def beta_tool(
    func: FunctionT,
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
) -> BetaFunctionTool[FunctionT]: ...


@overload
def beta_tool(
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
) -> Callable[[FunctionT], BetaFunctionTool[FunctionT]]: ...


def beta_tool(
    func: FunctionT | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
) -> BetaFunctionTool[FunctionT] | Callable[[FunctionT], BetaFunctionTool[FunctionT]]:
    """Create a FunctionTool from a function with automatic schema inference.

    Can be used as a decorator with or without parentheses:

    @function_tool
    def my_func(x: int) -> str: ...

    @function_tool()
    def my_func(x: int) -> str: ...

    @function_tool(name="custom_name")
    def my_func(x: int) -> str: ...
    """
    if _compat.PYDANTIC_V1:
        raise RuntimeError("Tool functions are only supported with Pydantic v2")

    if func is not None:
        # @beta_tool called without parentheses
        return BetaFunctionTool(func=func, name=name, description=description, input_schema=input_schema)

    # @beta_tool()
    def decorator(func: FunctionT) -> BetaFunctionTool[FunctionT]:
        return BetaFunctionTool(func=func, name=name, description=description, input_schema=input_schema)

    return decorator


@overload
def beta_async_tool(func: AsyncFunctionT) -> BetaAsyncFunctionTool[AsyncFunctionT]: ...


@overload
def beta_async_tool(
    func: AsyncFunctionT,
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
) -> BetaAsyncFunctionTool[AsyncFunctionT]: ...


@overload
def beta_async_tool(
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
) -> Callable[[AsyncFunctionT], BetaAsyncFunctionTool[AsyncFunctionT]]: ...


def beta_async_tool(
    func: AsyncFunctionT | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
) -> BetaAsyncFunctionTool[AsyncFunctionT] | Callable[[AsyncFunctionT], BetaAsyncFunctionTool[AsyncFunctionT]]:
    """Create an AsyncFunctionTool from a function with automatic schema inference.

    Can be used as a decorator with or without parentheses:

    @async_tool
    async def my_func(x: int) -> str: ...

    @async_tool()
    async def my_func(x: int) -> str: ...

    @async_tool(name="custom_name")
    async def my_func(x: int) -> str: ...
    """
    if _compat.PYDANTIC_V1:
        raise RuntimeError("Tool functions are only supported with Pydantic v2")

    if func is not None:
        # @beta_async_tool called without parentheses
        return BetaAsyncFunctionTool(
            func=func,
            name=name,
            description=description,
            input_schema=input_schema,
        )

    # @beta_async_tool()
    def decorator(func: AsyncFunctionT) -> BetaAsyncFunctionTool[AsyncFunctionT]:
        return BetaAsyncFunctionTool(
            func=func,
            name=name,
            description=description,
            input_schema=input_schema,
        )

    return decorator
