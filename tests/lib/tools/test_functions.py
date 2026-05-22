from __future__ import annotations

from typing import Any, cast
from contextlib import contextmanager, asynccontextmanager
from collections.abc import Callable, Iterator, Awaitable, AsyncIterator

import pytest
from pydantic import BaseModel

from anthropic import beta_tool
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools._beta_functions import (
    BaseFunctionTool,
    BetaFunctionTool,
    BetaAsyncFunctionTool,
    BetaCustomFunctionTool,
    BetaAsyncCustomFunctionTool,
    beta_async_tool,
)
from anthropic.types.beta.beta_tool_param import InputSchema


@pytest.mark.skipif(PYDANTIC_V1, reason="only applicable in pydantic v2")
class TestFunctionTool:
    def test_basic_function_schema_conversion(self) -> None:
        """Test basic function schema conversion with simple types."""

        def get_weather(location: str, unit: str = "celsius") -> str:
            """Get the weather for a specific location."""
            return f"Weather in {location} is 20 degrees {unit}"

        function_tool = beta_tool(get_weather)

        assert function_tool.name == "get_weather"
        assert function_tool.description == "Get the weather for a specific location."
        assert function_tool.input_schema == {
            "additionalProperties": False,
            "type": "object",
            "properties": {
                "location": {"title": "Location", "type": "string"},
                "unit": {"title": "Unit", "type": "string", "default": "celsius"},
            },
            "required": ["location"],
        }
        assert function_tool(location="CA") == "Weather in CA is 20 degrees celsius"

        # invalid types should be allowed because __call__ should just be the original function
        assert function_tool(location=cast(Any, 1)) == "Weather in 1 is 20 degrees celsius"

    def test_function_with_multiple_types(self) -> None:
        """Test function schema conversion with various Python types."""

        def simple_function(
            name: str,
            age: int,
        ) -> str:
            """A simple function with basic parameter types."""
            return f"Person: {name}, {age} years old"

        function_tool = beta_tool(simple_function)

        # Test that we can create the tool and call it
        assert function_tool.name == "simple_function"
        assert function_tool.description == "A simple function with basic parameter types."

        # Test calling the function
        result = function_tool.call(
            {
                "name": "John",
                "age": 25,
            }
        )
        assert result == "Person: John, 25 years old"

        # Test schema structure
        expected_schema = {
            "additionalProperties": False,
            "type": "object",
            "properties": {
                "name": {"title": "Name", "type": "string"},
                "age": {"title": "Age", "type": "integer"},
            },
            "required": ["name", "age"],
        }

        assert function_tool.input_schema == expected_schema

    def test_function_call_with_valid_input(self) -> None:
        def add_numbers(a: int, b: int) -> str:
            """Add two numbers together."""
            return str(a + b)

        function_tool = beta_tool(add_numbers)
        result = function_tool.call({"a": 5, "b": 3})

        assert result == "8"

    @pytest.mark.parametrize(
        "input_data, expected_error_type, expected_error_msg",
        [
            pytest.param(
                {"a": "not a number", "b": 3},
                ValueError,
                "Invalid arguments for function add_numbers",
                id="invalid_argument_type",
            ),
            pytest.param(
                {"b": 3},
                ValueError,
                "Invalid arguments for function add_numbers",
                id="missing_required_argument",
            ),
            pytest.param(
                None,
                TypeError,
                "Input must be a dictionary, got NoneType",
                id="invalid_input_object",
            ),
        ],
    )
    def test_function_call_with_invalid_input(
        self, input_data: dict[str, Any], expected_error_type: type[BaseException], expected_error_msg: str
    ) -> None:
        def add_numbers(a: int, b: int) -> str:
            return str(a + b)

        function_tool = beta_tool(add_numbers)

        with pytest.raises(expected_error_type, match=expected_error_msg):
            function_tool.call(input_data)

    def test_custom_name_and_description(self) -> None:
        def some_function(x: int) -> str:
            """Original description."""
            return str(x * 2)

        function_tool = beta_tool(some_function, name="custom_name", description="Custom description")

        assert function_tool.name == "custom_name"
        assert function_tool.description == "Custom description"

    def test_custom_input_schema_with_dict(self) -> None:
        def some_function(x: int) -> str:
            return str(x * 2)

        custom_schema: InputSchema = {
            "additionalProperties": False,
            "type": "object",
            "properties": {"x": {"type": "number", "description": "A number to double"}},
            "required": ["x"],
        }

        function_tool = beta_tool(some_function, input_schema=custom_schema)

        assert function_tool.input_schema == custom_schema

    def test_custom_input_schema_with_pydantic_model(self) -> None:
        class WeatherInput(BaseModel):
            location: str
            unit: str = "celsius"

        def get_weather(location: str, unit: str = "celsius") -> str:  # noqa: ARG001
            return f"Weather in {location}"

        # Pass the Pydantic model class directly as input_schema
        function_tool = beta_tool(get_weather, input_schema=WeatherInput)

        # Pydantic model schemas include additional metadata
        schema = function_tool.input_schema

        assert schema == {
            "title": "WeatherInput",
            "type": "object",
            "properties": {
                "location": {"title": "Location", "type": "string"},
                "unit": {"title": "Unit", "type": "string", "default": "celsius"},
            },
            "required": ["location"],
        }

    def test_to_dict_method(self) -> None:
        def simple_func(message: str) -> str:
            """A simple function."""
            return message

        function_tool = beta_tool(simple_func)
        tool_param = function_tool.to_dict()

        assert tool_param == {
            "name": "simple_func",
            "description": "A simple function.",
            "input_schema": {
                "additionalProperties": False,
                "type": "object",
                "properties": {"message": {"title": "Message", "type": "string"}},
                "required": ["message"],
            },
        }

    def test_custom_tool_to_dict(self) -> None:
        """``custom=True`` serializes as a managed-agents custom tool."""

        @beta_tool(custom=True)
        def get_weather(location: str) -> str:
            """Get the weather for a location."""
            return location

        assert isinstance(get_weather, BetaCustomFunctionTool)
        # still a BetaFunctionTool — same call / schema behavior
        assert isinstance(get_weather, BetaFunctionTool)
        assert get_weather.call({"location": "SF"}) == "SF"

        tool_param = get_weather.to_dict()
        assert tool_param == {
            "type": "custom",
            "name": "get_weather",
            "description": "Get the weather for a location.",
            "input_schema": {
                "type": "object",
                "properties": {"location": {"title": "Location", "type": "string"}},
                "required": ["location"],
            },
        }
        # the Agents API rejects `additionalProperties`; the custom variant drops it
        assert "additionalProperties" not in tool_param["input_schema"]

    def test_non_custom_tool_to_dict_unchanged(self) -> None:
        """The default (``custom=False``) still emits a plain BetaToolParam."""

        @beta_tool
        def get_weather(location: str) -> str:
            """Get the weather for a location."""
            return location

        assert isinstance(get_weather, BetaFunctionTool)
        assert not isinstance(get_weather, BetaCustomFunctionTool)
        assert "type" not in get_weather.to_dict()

    async def test_async_custom_tool_to_dict(self) -> None:
        """``custom=True`` works for the async decorator too."""

        @beta_async_tool(custom=True)
        async def get_weather(location: str) -> str:
            """Get the weather for a location."""
            return location

        assert isinstance(get_weather, BetaAsyncCustomFunctionTool)
        assert isinstance(get_weather, BetaAsyncFunctionTool)
        assert await get_weather.call({"location": "SF"}) == "SF"

        tool_param = get_weather.to_dict()
        assert tool_param == {
            "type": "custom",
            "name": "get_weather",
            "description": "Get the weather for a location.",
            "input_schema": {
                "type": "object",
                "properties": {"location": {"title": "Location", "type": "string"}},
                "required": ["location"],
            },
        }
        assert "additionalProperties" not in tool_param["input_schema"]

    def test_function_without_docstring(self) -> None:
        def no_docs(x: int) -> str:  # noqa: ARG001
            return ""

        function_tool = beta_tool(no_docs)

        assert function_tool.description == ""

    def test_function_without_type_hints(self) -> None:
        def no_types(x, y=10):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
            return x + y  # pyright: ignore[reportUnknownVariableType]

        function_tool = beta_tool(no_types)  # type: ignore

        # Should still create a schema, though less precise (uses Any type)
        assert function_tool.input_schema == {
            "additionalProperties": False,
            "type": "object",
            "properties": {
                "x": {"title": "X"},  # Any type gets title but no type
                "y": {"title": "Y", "default": 10},
            },
            "required": ["x"],
        }

    @pytest.mark.parametrize(
        "docstring",
        [
            pytest.param(
                (
                    """Get detailed weather information for a location.

                        This function retrieves current weather conditions and optionally
                        includes a forecast for the specified location.

                        Args:
                            location: The city or location to get weather for.
                            unit: Temperature unit, either 'celsius' or 'fahrenheit'.
                            include_forecast: Whether to include forecast data.

                        Returns:
                            Weather information as a formatted string

                        Examples:
                            >>> get_weather_detailed("London")
                            "London: 15°C, partly cloudy"

                            >>> get_weather_detailed("New York", "fahrenheit", True)
                            "New York: 59°F, sunny. Tomorrow: 62°F, cloudy"
                        """
                ),
                id="google_style_docstring",
            ),
            pytest.param(
                (
                    """Get detailed weather information for a location.

                        This function retrieves current weather conditions and optionally
                        includes a forecast for the specified location.

                        :param location: The city or location to get weather for.
                        :type location: str
                        :param unit: Temperature unit, either 'celsius' or 'fahrenheit'.
                        :type unit: str
                        :param include_forecast: Whether to include forecast data.
                        :type include_forecast: bool

                        :returns: Weather information as a formatted string.
                        :rtype: str

                        :example:
                            >>> get_weather_detailed("London")
                            "London: 15°C, partly cloudy"

                            >>> get_weather_detailed("New York", "fahrenheit", True)
                            "New York: 59°F, sunny. Tomorrow: 62°F, cloudy
                        """
                ),
                id="rest_style_docstring",
            ),
            pytest.param(
                (
                    """Get detailed weather information for a location.

                        This function retrieves current weather conditions and optionally
                        includes a forecast for the specified location.

                        Parameters
                        ----------
                        location : str
                            The city or location to get weather for.
                        unit : str
                            Temperature unit, either 'celsius' or 'fahrenheit'.
                        include_forecast : bool
                            Whether to include forecast data.

                        Returns
                        -------
                        str
                            Weather information as a formatted string.

                        Examples
                        --------
                        >>> get_weather_detailed("London")
                        "London: 15°C, partly cloudy"

                        >>> get_weather_detailed("New York", "fahrenheit", True)
                        "New York: 59°F, sunny. Tomorrow: 62°F, cloudy"
                        """
                ),
                id="numpy_style_docstring",
            ),
            pytest.param(
                (
                    """Get detailed weather information for a location.

                        This function retrieves current weather conditions and optionally
                        includes a forecast for the specified location.

                        @param location: The city or location to get weather for.
                        @type location: str
                        @param unit: Temperature unit, either 'celsius' or 'fahrenheit'.
                        @type unit: str
                        @param include_forecast: Whether to include forecast data.
                        @type include_forecast: bool

                        @return: Weather information as a formatted string.
                        @rtype: str

                        @example:
                            >>> get_weather_detailed("London")
                            "London: 15°C, partly cloudy"

                            >>> get_weather_detailed("New York", "fahrenheit", True)
                            "New York: 59°F, sunny. Tomorrow: 62°F, cloudy"
                        """
                ),
                id="epydoc_style_docstring",
            ),
        ],
    )
    def test_docstring_parsing_with_parameters(self, docstring: str) -> None:
        def get_weather_detailed(location: str, unit: str = "celsius", include_forecast: bool = False) -> str:  # noqa: ARG001
            return f"Weather for {location}"

        get_weather_detailed.__doc__ = docstring

        function_tool = beta_tool(get_weather_detailed)

        expected_description = (
            "Get detailed weather information for a location.\n\n"
            "This function retrieves current weather conditions and optionally\n"
            "includes a forecast for the specified location."
        )
        expected_schema = {
            "additionalProperties": False,
            "type": "object",
            "properties": {
                "location": {
                    "title": "Location",
                    "type": "string",
                    "description": "The city or location to get weather for.",
                },
                "unit": {
                    "title": "Unit",
                    "type": "string",
                    "default": "celsius",
                    "description": "Temperature unit, either 'celsius' or 'fahrenheit'.",
                },
                "include_forecast": {
                    "title": "Include Forecast",
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to include forecast data.",
                },
            },
            "required": ["location"],
        }
        assert function_tool.description == expected_description
        assert function_tool.input_schema == expected_schema

    def test_decorator_without_parentheses(self) -> None:
        """Test using @function_tool decorator without parentheses."""

        @beta_tool
        def multiply(x: int, y: int) -> str:
            """Multiply two numbers."""
            return str(x * y)

        assert multiply.name == "multiply"
        assert multiply.description == "Multiply two numbers."
        assert multiply.call({"x": 3, "y": 4}) == "12"

        expected_schema = {
            "additionalProperties": False,
            "type": "object",
            "properties": {
                "x": {"title": "X", "type": "integer"},
                "y": {"title": "Y", "type": "integer"},
            },
            "required": ["x", "y"],
        }
        assert multiply.input_schema == expected_schema

    def test_decorator_with_parentheses(self) -> None:
        """Test using @function_tool() decorator with parentheses."""

        @beta_tool()
        def divide(a: float, b: float) -> str:
            """Divide two numbers."""
            return str(a / b)

        assert divide.name == "divide"
        assert divide.description == "Divide two numbers."
        assert divide.call({"a": 10.0, "b": 2.0}) == "5.0"

    def test_decorator_with_custom_parameters(self) -> None:
        """Test using @function_tool() decorator with custom name and description."""

        @beta_tool(name="custom_calculator", description="A custom calculator function")
        def calculate(value: int) -> str:
            """Original description that should be overridden."""
            return str(value * 2)

        assert calculate.name == "custom_calculator"
        assert calculate.description == "A custom calculator function"
        assert calculate.call({"value": 5}) == "10"

    def test_docstring_parsing_simple(self) -> None:
        """Test that simple docstrings still work correctly."""

        def simple_add(a: int, b: int) -> str:
            """Add two numbers together."""
            return str(a + b)

        function_tool = beta_tool(simple_add)

        assert function_tool.description == "Add two numbers together."
        assert _get_parameters_info(function_tool) == {}

        # Schema should not have descriptions for parameters
        expected_schema = {
            "additionalProperties": False,
            "type": "object",
            "properties": {"a": {"title": "A", "type": "integer"}, "b": {"title": "B", "type": "integer"}},
            "required": ["a", "b"],
        }

        assert function_tool.input_schema == expected_schema


