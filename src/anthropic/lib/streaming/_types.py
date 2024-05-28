from typing import Union
from typing_extensions import Literal

from ...types import (
    Message,
    ContentBlock,
    MessageDeltaEvent as RawMessageDeltaEvent,
    MessageStartEvent as RawMessageStartEvent,
    RawMessageStopEvent,
    ContentBlockDeltaEvent as RawContentBlockDeltaEvent,
    ContentBlockStartEvent as RawContentBlockStartEvent,
    RawContentBlockStopEvent,
)
from ..._models import BaseModel


class TextEvent(BaseModel):
    type: Literal["text"]

    text: str
    """The text delta"""

    snapshot: str
    """The entire accumulated text"""


class MessageStopEvent(RawMessageStopEvent):
    type: Literal["message_stop"]

    message: Message


class ContentBlockStopEvent(RawContentBlockStopEvent):
    type: Literal["content_block_stop"]

    content_block: ContentBlock


MessageStreamEvent = Union[
    TextEvent,
    RawMessageStartEvent,
    RawMessageDeltaEvent,
    MessageStopEvent,
    RawContentBlockStartEvent,
    RawContentBlockDeltaEvent,
    ContentBlockStopEvent,
]
