from __future__ import annotations

from typing import TYPE_CHECKING

from .._extras import google_auth

if TYPE_CHECKING:
    from google.auth.credentials import Credentials  # type: ignore[import-untyped]

# pyright: reportMissingTypeStubs=false, reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false
# google libraries don't provide types :/

# Note: these functions are blocking as they make HTTP requests, the async
# client runs these functions in a separate thread to ensure they do not
# cause synchronous blocking issues.


def load_auth() -> tuple[Credentials, str]:
    from google.auth.transport.requests import Request  # type: ignore[import-untyped]

    credentials, project_id = google_auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    credentials.refresh(Request())

    return credentials, project_id


def refresh_auth(credentials: Credentials) -> None:
    from google.auth.transport.requests import Request  # type: ignore[import-untyped]

    credentials.refresh(Request())
