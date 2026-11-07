from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any
from contextlib import AbstractContextManager, nullcontext, contextmanager
from collections.abc import Mapping, Iterator, Sequence

from opentelemetry import trace
from opentelemetry.trace import Status, SpanKind, StatusCode

from ._utils import get
from ._content import tool_result_content, set_content_attributes
from ..._tracing import ERROR_TYPE, set_error_status
from ._attributes import attributes
from ...types.beta import BetaToolResultBlockParam
from .._stainless_helpers import get_helper_tag

if TYPE_CHECKING:
    from ..._base_client import BaseClient
    from ..tools._beta_session_runner import DispatchedToolResultParams

__all__ = [
    "start_tool_runner_span",
    "set_tool_runner_status",
    "end_tool_runner_span",
    "tool_use_span",
    "as_current_span",
    "ToolRun",
]

log: logging.Logger = logging.getLogger(__name__)


def start_tool_runner_span(
    client: BaseClient[Any, Any], *, model: str, params: Mapping[str, object]
) -> trace.Span | None:
    """Starts the span of one loop of the Messages tool runner. The runner sets its status and ends it.

    Never raises: a loop whose span cannot start runs without one.
    """
    tracer = client._tracer
    if tracer is None:
        return None
    try:
        # `output_format` is the deprecated form of `output_config.format`. Here it is a type that the runner makes a
        # JSON schema of.
        output_format = get(params.get("output_config"), "format")
        json_output = get(output_format, "type") == "json_schema" or isinstance(params.get("output_format"), type)
        return tracer.start_span(
            "anthropic.messages.tool_runner",
            kind=SpanKind.INTERNAL,
            attributes=attributes(
                {
                    "gen_ai.operation.name": "invoke_agent",
                    "gen_ai.provider.name": client._otel.provider_name,
                    "gen_ai.request.model": model,
                    "gen_ai.conversation.id": client._otel.conversation_id,
                    "gen_ai.output.type": "json" if json_output else None,
                }
            ),
        )
    except Exception:
        log.debug("Could not start the span of a tool runner", exc_info=True)
        return None


def set_tool_runner_status(span: trace.Span | None, error: BaseException | None = None) -> None:
    """Sets the status of a tool runner's span, if it has one: `OK`, or what `error` makes it. Never raises."""
    if span is None:
        return
    try:
        if error is None:
            span.set_status(Status(StatusCode.OK))
        else:
            set_error_status(span, error)
    except Exception:
        log.debug("Could not set the status of the span of a tool runner", exc_info=True)


def end_tool_runner_span(span: trace.Span | None) -> None:
    """Ends a tool runner's span, if it has one. Never raises."""
    if span is None:
        return
    try:
        span.end()
    except Exception:
        log.debug("Could not end the span of a tool runner", exc_info=True)


@contextmanager
def tool_use_span(
    client: BaseClient[Any, Any],
    tool: object,
    *,
    tool_use_id: str,
    tool_name: str,
    input: object,
    toolset_name: str | None = None,
    agent_tool: bool = False,
    session_id: str | None = None,
    session_thread_id: str | None = None,
    conversation_id: str | None = None,
) -> Iterator[ToolRun]:
    """Runs the block in the span of one client tool run, which ends with the result that the block set on the run.

    The span is named `anthropic.tool_use` for an agent-toolset tool (`agent_tool`), `anthropic.mcp_tool_use` for
    a tool the MCP helper made, and `anthropic.custom_tool_use` for any other tool, followed by the tool's name.
    Its conversation ID is the one that the client's options set, or else `conversation_id`.
    `toolset_name` is the one of the `tool_use` block or Session event, when it has one.
    A run whose span cannot start runs without one.
    """
    run = ToolRun()
    tracer = client._tracer
    if tracer is None:
        yield run
        return

    span: trace.Span | None = None
    try:
        if agent_tool:
            operation = "anthropic.tool_use"
        elif get_helper_tag(tool) == "mcp_tool":
            operation = "anthropic.mcp_tool_use"
        else:
            operation = "anthropic.custom_tool_use"
        span = tracer.start_span(
            f"{operation} {tool_name}" if tool_name else operation,
            kind=SpanKind.INTERNAL,
            attributes=attributes(
                {
                    "gen_ai.operation.name": "execute_tool",
                    "gen_ai.provider.name": client._otel.provider_name,
                    "gen_ai.tool.name": tool_name,
                    "anthropic.toolset.name": toolset_name if isinstance(toolset_name, str) else None,
                    "gen_ai.tool.description": tool_description(tool),
                    "gen_ai.tool.call.id": tool_use_id,
                    "gen_ai.conversation.id": client._otel.conversation_id or conversation_id,
                    "anthropic.session.id": session_id,
                    "anthropic.session.thread.id": session_thread_id,
                    "gen_ai.tool.type": "function",
                }
            ),
        )
    except Exception:
        log.debug("Could not start the span of a tool run", exc_info=True)
    if span is None:
        yield run
        return

    try:
        with as_current_span(span):
            yield run
    finally:
        end_tool_use_span(client, span, input, run)


def tool_description(tool: object) -> str | None:
    # Imported here: the package of the tool helpers imports the runners, which import this module.
    from ..tools._beta_functions import BaseFunctionTool, BetaBuiltinFunctionTool, BetaAsyncBuiltinFunctionTool

    description: object = None
    if isinstance(tool, BaseFunctionTool):
        description = tool.description
    elif isinstance(tool, (BetaBuiltinFunctionTool, BetaAsyncBuiltinFunctionTool)):
        description = tool.to_dict().get("description")
    # A function tool without a description or a docstring has an empty one.
    return description if isinstance(description, str) and description else None


def as_current_span(span: trace.Span | None) -> AbstractContextManager[object]:
    """Makes `span`, if any, the current span for the block, without ending it when the block exits."""
    if span is None:
        return nullcontext()
    return trace.use_span(span, end_on_exit=False, record_exception=False, set_status_on_exception=False)


class ToolRun:
    """What a tool runner made of one tool run to send back to the model, for the run's span."""

    result: BetaToolResultBlockParam | DispatchedToolResultParams | None = None
    """It stays `None` when the run was interrupted before the runner made anything of it."""

    content: Sequence[Mapping[str, object]] | None = None
    """What the span records in place of the result's content. The Sessions tool runner sends some blocks as the text
    of their JSON, and the span has the blocks themselves."""


def end_tool_use_span(client: BaseClient[Any, Any], span: trace.Span, input: object, run: ToolRun) -> None:
    """Ends the span with the run's result. An error result fails it with `tool_error`, and none leaves its status unset.

    Never raises.
    """
    result = run.result
    try:
        if span.is_recording() and client._otel.records_content:
            content = None if result is None else tool_result_content(run.content or result.get("content"))
            set_content_attributes(
                span,
                {"gen_ai.tool.call.arguments": input, "anthropic.tool_result.content": content},
                limit=client._otel.max_content_bytes,
            )
    except Exception:
        log.debug("Could not record the tool run on its span", exc_info=True)

    try:
        if result is not None and result.get("is_error") is True:
            span.set_status(Status(StatusCode.ERROR))
            span.set_attribute(ERROR_TYPE, "tool_error")
        elif result is not None:
            span.set_status(Status(StatusCode.OK))
        span.end()
    except Exception:
        log.debug("Could not end the span of a tool run", exc_info=True)
