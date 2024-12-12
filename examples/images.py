from pathlib import Path

from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hello!",
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": Path(__file__).parent.joinpath("logo.png"),
                    },
                },
            ],
        },
    ],
    model="claude-3-5-sonnet-latest",
)
print(response.model_dump_json(indent=2))
