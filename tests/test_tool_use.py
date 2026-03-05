"""Unit tests for the tool_use example.

Tests cover:
- Weather data retrieval with known and unknown locations
- Temperature unit conversion (Celsius to Fahrenheit)
- Tool call routing and error handling
- Edge cases: empty inputs, special characters, missing parameters
- Full tool use loop with mocked API responses
"""

import json
from unittest.mock import MagicMock, patch

import pytest

# Import functions from the example module
from examples.tool_use import get_weather, process_tool_call


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def known_locations():
    """Return the set of locations with predefined weather data."""
    return {
        "London, UK": {"temp": 12, "condition": "Cloudy", "humidity": 78},
        "New York, US": {"temp": 22, "condition": "Sunny", "humidity": 45},
        "Tokyo, JP": {"temp": 18, "condition": "Partly cloudy", "humidity": 60},
    }


@pytest.fixture
def sample_tool_use_block():
    """Return a mock tool use content block matching the API response shape."""
    block = MagicMock()
    block.type = "tool_use"
    block.id = "toolu_test_123"
    block.name = "get_weather"
    block.input = {"location": "London, UK", "unit": "celsius"}
    return block


# ---------------------------------------------------------------------------
# get_weather – known locations
# ---------------------------------------------------------------------------


class TestGetWeatherKnownLocations:
    """Tests for get_weather with locations that exist in the simulated data."""

    @pytest.mark.parametrize(
        "location, expected_temp, expected_condition",
        [
            ("London, UK", 12, "Cloudy"),
            ("New York, US", 22, "Sunny"),
            ("Tokyo, JP", 18, "Partly cloudy"),
        ],
    )
    def test_returns_correct_data_for_known_locations(
        self, location, expected_temp, expected_condition
    ):
        """Each known location should return its predefined temperature and condition."""
        result = get_weather(location)

        assert result["location"] == location
        assert result["temperature"] == expected_temp
        assert result["condition"] == expected_condition
        assert result["unit"] == "celsius"

    def test_response_contains_all_required_fields(self):
        """Every response must include location, temperature, unit, condition, humidity."""
        result = get_weather("London, UK")
        required_fields = {"location", "temperature", "unit", "condition", "humidity"}

        assert set(result.keys()) == required_fields

    @pytest.mark.parametrize(
        "location, expected_humidity",
        [
            ("London, UK", 78),
            ("New York, US", 45),
            ("Tokyo, JP", 60),
        ],
    )
    def test_returns_correct_humidity(self, location, expected_humidity):
        """Humidity values should match the simulated data."""
        result = get_weather(location)

        assert result["humidity"] == expected_humidity


# ---------------------------------------------------------------------------
# get_weather – unknown locations
# ---------------------------------------------------------------------------


class TestGetWeatherUnknownLocations:
    """Tests for get_weather with locations not in the simulated dataset."""

    @pytest.mark.parametrize(
        "location",
        [
            "Istanbul, TR",
            "Berlin, DE",
            "São Paulo, BR",
            "",
            "NonExistentCity",
        ],
    )
    def test_returns_defaults_for_unknown_locations(self, location):
        """Unknown locations should fall back to default values."""
        result = get_weather(location)

        assert result["temperature"] == 20
        assert result["condition"] == "Unknown"
        assert result["humidity"] == 50
        assert result["location"] == location


# ---------------------------------------------------------------------------
# get_weather – unit conversion
# ---------------------------------------------------------------------------


class TestGetWeatherUnitConversion:
    """Tests for Celsius to Fahrenheit conversion logic."""

    @pytest.mark.parametrize(
        "location, expected_fahrenheit",
        [
            ("London, UK", 54),       # 12°C → round(12 * 9/5 + 32) = 54°F
            ("New York, US", 72),      # 22°C → round(22 * 9/5 + 32) = 72°F
            ("Tokyo, JP", 64),         # 18°C → round(18 * 9/5 + 32) = 64°F
        ],
    )
    def test_fahrenheit_conversion_for_known_locations(
        self, location, expected_fahrenheit
    ):
        """Fahrenheit conversion should follow the formula: round(C * 9/5 + 32)."""
        result = get_weather(location, unit="fahrenheit")

        assert result["temperature"] == expected_fahrenheit
        assert result["unit"] == "fahrenheit"

    def test_fahrenheit_conversion_for_unknown_location(self):
        """Default temperature (20°C) should convert to 68°F."""
        result = get_weather("Unknown City", unit="fahrenheit")

        assert result["temperature"] == 68

    def test_celsius_is_default_unit(self):
        """When no unit is specified, celsius should be used."""
        result = get_weather("London, UK")

        assert result["unit"] == "celsius"


