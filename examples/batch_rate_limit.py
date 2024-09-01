#!/usr/bin/env -S rye run python

import pprint
import asyncio
import itertools

from anthropic import AsyncAnthropic


async def make_batch(sequence, batch_size):
    iterator = iter(sequence)
    while batch := tuple(itertools.islice(iterator, batch_size)):
        yield batch


async def process_prompt(client, prompt):
    try:
        response = await client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        return {"input": prompt, "repsonse": response.content[0].text}
    except Exception as e:
        print(f"Error processing prompt {prompt}: {e}")
        return None


async def process_batch(client, batch):
    tasks = [process_prompt(client, prompt) for prompt in batch]
    return await asyncio.gather(*tasks)


async def main(prompts, batch_size=5, delay_between_batches=60):
    client = AsyncAnthropic()

    results = []
    async for batch in make_batch(prompts, batch_size):
        batch_results = await process_batch(client, batch)
        results.extend(batch_results)
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
