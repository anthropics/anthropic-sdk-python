from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello!",
        }
    ],
    model="claude-sonnet-4-5-20250929",
)
print(response)

response2 = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello!",
        },
        {
            "role": response.role,
            "content": response.content,
        },
        {
            "role": "user",
            "content": "How are you?",
        },
    ],
    model="claude-sonnet-4-5-20250929",
)
print(response2)
