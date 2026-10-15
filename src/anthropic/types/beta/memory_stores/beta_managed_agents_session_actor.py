from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionActor"]


class BetaManagedAgentsSessionActor(BaseModel):
    """
    An agent acting during a session, for example through the session's mounted filesystem. It names the session itself, not the user or API key that started the session.
    """

    session_id: str
    """ID of the session (a `sesn_...` value).

    Look up the session via [Retrieve a session](/en/api/beta/sessions/retrieve) for
    further provenance.
    """

    type: Literal["session_actor"]
