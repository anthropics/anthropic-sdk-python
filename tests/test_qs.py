from typing import Any, cast
from datetime import date, datetime, timezone
from functools import partial
from urllib.parse import unquote

import pytest

from anthropic._qs import Querystring, stringify


def test_empty() -> None:
    assert stringify({}) == ""
    assert stringify({"a": {}}) == ""
    assert stringify({"a": {"b": {"c": {}}}}) == ""


def test_basic() -> None:
    assert stringify({"a": 1}) == "a=1"
    assert stringify({"a": "b"}) == "a=b"
    assert stringify({"a": True}) == "a=true"
    assert stringify({"a": False}) == "a=false"
    assert stringify({"a": 1.23456}) == "a=1.23456"
    assert stringify({"a": None}) == ""


def test_datetime() -> None:
    assert unquote(stringify({"a": datetime(2024, 1, 2, 3, 4, 5)})) == "a=2024-01-02T03:04:05"
    assert (
        unquote(stringify({"a": {"gte": datetime(2024, 1, 2, 3, 4, 5, 600, tzinfo=timezone.utc)}}))
        == "a[gte]=2024-01-02T03:04:05.000600+00:00"
    )
    assert unquote(stringify({"a": date(2024, 1, 2)})) == "a=2024-01-02"


@pytest.mark.parametrize("method", ["class", "function"])
def test_nested_dotted(method: str) -> None:
    if method == "class":
        serialise = Querystring(nested_format="dots").stringify
    else:
        serialise = partial(stringify, nested_format="dots")

    assert unquote(serialise({"a": {"b": "c"}})) == "a.b=c"
    assert unquote(serialise({"a": {"b": "c", "d": "e", "f": "g"}})) == "a.b=c&a.d=e&a.f=g"
    assert unquote(serialise({"a": {"b": {"c": {"d": "e"}}}})) == "a.b.c.d=e"
    assert unquote(serialise({"a": {"b": True}})) == "a.b=true"


def test_nested_brackets() -> None:
    assert unquote(stringify({"a": {"b": "c"}})) == "a[b]=c"
    assert unquote(stringify({"a": {"b": "c", "d": "e", "f": "g"}})) == "a[b]=c&a[d]=e&a[f]=g"
    assert unquote(stringify({"a": {"b": {"c": {"d": "e"}}}})) == "a[b][c][d]=e"
    assert unquote(stringify({"a": {"b": True}})) == "a[b]=true"


@pytest.mark.parametrize("method", ["class", "function"])
def test_array_comma(method: str) -> None:
    if method == "class":
        serialise = Querystring(array_format="comma").stringify
    else:
        serialise = partial(stringify, array_format="comma")

    assert unquote(serialise({"in": ["foo", "bar"]})) == "in=foo,bar"
    assert unquote(serialise({"a": {"b": [True, False]}})) == "a[b]=true,false"
    assert unquote(serialise({"a": {"b": [True, False, None, True]}})) == "a[b]=true,false,true"


def test_array_repeat() -> None:
    assert unquote(stringify({"in": ["foo", "bar"]})) == "in=foo&in=bar"
    assert unquote(stringify({"a": {"b": [True, False]}})) == "a[b]=true&a[b]=false"
    assert unquote(stringify({"a": {"b": [True, False, None, True]}})) == "a[b]=true&a[b]=false&a[b]=true"
    assert unquote(stringify({"in": ["foo", {"b": {"c": ["d", "e"]}}]})) == "in=foo&in[b][c]=d&in[b][c]=e"


@pytest.mark.parametrize("method", ["class", "function"])
def test_array_brackets(method: str) -> None:
    if method == "class":
        serialise = Querystring(array_format="brackets").stringify
    else:
        serialise = partial(stringify, array_format="brackets")

    assert unquote(serialise({"in": ["foo", "bar"]})) == "in[]=foo&in[]=bar"
    assert unquote(serialise({"a": {"b": [True, False]}})) == "a[b][]=true&a[b][]=false"
    assert unquote(serialise({"a": {"b": [True, False, None, True]}})) == "a[b][]=true&a[b][]=false&a[b][]=true"


def test_unknown_array_format() -> None:
    with pytest.raises(NotImplementedError, match="Unknown array_format value: foo, choose from comma, repeat"):
        stringify({"a": ["foo", "bar"]}, array_format=cast(Any, "foo"))
