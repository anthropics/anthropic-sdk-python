"""Turns request params into plain data that can be serialized, logged and sent again on a retry.

This takes two phases. `copy_tree` walks the params once, in document order, copying every
container on the way: mappings into dicts without their `NotGiven` / `Omit` entries, sequences,
sets and iterators into lists, pydantic models into their dumped form and dates into their ISO
8601 string. In a request body it also collects the slots holding a file that is to be sent
base64-encoded, but leaves reading them to the second phase -- the only step in which
`prepare_request_data` and `async_prepare_request_data` differ. Query params never involve any
IO: a path among them stays in place and is later rendered as its string.
"""

from __future__ import annotations

import os
import base64
import pathlib
from typing import IO, Any
from datetime import date
from collections.abc import Callable
from typing_extensions import Literal

import anyio
import pydantic

from ._json import is_sent_as_list, openapi_dumps_str, openapi_model_dump
from ._utils import is_mapping
from .._files import is_base64_file_input
from .._types import Omit, NotGiven, Base64FileInput
from .._constants import FILE_INPUT_MARKERS

PLAIN_TYPES = (str, int, float, bool, type(None))

# the walk does not recurse, so only this stops a sequence or iterator that keeps yielding fresh ones
# of its kind, which no cycle check catches; far deeper than anything that can be serialized
MAX_DEPTH = 100_000

# `(container, key)`: where a value lives, so that it can be replaced in place. A plain tuple
# rather than a NamedTuple, as one is created for every value visited
Slot = tuple[Any, Any]
VisitLater = Callable[[Slot], None]

# `(EXIT_CONTAINER, id(container))` is a stack entry marking the end of a container's slots: popped
# once every slot inside the container with that id has been prepared
EXIT_CONTAINER: Any = object()


def prepare_request_data(data: object, *, location: Literal["body", "query"], keep_top_level_omit: bool = False) -> Any:
    """Copy request params into plain data that can be serialized and re-sent.

    Drops `NotGiven` / `Omit` entries (`keep_top_level_omit` keeps `Omit` directly under the
    root, for `_merge_mappings`), turns sequences, sets and iterators into lists, dumps pydantic
    models and formats dates as ISO 8601 strings. In a `"body"`, a path / file object found under
    `field` of a mapping matching one of `FILE_INPUT_MARKERS` is read and base64-encoded --
    nowhere else, and never in a `"query"`.
    Never mutates the caller's containers; a container that contains itself raises `ValueError`.
    """
    root, file_slots = copy_tree(data, location=location, keep_top_level_omit=keep_top_level_omit)
    for container, key in file_slots:
        container[key] = read_base64(container[key])

    return root[0]


async def async_prepare_request_data(
    data: object, *, location: Literal["body", "query"], keep_top_level_omit: bool = False
) -> Any:
    """`prepare_request_data`, reading `pathlib.Path` inputs without blocking the event loop."""
    root, file_slots = copy_tree(data, location=location, keep_top_level_omit=keep_top_level_omit)
    for container, key in file_slots:
        container[key] = await async_read_base64(container[key])

    return root[0]


def serialize_data(data: object, *, location: Literal["body", "query"]) -> str:
    """The JSON text that `data` is sent as once prepared."""
    return openapi_dumps_str(prepare_request_data(data, location=location))


async def async_serialize_data(data: object, *, location: Literal["body", "query"]) -> str:
    """`serialize_data`, reading `pathlib.Path` inputs without blocking the event loop."""
    return openapi_dumps_str(await async_prepare_request_data(data, location=location))


