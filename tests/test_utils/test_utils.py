"""Tests for internal utility helpers in anthropic._utils._utils."""
from __future__ import annotations

import datetime

import pytest

from anthropic._utils._utils import json_safe, deepcopy_minimal


class TestJsonSafe:
    def test_primitive_passthrough(self) -> None:
        assert json_safe(42) == 42
        assert json_safe(3.14) == 3.14
        assert json_safe("hello") == "hello"
        assert json_safe(True) is True
        assert json_safe(None) is None

    def test_mapping(self) -> None:
        result = json_safe({"a": 1, "b": "two"})
        assert result == {"a": 1, "b": "two"}

    def test_list(self) -> None:
        result = json_safe([1, 2, 3])
        assert result == [1, 2, 3]

    def test_tuple(self) -> None:
        # Tuples are iterable and should be converted to lists.
        result = json_safe((1, 2, 3))
        assert result == [1, 2, 3]

    def test_datetime(self) -> None:
        dt = datetime.datetime(2024, 6, 15, 12, 30, 0)
        assert json_safe(dt) == "2024-06-15T12:30:00"

    def test_date(self) -> None:
        d = datetime.date(2024, 6, 15)
        assert json_safe(d) == "2024-06-15"

    def test_set_converted_to_sorted_list(self) -> None:
        result = json_safe({"c", "a", "b"})
        # Sets are unordered; json_safe must return a stable, sorted list.
        assert isinstance(result, list)
        assert sorted(result) == ["a", "b", "c"]  # type: ignore[arg-type]

    def test_frozenset_converted_to_sorted_list(self) -> None:
        result = json_safe(frozenset({"z", "x", "y"}))
        assert isinstance(result, list)
        assert sorted(result) == ["x", "y", "z"]  # type: ignore[arg-type]

    def test_set_is_deterministic(self) -> None:
        """json_safe must produce the same output on every call for the same set."""
        s = {"banana", "apple", "cherry"}
        results = [json_safe(s) for _ in range(20)]
        first = results[0]
        for r in results[1:]:
            assert r == first, "json_safe(set) is not deterministic"

    def test_nested_set_in_dict(self) -> None:
        result = json_safe({"tags": {"b", "a"}})
        assert isinstance(result, dict)
        tags = result["tags"]  # type: ignore[index]
        assert isinstance(tags, list)
        assert sorted(tags) == ["a", "b"]

    def test_nested_datetime_in_list(self) -> None:
        dt = datetime.datetime(2024, 1, 1)
        result = json_safe([dt, "text"])
        assert result == ["2024-01-01T00:00:00", "text"]

    def test_bytes_passthrough(self) -> None:
        # bytes are NOT iterable in this context (explicitly excluded).
        data = b"raw"
        assert json_safe(data) is data


class TestDeepcopyMinimal:
    def test_dict_is_copied(self) -> None:
        original = {"a": 1}
        copy = deepcopy_minimal(original)
        assert copy == original
        assert copy is not original

    def test_nested_dict_deep_copied(self) -> None:
        original = {"outer": {"inner": 42}}
        copy = deepcopy_minimal(original)
        assert copy == original
        assert copy["outer"] is not original["outer"]

    def test_list_is_copied(self) -> None:
        original = [1, 2, 3]
        copy = deepcopy_minimal(original)
        assert copy == original
        assert copy is not original

    def test_tuple_is_not_copied(self) -> None:
        # Tuples are immutable; deepcopy_minimal returns them as-is.
        original = ("a", "b")
        copy = deepcopy_minimal(original)
        assert copy is original

    def test_primitive_passthrough(self) -> None:
        for val in (42, "hello", True, None, 3.14):
            assert deepcopy_minimal(val) is val  # type: ignore[arg-type]
