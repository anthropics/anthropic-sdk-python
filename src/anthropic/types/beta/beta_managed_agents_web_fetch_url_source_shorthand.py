from typing_extensions import Literal, TypeAlias

__all__ = ["BetaManagedAgentsWebFetchURLSourceShorthand"]

BetaManagedAgentsWebFetchURLSourceShorthand: TypeAlias = Literal["all", "none"]
"""
String form of a url_sources value that has no field other than its type: "all" means {"type": "all"} and "none" means {"type": "none"}.
"""
