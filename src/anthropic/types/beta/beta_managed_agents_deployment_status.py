from typing_extensions import Literal, TypeAlias

__all__ = ["BetaManagedAgentsDeploymentStatus"]

BetaManagedAgentsDeploymentStatus: TypeAlias = Literal["active", "paused"]
"""Lifecycle status of a deployment.

- `active` - The deployment is active and can run sessions. Archived deployments also report this status; check `archived_at` to distinguish them.
- `paused` - The deployment is paused. Autonomous triggers are suppressed; manual runs are still permitted.
"""
