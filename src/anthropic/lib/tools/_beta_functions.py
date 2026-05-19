from __future__ import annotations

import sys
import logging
from abc import ABC, abstractmethod
from typing import Any, Union, Generic, TypeVar, Callable, Iterable, Coroutine, cast, overload
from inspect import isawaitable, isasyncgenfunction, iscoroutinefunction, isgeneratorfunction
from collections.abc import Awaitable
from typing_extensions import Literal, TypeAlias, override

import anyio
import pydantic
import docstring_parser
from pydantic import BaseModel

from ... import _compat
from ..._utils import is_dict
from ..._compat import cached_property
from ..._models import TypeAdapter
from ...types.beta import BetaToolParam, BetaToolUnionParam, BetaCacheControlEphemeralParam
from ..._utils._utils import CallableT
from ...types.tool_param import InputSchema
from ...types.beta.beta_tool_result_block_param import Content as BetaContent

log = logging.getLogger(__name__)

BetaFunctionToolResultType: TypeAlias = Union[str, Iterable[BetaContent]]


class ToolError(Exception):
    """Error that can be raised from a tool to return structured content with ``is_error: True``.

    When the tool runner catches this error, it will use the :attr:`content`
    property as the tool result instead of ``repr(exc)``.

    Example::

        raise ToolError(
            [
                {"type": "text", "text": "Error details here"},
                {"type": "image", "source": {"type": "base64", "data": "...", "media_type": "image/png"}},
            ]
        )
    """

    content: BetaFunctionToolResultType

    def __init__(self, content: BetaFunctionToolResultType) -> None:
        if isinstance(content, str):
            message = content
        else:
            parts: list[str] = []
            for block in content:
                text = block.get("text")
                if text is not None:
                    parts.append(str(text))
                else:
                    parts.append(f"[{block.get('type', 'unknown')}]")
            message = " ".join(parts) if parts else "Tool error"
        super().__init__(message)
        self.content = content


Function = Callable[..., BetaFunctionToolResultType]
FunctionT = TypeVar("FunctionT", bound=Function)

AsyncFunction = Callable[..., Coroutine[Any, Any, BetaFunctionToolResultType]]
AsyncFunctionT = TypeVar("AsyncFunctionT", bound=AsyncFunction)


class BetaBuiltinFunctionTool(ABC):
    @abstractmethod
    def to_dict(self) -> BetaToolUnionParam: ...

    @abstractmethod
    def call(self, input: object) -> BetaFunctionToolResultType: ...

    @property
    def name(self) -> str:
        raw = self.to_dict()
        if "mcp_server_name" in raw:
            return raw["mcp_server_name"]
        return raw["name"]


class BetaAsyncBuiltinFunctionTool(ABC):
    @abstractmethod
    def to_dict(self) -> BetaToolUnionParam: ...

    @abstractmethod
    async def call(self, input: object) -> BetaFunctionToolResultType: ...

    @property
    def name(self) -> str:
        raw = self.to_dict()
        if "mcp_server_name" in raw:
            return raw["mcp_server_name"]
        return raw["name"]


