#!/usr/bin/env -S poetry run python

import asyncio

from anthropic import Anthropic, AsyncAnthropic


def sync_tokens() -> None:
    """
    Synchronously count the number of tokens in text using the 'Anthropic' client.

    This function initializes an 'Anthropic' client, counts the number of tokens in the provided text, and prints the result
    to the console. It also includes an assertion to ensure the count matches the expected value.

    Raises:
        AssertionError: If the token count does not match the expected value.

    """
    client = Anthropic()

    text = "hello world!"

    tokens = client.count_tokens(text)
    print(f"'{text}' is {tokens} tokens")

    assert tokens == 3


async def async_tokens() -> None:
    """
    Asynchronously count the number of tokens in text using the 'AsyncAnthropic' client.

    This function initializes an 'AsyncAnthropic' client, asynchronously counts the number of tokens in the provided text,
    and prints the result to the console for two different text inputs.

    """
    anthropic = AsyncAnthropic()

    text = "fist message"
    tokens = await anthropic.count_tokens(text)
    print(f"'{text}' is {tokens} tokens")

    text = "second message"
    tokens = await anthropic.count_tokens(text)
    print(f"'{text}' is {tokens} tokens")


sync_tokens()
asyncio.run(async_tokens())
