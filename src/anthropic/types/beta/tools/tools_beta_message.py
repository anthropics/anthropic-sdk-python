# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ...usage import Usage
from ...._models import BaseModel
from .tools_beta_content_block import ToolsBetaContentBlock

__all__ = ["ToolsBetaMessage"]


class ToolsBetaMessage(BaseModel):
    id: str
    """Unique object identifier.

    The format and length of IDs may change over time.
    """

    content: List[ToolsBetaContentBlock]
    """Content generated by the model.

    This is an array of content blocks, each of which has a `type` that determines
    its shape. Currently, the only `type` in responses is `"text"`.

    Example:

    ```json
    [{ "type": "text", "text": "Hi, I'm Claude." }]
    ```

    If the request input `messages` ended with an `assistant` turn, then the
    response `content` will continue directly from that last turn. You can use this
    to constrain the model's output.

    For example, if the input `messages` were:

    ```json
    [
      {
        "role": "user",
        "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"
      },
      { "role": "assistant", "content": "The best answer is (" }
    ]
    ```

    Then the response `content` might be:

    ```json
    [{ "type": "text", "text": "B)" }]
    ```
    """

    model: str
    """The model that handled the request."""

    role: Literal["assistant"]
    """Conversational role of the generated message.

    This will always be `"assistant"`.
    """

    stop_reason: Optional[Literal["end_turn", "max_tokens", "stop_sequence", "tool_use"]] = None
    """The reason that we stopped.

    This may be one the following values:

    - `"end_turn"`: the model reached a natural stopping point
    - `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
    - `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
    - `"tool_use"`: (tools beta only) the model invoked one or more tools

    In non-streaming mode this value is always non-null. In streaming mode, it is
    null in the `message_start` event and non-null otherwise.
    """

    stop_sequence: Optional[str] = None
    """Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was
    generated.
    """

    type: Literal["message"]
    """Object type.

    For Messages, this is always `"message"`.
    """

    usage: Usage
    """Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the
    underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the
    model. The model's output then goes through a parsing stage before becoming an
    API response. As a result, the token counts in `usage` will not match one-to-one
    with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response
    from Claude.
    """
