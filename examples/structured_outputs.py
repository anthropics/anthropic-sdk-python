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

parsed_message = client.beta.messages.parse(
    model="claude-sonnet-4-5-20250929-structured-outputs",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1024,
    output_format=Order,
)

print(parsed_message.parsed_output)  # Order(product_name='Green Tea', price=5.5, quantity=2)
