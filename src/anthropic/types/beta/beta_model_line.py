from typing_extensions import Literal, TypeAlias

__all__ = ["BetaModelLine"]

BetaModelLine: TypeAlias = Literal["haiku", "sonnet", "opus", "fable", "mythos"]
"""A Claude model line, such as `opus` or `sonnet`.

More lines may be added as new values.
"""