class BaseFunctionTool(Generic[CallableT]):
    func: CallableT
    """The function this tool is wrapping"""

    name: str
    """The name of the tool that will be sent to the API"""

    description: str

    input_schema: InputSchema

    close: Callable[[], None | Awaitable[None]] | None = None
    """Optional cleanup hook.

    A tool that owns a resource (a subprocess, a connection, …) may set this on
    its instance; the result is awaited if it returns an awaitable.

    Which runners actually invoke it differs — check before relying on it for a
    stateful tool:

    - ``SessionToolRunner`` (``client.beta.sessions.events.tool_runner(...)``)
      and the :class:`~anthropic.lib.environments.EnvironmentWorker` built on it
      **do** call ``close`` when the run ends.
    - The Messages :class:`BetaToolRunner` / ``BetaAsyncToolRunner``
      (``client.beta.messages.tool_runner(...)``) does **not** call ``close``.
      A stateful tool (e.g. the ``bash`` tool's subprocess) handed to the
      Messages tool runner therefore leaks its resource — run it under
      ``SessionToolRunner`` / the environment worker instead.
    """

    _context_manager: object | None = None
    """Set by :func:`beta_tool` / :func:`beta_async_tool` when the tool was
    defined as a (sync/async) context manager: the *entered* context manager
    whose ``__exit__`` / ``__aexit__`` the tool-runner cleanup path drives on the
    way out. Additive to :attr:`close` — both run if both are present, so other
    tool-runner consumers that only set ``close`` keep working unchanged.
    """

    def __init__(
        self,
        func: CallableT,
        *,
        name: str | None = None,
        description: str | None = None,
        input_schema: InputSchema | type[BaseModel] | None = None,
        defer_loading: bool | None = None,
        cache_control: BetaCacheControlEphemeralParam | None = None,
        allowed_callers: list[Literal["direct", "code_execution_20250825", "code_execution_20260120"]] | None = None,
        eager_input_streaming: bool | None = None,
        input_examples: Iterable[dict[str, object]] | None = None,
        strict: bool | None = None,
    ) -> None:
        if _compat.PYDANTIC_V1:
            raise RuntimeError("Tool functions are only supported with Pydantic v2")

        self.func = func
        self._func_with_validate = pydantic.validate_call(func)
        self.name = name or func.__name__
        self._defer_loading = defer_loading
        self._cache_control = cache_control
        self._allowed_callers = allowed_callers
        self._eager_input_streaming = eager_input_streaming
        self._input_examples = input_examples
        self._strict = strict

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

    def to_dict(self) -> BetaToolParam:
        defn: BetaToolParam = {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }
        if self._defer_loading is not None:
            defn["defer_loading"] = self._defer_loading
        if self._cache_control is not None:
            defn["cache_control"] = self._cache_control
        if self._allowed_callers is not None:
            defn["allowed_callers"] = self._allowed_callers
        if self._eager_input_streaming is not None:
            defn["eager_input_streaming"] = self._eager_input_streaming
        if self._input_examples is not None:
            defn["input_examples"] = self._input_examples
        if self._strict is not None:
            defn["strict"] = self._strict
        return defn

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


def _is_sync_cm_factory(fn: object) -> bool:
    """True when ``fn`` is a function produced by :func:`contextlib.contextmanager`.

    ``contextmanager`` wraps the generator function with ``functools.wraps``, so
    the original generator function is reachable as ``__wrapped__`` — the same
    signal :mod:`inspect` itself uses. We never call ``fn`` to find out, so a
    plain tool function is never accidentally invoked during detection.
    """
    wrapped = getattr(fn, "__wrapped__", None)
    return wrapped is not None and isgeneratorfunction(wrapped)


def _is_async_cm_factory(fn: object) -> bool:
    """True when ``fn`` is a function produced by :func:`contextlib.asynccontextmanager`."""
    wrapped = getattr(fn, "__wrapped__", None)
    return wrapped is not None and isasyncgenfunction(wrapped)


async def aclose_runnable_tool(tool: object) -> None:
    """Run a runnable tool's optional cleanup.

    Drives the legacy ``aclose`` / ``close`` attribute (awaited if it returns an
    awaitable) and, when the tool was defined as a context manager via
    :func:`beta_tool` / :func:`beta_async_tool`, its ``__exit__`` /
    ``__aexit__``. Both run when both are present — the context-manager support
    is purely additive to ``close``. Exceptions are logged, never raised, so one
    tool's bad cleanup can't abort another tool's.
    """
    closer = getattr(tool, "aclose", None) or getattr(tool, "close", None)
    if closer is not None:
        try:
            result = closer()
            if isawaitable(result):
                await result
        except Exception as e:
            log.warning("tool.close failed tool=%s error=%s", getattr(tool, "name", "?"), e)

    cm = getattr(tool, "_context_manager", None)
    if cm is not None:
        try:
            aexit = getattr(cm, "__aexit__", None)
            if aexit is not None:
                await aexit(None, None, None)
            else:
                cm.__exit__(None, None, None)
        except Exception as e:
            log.warning("tool context-manager cleanup failed tool=%s error=%s", getattr(tool, "name", "?"), e)


