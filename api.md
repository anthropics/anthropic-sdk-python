# Messages

Types:

```python
from anthropic.types import (
    ContentBlock,
    ContentBlockDeltaEvent,
    ContentBlockStartEvent,
    ContentBlockStopEvent,
    ImageBlockParam,
    InputJSONDelta,
    Message,
    MessageDeltaEvent,
    MessageDeltaUsage,
    MessageParam,
    MessageStartEvent,
    MessageStopEvent,
    MessageStreamEvent,
    Model,
    RawContentBlockDeltaEvent,
    RawContentBlockStartEvent,
    RawContentBlockStopEvent,
    RawMessageDeltaEvent,
    RawMessageStartEvent,
    RawMessageStopEvent,
    RawMessageStreamEvent,
    TextBlock,
    TextBlockParam,
    TextDelta,
    Tool,
    ToolResultBlockParam,
    ToolUseBlock,
    ToolUseBlockParam,
    Usage,
)
```

Methods:

- <code title="post /v1/messages">client.messages.<a href="./src/anthropic/resources/messages.py">create</a>(\*\*<a href="src/anthropic/types/message_create_params.py">params</a>) -> <a href="./src/anthropic/types/message.py">Message</a></code>
- <code>client.messages.<a href="./src/anthropic/resources/messages.py">stream</a>(\*args) -> MessageStreamManager[MessageStream] | MessageStreamManager[MessageStreamT]</code>

# Beta

## PromptCaching

### Messages

Types:

```python
from anthropic.types.beta.prompt_caching import (
    PromptCachingBetaCacheControlEphemeral,
    PromptCachingBetaImageBlockParam,
    PromptCachingBetaMessage,
    PromptCachingBetaMessageParam,
    PromptCachingBetaTextBlockParam,
    PromptCachingBetaTool,
    PromptCachingBetaToolResultBlockParam,
    PromptCachingBetaToolUseBlockParam,
    PromptCachingBetaUsage,
    RawPromptCachingBetaMessageStartEvent,
    RawPromptCachingBetaMessageStreamEvent,
)
```

Methods:

- <code title="post /v1/messages?beta=prompt_caching">client.beta.prompt_caching.messages.<a href="./src/anthropic/resources/beta/prompt_caching/messages.py">create</a>(\*\*<a href="src/anthropic/types/beta/prompt_caching/message_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/prompt_caching/prompt_caching_beta_message.py">PromptCachingBetaMessage</a></code>
- <code title="post /v1/messages?beta=prompt_caching">client.beta.prompt_caching.messages.<a href="./src/anthropic/resources/beta/prompt_caching/messages.py">stream</a>(\*\*<a href="src/anthropic/types/beta/prompt_caching/message_create_params.py">params</a>) -> <a href="./src/anthropic/lib/streaming/_prompt_caching_beta_messages.py">PromptCachingBetaMessageStreamManager</a></code>
