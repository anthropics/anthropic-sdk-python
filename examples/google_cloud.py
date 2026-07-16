# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "anthropic[google_cloud]",
# ]
#
# [tool.uv.sources]
# anthropic = { path = "../", editable = true }
# ///

# Claude Platform on Google Cloud — the first-party Anthropic API served through Google's
# gateway. Authentication uses your Google credentials (Application Default
# Credentials by default), so run `gcloud auth application-default login` first.
#
# Configure via arguments or environment variables:
#   ANTHROPIC_GOOGLE_CLOUD_PROJECT   GCP consumer project id
#   ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID Anthropic workspace id (wrkspc_...)
#   ANTHROPIC_GOOGLE_CLOUD_LOCATION     override the GCP location (defaults to "global")
#   ANTHROPIC_GOOGLE_CLOUD_BASE_URL     override the derived gateway URL

from anthropic import AnthropicGoogleCloud

client = AnthropicGoogleCloud(
    project="your-gcp-project",  # or ANTHROPIC_GOOGLE_CLOUD_PROJECT
    workspace_id="wrkspc_...",  # or ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID
    # `location` is optional and defaults to "global".
    # Credentials default to ADC; pass `token_provider=...`, `credentials=...`, or
    # `access_token=...` to override.
)

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)

print(message.to_json())
