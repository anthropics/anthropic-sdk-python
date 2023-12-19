# File generated from our OpenAPI spec by Stainless.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .content_block import ContentBlock

__all__ = ["Message"]


class Message(BaseModel):
    id: str
    """Unique object identifier.

    The format and length of IDs may change over time.
    """

    content: List[ContentBlock]
    """Content generated by the model.

    This is an array of content blocks, each of which has a `type` that determines
    its shape. Currently, the only `type` available is `"text"`.

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
      {
        "role": "assistant",
        "content": "The best answer is ("
      }
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

    stop_reason: Optional[Literal["end_turn", "max_tokens", "stop_sequence"]]
    """The reason that we stopped.

    This may be one the following values:

    - `"end_turn"`: the model reached a natural stopping point
    - `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
    - `"stop_sequence"`: one of your provided custom `stop_sequences` was generated

    Note that these values are different than those in `/v1/complete`, where
    `end_turn` and `stop_sequence` were not differentiated.

    In non-streaming mode this value is always non-null. In streaming mode, it is
    null in the `message_start` event and non-null otherwise.
    """

    stop_sequence: Optional[str]
    """Which custom stop sequence was generated.

    This value will be non-null if one of your custom stop sequences was generated.
    """

    type: Literal["message"]
