from typing import Union
from typing_extensions import Literal

from .._types import TextEvent
from ....types import RawMessageStopEvent, RawMessageDeltaEvent, RawMessageStartEvent, RawContentBlockStopEvent
from ...._models import BaseModel
from ....types.beta.tools import (
    ToolsBetaMessage,
    ToolsBetaContentBlock,
    RawToolsBetaContentBlockDeltaEvent,
    RawToolsBetaContentBlockStartEvent,
)


class ToolsBetaMessageStopEvent(RawMessageStopEvent):
    type: Literal["message_stop"]

    message: ToolsBetaMessage


class ToolsBetaContentBlockStopEvent(RawContentBlockStopEvent):
    type: Literal["content_block_stop"]

    content_block: ToolsBetaContentBlock


class ToolsBetaInputJsonEvent(BaseModel):
    type: Literal["input_json"]

    partial_json: str
    """A partial JSON string delta

    e.g. `'"San Francisco,'`
    """

    snapshot: object
    """The currently accumulated parsed object.


    e.g. `{'location': 'San Francisco, CA'}`
    """


ToolsBetaMessageStreamEvent = Union[
    TextEvent,
    RawMessageStartEvent,
    RawMessageDeltaEvent,
    ToolsBetaMessageStopEvent,
    RawToolsBetaContentBlockDeltaEvent,
    RawToolsBetaContentBlockStartEvent,
    ToolsBetaInputJsonEvent,
    ToolsBetaContentBlockStopEvent,
]
