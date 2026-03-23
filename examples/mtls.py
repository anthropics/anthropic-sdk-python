# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "anthropic",
# ]
#
# [tool.uv.sources]
# anthropic = { path = "../", editable = true }
# ///
"""Configure the SDK for mTLS client certificates or corporate proxy CA bundles.

Enterprise environments often require mutual TLS (mTLS) for per-user attribution
through API gateways, or custom CA bundles for corporate TLS inspection proxies
(Zscaler, Netskope, etc.). This example shows how to configure both using the
SDK's existing http_client parameter.
"""

import ssl
import asyncio

from anthropic import Anthropic, AsyncAnthropic, DefaultHttpxClient, DefaultAsyncHttpxClient

# ---------------------------------------------------------------------------
# 1. mTLS client certificate authentication (synchronous)
# ---------------------------------------------------------------------------
# Build an SSL context with both the CA bundle and the client certificate,
# then pass it as verify= to DefaultHttpxClient. This preserves the SDK's
# default connection limits, timeouts, TCP keepalive, and proxy detection.

ctx = ssl.create_default_context()
ctx.load_verify_locations("/path/to/ca-bundle.crt")
ctx.load_cert_chain("/path/to/client.crt", "/path/to/client.key")

sync_client = Anthropic(
    http_client=DefaultHttpxClient(verify=ctx),
)

message = sync_client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello from behind an mTLS proxy!"}],
)
print(message.content)


# ---------------------------------------------------------------------------
# 2. mTLS client certificate authentication (asynchronous)
# ---------------------------------------------------------------------------


async def async_mtls_example() -> None:
    ctx = ssl.create_default_context()
    ctx.load_verify_locations("/path/to/ca-bundle.crt")
    ctx.load_cert_chain("/path/to/client.crt", "/path/to/client.key")

    async_client = AsyncAnthropic(
        http_client=DefaultAsyncHttpxClient(verify=ctx),
    )

    message = await async_client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello from async mTLS!"}],
    )
    print(message.content)


asyncio.run(async_mtls_example())


# ---------------------------------------------------------------------------
# 3. Corporate proxy with custom CA bundle (no client certificate)
# ---------------------------------------------------------------------------
# If your corporate proxy performs TLS inspection (e.g., Zscaler, Netskope),
# you only need to trust the proxy's CA — no client certificate is required.

proxy_client = Anthropic(
    http_client=DefaultHttpxClient(
        verify="/path/to/corporate-ca-bundle.crt",
    ),
)

message = proxy_client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello through the corporate proxy!"}],
)
print(message.content)
