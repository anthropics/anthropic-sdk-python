import anthropic

def main(sample_str: str = "Hello world!"):
    num_tokens = anthropic.count_tokens(sample_str)
    print(f"Number of tokens: {num_tokens}")


if __name__ == "__main__":
    main()
