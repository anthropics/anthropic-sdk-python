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
    Metadata,
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
    ToolChoice,
    ToolChoiceAny,
    ToolChoiceAuto,
    ToolChoiceTool,
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

Types:

```python
from anthropic.types import (
    AnthropicBeta,
    BetaAPIError,
    BetaAuthenticationError,
    BetaError,
    BetaErrorResponse,
    BetaInvalidRequestError,
    BetaNotFoundError,
    BetaOverloadedError,
    BetaPermissionError,
    BetaRateLimitError,
)
```

## Messages

Types:

```python
from anthropic.types.beta import (
    BetaCacheControlEphemeral,
    BetaContentBlock,
    BetaContentBlockParam,
    BetaImageBlockParam,
    BetaInputJSONDelta,
    BetaMessage,
    BetaMessageDeltaUsage,
    BetaMessageParam,
    BetaMetadata,
    BetaRawContentBlockDeltaEvent,
    BetaRawContentBlockStartEvent,
    BetaRawContentBlockStopEvent,
    BetaRawMessageDeltaEvent,
    BetaRawMessageStartEvent,
    BetaRawMessageStopEvent,
    BetaRawMessageStreamEvent,
    BetaTextBlock,
    BetaTextBlockParam,
    BetaTextDelta,
    BetaTool,
    BetaToolChoice,
    BetaToolChoiceAny,
    BetaToolChoiceAuto,
    BetaToolChoiceTool,
    BetaToolResultBlockParam,
    BetaToolUseBlock,
    BetaToolUseBlockParam,
    BetaUsage,
)
```

Methods:

- <code title="post /v1/messages?beta=true">client.beta.messages.<a href="./src/anthropic/resources/beta/messages/messages.py">create</a>(\*\*<a href="src/anthropic/types/beta/message_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_message.py">BetaMessage</a></code>

### Batches

Types:

```python
from anthropic.types.beta.messages import (
    BetaMessageBatch,
    BetaMessageBatchCanceledResult,
    BetaMessageBatchErroredResult,
    BetaMessageBatchExpiredResult,
    BetaMessageBatchIndividualResponse,
    BetaMessageBatchRequestCounts,
    BetaMessageBatchResult,
    BetaMessageBatchSucceededResult,
)
```

Methods:

- <code title="post /v1/messages/batches?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">create</a>(\*\*<a href="src/anthropic/types/beta/messages/batch_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/messages/beta_message_batch.py">BetaMessageBatch</a></code>
- <code title="get /v1/messages/batches/{message_batch_id}?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">retrieve</a>(message_batch_id) -> <a href="./src/anthropic/types/beta/messages/beta_message_batch.py">BetaMessageBatch</a></code>
- <code title="get /v1/messages/batches?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">list</a>(\*\*<a href="src/anthropic/types/beta/messages/batch_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/messages/beta_message_batch.py">SyncPage[BetaMessageBatch]</a></code>
- <code title="post /v1/messages/batches/{message_batch_id}/cancel?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">cancel</a>(message_batch_id) -> <a href="./src/anthropic/types/beta/messages/beta_message_batch.py">BetaMessageBatch</a></code>
- <code title="get /v1/messages/batches/{message_batch_id}/results?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">results</a>(message_batch_id) -> BinaryAPIResponse</code>

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
