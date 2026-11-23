from typing_extensions import Literal, TypeAlias

__all__ = ["BetaDreamStatus"]

BetaDreamStatus: TypeAlias = Literal["pending", "running", "completed", "failed", "canceled"]
"""Where a dream is in its lifecycle.

`completed`, `failed`, and `canceled` are final: once a dream has one of these statuses, its status doesn't change again.

See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#lifecycle) for what each status means.

- `pending` - The dream is waiting to start and hasn't read its inputs yet.

  `outputs` is empty and every `usage` count is zero.
- `running` - The dream is reading its inputs and writing its result.

  `usage` updates while the dream has this status.
- `completed` - The dream finished and its output memory store holds the complete result.
- `failed` - The dream stopped with an error, which `error` describes.

  If `outputs` references a memory store, that memory store keeps what the dream wrote before it stopped.
- `canceled` - A cancel request stopped the dream before it reached `completed` or `failed`.

  If `outputs` references a memory store, that memory store keeps what the dream wrote. `usage` can keep changing after the cancel.
"""
