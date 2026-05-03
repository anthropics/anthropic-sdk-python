from anthropic.types import (
    ToolSearchToolResultBlock,
    ToolSearchToolResultError,
    ToolSearchToolSearchResultBlock,
)


def test_tool_search_result_content_uses_search_result_variant() -> None:
    block = ToolSearchToolResultBlock.construct(
        content={
            "type": "tool_search_tool_search_result",
            "tool_references": [
                {
                    "type": "tool_reference",
                    "tool_name": "web_search",
                }
            ],
        },
        tool_use_id="toolu_123",
        type="tool_search_tool_result",
    )

    assert isinstance(block.content, ToolSearchToolSearchResultBlock)
    assert block.content.tool_references[0].tool_name == "web_search"


def test_tool_search_result_content_uses_error_variant() -> None:
    block = ToolSearchToolResultBlock.construct(
        content={
            "type": "tool_search_tool_result_error",
            "error_code": "invalid_tool_input",
            "error_message": "invalid query",
        },
        tool_use_id="toolu_123",
        type="tool_search_tool_result",
    )

    assert isinstance(block.content, ToolSearchToolResultError)
    assert block.content.error_code == "invalid_tool_input"
    assert block.content.error_message == "invalid query"
