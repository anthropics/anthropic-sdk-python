from typing_extensions import Literal, TypeAlias

__all__ = ["BetaManagedAgentsSessionThreadStatus"]

BetaManagedAgentsSessionThreadStatus: TypeAlias = Literal["running", "idle", "rescheduling", "terminated"]
