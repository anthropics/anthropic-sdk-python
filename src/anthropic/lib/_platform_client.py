from __future__ import annotations

from typing import Any, TypeVar, cast
from collections.abc import Mapping, Callable, Sequence

import httpx2

from .._types import Timeout, NotGiven, OpenTelemetryClientOption
from .._utils import is_given
from .._middleware import MiddlewareInput
from .._base_client import BaseClient, merge_headers

_ClientT = TypeVar("_ClientT", bound=BaseClient[Any, Any])


def copy_platform_client(
    client: _ClientT,
    /,
    *,
    timeout: float | Timeout | None | NotGiven,
    http_client: httpx2.Client | httpx2.AsyncClient | None,
    max_retries: int | NotGiven,
    open_telemetry: OpenTelemetryClientOption,
    default_headers: Mapping[str, str] | None,
    set_default_headers: Mapping[str, str] | None,
    default_query: Mapping[str, object] | None,
    set_default_query: Mapping[str, object] | None,
    middleware: Sequence[MiddlewareInput] | None | NotGiven,
    **platform_options: object,
) -> _ClientT:
    """Builds the client that a platform client's `copy()` returns.

    `platform_options` holds the other arguments of the constructor of `client`, with the values the copy gets.
    """
    if default_headers is not None and set_default_headers is not None:
        raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

    if default_query is not None and set_default_query is not None:
        raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

    headers = client._custom_headers
    if default_headers is not None:
        headers = merge_headers(headers, default_headers)
    elif set_default_headers is not None:
        headers = set_default_headers

    params = client._custom_query
    if default_query is not None:
        params = {**params, **default_query}
    elif set_default_query is not None:
        params = set_default_query

    copied = cast("Callable[..., _ClientT]", client.__class__)(
        timeout=client.timeout if isinstance(timeout, NotGiven) else timeout,
        http_client=http_client or client._client,
        max_retries=max_retries if is_given(max_retries) else client.max_retries,
        open_telemetry=client._copy_open_telemetry(open_telemetry),
        default_headers=headers,
        default_query=params,
        middleware=client._middleware if isinstance(middleware, NotGiven) else middleware,
        **platform_options,
    )
    copied._timeout_overridden = client._timeout_overridden or is_given(timeout)
    return copied
