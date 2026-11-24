from typing_extensions import Literal, TypeAlias

__all__ = ["ModelLine"]

ModelLine: TypeAlias = Literal["haiku", "sonnet", "opus", "fable", "mythos"]
"""A Claude model line, such as `opus` or `sonnet`.

More lines may be added as new values.
"""
