from __future__ import annotations

import json
from typing import Any
from datetime import date, datetime
from collections import UserString
from collections.abc import Set, Iterator, Sequence, MappingView
from typing_extensions import override

import pydantic

from ._utils import is_mapping
from .._files import is_base64_file_input
from .._compat import model_dump

# told apart by exact type alone, sparing the most common lists the slow abstract instance checks
LIST_TYPES = frozenset((list, tuple, set, frozenset))


def openapi_dumps(obj: Any) -> bytes:
    """
    Serialize an object to UTF-8 encoded JSON bytes.

    Extends the standard json.dumps with support for additional types
    commonly used in the SDK, such as `datetime`, `pydantic.BaseModel`, etc.
    """
    return encoder.encode(obj).encode()


def openapi_dumps_str(obj: Any) -> str:
    """`openapi_dumps`, as a `str`; for transports that send text frames."""
    return encoder.encode(obj)


def is_sent_as_list(value: object) -> bool:
    """Whether a value that is not a mapping is sent as a JSON array, or as `key[]=` entries in a query.

    Sequences, sets, dict views and iterators (generators, `map`, `iter(...)`) are. An object that
    merely defines `__iter__` is not iterated: it is left to the encoder in a body, and sent as
    its `str()` in a query.
    """
    kind = type(value)
    if kind in LIST_TYPES:
        return True

    # sequences of characters or bytes, and file objects -- iterators over their lines
    if isinstance(value, (str, bytes, bytearray, memoryview, UserString)) or is_base64_file_input(value):
        return False

    return isinstance(value, (Sequence, Set, MappingView, Iterator))


def openapi_model_dump(model: pydantic.BaseModel) -> dict[str, Any]:
    """Dump a model as it is sent in a request body, without the fields named in `__api_exclude__`."""
    return model_dump(
        model, exclude_unset=True, mode="json", by_alias=True, exclude=getattr(model, "__api_exclude__", None)
    )


class _CustomEncoder(json.JSONEncoder):
    @override
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date)):
            return o.isoformat()

        if isinstance(o, pydantic.BaseModel):
            return openapi_model_dump(o)

        if is_mapping(o):
            return dict(o)

        if is_sent_as_list(o):
            return list(o)

        return super().default(o)


encoder = _CustomEncoder(ensure_ascii=False, separators=(",", ":"), allow_nan=False)
