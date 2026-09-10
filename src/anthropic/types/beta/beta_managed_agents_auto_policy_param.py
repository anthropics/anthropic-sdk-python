from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsAutoPolicyParam"]


class BetaManagedAgentsAutoPolicyParam(TypedDict, total=False):
    """
    The server decides each tool call individually: it judges, from the tool, its input, and the session content so far, whether the call is safe to execute or high-risk, and evaluates it to allow when judged safe and to deny when judged high-risk. A call the server cannot reach a judgement on evaluates to ask.
    """

    type: Required[Literal["auto"]]
