#!/usr/bin/env -S rye run python

import pprint
import asyncio
import itertools
from typing import Dict, List, Tuple, Union
from collections.abc import AsyncGenerator

from anthropic import AsyncAnthropic
from anthropic.types import TextBlock


async def make_batch(sequence: List[str], batch_size: int) -> AsyncGenerator[Tuple[str, ...], None]:
    iterator = iter(sequence)
    while True:
        batch = tuple(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch


async def process_prompt(client: AsyncAnthropic, prompt: str) -> Union[Dict[str, str], None]:
    try:
        response = await client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        if response.content:
            content = response.content[0]
            if isinstance(content, TextBlock):
                return {"input": prompt, "response": content.text}
        return None
    except Exception as e:
        print(f"Error processing prompt {prompt}: {e}")
        return None


async def process_batch(client: AsyncAnthropic, batch: Tuple[str, ...]) -> List[Union[Dict[str, str], None]]:
    tasks = [process_prompt(client, prompt) for prompt in batch]
    return await asyncio.gather(*tasks)


async def main(prompts: List[str], batch_size: int = 5, delay_between_batches: int = 60) -> List[Dict[str, str]]:
    client = AsyncAnthropic()

    results: List[Dict[str, str]] = []
    async for batch in make_batch(prompts, batch_size):
        batch_results = await process_batch(client, batch)
        results.extend(filter(None, batch_results))
        await asyncio.sleep(delay_between_batches)

    return results


prompts = [
    "What is the capital of Mali?",
    "What is the difference between SQL and NoSQL?.",
    "What is the difference between the javascript's bind and Python's functools.partial?",
    "Explain rate limiting in no more than two sentences.",
    "Which country won the most gold medals in the 2024 Olympics'?",
    "What is a higher-order-function?",
]

pprint.pprint(asyncio.run(main(prompts)))
