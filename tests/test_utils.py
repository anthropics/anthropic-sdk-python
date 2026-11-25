from __future__ import annotations

import sys

import pytest

from anthropic._utils import removesuffix


def test_removesuffix_empty_suffix() -> None:
    assert removesuffix("abc", "") == "abc"


def test_removesuffix_matching_suffix() -> None:
    assert removesuffix("abc", "bc") == "a"


@pytest.mark.skipif(sys.version_info < (3, 9), reason="str.removesuffix was added in Python 3.9")
@pytest.mark.parametrize(
    ("string", "suffix"),
    [
        ("abc", ""),
        ("abc", "c"),
        ("abc", "bc"),
        ("abc", "abc"),
        ("abc", "abcd"),
        ("", ""),
        ("", "a"),
        ("abc", "a"),
    ],
)
def test_removesuffix_matches_builtin(string: str, suffix: str) -> None:
    assert removesuffix(string, suffix) == string.removesuffix(suffix)
