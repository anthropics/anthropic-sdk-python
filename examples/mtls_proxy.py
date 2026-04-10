from __future__ import annotations

import ssl

import httpx

from anthropic import Anthropic

# Configure these paths for your environment.
CLIENT_CERT_PATH = "./client-cert.pem"
CLIENT_KEY_PATH = "./client-key.pem"
CORPORATE_CA_BUNDLE_PATH = "./corp-ca.pem"
API_BASE_URL = "https://anthropic-proxy.example.com"

ssl_context = ssl.create_default_context(cafile=CORPORATE_CA_BUNDLE_PATH)
ssl_context.load_cert_chain(certfile=CLIENT_CERT_PATH, keyfile=CLIENT_KEY_PATH)

http_client = httpx.Client(verify=ssl_context)
client = Anthropic(base_url=API_BASE_URL, http_client=http_client)

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=256,
    messages=[{"role": "user", "content": "Say hello from behind an mTLS proxy."}],
)

print(message.content)
