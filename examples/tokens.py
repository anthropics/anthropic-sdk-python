#!/usr/bin/env -S poetry run python

import asyncio

from anthropic import Anthropic, AsyncAnthropic


def sync_tokens() -> None:
    client = Anthropic()

    text = "hello world!"

    tokens = client.count_tokens(text)
    print(f"'{text}' is {tokens} tokens")

    assert tokens == 3


async def async_tokens() -> None:
    anthropic = AsyncAnthropic()

    text = "first message"
    tokens = await anthropic.count_tokens(text)
    print(f"'{text}' is {tokens} tokens")

    text = "second message"
    tokens = await anthropic.count_tokens(text)
    print(f"'{text}' is {tokens} tokens")


sync_tokens()
asyncio.run(async_tokens())
