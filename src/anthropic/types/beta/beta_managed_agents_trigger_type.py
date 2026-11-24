from typing_extensions import Literal, TypeAlias

__all__ = ["BetaManagedAgentsTriggerType"]

BetaManagedAgentsTriggerType: TypeAlias = Literal["schedule", "manual"]
"""What triggered a deployment run.

- `schedule` - The run was fired by the deployment's cron schedule.
- `manual` - The run was started manually by creating a session directly against the deployment.
"""
