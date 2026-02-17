import json
import re
from typing import Any, List
from typing_extensions import Literal

import rich

from anthropic import Anthropic, beta_tool
from anthropic.lib.tools import BetaFunctionTool, BetaFunctionToolResultType
from anthropic.types.beta import BetaToolReferenceBlockParam

client = Anthropic()


def _is_cjk_char(char: str) -> bool:
    """Check if a character is a CJK (Chinese, Japanese, Korean) character."""
    code_point = ord(char)
    return (
        (0x4E00 <= code_point <= 0x9FFF)  # CJK Unified Ideographs
        or (0x3400 <= code_point <= 0x4DBF)  # CJK Extension A
        or (0x20000 <= code_point <= 0x2A6DF)  # CJK Extension B
        or (0x3040 <= code_point <= 0x309F)  # Hiragana
        or (0x30A0 <= code_point <= 0x30FF)  # Katakana
        or (0xAC00 <= code_point <= 0xD7AF)  # Hangul
    )


def _contains_cjk(text: str) -> bool:
    """Check if text contains any CJK characters."""
    return any(_is_cjk_char(char) for char in text)


def _cjk_aware_match(keyword: str, text: str) -> bool:
    """
    Perform CJK-aware text matching.
    
    For CJK text, uses bidirectional substring matching since there are no word
    boundaries. This handles cases where:
    - The keyword appears in the text (e.g., "法令" in description)
    - The text contains a meaningful substring from the keyword
    - Common CJK substrings exist between keyword and text
    
    For non-CJK text, uses case-insensitive substring matching.
    """
    keyword_lower = keyword.lower()
    text_lower = text.lower()
    
    # If keyword contains CJK characters, use bidirectional matching
    if _contains_cjk(keyword):
        # First, try exact substring match in either direction
        if keyword in text or text in keyword:
            return True
        
        # Extract CJK characters from keyword for substring matching
        cjk_chars_in_keyword = ''.join(char for char in keyword if _is_cjk_char(char))
        
        if len(cjk_chars_in_keyword) >= 2:
            # Try to find common CJK substrings of length 2+ between keyword and text
            # This handles "法令を調べて" matching "日本の法令を検索します" via "法令"
            min_match_len = 2
            
            # Check if any substring of the keyword's CJK chars appears in text
            for i in range(len(cjk_chars_in_keyword)):
                for j in range(i + min_match_len, len(cjk_chars_in_keyword) + 1):
                    substring = cjk_chars_in_keyword[i:j]
                    if substring in text:
                        return True
            
            # Also check reverse: if any CJK substring from text appears in keyword
            cjk_chars_in_text = ''.join(char for char in text if _is_cjk_char(char))
            for i in range(len(cjk_chars_in_text)):
                for j in range(i + min_match_len, min(i + 10, len(cjk_chars_in_text) + 1)):
                    # Limit substring length to avoid matching everything
                    substring = cjk_chars_in_text[i:j]
                    if substring in keyword:
                        return True
        
        return False
    
    # For non-CJK text, use word-boundary aware matching
    if _contains_cjk(text):
        # If text has CJK but keyword doesn't, do simple substring match
        return keyword_lower in text_lower
    
    # For both non-CJK, use word-boundary matching
    # Create a regex pattern that matches the keyword as whole words
    pattern = r'\b' + re.escape(keyword_lower) + r'\b'
    return bool(re.search(pattern, text_lower)) or keyword_lower in text_lower


@beta_tool(defer_loading=True)
def get_weather(location: str, units: Literal["c", "f"]) -> str:
    """Lookup the weather for a given city in either celsius or fahrenheit

    Args:
        location: The city and state, e.g. San Francisco, CA
        units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
    Returns:
        A dictionary containing the location, temperature, and weather condition.
    """
    # Simulate a weather API call
    print(f"Fetching weather for {location} in {units}")

    # Here you would typically make an API call to a weather service
    # For demonstration, we return a mock response
    if units == "c":
        return json.dumps(
            {
                "location": location,
                "temperature": "20°C",
                "condition": "Sunny",
            }
        )
    else:
        return json.dumps(
            {
                "location": location,
                "temperature": "68°F",
                "condition": "Sunny",
            }
        )


@beta_tool(defer_loading=True)
def search_laws(query: str) -> str:
    """日本の法令を検索します。憲法、法律、政令、省令などを検索できます。
    
    Args:
        query: 検索キーワード
    Returns:
        検索結果
    """
    return json.dumps({"query": query, "results": []})


def make_tool_searcher(tools: List[BetaFunctionTool[Any]]) -> BetaFunctionTool[Any]:
    """
    Returns a tool that Claude can use to search through all available tools.
    
    This implementation includes CJK-aware matching to handle Japanese, Chinese,
    and Korean text properly, addressing limitations in server-side BM25 search
    for these languages.
    """

    @beta_tool
    def search_available_tools(*, keyword: str) -> BetaFunctionToolResultType:
        """Search for useful tools using a query string.
        
        This search is CJK-aware and handles Japanese, Chinese, and Korean text
        better than simple substring matching.
        """

        results: list[BetaToolReferenceBlockParam] = []
        
        for tool in tools:
            # Get tool representation as string for searching
            tool_dict = tool.to_dict()
            tool_text = json.dumps(tool_dict, ensure_ascii=False)
            
            # Use CJK-aware matching
            if _cjk_aware_match(keyword, tool_text):
                results.append({"type": "tool_reference", "tool_name": tool.name})

        return results

    return search_available_tools


def main() -> None:
    tools: list[BetaFunctionTool[Any]] = [
        get_weather,
        search_laws,
        # ... many more tools
    ]
    runner = client.beta.messages.tool_runner(
        max_tokens=1024,
        model="claude-sonnet-4-5-20250929",
        tools=[*tools, make_tool_searcher(tools)],
        messages=[{"role": "user", "content": "What is the weather in SF?"}],
        betas=["tool-search-tool-2025-10-19"],
    )
    for message in runner:
        rich.print(message)


if __name__ == "__main__":
    main()
