from __future__ import annotations

import json
from typing import Any, Dict, Optional, cast

from pydantic import SecretStr

__all__ = [
    "SecretStr",
    "_NonObjectPayloadError",
    "_wrap_secret_fields",
    "_unwrap_secret",
    "_json_dumps_secrets",
    "_strip_traceback",
]


class _NonObjectPayloadError(TypeError):
    """Raised by :func:`_wrap_secret_fields` for JSON payloads that are not
    objects. Carries only the payload's type name — a non-object payload can
    be an echo of the request (assertion included), so it must never bind in
    a caller's frame or ride along in an exception.
    """

    def __init__(self, type_name: str) -> None:
        super().__init__(f"expected a JSON object, got {type_name}")
        self.type_name = type_name


# Top-level keys that are plumbing, not secrets, in the credentials file and
# in token-endpoint responses. Every OTHER string value is treated as secret
# by default, so new fields (id_token, client_secret, ...) are wrapped without
# anyone having to remember to list them.
_PLAIN_KEYS = frozenset(
    (
        # credentials file
        "type",
        "version",
        "expires_at",
        # RFC 6749 token / error response
        "token_type",
        "expires_in",
        "scope",
        "error",
        "error_description",
        "error_uri",
    )
)


def _wrap_secret_fields(payload: Any) -> Dict[str, Any]:
    """Wrap the secret fields of a parsed JSON object in ``SecretStr``.

    Called at every boundary where credential material enters SDK code.
    Traceback frames retain their locals, so any dict a raise site (or a
    frame an error merely propagates through) still holds must already be
    redacted — ``SecretStr`` renders as ``SecretStr('**********')`` under
    crash reporters that capture and render locals.

    String values are secret unless their key is in ``_PLAIN_KEYS``; wrapped
    empty strings stay falsy (``SecretStr`` defines ``__len__`` across the
    supported pydantic range), so ``if not creds.get("access_token")`` checks
    behave unchanged. Only top-level values are wrapped — the credential
    formats are flat; revisit if a nested shape ever appears. Mutates
    ``payload`` in place — a copy would leave the raw-valued original
    reachable — and returns it.

    Non-object payloads raise :class:`_NonObjectPayloadError` from this frame,
    with the payload unbound first, so the raw value never lands in any frame
    of the traceback — callers translate to their own redacted error.
    """
    if not isinstance(payload, dict):
        type_name = type(payload).__name__
        del payload
        raise _NonObjectPayloadError(type_name)
    mapping = cast("Dict[str, Any]", payload)
    for key in mapping:
        if key not in _PLAIN_KEYS and isinstance(mapping.get(key), str):
            mapping[key] = SecretStr(mapping[key])
    return mapping


def _unwrap_secret(value: Any) -> Any:
    """Inverse of :func:`_wrap_secret_fields` for a single value; pass-through
    for values that were never wrapped (absent or non-string fields)."""
    return value.get_secret_value() if isinstance(value, SecretStr) else value


def _json_default(value: Any) -> Any:
    if isinstance(value, SecretStr):
        return value.get_secret_value()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _json_dumps_secrets(payload: Any, *, indent: Optional[int] = None) -> bytes:
    """``json.dumps`` with ``SecretStr`` values unwrapped at dump time.

    Returns bytes so call sites can pass the result inline (request content,
    ``os.write``) without binding the raw serialization to a local.
    """
    return json.dumps(payload, indent=indent, default=_json_default).encode("utf-8")


def _strip_traceback(err: BaseException) -> BaseException:
    """Detach the frames chained onto ``err`` before raising from it.

    Foreign frames (json decoder, httpx transport) hold raw payloads —
    request bodies, response text, credentials-file contents — as locals.
    Dropping the traceback removes them from every renderer and programmatic
    chain-walker, while the cause's type and message (which never carry the
    payload) stay visible in renderings.
    """
    err.__traceback__ = None
    return err
