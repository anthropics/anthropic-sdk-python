# CLAUDE.md — Anthropic Python SDK

This file documents the codebase structure, development workflows, and conventions for AI assistants working in this repository.

## Project Overview

This is the **official Python SDK for the Anthropic API** (`anthropic` package on PyPI). It provides type-safe access to the Anthropic REST API from Python 3.8+ applications, including both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

**Important:** Most SDK source code (outside `src/anthropic/lib/` and `examples/`) is **auto-generated** from the OpenAPI spec by [Stainless](https://www.stainless.com/). Manual edits to generated files may be overwritten by future generations, though patches are attempted to be preserved.

Safe to edit manually:
- `src/anthropic/lib/` — custom helpers (streaming, Bedrock, Vertex)
- `examples/` — usage examples
- `tests/` — test suite

---

## Repository Structure

```
anthropic-sdk-python/
├── src/anthropic/           # Main package (mostly generated)
│   ├── __init__.py          # Public exports
│   ├── _client.py           # Anthropic / AsyncAnthropic client classes
│   ├── _base_client.py      # SyncAPIClient / AsyncAPIClient base classes
│   ├── _models.py           # Pydantic BaseModel with SDK helpers
│   ├── _resource.py         # SyncAPIResource / AsyncAPIResource base classes
│   ├── _types.py            # Core type aliases (NOT_GIVEN, NotGiven, Headers, etc.)
│   ├── _exceptions.py       # Error hierarchy (APIError, RateLimitError, etc.)
│   ├── _streaming.py        # Stream / AsyncStream for SSE
│   ├── _response.py         # APIResponse / AsyncAPIResponse
│   ├── _legacy_response.py  # LegacyAPIResponse (used by .with_raw_response)
│   ├── _files.py            # File upload utilities
│   ├── _constants.py        # Default timeouts, limits, prompts
│   ├── _version.py          # Package version string
│   ├── _compat.py           # Pydantic v1/v2 compatibility shims
│   ├── _qs.py               # Querystring serialization
│   ├── _utils/              # Internal utilities
│   │   ├── _transform.py    # Request param transformation
│   │   ├── _typing.py       # Typing helpers
│   │   ├── _logs.py         # Logging setup
│   │   ├── _streams.py      # Stream utilities
│   │   ├── _sync.py         # Sync/async helpers
│   │   └── ...
│   ├── _decoders/           # SSE / JSONL decoders
│   ├── resources/           # API resource implementations (generated)
│   │   ├── messages/        # Messages API (create, stream, count_tokens, batches)
│   │   ├── completions.py   # Text completions (legacy)
│   │   ├── models.py        # Models API
│   │   └── beta/            # Beta API endpoints (files, messages, models)
│   ├── types/               # TypedDicts for request params + Pydantic response models
│   │   ├── message.py       # Message response model
│   │   ├── message_create_params.py
│   │   ├── beta/            # Beta-specific types
│   │   └── ...
│   ├── lib/                 # Hand-written helpers (NOT generated)
│   │   ├── streaming/       # MessageStream, AsyncMessageStream helpers
│   │   ├── bedrock/         # AnthropicBedrock client + AWS auth
│   │   └── vertex/          # AnthropicVertex client + GCP auth
│   └── pagination.py        # SyncPage / AsyncPage for paginated responses
├── tests/                   # Pytest test suite
│   ├── conftest.py          # Shared fixtures (client, async_client)
│   ├── api_resources/       # Per-resource tests
│   ├── lib/                 # Tests for lib/ helpers
│   ├── test_client.py       # Client-level tests
│   ├── test_models.py       # Model serialization tests
│   ├── test_streaming.py    # Streaming tests
│   └── ...
├── examples/                # Runnable usage examples (NOT generated)
├── scripts/                 # Development scripts
│   ├── bootstrap            # Install all dependencies via uv
│   ├── lint                 # Run ruff + pyright + mypy
│   ├── format               # Auto-format with ruff
│   ├── test                 # Run pytest against Prism mock server
│   └── mock                 # Start/manage Prism mock server
├── pyproject.toml           # Project config, dependencies, tool settings
├── mypy.ini                 # Mypy configuration
├── api.md                   # Full API reference (generated)
├── helpers.md               # Streaming helpers documentation
├── CONTRIBUTING.md          # Contributor guide
└── CHANGELOG.md             # Version history
```

---

## Development Setup

### Using uv (recommended)

```sh
# Install all dependencies (including dev)
./scripts/bootstrap
# or manually:
uv sync --all-extras
```

### Without uv

```sh
pip install -r requirements-dev.lock
```

### Activating the virtualenv

```sh
source .venv/bin/activate
```

---

## Common Commands

### Linting

```sh
./scripts/lint
# Runs: ruff check, pyright (strict), mypy, import check
```

### Formatting

```sh
./scripts/format
# Runs: ruff format + ruff check --fix + ruffen-docs on README/api.md
```

### Running Tests

Tests require either a [Prism](https://github.com/stoplightio/prism) mock server or a real API base URL.

```sh
# Automatically starts a Prism mock server and runs tests
./scripts/test

# Against a real or custom server
TEST_API_BASE_URL=http://localhost:8080 ./scripts/test

# Run specific tests
./scripts/test tests/api_resources/test_messages.py -x -v

# Run with a specific Python version
UV_PYTHON=3.11 ./scripts/test
```

The test script runs against both Pydantic v1 and v2, and by default runs on Python 3.8 and 3.13.

### Building

```sh
uv build
# or
python -m build
```

---

## Code Conventions

### File Headers

Generated files begin with:
```python
# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.
```

Hand-written files do **not** have this header.

### Future Annotations

All modules use `from __future__ import annotations` at the top for forward references.

### Type Checking

The project uses **strict Pyright** (`typeCheckingMode = "strict"`) and **strict mypy**. All public functions must have full type annotations.

Private members (internal implementation details) are prefixed with `_` (e.g., `_client.py`, `_utils/`).

**Ruff rules enforced:**
- `I` — isort (imports sorted by length, combined-as-imports)
- `B` — bugbear
- `F401` — remove unused imports
- `E722` — no bare except
- `ARG` — no unused arguments
- `T201`/`T203` — no print statements (in library code; allowed in tests/examples)
- `TC004` — misuse of `TYPE_CHECKING`
- `TID251` — import rules

**Line length:** 120 characters

**Banned:** `functools.lru_cache` — use the custom `lru_cache` from `_utils` instead (preserves type info).

### Imports

- Standard library imports first, then third-party, then local
- Use `from __future__ import annotations` always
- `typing_extensions` is treated as standard library for isort
- `TYPE_CHECKING` blocks for circular import resolution

### NOT_GIVEN Pattern

Optional parameters use `NOT_GIVEN` sentinel instead of `None`:
```python
from anthropic._types import NOT_GIVEN, NotGiven

def create(self, *, temperature: float | NotGiven = NOT_GIVEN) -> ...:
    ...
```

This allows distinguishing between "not provided" and explicitly `None`.

### Resource Classes

Resources extend `SyncAPIResource` / `AsyncAPIResource` and expose HTTP methods via `self._get`, `self._post`, etc. Each resource provides:
- `.with_raw_response` — returns `LegacyAPIResponse`
- `.with_streaming_response` — returns `APIResponse` (context manager, lazy)
- Subresources via `@cached_property`

### Response Models

Responses are Pydantic models subclassing `BaseModel` (from `anthropic._models`). They support:
- `.to_json()` — serialize to JSON string
- `.to_dict()` — serialize to dict
- `._request_id` — public property from response headers
- `.model_fields_set` — distinguish `null` from missing fields

### Streaming

The `Stream` / `AsyncStream` classes wrap SSE event iteration. The higher-level `MessageStream` / `AsyncMessageStream` (in `lib/streaming/`) provide:
- `.text_stream` — async iterator of text deltas
- `.get_final_message()` — accumulated final `Message`
- `.get_final_text()` — accumulated final text

### Pagination

List endpoints return `SyncPage[T]` / `AsyncPage[T]` with:
- Auto-iteration (fetches next pages as needed)
- `.has_next_page()`, `.next_page_info()`, `.get_next_page()`
- `.data` — list of items on current page

---

## Key Client Features

| Feature | Description |
|---|---|
| `max_retries` | Auto-retry on 408, 409, 429, >=500; default 2 |
| `timeout` | Default 10 minutes; configurable per-client or per-request |
| `default_headers` | Sent with every request |
| `http_client` | Custom httpx client for proxies, transports, etc. |
| `base_url` | Override API base (also via `ANTHROPIC_BASE_URL`) |
| `.with_options()` | Create client copy with overridden settings |

**Environment variables:**
- `ANTHROPIC_API_KEY` — API key
- `ANTHROPIC_AUTH_TOKEN` — Auth token (alternative to API key)
- `ANTHROPIC_BASE_URL` — Custom base URL
- `ANTHROPIC_LOG` — Set to `info` or `debug` for logging
- `TEST_API_BASE_URL` — Override test server URL (tests)

---

## Optional Extras

```sh
pip install anthropic[aiohttp]    # Use aiohttp backend for async client
pip install anthropic[bedrock]    # AWS Bedrock support (boto3)
pip install anthropic[vertex]     # Google Vertex AI support (google-auth)
```

---

## Testing Patterns

- **Mock server:** Prism runs at `http://127.0.0.1:4010` by default
- **Fixtures:** `client` (sync) and `async_client` (async) from `conftest.py`
- **Async tests:** Automatically marked `asyncio` — no manual `@pytest.mark.asyncio` needed
- **Both Pydantic versions:** Test suite runs with Pydantic v1 and v2
- **aiohttp + respx_mock:** These are incompatible; such tests are auto-skipped
- **Parallel execution:** Tests run with `pytest-xdist` (`-n auto`)

---

## CI/CD

GitHub Actions workflows (`.github/workflows/`):

| Workflow | Trigger | Steps |
|---|---|---|
| `ci.yml` | push/PR | lint, build (internal), test |
| `publish-pypi.yml` | manual/release | publish to PyPI |
| `create-releases.yml` | automated | release PR creation |
| `detect-breaking-changes.yml` | PR | check API compatibility |
| `release-doctor.yml` | release | pre-release checks |

Releases are managed via `release-please` (`release-please-config.json`).

---

## Adding New Features

Since most code is generated, new hand-written features belong in `src/anthropic/lib/`. For example:
- Custom streaming helpers → `lib/streaming/`
- Provider-specific clients → `lib/bedrock/`, `lib/vertex/`

When adding to `lib/`, export from `src/anthropic/__init__.py` as needed, and add corresponding tests in `tests/lib/`.

Examples go in `examples/` and should be self-contained scripts with a shebang:
```python
#!/usr/bin/env -S uv run python
```
