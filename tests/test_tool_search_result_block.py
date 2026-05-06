from anthropic.types.tool_search_tool_result_block import ToolSearchToolResultBlock
from anthropic.types.beta.beta_tool_search_tool_result_block import BetaToolSearchToolResultBlock


def test_tool_search_tool_result_block_content_is_typed() -> None:
    block = ToolSearchToolResultBlock.model_validate(
        {
            "type": "tool_search_tool_result",
            "tool_use_id": "toolu_123",
            "content": {
                "type": "tool_search_tool_result_error",
                "error_code": "unavailable",
                "error_message": "search backend unavailable",
            },
        }
    )

    assert block.content.type == "tool_search_tool_result_error"
    assert type(block.content).__name__ == "ToolSearchToolResultError"


def test_beta_tool_search_tool_result_block_content_is_typed() -> None:
    block = BetaToolSearchToolResultBlock.model_validate(
        {
            "type": "tool_search_tool_result",
            "tool_use_id": "toolu_123",
            "content": {
                "type": "tool_search_tool_result_error",
                "error_code": "unavailable",
                "error_message": "search backend unavailable",
            },
        }
    )

    assert block.content.type == "tool_search_tool_result_error"
    assert type(block.content).__name__ == "BetaToolSearchToolResultError"
