from __future__ import annotations

import copy
import pickle
import multiprocessing
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor

import httpx2
import pytest

from anthropic import (
    APIError,
    Anthropic,
    AnthropicError,
    APIStatusError,
    APITimeoutError,
    APIConnectionError,
    APIResponseValidationError,
)
from anthropic._response import StreamAlreadyConsumed
from anthropic._error_classes import ERROR_CLASSES


def make_request() -> httpx2.Request:
    return httpx2.Request("POST", "https://example.com/foo")


def make_response() -> httpx2.Response:
    return httpx2.Response(400, request=make_request())


def pickle_round_trip(error: AnthropicError) -> AnthropicError:
    return pickle.loads(pickle.dumps(error))


parametrize_duplicate = pytest.mark.parametrize(
    "duplicate",
    [pickle_round_trip, copy.copy, copy.deepcopy],
    ids=["pickle", "copy", "deepcopy"],
)


@parametrize_duplicate
@pytest.mark.parametrize(
    "error",
    [
        AnthropicError("message"),
        StreamAlreadyConsumed(),
        APIError("message", make_request(), body=None),
        APIResponseValidationError(make_response(), None),
        APIConnectionError(request=make_request()),
        APITimeoutError(make_request()),
        APIStatusError("message", response=make_response(), body=None),
    ],
    ids=lambda error: type(error).__name__,
)
def test_duplicate_has_the_class_and_message_of_the_error(
    duplicate: Callable[[AnthropicError], AnthropicError], error: AnthropicError
) -> None:
    duplicated = duplicate(error)

    assert type(duplicated) is type(error)
    assert str(duplicated) == str(error)


@parametrize_duplicate
def test_duplicate_of_a_raised_status_error_keeps_its_attributes(
    client: Anthropic, duplicate: Callable[[APIStatusError], APIStatusError]
) -> None:
    def handler(_: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(400, headers={"x-foo": "bar"}, json={"error": "oops"})

    http_client = httpx2.Client(transport=httpx2.MockTransport(handler))
    failing_client = client.with_options(http_client=http_client, max_retries=0)
    with pytest.raises(APIStatusError) as exc_info:
        failing_client.post("/foo", cast_to=httpx2.Response, body={"foo": "bar"})
    error = exc_info.value

    duplicated = duplicate(error)

    assert duplicated.message == error.message
    assert duplicated.body == {"error": "oops"}
    assert duplicated.status_code == 400
    assert duplicated.response.headers["x-foo"] == "bar"
    assert duplicated.response.json() == {"error": "oops"}
    assert duplicated.request.url == error.request.url
    assert duplicated.request.content == error.request.content


@pytest.mark.parametrize("error_class", ERROR_CLASSES.values(), ids=lambda error_class: error_class.__name__)
def test_pickled_status_error_loads_as_its_own_class(error_class: type[APIStatusError]) -> None:
    error = error_class("message", response=make_response(), body=None)

    loaded = pickle_round_trip(error)

    assert type(loaded) is error_class


def raise_status_error() -> None:
    raise APIStatusError("message", response=make_response(), body=None)


def test_error_raised_in_a_process_pool_reaches_the_caller() -> None:
    # forking a process that has threads, as a `pytest-xdist` worker does, warns on Python 3.12+
    with ProcessPoolExecutor(max_workers=1, mp_context=multiprocessing.get_context("spawn")) as pool:
        future = pool.submit(raise_status_error)

        with pytest.raises(APIStatusError, match="message"):
            future.result()
