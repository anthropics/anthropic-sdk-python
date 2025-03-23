"""
Example of using the offline mode feature in the Anthropic Python SDK.

This demonstrates how to:
1. Enable offline mode when creating the client
2. Set up mock responses for different API endpoints
3. Make API calls that return the mock responses instead of making actual network requests
"""

from anthropic import Anthropic
from anthropic.lib.mock import setup_offline_mode, MockResponse

# Set up the mock responses before creating any clients
mock_builder = setup_offline_mode()

# Add custom responses for specific endpoints
mock_builder.add(
    "POST",
    "messages",
    MockResponse(
        content={
            "id": "msg_mock_01234",
            "type": "message",
            "role": "assistant",
            "content": [
                {"type": "text", "text": "This is a custom mock response!"}
            ],
            "model": "claude-3-opus-20240229",
            "stop_reason": "end_turn",
            "usage": {
                "input_tokens": 20,
                "output_tokens": 10
            }
        }
    )
)

# For multiple sequential calls to the same endpoint, add multiple responses
# They'll be used in the order they were added
mock_builder.add(
    "POST",
    "messages",
    MockResponse(
        content={
            "id": "msg_mock_56789",
            "type": "message",
            "role": "assistant", 
            "content": [
                {"type": "text", "text": "This is the second mock response!"}
            ],
            "model": "claude-3-opus-20240229",
            "stop_reason": "end_turn",
            "usage": {
                "input_tokens": 15,
                "output_tokens": 10
            }
        }
    )
)

# Create a client with offline mode enabled
client = Anthropic(
    api_key="dummy-api-key-not-used-in-offline-mode",
    offline_mode=True
)

# Now make API calls that will use the mock responses
first_response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello! This will be handled by the first mock response."}
    ]
)

print(f"First mock response: {first_response.content[0].text}")

# This will use the second mock response we added
second_response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Can you tell me about offline mode?"}
    ]
)

print(f"Second mock response: {second_response.content[0].text}")

# If we've run out of specific mock responses for an endpoint,
# it will use the default mock response
third_response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "This will use the default mock response"}
    ]
)

print(f"Default mock response: {third_response.content[0].text}")