# ---------------------------------------------------------------------------
# process_tool_call – routing
# ---------------------------------------------------------------------------


class TestProcessToolCall:
    """Tests for the tool call routing function."""

    def test_routes_get_weather_correctly(self):
        """Calling 'get_weather' should return valid JSON with weather data."""
        result = process_tool_call("get_weather", {"location": "Tokyo, JP"})
        parsed = json.loads(result)

        assert parsed["location"] == "Tokyo, JP"
        assert "temperature" in parsed

    def test_returns_error_for_unknown_tool(self):
        """An unknown tool name should return a JSON error message."""
        result = process_tool_call("nonexistent_tool", {})
        parsed = json.loads(result)

        assert "error" in parsed
        assert "nonexistent_tool" in parsed["error"]

    def test_returns_valid_json(self):
        """All responses from process_tool_call must be valid JSON strings."""
        for tool_name in ["get_weather", "unknown_tool"]:
            result = process_tool_call(tool_name, {"location": "London, UK"})

            assert isinstance(result, str)
            json.loads(result)  # Should not raise

    def test_passes_keyword_arguments_correctly(self):
        """Tool input dict should be unpacked as keyword arguments."""
        result = process_tool_call(
            "get_weather",
            {"location": "London, UK", "unit": "fahrenheit"},
        )
        parsed = json.loads(result)

        assert parsed["unit"] == "fahrenheit"
        assert parsed["temperature"] == 54


# ---------------------------------------------------------------------------
# Full tool use loop with mocked API
# ---------------------------------------------------------------------------


class TestToolUseLoop:
    """Integration tests for the complete tool use workflow using mocked API."""

    def _make_mock_response(self, *, stop_reason, content):
        """Helper to create a mock API response object."""
        response = MagicMock()
        response.stop_reason = stop_reason
        response.content = content
        return response

    def test_single_tool_call_loop(self, sample_tool_use_block):
        """Simulate a single tool call followed by a final text response."""
        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = "The weather in London is 12°C and cloudy."

        tool_response = self._make_mock_response(
            stop_reason="tool_use",
            content=[sample_tool_use_block],
        )
        final_response = self._make_mock_response(
            stop_reason="end_turn",
            content=[text_block],
        )

        with patch("examples.tool_use.client") as mock_client:
            mock_client.messages.create.side_effect = [tool_response, final_response]

            from examples.tool_use import main

            main()

            assert mock_client.messages.create.call_count == 2

    def test_multiple_tool_calls_in_single_response(self):
        """Simulate Claude requesting two tools in one response."""
        block_london = MagicMock()
        block_london.type = "tool_use"
        block_london.id = "toolu_1"
        block_london.name = "get_weather"
        block_london.input = {"location": "London, UK"}

        block_tokyo = MagicMock()
        block_tokyo.type = "tool_use"
        block_tokyo.id = "toolu_2"
        block_tokyo.name = "get_weather"
        block_tokyo.input = {"location": "Tokyo, JP"}

        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = "London is 12°C, Tokyo is 18°C."

        tool_response = self._make_mock_response(
            stop_reason="tool_use",
            content=[block_london, block_tokyo],
        )
        final_response = self._make_mock_response(
            stop_reason="end_turn",
            content=[text_block],
        )

        with patch("examples.tool_use.client") as mock_client:
            mock_client.messages.create.side_effect = [tool_response, final_response]

            from examples.tool_use import main

            main()

            assert mock_client.messages.create.call_count == 2
