from typing import Union
from typing_extensions import Literal

from ..._models import BaseModel
from ...types.beta import (
    BetaMessage,
    BetaContentBlock,
    BetaRawMessageStopEvent,
    BetaRawMessageDeltaEvent,
    BetaRawMessageStartEvent,
    BetaRawContentBlockStopEvent,
    BetaRawContentBlockDeltaEvent,
    BetaRawContentBlockStartEvent,
)


class BetaTextEvent(BaseModel):
    type: Literal["text"]

    text: str
    """The text delta"""

    snapshot: str
    """The entire accumulated text"""


class BetaInputJsonEvent(BaseModel):
    type: Literal["input_json"]

    partial_json: str
    """A partial JSON string delta

    e.g. `'"San Francisco,'`
    """

    snapshot: object
    """The currently accumulated parsed object.


    e.g. `{'location': 'San Francisco, CA'}`
    """


class BetaMessageStopEvent(BetaRawMessageStopEvent):
    type: Literal["message_stop"]

    message: BetaMessage


class BetaContentBlockStopEvent(BetaRawContentBlockStopEvent):
    type: Literal["content_block_stop"]

    content_block: BetaContentBlock


BetaMessageStreamEvent = Union[
    BetaTextEvent,
    BetaInputJsonEvent,
    BetaRawMessageStartEvent,
    BetaRawMessageDeltaEvent,
    BetaMessageStopEvent,
    BetaRawContentBlockStartEvent,
    BetaRawContentBlockDeltaEvent,
    BetaContentBlockStopEvent,
]
