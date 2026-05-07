# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionActor"]


class BetaManagedAgentsSessionActor(BaseModel):
    """
    Attribution for a write made by an agent during a session, through the mounted filesystem at `/mnt/memory/`.
    """

    session_id: str
    """ID of the session that performed the write (a `sesn_...` value).

    Look up the session via [Retrieve a session](/en/api/sessions-retrieve) for
    further provenance.
    """

    type: Literal["session_actor"]
