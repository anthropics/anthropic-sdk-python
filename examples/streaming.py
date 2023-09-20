#!/usr/bin/env -S poetry run python

import asyncio

from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic, APIStatusError, AsyncAnthropic

client = Anthropic()
async_client = AsyncAnthropic()

question = """
Hey Claude! How can I recursively list all files in a directory in Python?
"""


def sync_stream() -> None:
    """
    Synchronously initiate a streaming completion process.

    This function sends a prompt to a model and streams back completions as they become available. It prints the generated
    completions to the console.

    Raises:
        APIStatusError: If there is an issue with the API response.

    """
    stream = client.completions.create(
        prompt=f"{HUMAN_PROMPT} {question}{AI_PROMPT}",
        model="claude-2",
        stream=True,
        max_tokens_to_sample=300,
    )

    for completion in stream:
        print(completion.completion, end="", flush=True)

    print()


async def async_stream() -> None:
    """
    Asynchronously initiate a streaming completion process.

    This function sends a prompt to a model asynchronously and streams back completions as they become available. It prints
    the generated completions to the console.

    Raises:
        APIStatusError: If there is an issue with the API response.

    """
    stream = await async_client.completions.create(
        prompt=f"{HUMAN_PROMPT} {question}{AI_PROMPT}",
        model="claude-2",
        stream=True,
        max_tokens_to_sample=300,
    )

    async for completion in stream:
        print(completion.completion, end="", flush=True)

    print()


def stream_error() -> None:
    """
    Simulate an error while attempting to initiate a streaming completion process.

    This function intentionally triggers an API status error by using an unknown model, demonstrating how to handle such
    errors.

    """
    try:
        client.completions.create(
            prompt=f"{HUMAN_PROMPT} {question}{AI_PROMPT}",
            model="claude-unknown-model",
            stream=True,
            max_tokens_to_sample=300,
        )
    except APIStatusError as err:
        print(f"Caught API status error with response body: {err.response.text}")


sync_stream()
asyncio.run(async_stream())
stream_error()
