from typing_extensions import Literal, TypeAlias

__all__ = ["BetaManagedAgentsDeltaType"]

BetaManagedAgentsDeltaType: TypeAlias = Literal["agent.message", "agent.thinking"]
