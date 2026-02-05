# CLAUDE.md

This file provides guidance for AI assistants and developers working with the anthropic-sdk-python codebase.

## Project Overview

This is the official Python SDK for the Anthropic API. It provides both synchronous and asynchronous clients for interacting with Claude models.

## Key Directories

- `src/anthropic/` - Main SDK source code
  - `lib/` - Non-generated library code (safe to modify)
    - `bedrock/` - AWS Bedrock integration
    - `vertex/` - Google Vertex AI integration
    - `streaming/` - Streaming utilities
    - `tools/` - Tool/function calling helpers
  - `resources/` - API resource classes (generated)
  - `types/` - Type definitions (generated)
  - `_base_client.py` - Core HTTP client logic
  - `_client.py` - Main Anthropic client

- `examples/` - Example code (safe to modify/add)
- `tests/` - Test suite

## Development Commands

```bash
# Setup
./scripts/bootstrap           # Install dependencies with uv
uv sync --all-extras         # Alternative setup

# Linting & Formatting
./scripts/lint               # Run ruff, pyright, mypy
./scripts/format             # Auto-format code

# Testing
./scripts/test               # Run test suite
```

## Important Notes

1. **Generated Code**: Most code in `resources/` and `types/` is auto-generated from OpenAPI spec by Stainless. Avoid modifying these directly.

2. **Safe to Modify**: The `lib/` and `examples/` directories are not regenerated and can be freely edited.

3. **Type Checking**: The project uses both pyright and mypy. Ensure changes pass both.

4. **Bedrock/Vertex**: These integrations have their own client classes in `lib/bedrock/` and `lib/vertex/`.

## Common Patterns

### Adding retry logic
See `_base_client.py` - the `_should_retry()` method handles retry decisions.

### Adding beta features
Beta features go in `resources/beta/` with corresponding types in `types/beta/`.

### Tool helpers
Tool/function calling utilities are in `lib/tools/`.
