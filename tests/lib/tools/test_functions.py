from __future__ import annotations

from typing import Any, cast

import pytest
from pydantic import BaseModel

from anthropic import beta_tool
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools._beta_functions import BaseFunctionTool
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
