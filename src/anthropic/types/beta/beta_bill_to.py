from typing_extensions import Literal, TypeAlias

__all__ = ["BetaBillTo"]

BetaBillTo: TypeAlias = Literal["self", "user_profile"]
"""Who is billed for a request."""
