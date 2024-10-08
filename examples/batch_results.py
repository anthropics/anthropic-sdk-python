import sys
import time

import rich

from anthropic import Anthropic

client = Anthropic()

try:
    batch_id = sys.argv[1]
except IndexError as exc:
    raise RuntimeError("must specify a message batch ID, `python examples/batch_results.py msgbatch_123`") from exc

s = time.monotonic()

result_stream = client.beta.messages.batches.results(batch_id)
for result in result_stream:
    rich.print(result)
