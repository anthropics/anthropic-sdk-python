from typing_extensions import Literal, TypeAlias

__all__ = ["BetaManagedAgentsCredentialValidationStatus"]

BetaManagedAgentsCredentialValidationStatus: TypeAlias = Literal["valid", "invalid", "unknown"]
