from __future__ import annotations

import os
import json
import stat
import time
import logging
import pathlib
import tempfile
from typing import TYPE_CHECKING, Any, Dict, Union, Optional, cast
from typing_extensions import override

import httpx

from ._types import AccessToken, IdentityTokenProvider
from ._constants import (
    ENV_SCOPE,
    ENV_PROFILE,
    ENV_BASE_URL,
    ENV_AUTH_TOKEN,
    ENV_CONFIG_DIR,
    TOKEN_ENDPOINT,
    DEFAULT_BASE_URL,
    ENV_WORKSPACE_ID,
    ENV_ORGANIZATION_ID,
    OAUTH_API_BETA_HEADER,
    ENV_FEDERATION_RULE_ID,
    ENV_SERVICE_ACCOUNT_ID,
    TOKEN_EXCHANGE_TIMEOUT,
    ENV_IDENTITY_TOKEN_FILE,
    GRANT_TYPE_REFRESH_TOKEN,
    MANDATORY_REFRESH_SECONDS,
    _user_agent,
    _require_https,
    _active_profile,
    _config_file_path,
    _credentials_file_path,
    resolve_identity_token_path,
)
from ..._exceptions import AnthropicError

log: logging.Logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ._workload import WorkloadIdentityCredentials

__all__ = ["StaticToken", "EnvToken", "CredentialsFile", "InMemoryConfig", "IdentityTokenFile"]


