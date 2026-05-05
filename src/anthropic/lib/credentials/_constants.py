from __future__ import annotations

import os
import sys
import pathlib
from typing import Optional

from ..._exceptions import AnthropicError

GRANT_TYPE_JWT_BEARER = "urn:ietf:params:oauth:grant-type:jwt-bearer"
GRANT_TYPE_REFRESH_TOKEN = "refresh_token"
TOKEN_ENDPOINT = "/v1/oauth/token"

# Seconds to wait on the /v1/oauth/token POST before giving up. Tokens are cheap
# to mint and the handler is fast; a long timeout mostly means a sick backend.
TOKEN_EXCHANGE_TIMEOUT = 30.0

# Beta header required on any authenticated API request that uses a Bearer
# token obtained via OAuth/federation (unlocks `Authorization: Bearer` auth
# at all), and on refresh_token grants against /v1/oauth/token.
OAUTH_API_BETA_HEADER = "oauth-2025-04-20"

# Beta header routing switch for /v1/oauth/token jwt-bearer grants. Presence
# routes the POST to the api-go userauth handler (jwt-bearer only); absence
# routes it to the Python oauth_server (authorization_code / refresh_token).
# MUST only be sent on jwt-bearer exchanges — sending it on refresh_token would
# misroute the request to userauth and fail with "unsupported grant_type".
FEDERATION_BETA_HEADER = "oidc-federation-2026-04-01"

# Proactive refresh thresholds (seconds before expiry). Tuned for ≤10min token TTL.
ADVISORY_REFRESH_SECONDS = 120
MANDATORY_REFRESH_SECONDS = 30

DEFAULT_PROFILE = "default"
DEFAULT_BASE_URL = "https://api.anthropic.com"

# Env vars — explicit auth (tier 0)
ENV_API_KEY = "ANTHROPIC_API_KEY"
ENV_AUTH_TOKEN = "ANTHROPIC_AUTH_TOKEN"

# Env vars — config dir + profile selection (tier 1)
ENV_CONFIG_DIR = "ANTHROPIC_CONFIG_DIR"
ENV_PROFILE = "ANTHROPIC_PROFILE"

# Env vars — direct workload identity, bypassing config files (tier 2)
ENV_IDENTITY_TOKEN = "ANTHROPIC_IDENTITY_TOKEN"
ENV_IDENTITY_TOKEN_FILE = "ANTHROPIC_IDENTITY_TOKEN_FILE"
ENV_FEDERATION_RULE_ID = "ANTHROPIC_FEDERATION_RULE_ID"
ENV_ORGANIZATION_ID = "ANTHROPIC_ORGANIZATION_ID"
ENV_SERVICE_ACCOUNT_ID = "ANTHROPIC_SERVICE_ACCOUNT_ID"
ENV_WORKSPACE_ID = "ANTHROPIC_WORKSPACE_ID"
ENV_SCOPE = "ANTHROPIC_SCOPE"
ENV_BASE_URL = "ANTHROPIC_BASE_URL"


def _user_agent() -> str:  # pyright: ignore[reportUnusedFunction] — used by _workload/_providers
    """``User-Agent`` value sent on token-endpoint POSTs.

    Computed lazily so this module doesn't need to import ``_version`` at
    module load time (the credentials package is otherwise import-light).
    """
    from ..._version import __version__

    return f"anthropic-python/{__version__}"


def _config_dir() -> pathlib.Path:
    """Resolve the config directory.

    ``ANTHROPIC_CONFIG_DIR`` env var → platform default.

    Platform defaults:
      * Linux & macOS: ``~/.config/anthropic/`` — XDG-style on both platforms
        for consistency across SDKs (macOS does **not** use
        ``~/Library/Application Support/``).
      * Windows: ``%APPDATA%\\Anthropic\\``
    """
    env = os.environ.get(ENV_CONFIG_DIR)
    if env:
        return pathlib.Path(env)
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        base = pathlib.Path(appdata) if appdata else pathlib.Path.home() / "AppData" / "Roaming"
        return base / "Anthropic"
    return pathlib.Path.home() / ".config" / "anthropic"


def _read_active_config_pointer() -> Optional[str]:
    """Return the stripped contents of ``<config_dir>/active_config``, or ``None``
    if the pointer file is missing or empty."""
    try:
        name = (_config_dir() / "active_config").read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return name or None


def _active_profile() -> str:  # pyright: ignore[reportUnusedFunction] — used by _providers
    """Resolve the active profile name.

    ``ANTHROPIC_PROFILE`` env var → ``<config_dir>/active_config`` pointer file
    → ``"default"`` literal. The resolved name is validated against path-
    traversal patterns before being returned.
    """
    env = os.environ.get(ENV_PROFILE)
    if env:
        _validate_profile_name(env, source=ENV_PROFILE)
        return env
    name = _read_active_config_pointer()
    if name is None:
        return DEFAULT_PROFILE
    _validate_profile_name(name, source="active_config pointer file")
    return name


def _require_https(url: str, *, field: str) -> None:  # pyright: ignore[reportUnusedFunction] — used by _workload/_providers
    """Reject non-``https://`` token-endpoint URLs.

    Localhost is allowed for testing so ``base_url="http://localhost:8080"``
    works against a local ``oauth_server`` instance; everything else must be
    TLS-encrypted because the body of these POSTs carries the assertion JWT
    or a long-lived refresh token.
    """
    lowered = url.lower().rstrip("/")
    if lowered.startswith("https://"):
        return
    if lowered.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        return
    raise AnthropicError(
        f"{field} must use https (got {url!r}); the token-exchange endpoint "
        f"carries secret material and cannot be used over cleartext HTTP."
    )


