# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "CompletionCreateParams",
    "CompletionRequestNonStreaming",
    "CompletionRequestNonStreamingMetadata",
    "CompletionRequestStreaming",
    "CompletionRequestStreamingMetadata",
]


class CompletionRequestNonStreaming(TypedDict, total=False):
    max_tokens_to_sample: Required[int]
    """The maximum number of tokens to generate before stopping.

    Note that our models may stop _before_ reaching this maximum. This parameter
    only specifies the absolute maximum number of tokens to generate.
    """

    model: Required[str]
    """The model that will complete your prompt.

    As we improve Claude, we develop new versions of it that you can query. This
    parameter controls which version of Claude answers your request. Right now we
    are offering two model families: Claude, and Claude Instant. You can use them by
    setting `model` to `"claude-2"` or `"claude-instant-1"`, respectively. See
    [models](https://docs.anthropic.com/claude/reference/selecting-a-model) for
    additional details.
    """

    prompt: Required[str]
    """The prompt that you want Claude to complete.

    For proper response generation you will need to format your prompt as follows:

    ```javascript
    const userQuestion = r"Why is the sky blue?";
    const prompt = `\n\nHuman: ${userQuestion}\n\nAssistant:`;
    ```

    See our
    [comments on prompts](https://docs.anthropic.com/claude/docs/introduction-to-prompt-design)
    for more context.
    """

    metadata: CompletionRequestNonStreamingMetadata
    """An object describing metadata about the request."""

    stop_sequences: List[str]
    """Sequences that will cause the model to stop generating completion text.

    Our models stop on `"\n\nHuman:"`, and may include additional built-in stop
    sequences in the future. By providing the stop_sequences parameter, you may
    include additional strings that will cause the model to stop generating.
    """

    stream: Literal[False]
    """Whether to incrementally stream the response using server-sent events.

    See
    [this guide to SSE events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
    for details.
    """

    temperature: float
    """Amount of randomness injected into the response.

    Defaults to 1. Ranges from 0 to 1. Use temp closer to 0 for analytical /
    multiple choice, and closer to 1 for creative and generative tasks.
    """

    top_k: int
    """Only sample from the top K options for each subsequent token.

    Used to remove "long tail" low probability responses.
    [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).
    """

    top_p: float
    """Use nucleus sampling.

    In nucleus sampling, we compute the cumulative distribution over all the options
    for each subsequent token in decreasing probability order and cut it off once it
    reaches a particular probability specified by `top_p`. You should either alter
    `temperature` or `top_p`, but not both.
    """


class CompletionRequestNonStreamingMetadata(TypedDict, total=False):
    user_id: str
    """An external identifier for the user who is associated with the request.

    This should be a uuid, hash value, or other opaque identifier. Anthropic may use
    this id to help detect abuse. Do not include any identifying information such as
    name, email address, or phone number.
    """


class CompletionRequestStreaming(TypedDict, total=False):
    max_tokens_to_sample: Required[int]
    """The maximum number of tokens to generate before stopping.

    Note that our models may stop _before_ reaching this maximum. This parameter
    only specifies the absolute maximum number of tokens to generate.
    """

    model: Required[str]
    """The model that will complete your prompt.

    As we improve Claude, we develop new versions of it that you can query. This
    parameter controls which version of Claude answers your request. Right now we
    are offering two model families: Claude, and Claude Instant. You can use them by
    setting `model` to `"claude-2"` or `"claude-instant-1"`, respectively. See
    [models](https://docs.anthropic.com/claude/reference/selecting-a-model) for
    additional details.
    """

    prompt: Required[str]
    """The prompt that you want Claude to complete.

    For proper response generation you will need to format your prompt as follows:

    ```javascript
    const userQuestion = r"Why is the sky blue?";
    const prompt = `\n\nHuman: ${userQuestion}\n\nAssistant:`;
    ```

    See our
    [comments on prompts](https://docs.anthropic.com/claude/docs/introduction-to-prompt-design)
    for more context.
    """

    stream: Required[Literal[True]]
    """Whether to incrementally stream the response using server-sent events.

    See
    [this guide to SSE events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
    for details.
    """

    metadata: CompletionRequestStreamingMetadata
    """An object describing metadata about the request."""

    stop_sequences: List[str]
    """Sequences that will cause the model to stop generating completion text.

    Our models stop on `"\n\nHuman:"`, and may include additional built-in stop
    sequences in the future. By providing the stop_sequences parameter, you may
    include additional strings that will cause the model to stop generating.
    """

    temperature: float
    """Amount of randomness injected into the response.

    Defaults to 1. Ranges from 0 to 1. Use temp closer to 0 for analytical /
    multiple choice, and closer to 1 for creative and generative tasks.
    """

    top_k: int
    """Only sample from the top K options for each subsequent token.

    Used to remove "long tail" low probability responses.
    [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).
    """

    top_p: float
    """Use nucleus sampling.

    In nucleus sampling, we compute the cumulative distribution over all the options
    for each subsequent token in decreasing probability order and cut it off once it
    reaches a particular probability specified by `top_p`. You should either alter
    `temperature` or `top_p`, but not both.
    """


class CompletionRequestStreamingMetadata(TypedDict, total=False):
    user_id: str
    """An external identifier for the user who is associated with the request.

    This should be a uuid, hash value, or other opaque identifier. Anthropic may use
    this id to help detect abuse. Do not include any identifying information such as
    name, email address, or phone number.
    """


CompletionCreateParams = Union[CompletionRequestNonStreaming, CompletionRequestStreaming]
