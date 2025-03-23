# Python SDK for Anthropic API

[![PyPI version](https://badge.fury.io/py/anthropic.svg)](https://badge.fury.io/py/anthropic)

Official Python SDK for accessing the Anthropic Claude API.

## Installation

```bash
pip install anthropic
```

## Usage

First, get your API key from [Anthropic Console](https://console.anthropic.com/).

```python
from anthropic import Anthropic

client = Anthropic(
    # This is the default and can be omitted
    api_key="my_api_key",
)

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, world"
        }
    ]
)

print(message.content)
```

### Streaming

```python
from anthropic import Anthropic

client = Anthropic(
    # This is the default and can be omitted
    api_key="my_api_key",
)

with client.messages.stream(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, world"
        }
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Offline Mode for Testing

```python
from anthropic import Anthropic
from anthropic.lib.mock import setup_offline_mode, MockResponse

# Set up mock responses before creating clients
mock_builder = setup_offline_mode()
mock_builder.add(
    "POST",
    "messages",
    MockResponse(
        content={
            "id": "msg_mock",
            "type": "message",
            "role": "assistant",
            "content": [
                {"type": "text", "text": "This is a mock response for testing!"}
            ],
            "model": "claude-3-opus-20240229",
            "stop_reason": "end_turn",
            "usage": {
                "input_tokens": 10,
                "output_tokens": 15
            }
        }
    )
)

# Create a client with offline mode enabled
client = Anthropic(
    api_key="dummy-api-key-not-used-in-offline-mode",
    offline_mode=True
)

# Make API calls with mock responses
response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

# The response will be the mock response we defined
print(response.content[0].text)  # This is a mock response for testing!
```

## Authentication

By default, this library uses your `ANTHROPIC_API_KEY` environment variable. You can also configure the API key via the `api_key` parameter:

```python
client = Anthropic(
    api_key="my_api_key",
)
```

## AWS Bedrock Support

This library supports AWS Bedrock through a dedicated `AnthropicBedrock` client:

```python
from anthropic import AnthropicBedrock
import boto3

# Configure AWS credentials through environment variables or ~/.aws/credentials

# Use specific AWS credentials
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id="YOUR_ACCESS_KEY",
    aws_secret_access_key="YOUR_SECRET_KEY",
)

# Create AnthropicBedrock client with the bedrock client
client = AnthropicBedrock(
    bedrock_client=bedrock,
)

message = client.messages.create(
    model="anthropic.claude-3-sonnet-20240229-v1:0",  # Note the bedrock model name format
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, world"
        }
    ]
)

print(message.content)
```

## Google Vertex AI Support

This library also supports Google Vertex AI:

```python
from anthropic import AnthropicVertex

client = AnthropicVertex(
    project_id="your-project-id",
    location="us-central1",  # Set your region
)

message = client.messages.create(
    model="claude-3-sonnet@20240229",  # Vertex AI model identifier
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, world"
        }
    ]
)

print(message.content)
```

## Documentation

For full details on all SDK functionality, see the [Anthropic API documentation](https://docs.anthropic.com/).

## Requirements

Python 3.8 or higher.

## Development

After cloning the repository, install dependencies:

```bash
pip install -e ".[dev]"
```

To run tests:

```bash
pytest
```