from .raw_message_delta_event import Delta, RawMessageDeltaEvent

__all__ = ["MessageDeltaEvent", "Delta"]

MessageDeltaEvent = RawMessageDeltaEvent
"""The RawMessageDeltaEvent type should be used instead"""
