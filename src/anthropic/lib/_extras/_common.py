from ..._exceptions import AnthropicError

INSTRUCTIONS = """

Anthropic error: missing required dependency `{library}`.

    $ pip install anthropic[{extra}]
"""


class MissingDependencyError(AnthropicError):
    def __init__(self, *, library: str, extra: str) -> None:
        super().__init__(INSTRUCTIONS.format(library=library, extra=extra))


def patch_anthropic_base_url_for_testing(base_url: str) -> None:
    """
    Override the Anthropic API base URL for testing purposes.
    This is useful when running tests against a mock server.
    
    Args:
        base_url: The base URL to use for API requests.
    """
    import os
    os.environ["ANTHROPIC_BASE_URL"] = base_url