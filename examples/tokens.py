#!/usr/bin/env poetry run python

from anthropic import Anthropic

client = Anthropic()

text = "hello world!"

tokens = client.count_tokens(text)
print(f"'{text}' is {tokens} tokens")

assert tokens == 3
