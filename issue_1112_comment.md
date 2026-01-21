Hey! I investigated this and found the root cause.

## Root Cause

The `caller` field was added to `BetaToolUseBlockParam` (the **request** type) in commit `9843a8e` (Nov 24, 2025), but the API only accepts `caller` as an **output-only** field in responses.

When you convert API response content blocks back to params for multi-turn conversations (e.g., passing `message.content` back), the `caller` field gets included in the request payload and the API rejects it with:

```
'messages.1.content.1.tool_use.caller: Extra inputs are not permitted'
```

## Where the issue is

Looking at the type definitions:
- [beta_tool_use_block.py](https://github.com/anthropics/anthropic-sdk-python/blob/main/src/anthropic/types/beta/beta_tool_use_block.py#L25) - Response type has `caller: Optional[Caller] = None`  
- [beta_tool_use_block_param.py](https://github.com/anthropics/anthropic-sdk-python/blob/main/src/anthropic/types/beta/beta_tool_use_block_param.py#L29) - Request type also has `caller: Caller`

The `Param` type shouldn't include `caller` since it's output-only.

## Suggested Fix

Since these files are auto-generated from OpenAPI spec by Stainless, the fix would need to be in the OpenAPI spec to mark `caller` as `readOnly: true` (output-only), which would exclude it from the `Param` types.

**Workaround for now:** Strip the `caller` field from tool_use blocks before sending them back:

```python
for msg in messages:
    if msg.get("content"):
        for block in msg["content"]:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                block.pop("caller", None)
```
