from anthropic import Anthropic
import httpx

# Example: route Anthropic traffic through a corporate gateway that requires
# mutual TLS and a custom CA bundle for TLS interception or private PKI.
#
# Update these paths and URLs for your environment.
http_client = httpx.Client(
    cert=("/path/to/client-cert.pem", "/path/to/client-key.pem"),
    verify="/path/to/corporate-ca-bundle.pem",
    proxy="http://proxy.internal.example.com:8080",
)

client = Anthropic(
    base_url="https://anthropic-gateway.internal.example.com",
    http_client=http_client,
)

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=256,
    messages=[
        {
            "role": "user",
            "content": "Reply with a short greeting.",
        }
    ],
)

print(message.content)
