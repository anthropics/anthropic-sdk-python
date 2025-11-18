"""Tests for _reflection utility functions."""

from __future__ import annotations

import pytest

from anthropic._utils._reflection import function_has_argument, assert_signatures_in_sync


class TestFunctionHasArgument:
    """Test the function_has_argument function."""

    def test_function_has_positional_argument(self) -> None:
        """Test detecting positional arguments."""

        def test_func(arg1: str, arg2: int) -> None:
            pass

        assert function_has_argument(test_func, "arg1") is True
        assert function_has_argument(test_func, "arg2") is True

    def test_function_does_not_have_argument(self) -> None:
        """Test that missing arguments return False."""

        def test_func(arg1: str) -> None:
            pass

        assert function_has_argument(test_func, "arg2") is False
        assert function_has_argument(test_func, "nonexistent") is False

    def test_function_has_keyword_only_argument(self) -> None:
        """Test detecting keyword-only arguments."""

        def test_func(*, kwarg1: str, kwarg2: int) -> None:
            pass

        assert function_has_argument(test_func, "kwarg1") is True
        assert function_has_argument(test_func, "kwarg2") is True

    def test_function_has_default_argument(self) -> None:
        """Test detecting arguments with defaults."""

        def test_func(arg1: str, arg2: int = 10) -> None:
            pass

        assert function_has_argument(test_func, "arg1") is True
        assert function_has_argument(test_func, "arg2") is True

    def test_function_has_var_positional(self) -> None:
        """Test with *args."""

        def test_func(*args: int) -> None:
            pass

        assert function_has_argument(test_func, "args") is True

    def test_function_has_var_keyword(self) -> None:
        """Test with **kwargs."""

        def test_func(**kwargs: str) -> None:
            pass

        assert function_has_argument(test_func, "kwargs") is True

    def test_function_with_mixed_parameters(self) -> None:
        """Test function with mixed parameter types."""

        def test_func(pos: str, /, normal: int, *args: int, kw_only: bool, **kwargs: str) -> None:
            pass

        assert function_has_argument(test_func, "pos") is True
        assert function_has_argument(test_func, "normal") is True
        assert function_has_argument(test_func, "args") is True
        assert function_has_argument(test_func, "kw_only") is True
        assert function_has_argument(test_func, "kwargs") is True
        assert function_has_argument(test_func, "nonexistent") is False

    def test_lambda_function(self) -> None:
        """Test with lambda functions."""
        test_lambda = lambda x, y: x + y  # noqa: E731

        assert function_has_argument(test_lambda, "x") is True
        assert function_has_argument(test_lambda, "y") is True
        assert function_has_argument(test_lambda, "z") is False

    def test_callable_class(self) -> None:
        """Test with callable class instances."""

        class CallableClass:
            def __call__(self, param1: str, param2: int) -> None:
                pass

        instance = CallableClass()
        assert function_has_argument(instance, "param1") is True
        assert function_has_argument(instance, "param2") is True


class TestAssertSignaturesInSync:
    """Test the assert_signatures_in_sync function."""

    def test_matching_signatures(self) -> None:
        """Test that matching signatures don't raise."""

        def source_func(a: int, b: str, c: bool = True) -> None:
            pass

        def check_func(a: int, b: str, c: bool = True) -> None:
            pass

        # Should not raise
        assert_signatures_in_sync(source_func, check_func)

    def test_mismatched_signatures_missing_param(self) -> None:
        """Test that missing parameters raise AssertionError."""

        def source_func(a: int, b: str, c: bool) -> None:
            pass

        def check_func(a: int, b: str) -> None:
            pass

        with pytest.raises(AssertionError, match="the `c` param is missing"):
            assert_signatures_in_sync(source_func, check_func)

    def test_mismatched_signatures_wrong_type(self) -> None:
        """Test that type mismatches raise AssertionError."""

        def source_func(a: int, b: str) -> None:
            pass

        def check_func(a: int, b: int) -> None:
            pass

        with pytest.raises(AssertionError, match="types for the `b` param are do not match"):
            assert_signatures_in_sync(source_func, check_func)

    def test_exclude_params(self) -> None:
        """Test excluding specific parameters from the check."""

        def source_func(a: int, b: str, c: bool) -> None:
            pass

        def check_func(a: int, b: str) -> None:
            pass

        # Should not raise when c is excluded
        assert_signatures_in_sync(source_func, check_func, exclude_params={"c"})

    def test_exclude_multiple_params(self) -> None:
        """Test excluding multiple parameters."""

        def source_func(a: int, b: str, c: bool, d: float) -> None:
            pass

        def check_func(a: int, b: str) -> None:
            pass

        # Should not raise when c and d are excluded
        assert_signatures_in_sync(source_func, check_func, exclude_params={"c", "d"})

    def test_matching_complex_signatures(self) -> None:
        """Test with more complex type annotations."""
        from typing import List, Dict, Optional

        def source_func(
            a: List[int],
            b: Dict[str, int],
            c: Optional[str] = None,
        ) -> None:
            pass

        def check_func(
            a: List[int],
            b: Dict[str, int],
            c: Optional[str] = None,
        ) -> None:
            pass

        # Should not raise
        assert_signatures_in_sync(source_func, check_func)

    def test_multiple_errors(self) -> None:
        """Test that multiple errors are all reported."""

        def source_func(a: int, b: str, c: bool) -> None:
            pass

        def check_func(a: str, c: int) -> None:
            pass

        with pytest.raises(AssertionError) as exc_info:
            assert_signatures_in_sync(source_func, check_func)

        error_message = str(exc_info.value)
        # Should mention both type mismatch and missing param
        assert "errors encountered" in error_message

    def test_keyword_only_parameters(self) -> None:
        """Test with keyword-only parameters."""

        def source_func(*, a: int, b: str) -> None:
            pass

        def check_func(*, a: int, b: str) -> None:
            pass

        # Should not raise
        assert_signatures_in_sync(source_func, check_func)

    def test_default_values_dont_matter(self) -> None:
        """Test that different default values don't cause mismatch."""

        def source_func(a: int = 5) -> None:
            pass

        def check_func(a: int = 10) -> None:
            pass

        # Should not raise - only types matter, not default values
        assert_signatures_in_sync(source_func, check_func)

    def test_extra_params_in_check_func(self) -> None:
        """Test that extra parameters in check_func are ignored."""

        def source_func(a: int) -> None:
            pass

        def check_func(a: int, b: str) -> None:
            pass

        # Should not raise - we only check source params exist in check
        assert_signatures_in_sync(source_func, check_func)