def copy_tree(
    data: object, *, location: Literal["body", "query"], keep_top_level_omit: bool
) -> tuple[list[Any], list[Slot]]:
    """Returns `[copied data]` and the slots whose file input is still to be read (in a body only)."""
    # wrapping the data gives the top-level value a slot like any other
    root: list[Any] = [data]
    file_slots: list[Slot] = []
    markers = FILE_INPUT_MARKERS if location == "body" else ()

    # the source containers around the slot being visited, by id: meeting one of them again is
    # a cycle. Holding each container as the value keeps its id from being reused meanwhile
    ancestors: dict[int, object] = {}

    # an explicit stack instead of recursion, as bodies may nest deeper than the recursion limit
    pending: list[Slot] = [(root, 0)]
    visit_later = pending.append

    while pending:
        container, key = pending.pop()
        if container is EXIT_CONTAINER:
            del ancestors[key]
            continue

        value: object = container[key]
        kind = type(value)
        inner_start = len(pending)

        # plain dicts and lists, by far the most common, are told apart by exact type alone,
        # sparing them the slow abstract `Mapping` / `Iterable` instance checks
        if kind is dict or (kind is not list and is_mapping(value)):
            copied = copy_mapping(value, visit_later, keep_omit=keep_top_level_omit and container is root)
            for discriminator, tag, field in markers:
                if copied.get(discriminator) == tag and is_base64_file_input(copied.get(field)):
                    file_slots.append((copied, field))

            container[key] = copied
        elif kind is list or is_sent_as_list(value):
            container[key] = copy_items(value, visit_later)
        elif isinstance(value, pydantic.BaseModel):
            container[key] = openapi_model_dump(value)
        elif isinstance(value, date):
            container[key] = value.isoformat()
        else:
            # left for the encoder: a scalar subclass, a file input still to be read, or a value it rejects
            continue

        if len(pending) > inner_start:
            # slots inside `value` are still to be visited, so it stays an ancestor until they are all done
            ident = id(value)
            if ident in ancestors:
                raise ValueError("Circular reference detected")

            if len(ancestors) >= MAX_DEPTH:
                raise ValueError("Exceeds the maximum nesting depth")

            ancestors[ident] = value
            # the stack pops the last slot first, so the new ones are reversed: values are visited,
            # iterators drained and file slots collected in document order
            inner = pending[inner_start:]
            inner.append((EXIT_CONTAINER, ident))
            inner.reverse()
            pending[inner_start:] = inner

    return root, file_slots


def copy_mapping(mapping: Any, visit_later: VisitLater, *, keep_omit: bool) -> dict[Any, object]:
    """Copies the `Mapping` into a dict without its `NotGiven` / `Omit` entries.

    Schedules a visit to the slots of the copy whose value may need preparing itself.
    """
    copied: dict[Any, object] = {}
    for key, value in mapping.items():
        if type(value) in PLAIN_TYPES:
            copied[key] = value
        elif not isinstance(value, (NotGiven, Omit)):
            copied[key] = value
            visit_later((copied, key))
        elif keep_omit and isinstance(value, Omit):
            # an `Omit` directly under the root tells `_merge_mappings` to drop this key from the
            # mapping it merges the copy into, so it has to survive until then
            copied[key] = value

    return copied


def copy_items(items: Any, visit_later: VisitLater) -> list[object]:
    """Copies the items into a list, scheduling a visit to the slots whose item may need preparing itself."""
    copied = list(items)
    for i, item in enumerate(copied):
        if type(item) not in PLAIN_TYPES:
            visit_later((copied, i))

    return copied


def read_base64(file: Base64FileInput) -> str:
    if isinstance(file, pathlib.Path):
        return b64encode(file, file.read_bytes())

    return b64encode(file, readable(file).read())


async def async_read_base64(file: Base64FileInput) -> str:
    if isinstance(file, pathlib.Path):
        return b64encode(file, await anyio.Path(file).read_bytes())

    return b64encode(file, readable(file).read())


def readable(file: Base64FileInput) -> IO[bytes]:
    """The file object to read; any other `os.PathLike` is rejected without touching the filesystem."""
    if isinstance(file, os.PathLike):
        raise TypeError(f"Cannot read {type(file)}; only pathlib.Path and file objects are read")

    return file


def b64encode(file: Base64FileInput, content: object) -> str:
    if isinstance(content, str):
        content = content.encode()

    if not isinstance(content, bytes):
        raise RuntimeError(f"Could not read bytes from {file}; Received {type(content)}")

    return base64.b64encode(content).decode("ascii")
