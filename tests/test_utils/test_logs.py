"""Tests for _logs utility functions."""

from __future__ import annotations

import os
import logging
from unittest import mock

import pytest

from anthropic._utils._logs import setup_logging, logger, httpx_logger


class TestSetupLogging:
    """Test the setup_logging function."""

    def test_setup_logging_debug(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test setup_logging with debug level."""
        monkeypatch.setenv("ANTHROPIC_LOG", "debug")

        with mock.patch("anthropic._utils._logs._basic_config") as mock_basic_config:
            setup_logging()

            mock_basic_config.assert_called_once()
            assert logger.level == logging.DEBUG
            assert httpx_logger.level == logging.DEBUG

    def test_setup_logging_info(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test setup_logging with info level."""
        monkeypatch.setenv("ANTHROPIC_LOG", "info")

        with mock.patch("anthropic._utils._logs._basic_config") as mock_basic_config:
            setup_logging()

            mock_basic_config.assert_called_once()
            assert logger.level == logging.INFO
            assert httpx_logger.level == logging.INFO

    def test_setup_logging_no_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test setup_logging with no environment variable set."""
        monkeypatch.delenv("ANTHROPIC_LOG", raising=False)

        with mock.patch("anthropic._utils._logs._basic_config") as mock_basic_config:
            # Reset logger levels
            logger.setLevel(logging.NOTSET)
            httpx_logger.setLevel(logging.NOTSET)

            setup_logging()

            # Should not call basic_config
            mock_basic_config.assert_not_called()

    def test_setup_logging_invalid_value(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test setup_logging with an invalid environment variable value."""
        monkeypatch.setenv("ANTHROPIC_LOG", "invalid")

        with mock.patch("anthropic._utils._logs._basic_config") as mock_basic_config:
            setup_logging()

            # Should not configure logging for invalid values
            mock_basic_config.assert_not_called()

    def test_setup_logging_case_sensitive(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that ANTHROPIC_LOG is case-sensitive."""
        monkeypatch.setenv("ANTHROPIC_LOG", "DEBUG")

        with mock.patch("anthropic._utils._logs._basic_config") as mock_basic_config:
            setup_logging()

            # Should not match "DEBUG" (uppercase)
            mock_basic_config.assert_not_called()

    def test_logger_name(self) -> None:
        """Test that logger has correct name."""
        assert logger.name == "anthropic"

    def test_httpx_logger_name(self) -> None:
        """Test that httpx_logger has correct name."""
        assert httpx_logger.name == "httpx"

    def test_basic_config_format(self) -> None:
        """Test that basic_config sets up correct format."""
        from anthropic._utils._logs import _basic_config

        with mock.patch("anthropic._utils._logs.logging.basicConfig") as mock_config:
            _basic_config()

            mock_config.assert_called_once()
            call_kwargs = mock_config.call_args[1]
            assert "format" in call_kwargs
            assert "datefmt" in call_kwargs
            # Verify the format contains expected fields
            assert "asctime" in call_kwargs["format"]
            assert "name" in call_kwargs["format"]
            assert "lineno" in call_kwargs["format"]
            assert "levelname" in call_kwargs["format"]
            assert "message" in call_kwargs["format"]

    def test_multiple_setup_calls(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test calling setup_logging multiple times."""
        monkeypatch.setenv("ANTHROPIC_LOG", "debug")

        with mock.patch("anthropic._utils._logs._basic_config") as mock_basic_config:
            setup_logging()
            setup_logging()

            # basicConfig should be called each time
            assert mock_basic_config.call_count == 2