def _coerce_expires_at(value: Any, source: Optional[pathlib.Path]) -> Optional[int]:
    """Parse a credentials-file ``expires_at`` field into Unix seconds."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError) as err:
        where = f"credentials file at {source}" if source is not None else "credentials"
        raise AnthropicError(
            f"{where} has invalid 'expires_at' {value!r}; expected an integer "
            f"Unix timestamp in seconds. The SDK does not parse ISO8601 — convert "
            f"with int(datetime.timestamp()) before writing the file."
        ) from err


# Discriminator written to credentials/<profile>.json. Only one value in v1;
# future credential shapes (e.g. private key material) get their own.
CREDENTIALS_FILE_TYPE = "oauth_token"

# On-disk file-format versions. Absent on read = 1 (current shape).
CONFIG_FILE_VERSION = "1.0"
CREDENTIALS_FILE_VERSION = "1.0"

# Discriminator values for the config file's ``authentication.type`` field.
AUTH_TYPE_OIDC_FEDERATION = "oidc_federation"
AUTH_TYPE_USER_OAUTH = "user_oauth"


def _fill_missing_from_env(config: Dict[str, Any], auth: Dict[str, Any]) -> None:
    """Fill empty profile fields from corresponding ANTHROPIC_* env vars.

    The profile file is authoritative — this only fills fields the file left
    unset. Empty-string env values are treated as unset.
    """

    def fill(target: Dict[str, Any], key: str, env_var: str) -> None:
        # Absent-key and empty-string profile values are both treated as unset.
        if not target.get(key):
            v = os.environ.get(env_var)
            if v:
                target[key] = v

    fill(config, "base_url", ENV_BASE_URL)
    fill(config, "organization_id", ENV_ORGANIZATION_ID)
    fill(config, "workspace_id", ENV_WORKSPACE_ID)

    auth_type = auth.get("type")
    if auth_type == AUTH_TYPE_OIDC_FEDERATION:
        fill(auth, "federation_rule_id", ENV_FEDERATION_RULE_ID)
        fill(auth, "service_account_id", ENV_SERVICE_ACCOUNT_ID)
        fill(auth, "scope", ENV_SCOPE)
        if not auth.get("identity_token"):
            v = os.environ.get(ENV_IDENTITY_TOKEN_FILE)
            if v:
                auth["identity_token"] = {"source": "file", "path": v}
    elif auth_type == AUTH_TYPE_USER_OAUTH:
        fill(auth, "scope", ENV_SCOPE)


class StaticToken:
    """An :class:`AccessTokenProvider` that always returns a fixed token with no expiry."""

    def __init__(self, token: str) -> None:
        self._token = token

    def __call__(self, *, force_refresh: bool = False) -> AccessToken:
        del force_refresh  # no provider-side cache to bypass
        return AccessToken(token=self._token, expires_at=None)


class EnvToken:
    """An :class:`AccessTokenProvider` that reads ``ANTHROPIC_AUTH_TOKEN`` at call time."""

    def __init__(self, env_var: str = ENV_AUTH_TOKEN) -> None:
        self._env_var = env_var

    def __call__(self, *, force_refresh: bool = False) -> AccessToken:
        del force_refresh
        value = os.environ.get(self._env_var)
        if value is None:
            raise AnthropicError(
                f"Environment variable {self._env_var} is not set. "
                f"Set it or pass an explicit `credentials=` provider to the client."
            )
        return AccessToken(token=value, expires_at=None)


class CredentialsFile:
    """An :class:`AccessTokenProvider` backed by a named profile.

    A profile is a pair of files under the config directory
    (``~/.config/anthropic/`` by default; override with ``ANTHROPIC_CONFIG_DIR``):

    * ``configs/<profile>.json`` — non-secret. Holds the nested
      ``"authentication"`` object (discriminated by its ``"type"`` field), plus
      top-level ``organization_id``, ``workspace_id``, and ``base_url``.
      The ``authentication`` object may contain a ``credentials_path`` field
      overriding the credentials file location.
    * ``credentials/<profile>.json`` — secret (0600). Holds ``access_token``,
      ``expires_at``, and (for ``user_oauth`` with a ``client_id``)
      ``refresh_token``.

    The split keeps secret material out of files that may need to be readable
    by config-only consumers, and lets the SDK enforce 0600 on the credentials
    file without locking out config readers.

    Dispatches on the ``authentication.type`` discriminator:

    ``"oidc_federation"``
        OIDC workload identity federation. Lazily constructs a
        :class:`WorkloadIdentityCredentials` delegate from the nested auth
        fields plus the top-level ``organization_id`` and calls it to perform
        the jwt-bearer exchange.

    ``"user_oauth"``
        Output of an interactive PKCE login. If the auth block has a
        ``client_id``, performs ``refresh_token`` grants on expiry and
        writes the new tokens back to the credentials file (atomic replace,
        refresh-token rotation supported). Without a ``client_id``, the
        credentials file is treated as externally rotated — the SDK re-reads
        it on every invocation and returns whatever ``access_token`` is
        there, no refresh grant attempted. This is the pattern for a
        sidecar/daemon that mints the access token out-of-band.

    Args:
        profile: Profile name. ``None`` resolves via ``ANTHROPIC_PROFILE`` env
            → ``<config_dir>/active_config`` pointer file → ``"default"``.
    """

    def __init__(
        self,
        profile: Optional[str] = None,
        *,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self._profile = profile if profile is not None else _active_profile()
        self._config_path = _config_file_path(self._profile)
        self._bound_base_url: Optional[str] = None
        self._http_client = http_client
        self._owned_http_client: Optional[httpx.Client] = None

        # Populated on first __call__ — keeps construction cheap and exception-free
        # so the chain can construct us optimistically after an existence check.
        self._config: Optional[Dict[str, Any]] = None
        self._credentials_path: Optional[pathlib.Path] = None
        self._base_url: str = DEFAULT_BASE_URL
        self._workload_delegate: Optional[WorkloadIdentityCredentials] = None

    @property
    def profile(self) -> str:
        return self._profile

    @property
    def config_path(self) -> pathlib.Path:
        return self._config_path

    @property
    def resolved_base_url(self) -> Optional[str]:
        """The ``base_url`` declared in the profile config file, if any.

        Returns ``None`` when the config has no top-level ``base_url`` key —
        callers should fall back to their own default rather than the
        provider's bound/default value, so a profile that *doesn't* pin a
        host never overrides an explicit client setting. Loads the config
        on first access.
        """
        config = self._load_config()
        raw = config.get("base_url")
        return str(raw).rstrip("/") if raw else None

    def bind_base_url(self, base_url: str) -> None:
        """Adopt the owning client's ``base_url`` as a fallback for the token
        exchange. Slots between the config file's own ``base_url`` field and
        the hard-coded default; a ``base_url`` in the config file still wins.

        The owning client binds exactly once at construction; sharing one
        instance across clients with different ``base_url`` values is
        unsupported and silently picks the last bind when the config file
        doesn't pin a host.
        """
        bound = base_url.rstrip("/")
        # Validate eagerly so an invalid bind fails at bind time, not at the
        # subsequent _load_config() — matches WorkloadIdentityCredentials.
        _require_https(bound, field=f"{self._config_path}: base_url")
        self._bound_base_url = bound
        if self._config is not None:
            self._base_url = self._resolve_base_url(self._config)
            _require_https(self._base_url, field=f"{self._config_path}: base_url")

    def _resolve_base_url(self, config: Dict[str, Any]) -> str:
        """base_url precedence: top-level config field → bound (the owning
        client's base_url, via :meth:`bind_base_url`) → default. Validated
        against the scheme/TLS rules so a malicious config with
        ``base_url="http://evil/"`` can't exfiltrate the assertion or refresh
        token."""
        if config.get("base_url"):
            return str(config["base_url"]).rstrip("/")
        if self._bound_base_url is not None:
            return self._bound_base_url
        return DEFAULT_BASE_URL

    def extra_headers(self) -> Dict[str, str]:
        """Return headers derived from the config file (e.g. ``workspace_id``).

        Eagerly reads the config if not yet loaded. The returned dict is
        suitable for merging into the client's default headers.
        """
        config = self._load_config()
        headers: Dict[str, str] = {}
        # For federation profiles workspace_id is sent in the jwt-bearer
        # exchange body, not as a request header (the minted token is already
        # workspace-scoped, so the header would be ignored).
        if self._auth_block().get("type") != AUTH_TYPE_OIDC_FEDERATION:
            workspace_id = config.get("workspace_id")
            if workspace_id:
                headers["anthropic-workspace-id"] = str(workspace_id)
        return headers

    # -- file IO -----------------------------------------------------------

    def _load_config(self) -> Dict[str, Any]:
        """Read and cache the config file, resolving ``base_url`` and ``credentials_path``."""
        if self._config is not None:
            return self._config

        try:
            raw = self._config_path.read_text(encoding="utf-8")
        except FileNotFoundError as err:
            raise AnthropicError(
                f"Config file not found at {self._config_path} (profile {self._profile!r}). "
                f"Set {ENV_PROFILE} to select a different profile, or set {ENV_CONFIG_DIR} "
                f"to relocate the config directory."
            ) from err
        except (OSError, UnicodeDecodeError) as err:
            raise AnthropicError(f"Config file at {self._config_path} could not be read: {err}") from err
        try:
            raw_config: Any = json.loads(raw)
        except json.JSONDecodeError as err:
            raise AnthropicError(f"Config file at {self._config_path} is not valid JSON: {err}") from err

        if not isinstance(raw_config, dict):
            raise AnthropicError(
                f"Config file at {self._config_path} must contain a JSON object, not {type(raw_config).__name__}."
            )
        config = cast("Dict[str, Any]", raw_config)

        raw_auth = config.get("authentication")
        if not isinstance(raw_auth, dict):
            raise AnthropicError(
                f"Config file at {self._config_path} is missing the 'authentication' object. "
                f'Expected shape: {{"authentication": {{"type": '
                f'"{AUTH_TYPE_OIDC_FEDERATION}"|"{AUTH_TYPE_USER_OAUTH}", ...}}, ...}}'
            )
        auth = cast("Dict[str, Any]", raw_auth)

        # Env-vars fill only what the file left empty; runs before derived
        # state (base_url, identity_token path) is resolved.
        _fill_missing_from_env(config, auth)

        self._base_url = self._resolve_base_url(config)
        _require_https(self._base_url, field=f"{self._config_path}: base_url")

        override = auth.get("credentials_path")
        if override:
            self._credentials_path = pathlib.Path(str(override)).expanduser()
        else:
            self._credentials_path = _credentials_file_path(self._profile)

        self._config = config
        return config

    def _read_credentials(self) -> Dict[str, Any]:
        """Read the credentials file. Re-reads on every call — daemons rotate it.

        On Unix, verifies the file is not group/world-readable. World-readable
        credentials files are refused outright; group-readable files log a
        warning but are accepted. The check is skipped on Windows where POSIX
        mode bits don't carry the same meaning.
        """
        assert self._credentials_path is not None  # set by _load_config
        path = self._credentials_path
        if os.name == "posix":
            try:
                file_stat = os.stat(path, follow_symlinks=False)
            except FileNotFoundError as err:
                raise AnthropicError(f"Credentials file not found at {path} (profile {self._profile!r}).") from err
            except OSError as err:
                raise AnthropicError(f"Credentials file at {path} could not be accessed: {err}") from err
            if stat.S_ISLNK(file_stat.st_mode):
                raise AnthropicError(
                    f"Credentials file at {path} is a symlink; refusing to follow "
                    f"(move the real file into place to keep secret material on the expected filesystem)."
                )
            mode = stat.S_IMODE(file_stat.st_mode)
            if mode & 0o004:
                raise AnthropicError(
                    f"Credentials file at {path} is world-readable (mode {mode:#o}); "
                    f"run `chmod 600 {path}` before retrying."
                )
            if mode & 0o070:
                log.warning(
                    "Credentials file at %s is group-readable (mode %#o); consider `chmod 600 %s`.",
                    path,
                    mode,
                    path,
                )
        try:
            raw = path.read_text(encoding="utf-8")
        except FileNotFoundError as err:
            raise AnthropicError(f"Credentials file not found at {path} (profile {self._profile!r}).") from err
        except (OSError, UnicodeDecodeError) as err:
            raise AnthropicError(f"Credentials file at {path} could not be read: {err}") from err
        try:
            creds: Dict[str, Any] = json.loads(raw)
        except json.JSONDecodeError as err:
            raise AnthropicError(f"Credentials file at {path} is not valid JSON: {err}") from err

        # Validate discriminator if present; lenient if absent so hand-written
        # or older files keep working. Catches config/credentials drift early.
        actual = creds.get("type")
        if actual is not None and actual != CREDENTIALS_FILE_TYPE:
            assert self._config is not None  # _load_config always precedes _read_credentials
            auth_type = self._config["authentication"].get("type")
            raise AnthropicError(
                f"credentials file has type {actual!r}; expected {CREDENTIALS_FILE_TYPE!r} "
                f"for authentication.type {auth_type!r}"
            )
        return creds

    def _get_http_client(self) -> httpx.Client:
        """Return an ``httpx.Client``, lazily creating (and tracking) one we own."""
        if self._http_client is not None:
            return self._http_client
        if self._owned_http_client is None:
            self._owned_http_client = httpx.Client(timeout=TOKEN_EXCHANGE_TIMEOUT)
        return self._owned_http_client

    def close(self) -> None:
        """Close the owned ``httpx.Client`` if we created one."""
        if self._owned_http_client is not None:
            self._owned_http_client.close()
            self._owned_http_client = None
        if self._workload_delegate is not None:
            self._workload_delegate.close()

    def reload(self) -> None:
        """Drop the cached config so the next call re-reads it from disk.

        ``CredentialsFile`` caches the parsed config across calls to keep the
        hot path cheap; a daemon that rotates a profile in place (e.g. flips
        ``"type": "user_oauth"`` to ``"type": "oidc_federation"``) will not be
        picked up automatically. Callers that need to react to such changes
        can call ``reload()`` to force a fresh read on the next ``__call__``.
        """
        self._config = None
        self._workload_delegate = None

    def _atomic_write_credentials(self, data: Dict[str, Any]) -> None:
        """Atomic write to the credentials file (NOT the config file)."""
        assert self._credentials_path is not None
        parent = self._credentials_path.parent
        parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        # mkstemp gives a unique temp name so concurrent writers (e.g.
        # gunicorn workers cold-starting together) don't race on a fixed
        # ``.tmp`` path; whichever os.replace lands last wins, which is fine
        # for a best-effort cache.
        fd, tmp = tempfile.mkstemp(dir=parent, prefix=f".{self._credentials_path.name}.", suffix=".tmp")
        try:
            try:
                os.fchmod(fd, 0o600)
                os.write(fd, json.dumps(data, indent=2).encode("utf-8"))
                os.fsync(fd)
            finally:
                os.close(fd)
            os.replace(tmp, self._credentials_path)
        except BaseException:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise
        # fsync the parent directory so the rename itself survives a crash on
        # filesystems that defer directory-entry writes. Best-effort: Windows
        # and some POSIX flavours don't support directory fds.
        try:
            dir_fd = os.open(parent, os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError:
            pass

    # -- dispatch ----------------------------------------------------------

    def _auth_block(self) -> Dict[str, Any]:
        """Return the cached ``authentication`` sub-object from the config file."""
        config = self._load_config()
        return cast("Dict[str, Any]", config["authentication"])

    def __call__(self, *, force_refresh: bool = False) -> AccessToken:
        auth = self._auth_block()
        auth_type = auth.get("type")

        if auth_type == AUTH_TYPE_OIDC_FEDERATION:
            return self._call_oidc_federation(auth, force_refresh=force_refresh)

        if auth_type == AUTH_TYPE_USER_OAUTH:
            return self._call_user_oauth(auth, force_refresh=force_refresh)

        raise AnthropicError(
            f"Unknown authentication.type {auth_type!r} at {self._config_path}. "
            f"Expected {AUTH_TYPE_OIDC_FEDERATION!r} or {AUTH_TYPE_USER_OAUTH!r}."
        )

    # -- "user_oauth" -----------------------------------------------------

    def _call_user_oauth(self, auth: Dict[str, Any], *, force_refresh: bool = False) -> AccessToken:
        """Interactive-login profile. With a ``client_id`` in the auth block,
        we run the refresh_token grant on expiry; without one, we treat the
        credentials file as externally rotated and just read it fresh.
        """
        from ._workload import WorkloadIdentityError, _raise_token_endpoint_error

        creds = self._read_credentials()
        access_token = creds.get("access_token")
        if not access_token:
            raise AnthropicError(f"Credentials file at {self._credentials_path} is missing 'access_token'.")

        client_id = auth.get("client_id")
        if not client_id:
            # No client_id → externally rotated. Return whatever the file has;
            # a sidecar/daemon is responsible for keeping it fresh.
            expires_at = _coerce_expires_at(creds.get("expires_at"), self._credentials_path)
            return AccessToken(token=access_token, expires_at=expires_at)

        refresh_token = creds.get("refresh_token")
        if not refresh_token:
            raise WorkloadIdentityError(
                f"credentials file for profile {self._profile!r} (authentication.type "
                f"{AUTH_TYPE_USER_OAUTH!r} with client_id) must include 'refresh_token': "
                f"{self._credentials_path}"
            )

        # Strict expiry only — TokenCache owns the advisory/mandatory refresh
        # policy. A second threshold here could trigger a refresh grant while
        # the outer cache is still serving fine.
        # force_refresh (set by TokenCache.invalidate after a 401) bypasses
        # the disk-freshness short-circuit so a revoked token isn't re-served.
        expires_at = _coerce_expires_at(creds.get("expires_at"), self._credentials_path)
        if not force_refresh and expires_at is not None and time.time() < expires_at:
            return AccessToken(token=access_token, expires_at=expires_at)

        body: Dict[str, str] = {
            "grant_type": GRANT_TYPE_REFRESH_TOKEN,
            "refresh_token": refresh_token,
            "client_id": client_id,
        }

        try:
            resp = self._get_http_client().post(
                f"{self._base_url}{TOKEN_ENDPOINT}",
                json=body,
                headers={
                    "Content-Type": "application/json",
                    # oauth-2025-04-20 unlocks the token endpoint family. Do
                    # NOT send oidc-federation-2026-04-01 — that's a routing
                    # switch that misroutes refresh_token grants to the Go
                    # userauth handler, which only accepts jwt-bearer.
                    "anthropic-beta": OAUTH_API_BETA_HEADER,
                    "User-Agent": _user_agent(),
                },
            )
        except httpx.HTTPError as err:
            raise WorkloadIdentityError(f"user_oauth refresh failed to reach token endpoint: {err}") from err

        if resp.status_code != 200:
            _raise_token_endpoint_error(resp, message_prefix="user_oauth refresh failed")

        payload: Dict[str, Any] = resp.json()
        new_access = payload.get("access_token")
        if not new_access:
            raise WorkloadIdentityError("user_oauth refresh response missing 'access_token'")
        raw_expires_in = payload.get("expires_in", 3600)
        try:
            expires_in = int(raw_expires_in)
        except (TypeError, ValueError) as err:
            raise WorkloadIdentityError(
                f"user_oauth refresh response has invalid 'expires_in' {raw_expires_in!r}; "
                f"expected an integer number of seconds."
            ) from err
        new_expires_at = int(time.time()) + expires_in
        new_refresh = payload.get("refresh_token") or refresh_token

        creds["version"] = CREDENTIALS_FILE_VERSION
        creds["type"] = CREDENTIALS_FILE_TYPE
        creds["access_token"] = new_access
        creds["expires_at"] = new_expires_at
        creds["refresh_token"] = new_refresh
        self._atomic_write_credentials(creds)

        return AccessToken(token=new_access, expires_at=new_expires_at)

    # -- "oidc_federation" ------------------------------------------------

    def _read_credentials_if_exists(self) -> Optional[Dict[str, Any]]:
        """``_read_credentials`` variant that returns ``None`` on absence
        instead of raising — used by the federation disk-cache path where a
        missing credentials file just means "exchange now".
        """
        assert self._credentials_path is not None
        if not self._credentials_path.exists():
            return None
        try:
            return self._read_credentials()
        except AnthropicError as err:
            if isinstance(err.__cause__, FileNotFoundError):
                return None
            raise

    def _call_oidc_federation(self, auth: Dict[str, Any], *, force_refresh: bool = False) -> AccessToken:
        if self._workload_delegate is None:
            self._workload_delegate = self._build_workload_delegate(auth)

        # Disk cache: if a prior exchange wrote credentials/<profile>.json and
        # the token there is unexpired, return it instead of re-exchanging.
        # The in-memory TokenCache layer applies the proactive 120s/30s policy
        # on top of this; the disk cache only matters across process restarts.
        # ``_credentials_path`` is always set for ``CredentialsFile`` proper
        # (``_load_config`` defaults it); subclasses (``InMemoryConfig``)
        # leave it ``None`` to opt out of the disk cache entirely.
        if self._credentials_path is None:
            return self._workload_delegate()

        # force_refresh (set by TokenCache.invalidate after a 401) bypasses
        # the disk-cache short-circuit so a revoked token isn't re-served.
        cached = self._read_credentials_if_exists()
        if not force_refresh and cached is not None:
            access_token = cached.get("access_token")
            expires_at = cached.get("expires_at")
            try:
                if (
                    access_token
                    and expires_at is not None
                    and time.time() < float(expires_at) - MANDATORY_REFRESH_SECONDS
                ):
                    return AccessToken(token=str(access_token), expires_at=int(expires_at))
            except (TypeError, ValueError):
                # corrupted expires_at — fall through to re-exchange and overwrite
                pass

        token = self._workload_delegate()
        try:
            self._atomic_write_credentials(
                {
                    **(cached or {}),
                    "version": CREDENTIALS_FILE_VERSION,
                    "type": CREDENTIALS_FILE_TYPE,
                    "access_token": token.token,
                    "expires_at": token.expires_at,
                }
            )
        except OSError as err:
            log.debug("federation token disk-cache write-back failed (best-effort): %s", err)
        return token

    def _build_workload_delegate(self, auth: Dict[str, Any]) -> WorkloadIdentityCredentials:
        # Import here to avoid a circular import (_workload imports nothing from
        # _providers so the dependency is one-way at runtime).
        from ._workload import WorkloadIdentityError, WorkloadIdentityCredentials

        federation_rule_id = auth.get("federation_rule_id")
        assert self._config is not None  # _load_config precedes dispatch
        organization_id = self._config.get("organization_id")
        if not federation_rule_id or not organization_id:
            raise WorkloadIdentityError(
                f"config file with authentication.type {AUTH_TYPE_OIDC_FEDERATION!r} must include "
                f"'authentication.federation_rule_id' and top-level 'organization_id': "
                f"{self._config_path}"
            )

        # identity_token is a discriminated object so future variants (url,
        # executable, aws_sigv4) slot in without renaming. v1 implements
        # source:"file" only. Absent → fall back to ANTHROPIC_IDENTITY_TOKEN_FILE.
        identity_token_cfg = auth.get("identity_token")
        if identity_token_cfg is not None:
            source = identity_token_cfg.get("source")
            if source != "file":
                raise AnthropicError(f"identity_token source {source!r} is not supported; only 'file' is implemented")
            identity_token_path = identity_token_cfg.get("path")
            if not identity_token_path:
                # Empty/missing path is a config bug, not an env-var fallback
                # signal — the source explicitly says "file", which has no
                # meaning without a path. Without this check we'd silently
                # fall through to ANTHROPIC_IDENTITY_TOKEN_FILE and override
                # user intent.
                raise AnthropicError(
                    f"identity_token source 'file' requires a non-empty path; "
                    f"profile {self._profile!r} at {self._config_path} has identity_token={identity_token_cfg!r}."
                )
        else:
            identity_token_path = None
        provider = IdentityTokenFile(identity_token_path) if identity_token_path else IdentityTokenFile()

        # The delegate borrows our owned httpx.Client: passing http_client=
        # sets _owns_http_client=False on the delegate so its close() is a
        # no-op. CredentialsFile.close() remains the single closer.
        delegate = WorkloadIdentityCredentials(
            identity_token_provider=provider,
            federation_rule_id=federation_rule_id,
            organization_id=organization_id,
            service_account_id=auth.get("service_account_id"),
            workspace_id=self._config.get("workspace_id"),
            scope=auth.get("scope"),
            http_client=self._get_http_client(),
        )
        delegate.bind_base_url(self._base_url)
        return delegate


class IdentityTokenFile:
    """An :class:`IdentityTokenProvider` that reads a JWT from a file on every call.

    Kubernetes projected service-account tokens (and similar) are rotated in place,
    so the file MUST be re-read on every invocation rather than cached.
    """

    def __init__(self, path: Union[str, "os.PathLike[str]", None] = None) -> None:
        resolved = resolve_identity_token_path(path)
        if resolved is None:
            raise AnthropicError(
                f"No identity token file path given. Pass `path=` or set the {ENV_IDENTITY_TOKEN_FILE} "
                f"environment variable."
            )
        self._path = resolved

    @property
    def path(self) -> pathlib.Path:
        return self._path

    def __call__(self) -> str:
        try:
            content = self._path.read_text(encoding="utf-8").strip()
        except FileNotFoundError as err:
            raise AnthropicError(f"Identity token file not found at {self._path}.") from err
        except PermissionError as err:
            raise AnthropicError(
                f"Identity token file at {self._path} is not readable by this process: {err}. "
                f"Check the file mode and the effective uid of the process."
            ) from err
        except IsADirectoryError as err:
            raise AnthropicError(
                f"Identity token path {self._path} is a directory, not a file. "
                f"Point at the projected token file itself."
            ) from err
        except (OSError, UnicodeDecodeError) as err:
            raise AnthropicError(f"Identity token file at {self._path} could not be read: {err}") from err
        if not content:
            raise AnthropicError(
                f"Identity token file at {self._path} is empty. "
                f"If this is a Kubernetes projected service-account token, check the "
                f"volume mount and the serviceAccountToken projection audience."
            )
        return content


class InMemoryConfig(CredentialsFile):
    """An :class:`AccessTokenProvider` driven by an in-memory config dict
    (same shape as ``configs/<profile>.json``) rather than files on disk.

    Intended for callers that want to construct an :class:`anthropic.Anthropic`
    client with a fully programmatic credentials setup — equivalent to the Go
    SDK's ``option.WithConfig`` / TypeScript SDK's ``ClientOptions.config``.

    Both ``authentication.type`` discriminator values are supported:

    ``"oidc_federation"``
        ``authentication.credentials_path`` is **optional**. If set, exchanged
        tokens are cached to / read from that file (same atomic 0600 write as
        :class:`CredentialsFile`). If omitted, every call performs a fresh
        jwt-bearer exchange with no on-disk cache.

    ``"user_oauth"``
        ``authentication.credentials_path`` is **required** — it is where the
        access/refresh tokens live. Behaviour is identical to a file-backed
        :class:`CredentialsFile` profile of the same shape.

    The implementation subclasses :class:`CredentialsFile` so the dispatch,
    refresh-grant, disk-cache and atomic-write logic are shared verbatim;
    only config loading and identity-token resolution are overridden.
    """

    _IN_MEMORY_PATH = pathlib.Path("<in-memory config>")

    def __init__(
        self,
        config: Dict[str, Any],
        *,
        identity_token_provider: Optional[IdentityTokenProvider] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        raw_auth = config.get("authentication")
        if not isinstance(raw_auth, dict):
            raise AnthropicError(
                "config dict is missing the 'authentication' object. "
                f'Expected shape: {{"authentication": {{"type": "{AUTH_TYPE_OIDC_FEDERATION}"'
                f'|"{AUTH_TYPE_USER_OAUTH}", ...}}, ...}}'
            )
        auth = cast("Dict[str, Any]", raw_auth)
        auth_type = auth.get("type")
        if auth_type not in (AUTH_TYPE_OIDC_FEDERATION, AUTH_TYPE_USER_OAUTH):
            raise AnthropicError(
                f"Unknown authentication.type {auth_type!r}. "
                f"Expected {AUTH_TYPE_OIDC_FEDERATION!r} or {AUTH_TYPE_USER_OAUTH!r}."
            )

        credentials_path = auth.get("credentials_path")
        if auth_type == AUTH_TYPE_USER_OAUTH and not credentials_path:
            raise AnthropicError(
                f"authentication.type {AUTH_TYPE_USER_OAUTH!r} requires "
                f"'authentication.credentials_path' (where the access/refresh tokens live). "
                f"For profile-based resolution, use CredentialsFile instead."
            )

        # CredentialsFile state — set directly rather than calling super().__init__()
        # because the parent constructor reads env/disk for profile resolution.
        self._profile = "<in-memory>"
        self._config_path = self._IN_MEMORY_PATH
        self._bound_base_url: Optional[str] = None
        self._http_client = http_client
        self._owned_http_client: Optional[httpx.Client] = None
        self._workload_delegate: Optional[WorkloadIdentityCredentials] = None
        self._identity_token_provider_override = identity_token_provider

        self._config = config
        self._credentials_path = pathlib.Path(str(credentials_path)).expanduser() if credentials_path else None
        self._base_url = self._resolve_base_url(config)
        _require_https(self._base_url, field="config: base_url")

    @override
    def _load_config(self) -> Dict[str, Any]:
        assert self._config is not None
        return self._config

    @override
    def reload(self) -> None:
        # Config is fixed at construction; only drop the workload delegate so
        # a re-exchange picks up rotated identity-token state.
        self._workload_delegate = None

    @override
    def _build_workload_delegate(self, auth: Dict[str, Any]) -> WorkloadIdentityCredentials:
        if self._identity_token_provider_override is None:
            return super()._build_workload_delegate(auth)

        from ._workload import WorkloadIdentityError, WorkloadIdentityCredentials

        federation_rule_id = auth.get("federation_rule_id")
        assert self._config is not None
        organization_id = self._config.get("organization_id")
        if not federation_rule_id or not organization_id:
            raise WorkloadIdentityError(
                f"config dict with authentication.type {AUTH_TYPE_OIDC_FEDERATION!r} must include "
                f"'authentication.federation_rule_id' and top-level 'organization_id'"
            )
        delegate = WorkloadIdentityCredentials(
            identity_token_provider=self._identity_token_provider_override,
            federation_rule_id=federation_rule_id,
            organization_id=organization_id,
            service_account_id=auth.get("service_account_id"),
            workspace_id=self._config.get("workspace_id"),
            scope=auth.get("scope"),
            http_client=self._get_http_client(),
        )
        delegate.bind_base_url(self._base_url)
        return delegate
