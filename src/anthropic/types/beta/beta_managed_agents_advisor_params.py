# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsAdvisorParams"]


class BetaManagedAgentsAdvisorParams(TypedDict, total=False):
    """
    Platform advisor roster entry: a model the session's primary thread may consult mid-turn. At most one per roster; the entry occupies the roster name `anthropic.advisor`.
    """

    model: Required[str]
    """A Claude model id.

    The model must be permitted as an advisor for this agent's model — see the
    sessions/threads/advisor spec.
    """

    type: Required[Literal["advisor"]]
