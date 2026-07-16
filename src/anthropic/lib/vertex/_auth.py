from __future__ import annotations

from typing import TYPE_CHECKING

from .._extras._google_auth import refresh_credentials as refresh_auth, load_default_credentials

if TYPE_CHECKING:
    from google.auth.credentials import Credentials  # type: ignore[import-untyped]

# Note: these functions are blocking as they make HTTP requests, the async
# client runs these functions in a separate thread to ensure they do not
# cause synchronous blocking issues.

__all__ = ["load_auth", "refresh_auth"]


def load_auth(*, project_id: str | None) -> tuple[Credentials, str]:
    credentials, loaded_project_id = load_default_credentials(extra="vertex")

    if not project_id:
        project_id = loaded_project_id

    if not project_id:
        raise ValueError("Could not resolve project_id")

    return credentials, project_id
