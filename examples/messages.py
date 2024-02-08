from anthropic import Anthropic

client = Anthropic()

response = client.beta.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello!",
        }
    ],
    model="claude-2.1",
)
print(response)

response2 = client.beta.messages.create(
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
    model="claude-2.1",
)
print(response2)
