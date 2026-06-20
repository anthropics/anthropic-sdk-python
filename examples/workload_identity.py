#!/usr/bin/env python3
"""
Workload Identity Federation & Credential Providers — comprehensive examples.

The Anthropic client resolves auth in this precedence order:
  1. Constructor args: api_key=, auth_token=, or credentials=
  2. Env vars: ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, then the credential chain below
  3. Standard defaults: ~/.config/anthropic/credentials.json if it exists

The `credentials=` arg accepts any AccessTokenProvider — a zero-arg callable returning
AccessToken(token, expires_at). The client caches the token and proactively refreshes
it (120s advisory / 30s mandatory before expiry).
"""

import os

import anthropic
from anthropic import (
    AccessToken,
    StaticToken,
    CredentialsFile,
    IdentityTokenFile,
    WorkloadIdentityCredentials,
)

# =============================================================================
# Section 1: Zero-config (recommended for production workloads)
# =============================================================================
# Just construct the client. Auth is resolved from the environment.
#
# For Kubernetes / GitHub Actions / etc., set these env vars on the workload:
#   ANTHROPIC_IDENTITY_TOKEN_FILE=/var/run/secrets/kubernetes.io/serviceaccount/token
#   ANTHROPIC_FEDERATION_RULE_ID=fdrl_01...
#   ANTHROPIC_ORGANIZATION_ID=00000000-0000-0000-0000-000000000000
#   ANTHROPIC_SERVICE_ACCOUNT_ID=svac_01...   (optional)
#
# Or, if a sidecar/daemon writes a profile config + credentials file:
#   ANTHROPIC_PROFILE=my-profile     (picks ~/.config/anthropic/configs/my-profile.json
#                                     and ~/.config/anthropic/credentials/my-profile.json)
#   ANTHROPIC_CONFIG_DIR=/etc/anthropic   (relocates the root; optional)
#
# Or, the existing env vars still work:
#   ANTHROPIC_API_KEY=sk-ant-...
#   ANTHROPIC_AUTH_TOKEN=sk-ant-oat01-...

client = anthropic.Anthropic()


# =============================================================================
# Section 2: Explicit credentials= via constructor
# =============================================================================

# --- 2a. WorkloadIdentityCredentials: exchange an external OIDC JWT --------

# JWT source option i: read from a file (re-read on every refresh — handles k8s rotation)
client = anthropic.Anthropic(
    credentials=WorkloadIdentityCredentials(
        identity_token_provider=IdentityTokenFile(
            "/var/run/secrets/kubernetes.io/serviceaccount/token",
        ),
        federation_rule_id="fdrl_01...",
        organization_id="00000000-0000-0000-0000-000000000000",
        service_account_id="svac_01...",
    ),
)

# JWT source option ii: from an env var (CI systems that inject the token directly)
client = anthropic.Anthropic(
    credentials=WorkloadIdentityCredentials(
        identity_token_provider=lambda: os.environ["ANTHROPIC_IDENTITY_TOKEN"],
        federation_rule_id="fdrl_01...",
        organization_id="00000000-0000-0000-0000-000000000000",
    ),
)


# JWT source option iii: custom callable (secrets manager, internal token service, etc.)
def fetch_jwt_from_vault() -> str:
    # your logic here
    return ""


client = anthropic.Anthropic(
    credentials=WorkloadIdentityCredentials(
        identity_token_provider=fetch_jwt_from_vault,
        federation_rule_id="fdrl_01...",
        organization_id="00000000-0000-0000-0000-000000000000",
    ),
)

# --- 2b. CredentialsFile: read auth config from a named profile on disk ----
#
# Profiles live under the config directory (default ~/.config/anthropic/,
# override with ANTHROPIC_CONFIG_DIR) as a pair of files:
#
#   configs/<profile>.json       — non-secret. Shape:
#
#     {
#       "authentication": {"type": "oidc_federation"|"user_oauth", ...},
#       "organization_id": "00000000-0000-0000-0000-000000000000",
#       "workspace_id": "wrkspc_01...",
#       "base_url": "https://api.anthropic.com"
#     }
#
#   The "authentication" object is a tagged union discriminated on "type":
#
#     {"type": "oidc_federation",
#      "federation_rule_id": "fdrl_...",
#      "service_account_id": "svac_...",
#      "identity_token": {"source": "file", "path": "..."}}
#       → SDK performs the jwt-bearer exchange itself. If "identity_token"
#         is omitted, ANTHROPIC_IDENTITY_TOKEN_FILE is used instead.
#         organization_id is read from the top level of the config.
#
#     {"type": "user_oauth", "client_id": "..."}
#       → interactive PKCE login with refresh_token rotation. On access-token
#         expiry the SDK performs a refresh_token grant against
#         /v1/oauth/token and writes the new tokens back to
#         credentials/<profile>.json (atomic replace).
#
#     {"type": "user_oauth"}  (no client_id)
#       → credentials file is externally rotated by a sidecar/daemon. The
#         SDK re-reads the file on every refresh and returns whatever
#         access_token is there; no refresh grant is attempted.
#
#   credentials/<profile>.json   — secret (0600). Holds access_token,
#                                  expires_at, and (for user_oauth with
#                                  a client_id) refresh_token.

# Point at a specific profile name:
client = anthropic.Anthropic(credentials=CredentialsFile(profile="production"))
# Or resolve the profile from ANTHROPIC_PROFILE / <config_dir>/active_config / "default":
client = anthropic.Anthropic(credentials=CredentialsFile())

# --- 2c. StaticToken: you already have a bearer token ---------------------
client = anthropic.Anthropic(credentials=StaticToken("sk-ant-oat01-..."))
# (equivalent to anthropic.Anthropic(auth_token="sk-ant-oat01-..."))


# --- 2d. Custom AccessTokenProvider ---------------------------------------
# Any callable matching AccessTokenProvider works. The optional `force_refresh`
# kwarg is set after a 401 retry; providers without a cache can ignore it.
def my_provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
    # call your internal auth service here
    return AccessToken(token="sk-ant-oat01-...", expires_at=1775000000)


client = anthropic.Anthropic(credentials=my_provider)

# =============================================================================
# Section 3: Precedence demonstration
# =============================================================================
# Constructor args always win over env vars, which win over default file paths.
# Within constructor args, passing more than one of api_key/auth_token/credentials
# is supported but credentials takes the Bearer slot (api_key still sends X-Api-Key
# if both are set — generally don't do this).

# =============================================================================
# Section 4: Async
# =============================================================================


async def main() -> None:
    aclient = anthropic.AsyncAnthropic(
        credentials=WorkloadIdentityCredentials(
            identity_token_provider=IdentityTokenFile(),  # uses ANTHROPIC_IDENTITY_TOKEN_FILE
            federation_rule_id="fdrl_01...",
            organization_id="00000000-0000-0000-0000-000000000000",
        ),
    )
    msg = await aclient.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
    )
    print(msg)


# asyncio.run(main())
