# Anthropic

Methods:

- <code>client.<a href="./src/anthropic/_client.py">count_tokens</a>(\*args) -> int</code>

# Completions

Types:

```python
from anthropic.types import Completion
```

Methods:

- <code title="post /v1/complete">client.completions.<a href="./src/anthropic/resources/completions.py">create</a>(\*\*<a href="src/anthropic/types/completion_create_params.py">params</a>) -> <a href="./src/anthropic/types/completion.py">Completion</a></code>

# Beta

## Messages

Types:

```python
from anthropic.types.beta import (
    ContentBlock,
    ContentBlockDeltaEvent,
    ContentBlockStartEvent,
    ContentBlockStopEvent,
    Message,
    MessageDeltaEvent,
    MessageDeltaUsage,
    MessageParam,
    MessageStartEvent,
    MessageStopEvent,
    MessageStreamEvent,
    TextBlock,
    TextDelta,
    Usage,
)
```

Methods:

- <code title="post /v1/messages">client.beta.messages.<a href="./src/anthropic/resources/beta/messages.py">create</a>(\*\*<a href="src/anthropic/types/beta/message_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/message.py">Message</a></code>
- <code>client.beta.messages.<a href="./src/anthropic/resources/beta/messages.py">stream</a>(\*args) -> MessageStreamManager[MessageStream] | MessageStreamManager[MessageStreamT]</code>
