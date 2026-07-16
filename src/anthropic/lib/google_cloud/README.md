# Claude Platform on Google Cloud

`AnthropicGoogleCloud` is a client for the full Anthropic API — Messages, Models,
Batches, Files, Admin, and every beta surface — served through Google Cloud. You
authenticate with Google Cloud IAM credentials, billing flows through Google
Cloud Marketplace, and model strings are the same first-party identifiers used
with the `Anthropic` client. The deprecated Completions endpoint is not exposed.

This client never reads `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, or
`ANTHROPIC_BASE_URL`; it authenticates with Google credentials only.

> **Note:** the class name and `ANTHROPIC_GOOGLE_CLOUD_*` environment variable
> names are provisional and may change before a stable release.

## Installation

Google auth support is an optional dependency:

```bash
pip install "anthropic[google_cloud]"
```

## Authentication

Precedence (first match wins, unless `skip_auth=True`):

1. `token_provider` — a callable returning a GCP access token, invoked on every
   request (so it can refresh internally). On the async client it may be async or
   return an awaitable; sync providers are run off the event loop.
2. `credentials` — a `google.auth` Credentials object, refreshed as needed.
3. Application Default Credentials — discovered via `google.auth.default()`,
   loaded lazily on the first request and cached for the life of the client. ADC
   covers `gcloud auth application-default login`, `GOOGLE_APPLICATION_CREDENTIALS`,
   workload identity on GKE/Cloud Run, and the GCE/Cloud Functions metadata server.

A `workspace_id` is required unless `skip_auth=True` with an explicit
`base_url`. `skip_auth` is mutually exclusive
with the credential arguments.

## Usage

### Application Default Credentials (recommended)

Run `gcloud auth application-default login` first, then:

```python
from anthropic import AnthropicGoogleCloud

client = AnthropicGoogleCloud(
    project="your-gcp-project",  # or ANTHROPIC_GOOGLE_CLOUD_PROJECT
    location="us-central1",
    workspace_id="wrkspc_...",  # or ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID
)

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)
print(message.content[0].text)
```

`project` may be omitted: it is taken from an explicit `credentials=` object when
it exposes one (e.g. a service-account credential's `project_id`), or back-filled
lazily on the first request from the project ADC resolves to (a service-account
keyfile, the `GOOGLE_CLOUD_PROJECT` environment variable, or instance metadata).
If no project can be resolved — plain user ADC, an explicit `token_provider`, or
credentials without a project — the first request raises an error asking for
`project`.

### Other credential modes

<details>
<summary>Explicit <code>google.auth</code> credentials</summary>

```python
from google.oauth2 import service_account
from anthropic import AnthropicGoogleCloud

credentials = service_account.Credentials.from_service_account_file(
    "service-account.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = AnthropicGoogleCloud(
    location="us-central1",
    workspace_id="wrkspc_...",
    credentials=credentials,
    # project= is taken from the service account when omitted
)
```

</details>

<details>
<summary>Custom token provider</summary>

Use this when you already have a token-minting layer (a sidecar, a proxy, a
broker) and don't want the SDK to talk to `google.auth` at all:

```python
from anthropic import AnthropicGoogleCloud

client = AnthropicGoogleCloud(
    project="your-gcp-project",
    location="us-central1",
    workspace_id="wrkspc_...",
    token_provider=lambda: my_token_broker.fetch(),  # invoked on every request
)
```

On `AsyncAnthropicGoogleCloud` the provider may also be `async`.

</details>

### Streaming

```python
with client.messages.stream(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Async

```python
from anthropic import AsyncAnthropicGoogleCloud

client = AsyncAnthropicGoogleCloud(
    project="your-gcp-project", location="us-central1", workspace_id="wrkspc_..."
)

message = await client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)

async with client.messages.stream(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
) as stream:
    async for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Configuration

| Argument | Environment variable | Notes |
|---|---|---|
| `project` | `ANTHROPIC_GOOGLE_CLOUD_PROJECT` | Only needed when the base URL is derived; if omitted, back-filled from Google credentials on the first request. |
| `location` | — | Required only when deriving the base URL. |
| `workspace_id` | `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID` | Required unless `skip_auth=True` with an explicit `base_url`. |
| `base_url` | `ANTHROPIC_GOOGLE_CLOUD_BASE_URL` | Overrides the derived gateway URL. |
| `skip_auth` | — | For pre-authenticated proxies: skips token attachment and the workspace requirement. |
