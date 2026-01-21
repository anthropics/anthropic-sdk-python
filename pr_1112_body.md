## Summary

Removes the `caller` field from `BetaToolUseBlockParam` and `BetaServerToolUseBlockParam` since it's output-only.

## Problem

Fixes #1112

When users convert API response content blocks back to params for multi-turn conversations, the `caller` field gets included in the request payload and the API rejects it:

```
'messages.1.content.1.tool_use.caller: Extra inputs are not permitted'
```

## Root Cause

The `caller` field was added to both the response types (`BetaToolUseBlock`) and the request param types (`BetaToolUseBlockParam`). However, `caller` is output-only - it's returned by the API but should not be sent in requests.

## Changes

Removed `caller` field from:
- `src/anthropic/types/beta/beta_tool_use_block_param.py`
- `src/anthropic/types/beta/beta_server_tool_use_block_param.py`

Also cleaned up unused imports (`BetaDirectCallerParam`, `BetaServerToolCallerParam`, `TypeAlias`, `Union`).

> **Note:** These files are auto-generated from OpenAPI spec by Stainless. The permanent fix should mark `caller` as `readOnly: true` in the spec so it's excluded from Param types during generation.

## Checklist
- [x] Changes follow existing code patterns
- [x] No breaking changes
- [x] Tested that the fix resolves the 400 error
