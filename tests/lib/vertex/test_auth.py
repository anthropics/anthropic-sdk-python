"""Tests for Vertex AI authentication."""

from __future__ import annotations

from unittest import mock

import pytest


class TestVertexAuth:
    """Test Vertex AI authentication functionality."""

    def test_load_auth_success_with_project_id(self) -> None:
        """Test loading auth when project_id is provided."""
        from anthropic.lib.vertex._auth import load_auth

        mock_credentials = mock.Mock()
        mock_credentials.refresh = mock.Mock()

        with mock.patch("anthropic.lib._extras._google_auth.default") as mock_default:
            with mock.patch("anthropic.lib.vertex._auth.Request") as mock_request:
                mock_default.return_value = (mock_credentials, "default-project")

                credentials, project_id = load_auth(project_id="my-project")

                assert credentials is mock_credentials
                assert project_id == "my-project"
                mock_credentials.refresh.assert_called_once()
                mock_default.assert_called_once_with(
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )

    def test_load_auth_success_without_project_id(self) -> None:
        """Test loading auth when project_id is not provided."""
        from anthropic.lib.vertex._auth import load_auth

        mock_credentials = mock.Mock()
        mock_credentials.refresh = mock.Mock()

        with mock.patch("anthropic.lib._extras._google_auth.default") as mock_default:
            with mock.patch("anthropic.lib.vertex._auth.Request"):
                mock_default.return_value = (mock_credentials, "loaded-project")

                credentials, project_id = load_auth(project_id=None)

                assert credentials is mock_credentials
                assert project_id == "loaded-project"
                mock_credentials.refresh.assert_called_once()

    def test_load_auth_raises_when_no_project_id(self) -> None:
        """Test that ValueError is raised when project_id cannot be resolved."""
        from anthropic.lib.vertex._auth import load_auth

        mock_credentials = mock.Mock()
        mock_credentials.refresh = mock.Mock()

        with mock.patch("anthropic.lib._extras._google_auth.default") as mock_default:
            with mock.patch("anthropic.lib.vertex._auth.Request"):
                # Both provided and loaded project_id are None
                mock_default.return_value = (mock_credentials, None)

                with pytest.raises(ValueError, match="Could not resolve project_id"):
                    load_auth(project_id=None)

    def test_load_auth_raises_when_project_id_wrong_type(self) -> None:
        """Test that TypeError is raised when project_id is not a string."""
        from anthropic.lib.vertex._auth import load_auth

        mock_credentials = mock.Mock()
        mock_credentials.refresh = mock.Mock()

        with mock.patch("anthropic.lib._extras._google_auth.default") as mock_default:
            with mock.patch("anthropic.lib.vertex._auth.Request"):
                # Return non-string project_id
                mock_default.return_value = (mock_credentials, 12345)  # type: ignore[arg-type]

                with pytest.raises(TypeError, match="Expected project_id to be a str"):
                    load_auth(project_id=None)

    def test_load_auth_raises_when_google_auth_not_installed(self) -> None:
        """Test that RuntimeError is raised when google.auth is not installed."""
        from anthropic.lib.vertex._auth import load_auth

        with mock.patch.dict("sys.modules", {"google.auth.transport.requests": None}):
            # Simulate import error by making the import fail
            with mock.patch(
                "anthropic.lib.vertex._auth.Request",
                side_effect=ModuleNotFoundError("No module named 'google.auth'"),
            ):
                with pytest.raises(
                    RuntimeError,
                    match="Could not import google.auth, you need to install the SDK with `pip install anthropic\\[vertex\\]`",
                ):
                    load_auth(project_id="my-project")

    def test_load_auth_refreshes_credentials(self) -> None:
        """Test that credentials are refreshed during load_auth."""
        from anthropic.lib.vertex._auth import load_auth

        mock_credentials = mock.Mock()
        mock_request = mock.Mock()

        with mock.patch("anthropic.lib._extras._google_auth.default") as mock_default:
            with mock.patch("anthropic.lib.vertex._auth.Request", return_value=mock_request):
                mock_default.return_value = (mock_credentials, "test-project")

                load_auth(project_id="test-project")

                # Verify refresh was called with Request instance
                mock_credentials.refresh.assert_called_once_with(mock_request)

    def test_refresh_auth(self) -> None:
        """Test refreshing credentials."""
        from anthropic.lib.vertex._auth import refresh_auth

        mock_credentials = mock.Mock()
        mock_request = mock.Mock()

        with mock.patch("anthropic.lib.vertex._auth.Request", return_value=mock_request):
            refresh_auth(mock_credentials)

            mock_credentials.refresh.assert_called_once_with(mock_request)

    def test_refresh_auth_propagates_exceptions(self) -> None:
        """Test that refresh_auth propagates exceptions from credentials.refresh."""
        from anthropic.lib.vertex._auth import refresh_auth

        mock_credentials = mock.Mock()
        mock_credentials.refresh.side_effect = RuntimeError("Refresh failed")

        with mock.patch("anthropic.lib.vertex._auth.Request"):
            with pytest.raises(RuntimeError, match="Refresh failed"):
                refresh_auth(mock_credentials)

    def test_load_auth_uses_correct_scopes(self) -> None:
        """Test that load_auth uses the correct Google Cloud scopes."""
        from anthropic.lib.vertex._auth import load_auth

        mock_credentials = mock.Mock()
        mock_credentials.refresh = mock.Mock()

        with mock.patch("anthropic.lib._extras._google_auth.default") as mock_default:
            with mock.patch("anthropic.lib.vertex._auth.Request"):
                mock_default.return_value = (mock_credentials, "test-project")

                load_auth(project_id="test-project")

                # Verify the correct scope is used
                mock_default.assert_called_once()
                call_kwargs = mock_default.call_args[1]
                assert call_kwargs["scopes"] == ["https://www.googleapis.com/auth/cloud-platform"]

    def test_load_auth_prefers_provided_project_id(self) -> None:
        """Test that provided project_id takes precedence over loaded one."""
        from anthropic.lib.vertex._auth import load_auth

        mock_credentials = mock.Mock()
        mock_credentials.refresh = mock.Mock()

        with mock.patch("anthropic.lib._extras._google_auth.default") as mock_default:
            with mock.patch("anthropic.lib.vertex._auth.Request"):
                mock_default.return_value = (mock_credentials, "loaded-project")

                credentials, project_id = load_auth(project_id="provided-project")

                # Should use provided project_id, not loaded one
                assert project_id == "provided-project"
