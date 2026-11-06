from __future__ import annotations

from typing import List, Union, Generic, Mapping, TypeVar, Iterable, cast
from typing_extensions import Literal, Required, TypedDict

import httpx2

from ..._types import Body, Omit, Query, Headers
from ..._utils import is_given
from ...types.beta import (
    BetaMessageParam,
    ThreadSendParams,
    BetaToolUnionParam,
    ThreadCreateParams,
    BetaMessageThreadParam,
)
from ...types.model_param import ModelParam
from ..tools._beta_functions import BetaRunnableTool, BetaAsyncRunnableTool
from ...types.beta.parsed_beta_message import ResponseFormatT
from ...types.beta.message_create_params import ParseMessageCreateParamsBase


class UnchangedCreateFields(ThreadCreateParams, total=False):
    """The `create()` fields that `thread()` takes as they are, the required ones included."""

    max_tokens: Required[int]
    model: Required[ModelParam]


class ThreadFields(UnchangedCreateFields, total=False):
    """The `create()` fields a thread holds between turns: every field except `messages`, `thread` and `stream`."""

    tools: Iterable[BetaToolUnionParam]


class RequestOptions(TypedDict, total=False):
    extra_headers: Headers
    extra_query: Query
    extra_body: Body
    timeout: Union[float, httpx2.Timeout, None]


class TurnOverrides(ThreadSendParams, RequestOptions, total=False):
    """Per-turn overrides for `send()` / `parse()` / `stream()`: any `ThreadFields` field except `output_config`, or a
    request option. Anything omitted falls back to the thread's value."""

    tools: Iterable[BetaToolUnionParam]


RunnableToolT = TypeVar("RunnableToolT", bound=BetaRunnableTool | BetaAsyncRunnableTool)


class ThreadParams(UnchangedCreateFields, Generic[RunnableToolT, ResponseFormatT], total=False):
    """A thread as the arguments of one `thread()` call for the whole conversation: its request fields, tools
    (`@beta_tool` functions included), output format, full history and `unsupported_request_behavior`."""

    messages: Required[List[BetaMessageParam]]
    tools: Iterable[Union[BetaToolUnionParam, RunnableToolT]]
    output_format: type[ResponseFormatT]
    unsupported_request_behavior: Required[UnsupportedRequestBehavior]


UnsupportedRequestBehavior = Literal["error", "continue_unthreaded"]
"""What a thread does with a request the server cannot thread: `"error"`, the default, raises the API's error, and
`"continue_unthreaded"` sends that turn and every later one with the full history and no `thread`."""


class CreateArguments(ThreadFields, RequestOptions, total=False):
    """The keyword arguments of one turn's `create()` call, except `stream`."""

    messages: Required[List[BetaMessageParam]]
    thread: BetaMessageThreadParam


def thread_arguments(
    params: ThreadCreateParams,
    *,
    max_tokens: int,
    model: ModelParam,
    messages: Iterable[BetaMessageParam] | Omit,
    tools: Iterable[BetaToolUnionParam | BetaRunnableTool | BetaAsyncRunnableTool] | Omit,
    output_format: type[ResponseFormatT] | None | Omit,
) -> ParseMessageCreateParamsBase[ResponseFormatT]:
    """The arguments of a `thread()` call as the params a thread's state starts from."""
    reject_unexpected_keywords(params, ThreadCreateParams)

    return cast(
        ParseMessageCreateParamsBase[ResponseFormatT],
        given(
            {
                **params,
                "max_tokens": max_tokens,
                "model": model,
                "messages": messages if is_given(messages) else [],
                "tools": tools,
                "output_format": output_format,
            }
        ),
    )


def turn_overrides(**values: object) -> TurnOverrides:
    """The given keyword arguments as `TurnOverrides`, without the ones left at their "not given" default."""
    reject_unexpected_keywords(values, TurnOverrides)
    return cast(TurnOverrides, given(values))


def request_options(**values: object) -> RequestOptions:
    """The given keyword arguments as `RequestOptions`, without the ones left at their "not given" default."""
    return cast(RequestOptions, given(values))


def reject_unexpected_keywords(
    keywords: Mapping[str, object], params_type: type[ThreadCreateParams] | type[TurnOverrides]
) -> None:
    """Raise the `TypeError` of a signature that spells its keywords out, because `**params: Unpack[...]` takes any
    keyword at runtime and the thread would leave out one it does not know, such as `thread`, without a word."""
    unexpected = sorted(keywords.keys() - params_type.__annotations__.keys())
    if unexpected:
        raise TypeError(f"Got an unexpected keyword argument '{unexpected[0]}'")


def reject_thread_param(thread: object) -> None:
    if thread is None or thread is False or not is_given(thread):
        return
    raise TypeError(
        f"`thread` cannot be set in the params of a tool runner, got {thread!r}. The runner sets it for each request "
        "itself. To run without a message thread, pass `thread=False` to `tool_runner()`."
    )


def given(values: Mapping[str, object]) -> dict[str, object]:
    """`values` without the entries whose value is `omit` or `not_given`, or `None` for an `extra_*` request option
    (whose "not given" default is `None`)."""
    return {
        key: value
        for key, value in values.items()
        if is_given(value) and not (value is None and key in NONE_MEANS_NOT_GIVEN)
    }


NONE_MEANS_NOT_GIVEN = frozenset({"extra_headers", "extra_query", "extra_body"})


def override_fields(params: ThreadFields, overrides: TurnOverrides) -> ThreadFields:
    """`params` with every field that `overrides` sets replaced."""
    return cast(ThreadFields, {**params, **{key: value for key, value in overrides.items() if key in THREAD_FIELDS}})


THREAD_FIELDS = ThreadFields.__required_keys__ | ThreadFields.__optional_keys__


def override_request_options(options: RequestOptions, overrides: TurnOverrides) -> RequestOptions:
    """`options` with every request option that `overrides` sets replaced as a whole."""
    return cast(
        RequestOptions, {**options, **{key: value for key, value in overrides.items() if key in REQUEST_OPTIONS}}
    )


REQUEST_OPTIONS = RequestOptions.__optional_keys__