@overload
def beta_tool(func: FunctionT) -> BetaFunctionTool[FunctionT]: ...


@overload
def beta_tool(
    func: FunctionT,
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
    defer_loading: bool | None = None,
    cache_control: BetaCacheControlEphemeralParam | None = None,
    allowed_callers: list[Literal["direct", "code_execution_20250825", "code_execution_20260120"]] | None = None,
    eager_input_streaming: bool | None = None,
    input_examples: Iterable[dict[str, object]] | None = None,
    strict: bool | None = None,
) -> BetaFunctionTool[FunctionT]: ...


@overload
def beta_tool(
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
    defer_loading: bool | None = None,
    cache_control: BetaCacheControlEphemeralParam | None = None,
    allowed_callers: list[Literal["direct", "code_execution_20250825", "code_execution_20260120"]] | None = None,
    eager_input_streaming: bool | None = None,
    input_examples: Iterable[dict[str, object]] | None = None,
    strict: bool | None = None,
) -> Callable[[FunctionT], BetaFunctionTool[FunctionT]]: ...


def beta_tool(
    func: FunctionT | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
    defer_loading: bool | None = None,
    cache_control: BetaCacheControlEphemeralParam | None = None,
    allowed_callers: list[Literal["direct", "code_execution_20250825", "code_execution_20260120"]] | None = None,
    eager_input_streaming: bool | None = None,
    input_examples: Iterable[dict[str, object]] | None = None,
    strict: bool | None = None,
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

    def _make(fn: FunctionT) -> BetaFunctionTool[FunctionT]:
        if _is_async_cm_factory(fn):
            raise TypeError(
                "@beta_tool was applied to an @asynccontextmanager; "
                "use @beta_async_tool for an async context-manager tool"
            )
        if _is_sync_cm_factory(fn):
            # The decorated function is a @contextmanager that yields the tool
            # callable: enter it now to obtain the callable, build the tool from
            # it (so schema inference still sees the real signature), and keep
            # the entered context manager so the runner cleanup can exit it.
            cm = cast(Any, fn)()
            inner = cm.__enter__()
            try:
                tool = BetaFunctionTool(
                    cast(FunctionT, inner),
                    name=name,
                    description=description,
                    input_schema=input_schema,
                    defer_loading=defer_loading,
                    cache_control=cache_control,
                    allowed_callers=allowed_callers,
                    eager_input_streaming=eager_input_streaming,
                    input_examples=input_examples,
                    strict=strict,
                )
            except BaseException:
                # Construction failed after we entered the context manager —
                # unwind it so its resource isn't leaked.
                cm.__exit__(*sys.exc_info())
                raise
            tool._context_manager = cm
            return tool
        return BetaFunctionTool(
            fn,
            name=name,
            description=description,
            input_schema=input_schema,
            defer_loading=defer_loading,
            cache_control=cache_control,
            allowed_callers=allowed_callers,
            eager_input_streaming=eager_input_streaming,
            input_examples=input_examples,
            strict=strict,
        )

    if func is not None:
        return _make(func)

    return _make


@overload
def beta_async_tool(func: AsyncFunctionT) -> BetaAsyncFunctionTool[AsyncFunctionT]: ...


@overload
def beta_async_tool(
    func: AsyncFunctionT,
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
    defer_loading: bool | None = None,
    cache_control: BetaCacheControlEphemeralParam | None = None,
    allowed_callers: list[Literal["direct", "code_execution_20250825", "code_execution_20260120"]] | None = None,
    eager_input_streaming: bool | None = None,
    input_examples: Iterable[dict[str, object]] | None = None,
    strict: bool | None = None,
) -> BetaAsyncFunctionTool[AsyncFunctionT]: ...  # noqa: E501


@overload
def beta_async_tool(
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
    defer_loading: bool | None = None,
    cache_control: BetaCacheControlEphemeralParam | None = None,
    allowed_callers: list[Literal["direct", "code_execution_20250825", "code_execution_20260120"]] | None = None,
    eager_input_streaming: bool | None = None,
    input_examples: Iterable[dict[str, object]] | None = None,
    strict: bool | None = None,
) -> Callable[[AsyncFunctionT], BetaAsyncFunctionTool[AsyncFunctionT]]: ...


def beta_async_tool(
    func: AsyncFunctionT | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
    input_schema: InputSchema | type[BaseModel] | None = None,
    defer_loading: bool | None = None,
    cache_control: BetaCacheControlEphemeralParam | None = None,
    allowed_callers: list[Literal["direct", "code_execution_20250825", "code_execution_20260120"]] | None = None,
    eager_input_streaming: bool | None = None,
    input_examples: Iterable[dict[str, object]] | None = None,
    strict: bool | None = None,
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

    def _make(fn: AsyncFunctionT) -> BetaAsyncFunctionTool[AsyncFunctionT]:
        if _is_sync_cm_factory(fn):
            raise TypeError(
                "@beta_async_tool was applied to a @contextmanager; use @beta_tool for a sync context-manager tool"
            )
        if _is_async_cm_factory(fn):
            # The decorated function is an @asynccontextmanager that yields the
            # tool callable. Entering it requires awaiting, which the decorator
            # can't do, so enter lazily on first call and cache the result; the
            # parameters can't be inferred until then, so an explicit
            # ``input_schema`` is required.
            if input_schema is None:
                raise TypeError(
                    "an @asynccontextmanager tool needs an explicit input_schema= "
                    "(its parameters can't be inferred until the context manager is entered)"
                )
            cm = cast(Any, fn)()
            state: dict[str, Any] = {"validated": None, "entered": False}
            enter_lock = anyio.Lock()
            tool_box: list[BetaAsyncFunctionTool[AsyncFunctionT]] = []

            async def _entered() -> Any:
                if not state["entered"]:
                    async with enter_lock:
                        if not state["entered"]:
                            inner = await cm.__aenter__()
                            state["validated"] = pydantic.validate_call(inner)
                            state["entered"] = True
                            # Only now is there an entered __aexit__ to drive on
                            # the cleanup path.
                            tool_box[0]._context_manager = cm
                return state["validated"]

            async def _lazy(**kwargs: Any) -> BetaFunctionToolResultType:
                validated = await _entered()
                return cast(BetaFunctionToolResultType, await validated(**kwargs))

            _lazy.__name__ = name or getattr(fn, "__name__", "tool")
            _lazy.__doc__ = description if description is not None else getattr(fn, "__doc__", None)
            tool = BetaAsyncFunctionTool(
                cast(AsyncFunctionT, _lazy),
                name=name,
                description=description,
                input_schema=input_schema,
                defer_loading=defer_loading,
                cache_control=cache_control,
                allowed_callers=allowed_callers,
                eager_input_streaming=eager_input_streaming,
                input_examples=input_examples,
                strict=strict,
            )
            tool_box.append(tool)
            return tool
        return BetaAsyncFunctionTool(
            fn,
            name=name,
            description=description,
            input_schema=input_schema,
            defer_loading=defer_loading,
            cache_control=cache_control,
            allowed_callers=allowed_callers,
            eager_input_streaming=eager_input_streaming,
            input_examples=input_examples,
            strict=strict,
        )

    if func is not None:
        return _make(func)

    return _make


BetaRunnableTool = Union[BetaFunctionTool[Any], BetaBuiltinFunctionTool]
BetaAsyncRunnableTool = Union[BetaAsyncFunctionTool[Any], BetaAsyncBuiltinFunctionTool]
