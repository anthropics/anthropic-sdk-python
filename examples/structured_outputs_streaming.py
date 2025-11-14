# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "anthropic",
# ]
#
# [tool.uv.sources]
# anthropic = { path = "../", editable = true }
# ///

import pydantic

import anthropic


class Order(pydantic.BaseModel):
    product_name: str
    price: float
    quantity: int


client = anthropic.Anthropic()

prompt = """
Extract the product name, price, and quantity from this customer message:
"Hi, I’d like to order 2 packs of Green Tea for 5.50 dollars each."
"""

with client.beta.messages.stream(
    model="claude-sonnet-4-5-20250929-structured-outputs",
    messages=[{"role": "user", "content": prompt}],
    betas=["structured-outputs-2025-09-17"],
    max_tokens=1024,
    output_format=Order,
) as stream:
    for event in stream:
        if event.type == "text":
            print(event.parsed_snapshot())