def _get_parameters_info(fn: BaseFunctionTool[Any]) -> dict[str, str]:
    param_info: dict[str, str] = {}
    for param in fn._parsed_docstring.params:
        if param.description:
            param_info[param.arg_name] = param.description.strip()
    return param_info


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions need pydantic v2")
class TestContextManagerTool:
    """``@beta_tool`` / ``@beta_async_tool`` over an (async) context manager that
    yields the tool callable: the decorator enters it to obtain the callable and
    drives its ``__exit__`` / ``__aexit__`` on the cleanup path.

    The ``cast(Any, ...)`` call form mirrors how the SDK's own ``beta_bash_tool``
    adopts this; bare decorator syntax works the same at runtime.
    """

    def test_sync_context_manager_tool(self) -> None:
        import anyio

        from anthropic.lib.tools._beta_functions import aclose_runnable_tool

        seen: list[str] = []

        @contextmanager
        def adder_cm() -> Iterator[Callable[[int, int], str]]:
            seen.append("enter")

            def add(a: int, b: int) -> str:
                """Add two numbers."""
                return str(a + b)

            try:
                yield add
            finally:
                seen.append("exit")

        adder = beta_tool(cast(Any, adder_cm))

        # Entered eagerly; schema/description inferred from the yielded callable.
        assert seen == ["enter"]
        assert adder.name == "add"
        assert adder.description == "Add two numbers."
        assert adder.input_schema == {
            "additionalProperties": False,
            "type": "object",
            "properties": {"a": {"title": "A", "type": "integer"}, "b": {"title": "B", "type": "integer"}},
            "required": ["a", "b"],
        }
        assert adder.call({"a": 2, "b": 3}) == "5"

        anyio.run(aclose_runnable_tool, adder)
        assert seen == ["enter", "exit"]

    async def test_async_context_manager_tool_lazy_enter_and_cleanup(self) -> None:
        from anthropic.lib.tools._beta_functions import beta_async_tool, aclose_runnable_tool

        seen: list[str] = []
        schema: InputSchema = {
            "type": "object",
            "properties": {"value": {"type": "string"}},
            "required": ["value"],
        }

        @asynccontextmanager
        async def echo_cm() -> AsyncIterator[Callable[[str], Awaitable[str]]]:
            """Echo the value."""
            seen.append("enter")

            async def echo(value: str) -> str:
                return f"echo:{value}"

            try:
                yield echo
            finally:
                seen.append("exit")

        echo_tool = beta_async_tool(name="echo", input_schema=schema)(cast(Any, echo_cm))

        # Name/description/schema are available without entering (the runner
        # reads them before any tool call).
        assert echo_tool.name == "echo"
        assert echo_tool.description == "Echo the value."
        assert echo_tool.to_dict()["input_schema"] == schema
        assert seen == []

        assert await echo_tool.call({"value": "hi"}) == "echo:hi"
        assert seen == ["enter"]

        await aclose_runnable_tool(echo_tool)
        assert seen == ["enter", "exit"]

    def test_wrong_decorator_raises(self) -> None:
        from anthropic.lib.tools._beta_functions import beta_async_tool

        @asynccontextmanager
        async def an_async_cm() -> AsyncIterator[Callable[[], str]]:
            yield lambda: "x"

        @contextmanager
        def a_sync_cm() -> Iterator[Callable[[], str]]:
            yield lambda: "x"

        with pytest.raises(TypeError, match="use @beta_async_tool"):
            beta_tool(cast(Any, an_async_cm))

        with pytest.raises(TypeError, match="use @beta_tool"):
            beta_async_tool(name="bad2")(cast(Any, a_sync_cm))

    def test_async_context_manager_requires_input_schema(self) -> None:
        from anthropic.lib.tools._beta_functions import beta_async_tool

        @asynccontextmanager
        async def noschema_cm() -> AsyncIterator[Callable[[int], Awaitable[str]]]:
            async def fn(x: int) -> str:
                return str(x)

            yield fn

        with pytest.raises(TypeError, match="needs an explicit input_schema"):
            beta_async_tool(name="noschema")(cast(Any, noschema_cm))
