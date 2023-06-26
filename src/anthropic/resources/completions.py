# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import List, overload
from typing_extensions import Literal

from ..types import Completion, completion_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import required_args, maybe_transform
from .._resource import SyncAPIResource, AsyncAPIResource
from .._streaming import Stream, AsyncStream
from .._base_client import make_request_options

__all__ = ["Completions", "AsyncCompletions"]


class Completions(SyncAPIResource):
    @overload
    def create(
        self,
        *,
        max_tokens_to_sample: int,
        model: str,
        prompt: str,
        metadata: completion_create_params.CompletionRequestNonStreamingMetadata | NotGiven = NOT_GIVEN,
        stop_sequences: List[str] | NotGiven = NOT_GIVEN,
        stream: Literal[False] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> Completion:
        """
        Create a completion

        Args:
          max_tokens_to_sample: The maximum number of tokens to generate before stopping.

              Note that our models may stop _before_ reaching this maximum. This parameter
              only specifies the absolute maximum number of tokens to generate.

          model: The model that will complete your prompt.

              As we improve Claude, we develop new versions of it that you can query. This
              controls which version of Claude answers your request. Right now we are offering
              two model families: Claude and Claude Instant.

              Specifiying any of the following models will automatically switch to you the
              newest compatible models as they are released:

              - `"claude-1"`: Our largest model, ideal for a wide range of more complex tasks.
              - `"claude-1-100k"`: An enhanced version of `claude-1` with a 100,000 token
                (roughly 75,000 word) context window. Ideal for summarizing, analyzing, and
                querying long documents and conversations for nuanced understanding of complex
                topics and relationships across very long spans of text.
              - `"claude-instant-1"`: A smaller model with far lower latency, sampling at
                roughly 40 words/sec! Its output quality is somewhat lower than the latest
                `claude-1` model, particularly for complex tasks. However, it is much less
                expensive and blazing fast. We believe that this model provides more than
                adequate performance on a range of tasks including text classification,
                summarization, and lightweight chat applications, as well as search result
                summarization.
              - `"claude-instant-1-100k"`: An enhanced version of `claude-instant-1` with a
                100,000 token context window that retains its performance. Well-suited for
                high throughput use cases needing both speed and additional context, allowing
                deeper understanding from extended conversations and documents.

              You can also select specific sub-versions of the above models:

              - `"claude-1.3"`: Compared to `claude-1.2`, it's more robust against red-team
                inputs, better at precise instruction-following, better at code, and better
                and non-English dialogue and writing.
              - `"claude-1.3-100k"`: An enhanced version of `claude-1.3` with a 100,000 token
                (roughly 75,000 word) context window.
              - `"claude-1.2"`: An improved version of `claude-1`. It is slightly improved at
                general helpfulness, instruction following, coding, and other tasks. It is
                also considerably better with non-English languages. This model also has the
                ability to role play (in harmless ways) more consistently, and it defaults to
                writing somewhat longer and more thorough responses.
              - `"claude-1.0"`: An earlier version of `claude-1`.
              - `"claude-instant-1.1"`: Our latest version of `claude-instant-1`. It is better
                than `claude-instant-1.0` at a wide variety of tasks including writing,
                coding, and instruction following. It performs better on academic benchmarks,
                including math, reading comprehension, and coding tests. It is also more
                robust against red-teaming inputs.
              - `"claude-instant-1.1-100k"`: An enhanced version of `claude-instant-1.1` with
                a 100,000 token context window that retains its lightning fast 40 word/sec
                performance.
              - `"claude-instant-1.0"`: An earlier version of `claude-instant-1`.

          prompt: The prompt that you want Claude to complete.

              For proper response generation you will need to format your prompt as follows:

              ```javascript
              const userQuestion = r"Why is the sky blue?";
              const prompt = `\n\nHuman: ${userQuestion}\n\nAssistant:`;
              ```

              See our [comments on prompts](https://console.anthropic.com/docs/prompt-design)
              for more context.

          metadata: An object describing metadata about the request.

          stop_sequences: Sequences that will cause the model to stop generating completion text.

              Our models stop on `"\n\nHuman:"`, and may include additional built-in stop
              sequences in the future. By providing the stop_sequences parameter, you may
              include additional strings that will cause the model to stop generating.

          stream: Whether to incrementally stream the response using server-sent events.

              See
              [this guide to SSE events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
              for details.

          temperature: Amount of randomness injected into the response.

              Defaults to 1. Ranges from 0 to 1. Use temp closer to 0 for analytical /
              multiple choice, and closer to 1 for creative and generative tasks.

          top_k: Only sample from the top K options for each subsequent token.

              Used to remove "long tail" low probability responses.
              [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

          top_p: Use nucleus sampling.

              In nucleus sampling, we compute the cumulative distribution over all the options
              for each subsequent token in decreasing probability order and cut it off once it
              reaches a particular probability specified by `top_p`. You should either alter
              `temperature` or `top_p`, but not both.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        max_tokens_to_sample: int,
        model: str,
        prompt: str,
        stream: Literal[True],
        metadata: completion_create_params.CompletionRequestStreamingMetadata | NotGiven = NOT_GIVEN,
        stop_sequences: List[str] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> Stream[Completion]:
        """
        Create a completion

        Args:
          max_tokens_to_sample: The maximum number of tokens to generate before stopping.

              Note that our models may stop _before_ reaching this maximum. This parameter
              only specifies the absolute maximum number of tokens to generate.

          model: The model that will complete your prompt.

              As we improve Claude, we develop new versions of it that you can query. This
              controls which version of Claude answers your request. Right now we are offering
              two model families: Claude and Claude Instant.

              Specifiying any of the following models will automatically switch to you the
              newest compatible models as they are released:

              - `"claude-1"`: Our largest model, ideal for a wide range of more complex tasks.
              - `"claude-1-100k"`: An enhanced version of `claude-1` with a 100,000 token
                (roughly 75,000 word) context window. Ideal for summarizing, analyzing, and
                querying long documents and conversations for nuanced understanding of complex
                topics and relationships across very long spans of text.
              - `"claude-instant-1"`: A smaller model with far lower latency, sampling at
                roughly 40 words/sec! Its output quality is somewhat lower than the latest
                `claude-1` model, particularly for complex tasks. However, it is much less
                expensive and blazing fast. We believe that this model provides more than
                adequate performance on a range of tasks including text classification,
                summarization, and lightweight chat applications, as well as search result
                summarization.
              - `"claude-instant-1-100k"`: An enhanced version of `claude-instant-1` with a
                100,000 token context window that retains its performance. Well-suited for
                high throughput use cases needing both speed and additional context, allowing
                deeper understanding from extended conversations and documents.

              You can also select specific sub-versions of the above models:

              - `"claude-1.3"`: Compared to `claude-1.2`, it's more robust against red-team
                inputs, better at precise instruction-following, better at code, and better
                and non-English dialogue and writing.
              - `"claude-1.3-100k"`: An enhanced version of `claude-1.3` with a 100,000 token
                (roughly 75,000 word) context window.
              - `"claude-1.2"`: An improved version of `claude-1`. It is slightly improved at
                general helpfulness, instruction following, coding, and other tasks. It is
                also considerably better with non-English languages. This model also has the
                ability to role play (in harmless ways) more consistently, and it defaults to
                writing somewhat longer and more thorough responses.
              - `"claude-1.0"`: An earlier version of `claude-1`.
              - `"claude-instant-1.1"`: Our latest version of `claude-instant-1`. It is better
                than `claude-instant-1.0` at a wide variety of tasks including writing,
                coding, and instruction following. It performs better on academic benchmarks,
                including math, reading comprehension, and coding tests. It is also more
                robust against red-teaming inputs.
              - `"claude-instant-1.1-100k"`: An enhanced version of `claude-instant-1.1` with
                a 100,000 token context window that retains its lightning fast 40 word/sec
                performance.
              - `"claude-instant-1.0"`: An earlier version of `claude-instant-1`.

          prompt: The prompt that you want Claude to complete.

              For proper response generation you will need to format your prompt as follows:

              ```javascript
              const userQuestion = r"Why is the sky blue?";
              const prompt = `\n\nHuman: ${userQuestion}\n\nAssistant:`;
              ```

              See our [comments on prompts](https://console.anthropic.com/docs/prompt-design)
              for more context.

          stream: Whether to incrementally stream the response using server-sent events.

              See
              [this guide to SSE events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
              for details.

          metadata: An object describing metadata about the request.

          stop_sequences: Sequences that will cause the model to stop generating completion text.

              Our models stop on `"\n\nHuman:"`, and may include additional built-in stop
              sequences in the future. By providing the stop_sequences parameter, you may
              include additional strings that will cause the model to stop generating.

          temperature: Amount of randomness injected into the response.

              Defaults to 1. Ranges from 0 to 1. Use temp closer to 0 for analytical /
              multiple choice, and closer to 1 for creative and generative tasks.

          top_k: Only sample from the top K options for each subsequent token.

              Used to remove "long tail" low probability responses.
              [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

          top_p: Use nucleus sampling.

              In nucleus sampling, we compute the cumulative distribution over all the options
              for each subsequent token in decreasing probability order and cut it off once it
              reaches a particular probability specified by `top_p`. You should either alter
              `temperature` or `top_p`, but not both.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["max_tokens_to_sample", "model", "prompt"], ["max_tokens_to_sample", "model", "prompt", "stream"])
    def create(
        self,
        *,
        max_tokens_to_sample: int,
        model: str,
        prompt: str,
        metadata: completion_create_params.CompletionRequestNonStreamingMetadata
        | completion_create_params.CompletionRequestStreamingMetadata
        | NotGiven = NOT_GIVEN,
        stop_sequences: List[str] | NotGiven = NOT_GIVEN,
        stream: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> Completion | Stream[Completion]:
        return self._post(
            "/v1/complete",
            body=maybe_transform(
                {
                    "max_tokens_to_sample": max_tokens_to_sample,
                    "model": model,
                    "prompt": prompt,
                    "metadata": metadata,
                    "stop_sequences": stop_sequences,
                    "stream": stream,
                    "temperature": temperature,
                    "top_k": top_k,
                    "top_p": top_p,
                },
                completion_create_params.CompletionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Completion,
            stream=stream or False,
            stream_cls=Stream[Completion],
        )


class AsyncCompletions(AsyncAPIResource):
    @overload
    async def create(
        self,
        *,
        max_tokens_to_sample: int,
        model: str,
        prompt: str,
        metadata: completion_create_params.CompletionRequestNonStreamingMetadata | NotGiven = NOT_GIVEN,
        stop_sequences: List[str] | NotGiven = NOT_GIVEN,
        stream: Literal[False] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> Completion:
        """
        Create a completion

        Args:
          max_tokens_to_sample: The maximum number of tokens to generate before stopping.

              Note that our models may stop _before_ reaching this maximum. This parameter
              only specifies the absolute maximum number of tokens to generate.

          model: The model that will complete your prompt.

              As we improve Claude, we develop new versions of it that you can query. This
              controls which version of Claude answers your request. Right now we are offering
              two model families: Claude and Claude Instant.

              Specifiying any of the following models will automatically switch to you the
              newest compatible models as they are released:

              - `"claude-1"`: Our largest model, ideal for a wide range of more complex tasks.
              - `"claude-1-100k"`: An enhanced version of `claude-1` with a 100,000 token
                (roughly 75,000 word) context window. Ideal for summarizing, analyzing, and
                querying long documents and conversations for nuanced understanding of complex
                topics and relationships across very long spans of text.
              - `"claude-instant-1"`: A smaller model with far lower latency, sampling at
                roughly 40 words/sec! Its output quality is somewhat lower than the latest
                `claude-1` model, particularly for complex tasks. However, it is much less
                expensive and blazing fast. We believe that this model provides more than
                adequate performance on a range of tasks including text classification,
                summarization, and lightweight chat applications, as well as search result
                summarization.
              - `"claude-instant-1-100k"`: An enhanced version of `claude-instant-1` with a
                100,000 token context window that retains its performance. Well-suited for
                high throughput use cases needing both speed and additional context, allowing
                deeper understanding from extended conversations and documents.

              You can also select specific sub-versions of the above models:

              - `"claude-1.3"`: Compared to `claude-1.2`, it's more robust against red-team
                inputs, better at precise instruction-following, better at code, and better
                and non-English dialogue and writing.
              - `"claude-1.3-100k"`: An enhanced version of `claude-1.3` with a 100,000 token
                (roughly 75,000 word) context window.
              - `"claude-1.2"`: An improved version of `claude-1`. It is slightly improved at
                general helpfulness, instruction following, coding, and other tasks. It is
                also considerably better with non-English languages. This model also has the
                ability to role play (in harmless ways) more consistently, and it defaults to
                writing somewhat longer and more thorough responses.
              - `"claude-1.0"`: An earlier version of `claude-1`.
              - `"claude-instant-1.1"`: Our latest version of `claude-instant-1`. It is better
                than `claude-instant-1.0` at a wide variety of tasks including writing,
                coding, and instruction following. It performs better on academic benchmarks,
                including math, reading comprehension, and coding tests. It is also more
                robust against red-teaming inputs.
              - `"claude-instant-1.1-100k"`: An enhanced version of `claude-instant-1.1` with
                a 100,000 token context window that retains its lightning fast 40 word/sec
                performance.
              - `"claude-instant-1.0"`: An earlier version of `claude-instant-1`.

          prompt: The prompt that you want Claude to complete.

              For proper response generation you will need to format your prompt as follows:

              ```javascript
              const userQuestion = r"Why is the sky blue?";
              const prompt = `\n\nHuman: ${userQuestion}\n\nAssistant:`;
              ```

              See our [comments on prompts](https://console.anthropic.com/docs/prompt-design)
              for more context.

          metadata: An object describing metadata about the request.

          stop_sequences: Sequences that will cause the model to stop generating completion text.

              Our models stop on `"\n\nHuman:"`, and may include additional built-in stop
              sequences in the future. By providing the stop_sequences parameter, you may
              include additional strings that will cause the model to stop generating.

          stream: Whether to incrementally stream the response using server-sent events.

              See
              [this guide to SSE events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
              for details.

          temperature: Amount of randomness injected into the response.

              Defaults to 1. Ranges from 0 to 1. Use temp closer to 0 for analytical /
              multiple choice, and closer to 1 for creative and generative tasks.

          top_k: Only sample from the top K options for each subsequent token.

              Used to remove "long tail" low probability responses.
              [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

          top_p: Use nucleus sampling.

              In nucleus sampling, we compute the cumulative distribution over all the options
              for each subsequent token in decreasing probability order and cut it off once it
              reaches a particular probability specified by `top_p`. You should either alter
              `temperature` or `top_p`, but not both.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        max_tokens_to_sample: int,
        model: str,
        prompt: str,
        stream: Literal[True],
        metadata: completion_create_params.CompletionRequestStreamingMetadata | NotGiven = NOT_GIVEN,
        stop_sequences: List[str] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> AsyncStream[Completion]:
        """
        Create a completion

        Args:
          max_tokens_to_sample: The maximum number of tokens to generate before stopping.

              Note that our models may stop _before_ reaching this maximum. This parameter
              only specifies the absolute maximum number of tokens to generate.

          model: The model that will complete your prompt.

              As we improve Claude, we develop new versions of it that you can query. This
              controls which version of Claude answers your request. Right now we are offering
              two model families: Claude and Claude Instant.

              Specifiying any of the following models will automatically switch to you the
              newest compatible models as they are released:

              - `"claude-1"`: Our largest model, ideal for a wide range of more complex tasks.
              - `"claude-1-100k"`: An enhanced version of `claude-1` with a 100,000 token
                (roughly 75,000 word) context window. Ideal for summarizing, analyzing, and
                querying long documents and conversations for nuanced understanding of complex
                topics and relationships across very long spans of text.
              - `"claude-instant-1"`: A smaller model with far lower latency, sampling at
                roughly 40 words/sec! Its output quality is somewhat lower than the latest
                `claude-1` model, particularly for complex tasks. However, it is much less
                expensive and blazing fast. We believe that this model provides more than
                adequate performance on a range of tasks including text classification,
                summarization, and lightweight chat applications, as well as search result
                summarization.
              - `"claude-instant-1-100k"`: An enhanced version of `claude-instant-1` with a
                100,000 token context window that retains its performance. Well-suited for
                high throughput use cases needing both speed and additional context, allowing
                deeper understanding from extended conversations and documents.

              You can also select specific sub-versions of the above models:

              - `"claude-1.3"`: Compared to `claude-1.2`, it's more robust against red-team
                inputs, better at precise instruction-following, better at code, and better
                and non-English dialogue and writing.
              - `"claude-1.3-100k"`: An enhanced version of `claude-1.3` with a 100,000 token
                (roughly 75,000 word) context window.
              - `"claude-1.2"`: An improved version of `claude-1`. It is slightly improved at
                general helpfulness, instruction following, coding, and other tasks. It is
                also considerably better with non-English languages. This model also has the
                ability to role play (in harmless ways) more consistently, and it defaults to
                writing somewhat longer and more thorough responses.
              - `"claude-1.0"`: An earlier version of `claude-1`.
              - `"claude-instant-1.1"`: Our latest version of `claude-instant-1`. It is better
                than `claude-instant-1.0` at a wide variety of tasks including writing,
                coding, and instruction following. It performs better on academic benchmarks,
                including math, reading comprehension, and coding tests. It is also more
                robust against red-teaming inputs.
              - `"claude-instant-1.1-100k"`: An enhanced version of `claude-instant-1.1` with
                a 100,000 token context window that retains its lightning fast 40 word/sec
                performance.
              - `"claude-instant-1.0"`: An earlier version of `claude-instant-1`.

          prompt: The prompt that you want Claude to complete.

              For proper response generation you will need to format your prompt as follows:

              ```javascript
              const userQuestion = r"Why is the sky blue?";
              const prompt = `\n\nHuman: ${userQuestion}\n\nAssistant:`;
              ```

              See our [comments on prompts](https://console.anthropic.com/docs/prompt-design)
              for more context.

          stream: Whether to incrementally stream the response using server-sent events.

              See
              [this guide to SSE events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
              for details.

          metadata: An object describing metadata about the request.

          stop_sequences: Sequences that will cause the model to stop generating completion text.

              Our models stop on `"\n\nHuman:"`, and may include additional built-in stop
              sequences in the future. By providing the stop_sequences parameter, you may
              include additional strings that will cause the model to stop generating.

          temperature: Amount of randomness injected into the response.

              Defaults to 1. Ranges from 0 to 1. Use temp closer to 0 for analytical /
              multiple choice, and closer to 1 for creative and generative tasks.

          top_k: Only sample from the top K options for each subsequent token.

              Used to remove "long tail" low probability responses.
              [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

          top_p: Use nucleus sampling.

              In nucleus sampling, we compute the cumulative distribution over all the options
              for each subsequent token in decreasing probability order and cut it off once it
              reaches a particular probability specified by `top_p`. You should either alter
              `temperature` or `top_p`, but not both.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["max_tokens_to_sample", "model", "prompt"], ["max_tokens_to_sample", "model", "prompt", "stream"])
    async def create(
        self,
        *,
        max_tokens_to_sample: int,
        model: str,
        prompt: str,
        metadata: completion_create_params.CompletionRequestNonStreamingMetadata
        | completion_create_params.CompletionRequestStreamingMetadata
        | NotGiven = NOT_GIVEN,
        stop_sequences: List[str] | NotGiven = NOT_GIVEN,
        stream: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> Completion | AsyncStream[Completion]:
        return await self._post(
            "/v1/complete",
            body=maybe_transform(
                {
                    "max_tokens_to_sample": max_tokens_to_sample,
                    "model": model,
                    "prompt": prompt,
                    "metadata": metadata,
                    "stop_sequences": stop_sequences,
                    "stream": stream,
                    "temperature": temperature,
                    "top_k": top_k,
                    "top_p": top_p,
                },
                completion_create_params.CompletionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Completion,
            stream=stream or False,
            stream_cls=AsyncStream[Completion],
        )
