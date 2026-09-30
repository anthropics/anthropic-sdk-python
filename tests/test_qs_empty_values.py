from urllib.parse import unquote

from anthropic._qs import Querystring, stringify


def test_preserves_explicit_empty_string() -> None:
    assert stringify({"blank": ""}) == "blank="


def test_preserves_nested_empty_string() -> None:
    assert unquote(stringify({"filter": {"name": ""}})) == "filter[name]="


def test_repeat_array_preserves_empty_string_but_omits_none() -> None:
    assert unquote(stringify({"item": ["first", "", None, "last"]})) == "item=first&item=&item=last"


def test_bracket_array_preserves_empty_string_but_omits_none() -> None:
    serialise = Querystring(array_format="brackets").stringify
    assert unquote(serialise({"item": ["", None, "last"]})) == "item[]=&item[]=last"


def test_none_remains_omitted() -> None:
    assert stringify({"blank": None}) == ""
