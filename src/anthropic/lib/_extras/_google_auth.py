from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast
from typing_extensions import ClassVar, override

from ._common import MissingDependencyError
from ..._utils import LazyProxy

if TYPE_CHECKING:
    import google.auth  # type: ignore
    from google.auth.credentials import Credentials as GoogleCredentials  # type: ignore

    google_auth = google.auth

# pyright: reportMissingTypeStubs=false, reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false
# google libraries don't ship type stubs.

CLOUD_PLATFORM_SCOPE = "https://www.googleapis.com/auth/cloud-platform"


class GoogleAuthProxy(LazyProxy[Any]):
    should_cache: ClassVar[bool] = True

    @override
    def __load__(self) -> Any:
        try:
            import google.auth  # type: ignore
        except ImportError as err:
            raise MissingDependencyError(extra="vertex", library="google-auth") from err

        return google.auth


if not TYPE_CHECKING:
    google_auth = GoogleAuthProxy()


def _request(*, extra: str = "vertex") -> Any:
    try:
        from google.auth.transport.requests import Request  # type: ignore[import-untyped]
    except ImportError as err:
        raise MissingDependencyError(extra=extra, library="google-auth") from err
    return Request()


def load_default_credentials(*, extra: str = "vertex") -> tuple[GoogleCredentials, str | None]:
    """Load Application Default Credentials with the ``cloud-platform`` scope and
    mint an initial access token.

    Returns the credentials object and the project they resolve to (``None`` for
    plain user ADC). Blocking — async callers wrap with :func:`anthropic._utils.asyncify`.

    ``extra`` names the pip extra that the install hint in :class:`MissingDependencyError`
    points at when ``google-auth`` isn't installed; callers pass the extra for their client.
    """
    try:
        import google.auth  # type: ignore
    except ImportError as err:
        raise MissingDependencyError(extra=extra, library="google-auth") from err

    credentials, project = google.auth.default(scopes=[CLOUD_PLATFORM_SCOPE])
    cast(Any, credentials).refresh(_request(extra=extra))
    return cast("GoogleCredentials", credentials), project


def refresh_credentials(credentials: GoogleCredentials, *, extra: str = "vertex") -> None:
    """Refresh ``credentials`` in place via ``google.auth.transport.requests``.

    Blocking — async callers wrap with :func:`anthropic._utils.asyncify`.
    """
    cast(Any, credentials).refresh(_request(extra=extra))
