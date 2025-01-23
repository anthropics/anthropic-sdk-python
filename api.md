# Shared Types

```python
from anthropic.types import (
    APIErrorObject,
    AuthenticationError,
    BillingError,
    ErrorObject,
    ErrorResponse,
    GatewayTimeoutError,
    InvalidRequestError,
    NotFoundError,
    OverloadedError,
    PermissionError,
    RateLimitError,
)
```

# Messages

Types:

```python
from anthropic.types import (
    Base64PDFSource,
    CacheControlEphemeral,
    CitationCharLocation,
    CitationCharLocationParam,
    CitationContentBlockLocation,
    CitationContentBlockLocationParam,
    CitationPageLocation,
    CitationPageLocationParam,
    CitationsConfigParam,
    CitationsDelta,
    ContentBlock,
    ContentBlockDeltaEvent,
    ContentBlockParam,
    ContentBlockSource,
    ContentBlockSourceContent,
    ContentBlockStartEvent,
    ContentBlockStopEvent,
    DocumentBlockParam,
    ImageBlockParam,
    InputJSONDelta,
    Message,
    MessageDeltaEvent,
    MessageDeltaUsage,
    MessageParam,
    MessageStartEvent,
    MessageStopEvent,
    MessageStreamEvent,
    MessageTokensCount,
    Metadata,
    Model,
    PlainTextSource,
    RawContentBlockDeltaEvent,
    RawContentBlockStartEvent,
    RawContentBlockStopEvent,
    RawMessageDeltaEvent,
    RawMessageStartEvent,
    RawMessageStopEvent,
    RawMessageStreamEvent,
    TextBlock,
    TextBlockParam,
    TextCitation,
    TextCitationParam,
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

- <code title="post /v1/messages">client.messages.<a href="./src/anthropic/resources/messages/messages.py">create</a>(\*\*<a href="src/anthropic/types/message_create_params.py">params</a>) -> <a href="./src/anthropic/types/message.py">Message</a></code>
- <code>client.messages.<a href="./src/anthropic/resources/messages.py">stream</a>(\*args) -> MessageStreamManager[MessageStream] | MessageStreamManager[MessageStreamT]</code>
- <code title="post /v1/messages/count_tokens">client.messages.<a href="./src/anthropic/resources/messages/messages.py">count_tokens</a>(\*\*<a href="src/anthropic/types/message_count_tokens_params.py">params</a>) -> <a href="./src/anthropic/types/message_tokens_count.py">MessageTokensCount</a></code>

## Batches

Types:

```python
from anthropic.types.messages import (
    DeletedMessageBatch,
    MessageBatch,
    MessageBatchCanceledResult,
    MessageBatchErroredResult,
    MessageBatchExpiredResult,
    MessageBatchIndividualResponse,
    MessageBatchRequestCounts,
    MessageBatchResult,
    MessageBatchSucceededResult,
)
```

Methods:

- <code title="post /v1/messages/batches">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">create</a>(\*\*<a href="src/anthropic/types/messages/batch_create_params.py">params</a>) -> <a href="./src/anthropic/types/messages/message_batch.py">MessageBatch</a></code>
- <code title="get /v1/messages/batches/{message_batch_id}">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">retrieve</a>(message_batch_id) -> <a href="./src/anthropic/types/messages/message_batch.py">MessageBatch</a></code>
- <code title="get /v1/messages/batches">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">list</a>(\*\*<a href="src/anthropic/types/messages/batch_list_params.py">params</a>) -> <a href="./src/anthropic/types/messages/message_batch.py">SyncPage[MessageBatch]</a></code>
- <code title="delete /v1/messages/batches/{message_batch_id}">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">delete</a>(message_batch_id) -> <a href="./src/anthropic/types/messages/deleted_message_batch.py">DeletedMessageBatch</a></code>
- <code title="post /v1/messages/batches/{message_batch_id}/cancel">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">cancel</a>(message_batch_id) -> <a href="./src/anthropic/types/messages/message_batch.py">MessageBatch</a></code>
- <code title="get /v1/messages/batches/{message_batch_id}/results">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">results</a>(message_batch_id) -> <a href="./src/anthropic/types/messages/message_batch_individual_response.py">JSONLDecoder[MessageBatchIndividualResponse]</a></code>

# Models

Types:

```python
from anthropic.types import ModelInfo
```

Methods:

- <code title="get /v1/models/{model_id}">client.models.<a href="./src/anthropic/resources/models.py">retrieve</a>(model_id) -> <a href="./src/anthropic/types/model_info.py">ModelInfo</a></code>
- <code title="get /v1/models">client.models.<a href="./src/anthropic/resources/models.py">list</a>(\*\*<a href="src/anthropic/types/model_list_params.py">params</a>) -> <a href="./src/anthropic/types/model_info.py">SyncPage[ModelInfo]</a></code>

# Beta

Types:

```python
from anthropic.types import (
    AnthropicBeta,
    BetaAPIError,
    BetaAuthenticationError,
    BetaBillingError,
    BetaError,
    BetaErrorResponse,
    BetaGatewayTimeoutError,
    BetaInvalidRequestError,
    BetaNotFoundError,
    BetaOverloadedError,
    BetaPermissionError,
    BetaRateLimitError,
)
```

## Models

Types:

```python
from anthropic.types.beta import BetaModelInfo
```

Methods:

- <code title="get /v1/models/{model_id}?beta=true">client.beta.models.<a href="./src/anthropic/resources/beta/models.py">retrieve</a>(model_id) -> <a href="./src/anthropic/types/beta/beta_model_info.py">BetaModelInfo</a></code>
- <code title="get /v1/models?beta=true">client.beta.models.<a href="./src/anthropic/resources/beta/models.py">list</a>(\*\*<a href="src/anthropic/types/beta/model_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_model_info.py">SyncPage[BetaModelInfo]</a></code>

## Messages

Types:

```python
from anthropic.types.beta import (
    BetaBase64PDFBlock,
    BetaBase64PDFSource,
    BetaCacheControlEphemeral,
    BetaCitationCharLocation,
    BetaCitationCharLocationParam,
    BetaCitationContentBlockLocation,
    BetaCitationContentBlockLocationParam,
    BetaCitationPageLocation,
    BetaCitationPageLocationParam,
    BetaCitationsConfigParam,
    BetaCitationsDelta,
    BetaContentBlock,
    BetaContentBlockParam,
    BetaContentBlockSource,
    BetaContentBlockSourceContent,
    BetaImageBlockParam,
    BetaInputJSONDelta,
    BetaMessage,
    BetaMessageDeltaUsage,
    BetaMessageParam,
    BetaMessageTokensCount,
    BetaMetadata,
    BetaPlainTextSource,
    BetaRawContentBlockDeltaEvent,
    BetaRawContentBlockStartEvent,
    BetaRawContentBlockStopEvent,
    BetaRawMessageDeltaEvent,
    BetaRawMessageStartEvent,
    BetaRawMessageStopEvent,
    BetaRawMessageStreamEvent,
    BetaTextBlock,
    BetaTextBlockParam,
    BetaTextCitation,
    BetaTextCitationParam,
    BetaTextDelta,
    BetaTool,
    BetaToolBash20241022,
    BetaToolChoice,
    BetaToolChoiceAny,
    BetaToolChoiceAuto,
    BetaToolChoiceTool,
    BetaToolComputerUse20241022,
    BetaToolResultBlockParam,
    BetaToolTextEditor20241022,
    BetaToolUnion,
    BetaToolUseBlock,
    BetaToolUseBlockParam,
    BetaUsage,
)
```

Methods:

- <code title="post /v1/messages?beta=true">client.beta.messages.<a href="./src/anthropic/resources/beta/messages/messages.py">create</a>(\*\*<a href="src/anthropic/types/beta/message_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_message.py">BetaMessage</a></code>
- <code title="post /v1/messages/count_tokens?beta=true">client.beta.messages.<a href="./src/anthropic/resources/beta/messages/messages.py">count_tokens</a>(\*\*<a href="src/anthropic/types/beta/message_count_tokens_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_message_tokens_count.py">BetaMessageTokensCount</a></code>

### Batches

Types:

```python
from anthropic.types.beta.messages import (
    BetaDeletedMessageBatch,
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
- <code title="delete /v1/messages/batches/{message_batch_id}?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">delete</a>(message_batch_id) -> <a href="./src/anthropic/types/beta/messages/beta_deleted_message_batch.py">BetaDeletedMessageBatch</a></code>
- <code title="post /v1/messages/batches/{message_batch_id}/cancel?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">cancel</a>(message_batch_id) -> <a href="./src/anthropic/types/beta/messages/beta_message_batch.py">BetaMessageBatch</a></code>
- <code title="get /v1/messages/batches/{message_batch_id}/results?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">results</a>(message_batch_id) -> <a href="./src/anthropic/types/beta/messages/beta_message_batch_individual_response.py">JSONLDecoder[BetaMessageBatchIndividualResponse]</a></code>
