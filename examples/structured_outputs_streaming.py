import pydantic

import anthropic


class Order(pydantic.BaseModel):
    product_name: str
    price: float
    quantity: int


client = anthropic.Anthropic()

prompt = """
Extract the product name, price, and quantity from this customer message:
"Hi, I'd like to order 2 packs of Green Tea for 5.50 dollars each."
"""

with client.messages.stream(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1024,
    output_format=Order,
) as stream:
    for event in stream:
        if event.type == "text":
            print(event.parsed_snapshot())

    # Get the final parsed output
    final_message = stream.get_final_message()
    print(f"\nFinal parsed order: {final_message.parsed_output}")
