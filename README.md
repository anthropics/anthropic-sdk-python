# Anthropic Python SDK

This python repo provides access to Anthropic's safety-first language model APIs.

For more information on our APIs, please check out [Anthropic's documentation](https://console.anthropic.com/docs).

## How to use

Install the package with:
```
pip install anthropic
```
Then write code with:
```
import anthropic
client = anthropic.Client(api_key=<insert token here>)
client.XXX # look to examples/ directory for code demonstrations
```

## How to develop and run the examples in this repo
```
pip install .
export ANTHROPIC_API_KEY=<insert token here>
python examples/basic_sync.py
python examples/basic_stream.py
python examples/count_tokens.py
```
