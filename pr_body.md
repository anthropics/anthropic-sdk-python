## Summary

This PR adds `tool_runner` and `stream` method aliases to both Messages and AsyncMessages classes in the Bedrock beta module.

## Motivation

Fixes #1106
Fixes #1120

The `tool_runner` API (`client.beta.messages.tool_runner()`) was not available on the AnthropicBedrock or AsyncAnthropicBedrock clients. This creates feature parity for enterprise AWS Bedrock users.

## Changes

Added method aliases to `src/anthropic/lib/bedrock/_beta_messages.py`:
- `tool_runner` - Automatic tool execution loop  
- `stream` - Streaming message helpers

**Note:** `parse` was intentionally excluded as Bedrock doesn't currently support the structured output beta header.

## Checklist
- [x] Changes follow existing code patterns
- [x] No breaking changes
- [x] Commit follows conventional format
