# Bug Report: MCP Connection Timeout with Large Tool Sets

## Summary
MCP (Model Context Protocol) connections timeout when a server exposes more than ~50 tools simultaneously, causing Claude to fail to list available tools.

## Steps to Reproduce
1. Start an MCP server with 60+ tool definitions
2. Connect Claude to the MCP server
3. Attempt to list available tools
4. Observe timeout after ~30 seconds

## Expected Behavior
MCP server should paginate tool listings or stream them incrementally to avoid timeouts.

## Actual Behavior
Connection times out, Claude reports "MCP server unavailable" or "Tool list too large".

## Environment
- Claude version: 3.x
- MCP SDK version: Latest
- Transport: stdio and HTTP/SSE
- OS: macOS, Linux, Windows

## Proposed Fix
1. Add pagination support to `tools/list` MCP endpoint
2. Add `limit` and `cursor` parameters for incremental tool retrieval
3. Add tool streaming capability for large tool sets

## Workaround
Split tools across multiple MCP servers or reduce tool count per server.

## Submission
- **Platform**: Anthropic
- **Repository**: https://github.com/anthropics/anthropic-sdk-python or https://github.com/anthropics/anthropic-sdk-typescript
- **Issue Type**: Bug Report
- **Labels**: bug, mcp, timeout, tools
