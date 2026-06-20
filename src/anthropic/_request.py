from __future__ import annotations

import copy as _copy
from typing import Any
from typing_extensions import override

import httpx

from ._types import Body, Query, Headers, NotGiven, not_given
from ._utils import is_given
from ._compat import model_copy
from ._models import FinalRequestOptions


class APIRequest:
    """A view over the request that the client is about to execute.

    Treat instances as immutable; use `copy()` to derive a modified request.
    """

    def __init__(
        self,
        *,
        options: FinalRequestOptions,
        cast_to: Any,
        stream: bool = False,
        stream_cls: type[Any] | None = None,
        retries_taken: int = 0,
    ) -> None:
        self.options = options
        self.cast_to = cast_to
        self.stream = stream
        self.stream_cls = stream_cls
        self.retries_taken = retries_taken
        """The number of retries the SDK has already taken for this call.

        `0` on the first attempt; the middleware chain is invoked once per HTTP attempt.
        """

    @property
    def method(self) -> str:
        return self.options.method

    @property
    def url(self) -> str:
        return self.options.url

    @property
    def headers(self) -> Headers:
        headers = self.options.headers
        return headers if is_given(headers) else {}

    @property
    def query_params(self) -> Query:
        return self.options.params

    @property
    def json(self) -> Body | None:
        return self.options.json_data

    @property
    def timeout(self) -> float | httpx.Timeout | None | NotGiven:
        return self.options.timeout

    @property
    def max_retries(self) -> int | NotGiven:
        return self.options.max_retries

    def copy(
        self,
        *,
        method: str | NotGiven = not_given,
        url: str | NotGiven = not_given,
        headers: Headers | NotGiven = not_given,
        params: Query | NotGiven = not_given,
        body: Body | NotGiven = not_given,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIRequest:
        # Note: we intentionally avoid `model_copy(deep=True)` here as fields like
        # `files` and `content` can hold open file/IO objects which cannot be deep-copied.
        #
        # Instead we shallow-copy the options and then deep-copy only the JSON-safe mutable
        # fields so that mutating the returned request never affects the original request.
        options = model_copy(self.options)
        options.json_data = _copy.deepcopy(options.json_data)
        options.extra_json = _copy.deepcopy(options.extra_json)
        options.params = _copy.deepcopy(options.params)
        if is_given(options.headers):
            options.headers = dict(options.headers)

        if is_given(method):
            options.method = method
        if is_given(url):
            options.url = url
        if is_given(headers):
            options.headers = headers
        if is_given(params):
            options.params = params
        if not isinstance(body, NotGiven):
            options.json_data = body
        if not isinstance(timeout, NotGiven):
            options.timeout = timeout

        return APIRequest(
            options=options,
            cast_to=self.cast_to,
            stream=self.stream,
            stream_cls=self.stream_cls,
            retries_taken=self.retries_taken,
        )

    @override
    def __repr__(self) -> str:
        return f"<APIRequest method={self.method!r} url={self.url!r} stream={self.stream!r}>"
