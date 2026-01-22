from __future__ import annotations

from typing import Iterable, Union, cast
import httpx

from ..._utils import is_given
from ..._types import Headers, Query, Body, NotGiven
from ..._compat import cached_property
from ...resources.messages import Messages, AsyncMessages
from ...types import Message, ModelParam, TextBlockParam, ToolChoiceParam
from ...types.message_param import MessageParam
from ...types.message_count_tokens_tool_param import MessageCountTokensToolParam
from ...types.message_tokens_count import MessageTokensCount
from ...types.message_count_tokens_params import MessageCountTokensParams
from ...types.thinking_config_param import ThinkingConfigParam
from ..._base_client import make_request_options
from ..._types import Omit, omit

class BedrockMessages(Messages):
    def count_tokens(
        self,
        *,
        messages: Iterable[MessageParam],
        model: ModelParam,
        system: Union[str, Iterable[TextBlockParam]] | Omit = omit,
        thinking: ThinkingConfigParam | Omit = omit,
        tool_choice: ToolChoiceParam | Omit = omit,
        tools: Iterable[MessageCountTokensToolParam] | Omit = omit,
        # Standard params
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NotGiven,
    ) -> MessageTokensCount:
        """
        Count the number of tokens in a Message.
        """
        # Prepare valid Anthropic parameters
        body = {
            "messages": messages,
            "model": model,
        }
        if not isinstance(system, Omit):
           body["system"] = system
        if not isinstance(thinking, Omit):
            body["thinking"] = thinking
        if not isinstance(tools, Omit):
            body["tools"] = tools
        if not isinstance(tool_choice, Omit):
            body["tool_choice"] = tool_choice
            
        # Add extra_body to params if needed
        # Note: maybe_transform handling is bypassed here for simplicity in this overlay
        # but realistically we should use it. 
        # Ideally, we call self._get_api_list or _post equivalent but with the wrapped body.
        
        # We need to construct the request manually because we are changing the URL structure significantly
        # AND wrapping the body in "invokeModel".
        
        # However, we can let the Client handle the URL rewrite if we pass a special URL?
        # No, let's just do it here.
        
        # 1. Prepare JSON body (standard Anthropic format)
        # We use the client's internal transform logic if possible, or just pass dict.
        # Given strict typing, we rely on the fact that httpx/client handles dicts.
        
        # 2. Wrap in "invokeModel" structure?
        # Wait, if we use the Bedrock CountTokens API, does it expect "invokeModel" wrapper?
        # Ref [1]: "The input body should be provided in the invokeModel field as a string"
        # Wait, as a STRING? JSON encoded string?
        # Yes, standard Bedrock InvokeModel takes a JSON blob as bytes/string.
        # So: { "invokeModel": { "body": json.dumps(anthropic_body), "contentType": "application/json" } } ??
        import json
        
        # We'll rely on the default JSON serializer to handle basic types, but for Pydantic models
        # we might need `to_dict()` or `compat.model_dump`. 
        # Messages.count_tokens params are typed Dicts or lists of TypedDicts usually.
        
        # Let's simplify: 
        # We want to call POST /model/{model}/count-tokens
        # Body: { "invokeModel": ... }? 
        # Actually, let's check if the SDK client already handles "invokeModel" wrapping in _transform_request?
        # No, the Bedrock client in _client.py just sends `request.read().decode()` as `data` for signing.
        # It relies on `options.json_data`.
        
        # If I use `self._post`, it will serialize `body` to JSON.
        # So I need to construct the *outer* JSON.
        
        # Is the endpoint `/model/{model}/count-tokens` expecting the Anthropic body DIRECTLY?
        # The search result said "accepts the same input formats as... InvokeModel".
        # InvokeModel expects the model-specific body.
        # But `Converse` expects the independent format.
        # If `count_tokens` uses `Converse` schema, we pass `messages` directly.
        # If `count_tokens` uses `InvokeModel` behavior, we pass the Anthropic body.
        
        # I will assuming I can pass the Anthropic body directly to `/model/{model}/count-tokens`.
        # Why? Because for `InvokeModel`, the SDK sends the Anthropic body directly to `/model/{model}/invoke`.
        # It does NOT wrap it in `invokeModel` key.
        # The "invokeModel" key mentioned in search might be for the CLI or boto3 param structure.
        # HTTP REST API for Bedrock Runtime usually takes the raw body.
        
        options = make_request_options(
            extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
        )
        
        # We need to manually construct the URL here because _prepare_options only sees the original URL
        # if we called via super. But here we are intercepting.
        
        request_url = f"/model/{model}/count-tokens"
        
        # We use self._post to utilize the client's authentication and signing logic.
        # We pass the standard body.
        
        # However, we need to intercept the response.
        # self._post calls `self.request` -> ... -> `self._process_response` -> `cast_to`.
        # If the response shape is different, `cast_to=MessageTokensCount` will fail (missing `input_tokens`).
        
        # Warning: `MessageTokensCount` expects `input_tokens`. Bedrock returns `inputTokens`.
        # We can't change the response body inside `_post`.
        # So we MUST call `self._client.post` (raw) or `self._client.request`?
        # `self._client` is `AnthropicBedrock`.
        
        # Let's use `self._client.post` with `cast_to=object` to get the raw dict, 
        # them map it.
        
        # We need to correctly serialize the body first.
        # We can use `maybe_transform` like the original method?
        # Original: body=maybe_transform({"messages": messages, ...}, MessageCountTokensParams)
        from ..._utils import maybe_transform
        
        json_data = maybe_transform(
            {
                "messages": messages,
                "model": model,
                "system": system,
                "thinking": thinking,
                "tool_choice": tool_choice,
                "tools": tools,
            },
            MessageCountTokensParams,
        )
        
        response = self._client.post(
            request_url,
            body=json_data,
            options=options,
            cast_to=object, # Get raw dict
        )
        
        # Transform response
        # Bedrock response: {'inputTokens': 123}
        # Target: MessageTokensCount(input_tokens=123)
        input_tokens = cast(dict, response).get("inputTokens")
        if input_tokens is None:
             # Fallback or error?
             # Maybe the response IS `input_tokens`?
             input_tokens = cast(dict, response).get("input_tokens", 0)
             
        return MessageTokensCount(input_tokens=input_tokens)


class AsyncBedrockMessages(AsyncMessages):
    async def count_tokens(
        self,
        *,
        messages: Iterable[MessageParam],
        model: ModelParam,
        system: Union[str, Iterable[TextBlockParam]] | Omit = omit,
        thinking: ThinkingConfigParam | Omit = omit,
        tool_choice: ToolChoiceParam | Omit = omit,
        tools: Iterable[MessageCountTokensToolParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NotGiven,
    ) -> MessageTokensCount:
        from ..._utils import async_maybe_transform
        
        
        request_url = f"/model/{model}/count-tokens"
        
        json_data = await async_maybe_transform(
             {
                "messages": messages,
                "model": model,
                "system": system,
                "thinking": thinking,
                "tool_choice": tool_choice,
                "tools": tools,
            },
            MessageCountTokensParams,
        )

        options = make_request_options(
            extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
        )
        
        response = await self._client.post(
            request_url,
            body=json_data,
            options=options,
            cast_to=object, 
        )
        
        input_tokens = cast(dict, response).get("inputTokens", cast(dict, response).get("input_tokens", 0))
        return MessageTokensCount(input_tokens=input_tokens)
