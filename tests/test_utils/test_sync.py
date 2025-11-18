"""Tests for _sync utility functions."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from anthropic._utils._sync import to_thread, asyncify


class TestToThread:
    """Test the to_thread function."""

    async def test_to_thread_basic(self) -> None:
        """Test running a simple blocking function in a thread."""

        def blocking_func(x: int, y: int) -> int:
            return x + y

        result = await to_thread(blocking_func, 5, 10)
        assert result == 15

    async def test_to_thread_with_kwargs(self) -> None:
        """Test to_thread with keyword arguments."""

        def blocking_func(x: int, y: int, z: int = 0) -> int:
            return x + y + z

        result = await to_thread(blocking_func, 5, 10, z=3)
        assert result == 18

    async def test_to_thread_with_exception(self) -> None:
        """Test that exceptions are propagated correctly."""

        def failing_func() -> None:
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            await to_thread(failing_func)

    async def test_to_thread_return_value(self) -> None:
        """Test that return values are correctly passed back."""

        def return_complex() -> dict[str, Any]:
            return {"result": "success", "value": 42}

        result = await to_thread(return_complex)
        assert result == {"result": "success", "value": 42}

    async def test_to_thread_with_none_return(self) -> None:
        """Test functions that return None."""

        def returns_none() -> None:
            pass

        result = await to_thread(returns_none)
        assert result is None


class TestAsyncify:
    """Test the asyncify decorator."""

    async def test_asyncify_basic(self) -> None:
        """Test basic asyncify functionality."""

        def blocking_func(x: int) -> int:
            return x * 2

        async_func = asyncify(blocking_func)
        result = await async_func(5)
        assert result == 10

    async def test_asyncify_with_multiple_args(self) -> None:
        """Test asyncify with multiple arguments."""

        def blocking_func(a: int, b: int, c: int) -> int:
            return a + b + c

        async_func = asyncify(blocking_func)
        result = await async_func(1, 2, 3)
        assert result == 6

    async def test_asyncify_with_kwargs(self) -> None:
        """Test asyncify with keyword arguments."""

        def blocking_func(x: int, y: int = 10) -> int:
            return x + y

        async_func = asyncify(blocking_func)
        result = await async_func(5, y=20)
        assert result == 25

    async def test_asyncify_exception_propagation(self) -> None:
        """Test that exceptions are propagated in asyncified functions."""

        def failing_func() -> None:
            raise RuntimeError("Asyncify error")

        async_func = asyncify(failing_func)

        with pytest.raises(RuntimeError, match="Asyncify error"):
            await async_func()

    async def test_asyncify_complex_return_type(self) -> None:
        """Test asyncify with complex return types."""

        def blocking_func() -> list[dict[str, int]]:
            return [{"a": 1}, {"b": 2}, {"c": 3}]

        async_func = asyncify(blocking_func)
        result = await async_func()
        assert result == [{"a": 1}, {"b": 2}, {"c": 3}]

    async def test_asyncify_stateful_function(self) -> None:
        """Test asyncify with a function that has state."""
        counter = {"value": 0}

        def increment_counter() -> int:
            counter["value"] += 1
            return counter["value"]

        async_func = asyncify(increment_counter)

        result1 = await async_func()
        result2 = await async_func()
        result3 = await async_func()

        assert result1 == 1
        assert result2 == 2
        assert result3 == 3

    async def test_asyncify_parallel_execution(self) -> None:
        """Test that asyncified functions can run in parallel."""
        import time

        def slow_function(n: int) -> int:
            time.sleep(0.1)
            return n * 2

        async_func = asyncify(slow_function)

        # Run multiple tasks in parallel
        start_time = time.time()
        results = await asyncio.gather(
            async_func(1),
            async_func(2),
            async_func(3),
        )
        elapsed = time.time() - start_time

        assert results == [2, 4, 6]
        # Should take ~0.1s if parallel, ~0.3s if sequential
        # Allow some margin for CI
        assert elapsed < 0.25

    async def test_asyncify_callable_object(self) -> None:
        """Test asyncify with a callable object."""

        class Multiplier:
            def __init__(self, factor: int):
                self.factor = factor

            def __call__(self, x: int) -> int:
                return x * self.factor

        multiplier = Multiplier(3)
        async_multiplier = asyncify(multiplier)

        result = await async_multiplier(7)
        assert result == 21
