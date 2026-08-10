from anthropic.types import ToolUseBlockParam
from anthropic.types.beta import BetaToolUseBlockParam


def test_tool_use_block_params_allow_null_caller() -> None:
    tool_use: ToolUseBlockParam = {"id": "id", "input": {}, "name": "tool", "type": "tool_use", "caller": None}
    beta_tool_use: BetaToolUseBlockParam = {
        "id": "id",
        "input": {},
        "name": "tool",
        "type": "tool_use",
        "caller": None,
    }

    assert tool_use["caller"] is None
    assert beta_tool_use["caller"] is None
