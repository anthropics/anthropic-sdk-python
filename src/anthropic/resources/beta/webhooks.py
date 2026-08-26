# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import json
from typing import Mapping, cast

from ..._models import construct_type
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._exceptions import AnthropicError
from ...types.beta.beta_webhook_event import BetaWebhookEvent

__all__ = ["Webhooks", "AsyncWebhooks"]


class Webhooks(SyncAPIResource):
    def parse_unverified(self, payload: str) -> BetaWebhookEvent:
        """Parses a webhook payload into an event without verifying its signature.

        Prefer
        `unwrap()` unless you have already verified the signature yourself.
        """
        return cast(
            BetaWebhookEvent,
            construct_type(
                type_=BetaWebhookEvent,
                value=json.loads(payload),
            ),
        )

    def unwrap(self, payload: str, *, headers: Mapping[str, str], key: str | bytes | None = None) -> BetaWebhookEvent:
        """
        Verifies the webhook signature from the `webhook-id`, `webhook-timestamp` and
        `webhook-signature` headers using your webhook signing key, then parses the
        payload into an event. Fails if the signature is missing or invalid.
        """
        try:
            from standardwebhooks import Webhook
        except ImportError as exc:
            raise AnthropicError("You need to install `anthropic[webhooks]` to use this method") from exc

        if key is None:
            key = self._client.webhook_key
            if key is None:
                raise ValueError(
                    "Cannot verify a webhook without a key on either the client's webhook_key or passed in as an argument"
                )

        if not isinstance(headers, dict):
            headers = dict(headers)

        Webhook(key).verify(payload, headers)

        return cast(
            BetaWebhookEvent,
            construct_type(
                type_=BetaWebhookEvent,
                value=json.loads(payload),
            ),
        )


class AsyncWebhooks(AsyncAPIResource):
    def parse_unverified(self, payload: str) -> BetaWebhookEvent:
        """Parses a webhook payload into an event without verifying its signature.

        Prefer
        `unwrap()` unless you have already verified the signature yourself.
        """
        return cast(
            BetaWebhookEvent,
            construct_type(
                type_=BetaWebhookEvent,
                value=json.loads(payload),
            ),
        )

    def unwrap(self, payload: str, *, headers: Mapping[str, str], key: str | bytes | None = None) -> BetaWebhookEvent:
        """
        Verifies the webhook signature from the `webhook-id`, `webhook-timestamp` and
        `webhook-signature` headers using your webhook signing key, then parses the
        payload into an event. Fails if the signature is missing or invalid.
        """
        try:
            from standardwebhooks import Webhook
        except ImportError as exc:
            raise AnthropicError("You need to install `anthropic[webhooks]` to use this method") from exc

        if key is None:
            key = self._client.webhook_key
            if key is None:
                raise ValueError(
                    "Cannot verify a webhook without a key on either the client's webhook_key or passed in as an argument"
                )

        if not isinstance(headers, dict):
            headers = dict(headers)

        Webhook(key).verify(payload, headers)

        return cast(
            BetaWebhookEvent,
            construct_type(
                type_=BetaWebhookEvent,
                value=json.loads(payload),
            ),
        )
