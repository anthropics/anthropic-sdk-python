# Messages

Types:

```python
from anthropic.types import (
    ContentBlock,
    ContentBlockDeltaEvent,
    ContentBlockStartEvent,
    ContentBlockStopEvent,
    ImageBlockParam,
    Message,
    MessageDeltaEvent,
    MessageDeltaUsage,
    MessageParam,
    MessageStartEvent,
    MessageStopEvent,
    MessageStreamEvent,
    TextBlock,
    TextBlockParam,
    TextDelta,
    Usage,
)
```

Methods:

- <code title="post /v1/messages">client.messages.<a href="./src/anthropic/resources/messages.py">create</a>(\*\*<a href="src/anthropic/types/message_create_params.py">params</a>) -> <a href="./src/anthropic/types/message.py">Message</a></code>
- <code>client.messages.<a href="./src/anthropic/resources/messages.py">stream</a>(\*args) -> MessageStreamManager[MessageStream] | MessageStreamManager[MessageStreamT]</code>

# Beta

## Tools

### Messages

Types:

```python
from anthropic.types.beta.tools import (
    InputJsonDelta,
    Tool,
    ToolResultBlockParam,
    ToolUseBlock,
    ToolUseBlockParam,
    ToolsBetaContentBlock,
    ToolsBetaContentBlockDeltaEvent,
    ToolsBetaContentBlockStartEvent,
    ToolsBetaMessage,
    ToolsBetaMessageParam,
    ToolsBetaMessageStreamEvent,
)
```

Methods:

- <code title="post /v1/messages?beta=tools">client.beta.tools.messages.<a href="./src/anthropic/resources/beta/tools/messages.py">create</a>(\*\*<a href="src/anthropic/types/beta/tools/message_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/tools/tools_beta_message.py">ToolsBetaMessage</a></code>
- <code>client.beta.tools.messages.<a href="./src/anthropic/resources/beta/tools/messages.py">stream</a>(\*args) -> ToolsBetaMessageStreamManager[ToolsBetaMessageStream] | ToolsBetaMessageStreamManager[ToolsBetaMessageStreamT]</code>
