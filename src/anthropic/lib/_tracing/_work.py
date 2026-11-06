from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from opentelemetry.trace import Span, Status, SpanKind, StatusCode

from ..._tracing import set_error_status
from ._attributes import attributes
from ...types.beta.environments import BetaSelfHostedWork

if TYPE_CHECKING:
    from ..._base_client import BaseClient

__all__ = ["WorkSpan"]

log: logging.Logger = logging.getLogger(__name__)


class WorkSpan:
    """The `anthropic.environment.work` span of the work item that a work poller returned last.

    The poller starts it when a poll returns the item, and ends it with status `OK` when its consumer asks
    for the next item or stops polling. A consumer that gives the poller its own `WorkSpan`, as the
    environment worker does, handles the item with `span` current and ends the span first, with how
    the handling went.
    """

    span: Span | None = None
    """`None` without a tracer, before the first item, and once the span has ended."""

    def start(self, client: BaseClient[Any, Any], work_item: BetaSelfHostedWork) -> None:
        """Starts the span of `work_item`. Never raises: an item whose span cannot start is handled without one."""
        tracer = client._tracer
        if tracer is None:
            return
        try:
            self.span = tracer.start_span(
                "anthropic.environment.work",
                kind=SpanKind.INTERNAL,
                attributes=attributes(
                    {
                        "gen_ai.provider.name": client._otel.provider_name,
                        "anthropic.environment.id": work_item.environment_id,
                        "anthropic.environment.work.id": work_item.id,
                        # An item that the generated type does not model can have no data, or data without an ID.
                        "anthropic.session.id": getattr(work_item.data, "id", None),
                    }
                ),
            )
        except Exception:
            log.debug("Could not start the span of a work item", exc_info=True)

    def end(self, error: BaseException | None = None, *, finished: bool = True) -> None:
        """Ends the span, unless it has ended.

        The status stays unset when `error` is a cancellation, and when the consumer stopped before it
        `finished` with the item, as a worker that lost the item's lease does. Never raises.
        """
        span = self.span
        if span is None:
            return
        self.span = None
        try:
            if error is not None:
                set_error_status(span, error)
            elif finished:
                span.set_status(Status(StatusCode.OK))
            span.end()
        except Exception:
            log.debug("Could not end the span of a work item", exc_info=True)