def _validate_profile_name(profile: str, *, source: str = "profile name") -> None:
    """Reject profile names that could escape the config directory.

    Profile names come from user-controlled sources (``ANTHROPIC_PROFILE``,
    the ``active_config`` pointer file, ``CredentialsFile(profile=...)``) and
    are interpolated into filesystem paths. A value like ``"../../etc/shadow"``
    would otherwise let a read of ``configs/<profile>.json`` escape the config
    root entirely. Pass ``source=`` so the error message names where the bad
    value came from.
    """
    if not profile:
        raise AnthropicError(f"{source} must not be empty.")
    if profile != profile.strip():
        raise AnthropicError(f"{source} {profile!r} has leading or trailing whitespace.")
    if profile.startswith("."):
        raise AnthropicError(f"{source} {profile!r} must not start with a dot.")
    for sep in ("/", "\\", os.sep):
        if sep and sep in profile:
            raise AnthropicError(
                f"{source} {profile!r} must not contain path separators — "
                f"profiles are filenames under the config directory. Pick a name without {sep!r}."
            )
    if "\x00" in profile:
        raise AnthropicError(f"{source} {profile!r} must not contain null bytes.")


def _resolve_under(base: pathlib.Path, candidate: pathlib.Path) -> pathlib.Path:
    """Assert ``candidate`` resolves to a descendant of ``base``, return it verbatim.

    The containment check uses ``resolve(strict=False)`` on both sides so
    symlinks and ``..`` segments are normalized for the purposes of escape
    detection. The returned path is the *original* (unresolved) candidate —
    callers that care about symlink following must handle it themselves
    (e.g. ``os.stat(follow_symlinks=False)``).
    """
    base_resolved = base.resolve(strict=False)
    candidate_resolved = candidate.resolve(strict=False)
    try:
        candidate_resolved.relative_to(base_resolved)
    except ValueError as err:
        raise AnthropicError(
            f"Resolved path {candidate_resolved} escapes config directory {base_resolved}."
        ) from err
    return candidate


def _config_file_path(profile: str) -> pathlib.Path:  # pyright: ignore[reportUnusedFunction] — used by _providers
    """Path to ``<config_dir>/configs/<profile>.json`` (non-secret, 0644)."""
    _validate_profile_name(profile)
    base = _config_dir()
    return _resolve_under(base, base / "configs" / f"{profile}.json")


def _credentials_file_path(profile: str) -> pathlib.Path:  # pyright: ignore[reportUnusedFunction] — used by _providers
    """Path to ``<config_dir>/credentials/<profile>.json`` (secret, 0600)."""
    _validate_profile_name(profile)
    base = _config_dir()
    return _resolve_under(base, base / "credentials" / f"{profile}.json")


def _has_active_profile_config() -> bool:  # pyright: ignore[reportUnusedFunction] — used by _chain
    """Tighter auto-discover check for the tier-1 credential chain.

    Returns ``True`` only if the *active* profile's config file exists. The
    previous version returned ``True`` for any ``.json`` under ``configs/``,
    which meant a stray ``configs/work.json`` on disk was enough to steer
    ``default_credentials()`` into reading ``configs/default.json`` and
    failing because ``default.json`` wasn't there.
    """
    try:
        return _config_file_path(_active_profile()).is_file()
    except (OSError, AnthropicError):
        return False


def _has_explicit_active_config() -> bool:  # pyright: ignore[reportUnusedFunction] — used by _chain
    """True if the user wrote a non-empty ``active_config`` pointer file.

    This is an explicit opt-in signal equivalent to setting ``ANTHROPIC_PROFILE``:
    the user has told us which profile to load. If the target config file is
    missing or malformed, the chain should surface that error rather than
    silently falling through — matching how ``ANTHROPIC_PROFILE=missing``
    behaves today.
    """
    return _read_active_config_pointer() is not None


def resolve_identity_token_path(path: str | os.PathLike[str] | None = None) -> pathlib.Path | None:
    """ctor arg → ``ANTHROPIC_IDENTITY_TOKEN_FILE`` → ``None``."""
    if path is not None:
        return pathlib.Path(path)
    env = os.environ.get(ENV_IDENTITY_TOKEN_FILE)
    if env:
        return pathlib.Path(env)
    return None


def _has_auto_discoverable_credentials() -> bool:  # pyright: ignore[reportUnusedFunction] — used by _client
    """True if the environment / filesystem contains signals that would
    normally drive the tier-1 (profile) or tier-2 (env federation) paths of
    :func:`default_credentials`.

    Used by the shadow-warning detection in the client constructor: if a
    static ``ANTHROPIC_API_KEY`` / ``ANTHROPIC_AUTH_TOKEN`` is set alongside
    any of these signals, the auto-discovery would have yielded a credential
    but got silently shadowed — and the user should know.
    """
    if os.environ.get(ENV_PROFILE) or os.environ.get(ENV_CONFIG_DIR):
        return True
    if _has_explicit_active_config():
        return True
    if os.environ.get(ENV_FEDERATION_RULE_ID) and os.environ.get(ENV_ORGANIZATION_ID):
        if os.environ.get(ENV_IDENTITY_TOKEN_FILE) or os.environ.get(ENV_IDENTITY_TOKEN):
            return True
    return False
