from __future__ import annotations

import os
from typing import Optional

from ._types import CredentialResult, IdentityTokenProvider
from ._workload import WorkloadIdentityCredentials
from ._constants import (
    ENV_SCOPE,
    ENV_API_KEY,
    ENV_PROFILE,
    ENV_AUTH_TOKEN,
    ENV_CONFIG_DIR,
    ENV_WORKSPACE_ID,
    ENV_IDENTITY_TOKEN,
    ENV_ORGANIZATION_ID,
    ENV_FEDERATION_RULE_ID,
    ENV_SERVICE_ACCOUNT_ID,
    _has_active_profile_config,
    _has_explicit_active_config,
    resolve_identity_token_path,
)
from ._providers import StaticToken, CredentialsFile, IdentityTokenFile
from ..._exceptions import AnthropicError

__all__ = ["default_credentials"]


def _build_federation_result(*, base_url: str) -> Optional[CredentialResult]:
    """Build a :class:`CredentialResult` for the env-var federation path
    (step 4 in the precedence spec). Returns ``None`` if the required trio
    isn't fully set."""
    federation_rule_id = os.environ.get(ENV_FEDERATION_RULE_ID)
    organization_id = os.environ.get(ENV_ORGANIZATION_ID)
    has_literal_token = ENV_IDENTITY_TOKEN in os.environ
    identity_token_path = resolve_identity_token_path()

    if not federation_rule_id or not organization_id:
        return None
    if not has_literal_token and identity_token_path is None:
        return None

    identity_provider: IdentityTokenProvider
    if identity_token_path is not None:
        identity_provider = IdentityTokenFile(identity_token_path)
    else:
        # Read the env var on every call so a rotated value is picked up
        # at the next token exchange (don't capture into a closure).
        def _read_env_token() -> str:
            value = os.environ.get(ENV_IDENTITY_TOKEN)
            if value is None:
                raise AnthropicError(
                    f"{ENV_IDENTITY_TOKEN} is not set; the workload-identity chain "
                    f"selected this provider at construction time but the env var "
                    f"is no longer present."
                )
            return value

        identity_provider = _read_env_token

    provider = WorkloadIdentityCredentials(
        identity_token_provider=identity_provider,
        federation_rule_id=federation_rule_id,
        organization_id=organization_id,
        service_account_id=os.environ.get(ENV_SERVICE_ACCOUNT_ID),
        # Coerce empty string to None so a defaulted-but-empty CI variable
        # doesn't put ``"workspace_id": ""`` on the wire — matches the falsy
        # skip in :func:`._providers._fill_missing_from_env`.
        workspace_id=os.environ.get(ENV_WORKSPACE_ID) or None,
        scope=os.environ.get(ENV_SCOPE),
    )
    provider.bind_base_url(base_url)
    return CredentialResult(provider=provider)


def default_credentials(*, base_url: str = "https://api.anthropic.com") -> Optional[CredentialResult]:
    """Resolve a :class:`CredentialResult` from the environment per the
    credential-resolution spec. First match wins.

    Implements steps 2-5 of the spec precedence chain (step 1 is handled at
    the client constructor level, above this function):

    Step 2a: ``ANTHROPIC_API_KEY`` → return ``None`` so the client uses its
             existing ``X-Api-Key`` header path. (API keys are not Bearer
             tokens, so they can't flow through this chain.)
    Step 2b: ``ANTHROPIC_AUTH_TOKEN`` → :class:`StaticToken` (Bearer).
    Step 3:  ``ANTHROPIC_PROFILE`` / ``ANTHROPIC_CONFIG_DIR`` set, or the
             ``active_config`` pointer file exists → load that profile.
             This is *explicit profile selection*; failures propagate.
    Step 4:  ``ANTHROPIC_FEDERATION_RULE_ID`` + ``ANTHROPIC_ORGANIZATION_ID``
             + ``ANTHROPIC_IDENTITY_TOKEN[_FILE]`` → direct jwt-bearer
             exchange via :class:`WorkloadIdentityCredentials`. Critically,
             step 4 sits **between** explicit profile (step 3) and
             fallback profile (step 5): a machine with WIF env vars wired
             up must use WIF even if a leftover ``default`` profile exists
             on disk, but a user who explicitly ``ANTHROPIC_PROFILE=dev``
             still gets their profile.
    Step 5:  Fallback active profile from disk (``configs/default.json``
             or whatever ``active_config`` points at). Errors at this step
             are swallowed and the chain falls through — a corrupt
             unselected profile shouldn't break an otherwise-explicit
             api_key= path.

    Returns ``None`` when nothing matches — the client will fall back to
    its normal "no auth configured" error.
    """
    # Step 2a — env api_key: return None so the base client handles X-Api-Key.
    if os.environ.get(ENV_API_KEY):
        return None

    # Step 2b — env auth_token: static bearer.
    auth_token = os.environ.get(ENV_AUTH_TOKEN)
    if auth_token:
        return CredentialResult(provider=StaticToken(auth_token))

    # Step 3 — explicit profile selection (ANTHROPIC_PROFILE / ANTHROPIC_CONFIG_DIR
    # / active_config pointer). Failures propagate — a user who explicitly
    # names a profile expects a broken config to surface, not to fall through.
    env_explicit = bool(os.environ.get(ENV_PROFILE) or os.environ.get(ENV_CONFIG_DIR))
    pointer_explicit = _has_explicit_active_config()
    if env_explicit or pointer_explicit:
        creds_file = CredentialsFile()
        creds_file.bind_base_url(base_url)
        extra_headers = creds_file.extra_headers()
        return CredentialResult(
            provider=creds_file,
            extra_headers=extra_headers,
            base_url=creds_file.resolved_base_url,
        )

    # Step 4 — env-var workload identity federation. Sits above the
    # fallback on-disk profile so a machine with WIF env vars uses WIF
    # even if a leftover ``default`` profile exists on disk.
    federation_result = _build_federation_result(base_url=base_url)
    if federation_result is not None:
        return federation_result

    # Step 5 — fallback active profile from disk. Errors are swallowed and
    # the chain falls through because the user didn't explicitly select
    # this profile; a corrupt auto-discovered config shouldn't break
    # construction.
    if _has_active_profile_config():
        creds_file = CredentialsFile()
        creds_file.bind_base_url(base_url)
        try:
            extra_headers = creds_file.extra_headers()
        except AnthropicError:
            return None
        return CredentialResult(
            provider=creds_file,
            extra_headers=extra_headers,
            base_url=creds_file.resolved_base_url,
        )

    return None
