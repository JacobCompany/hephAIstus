from gpt4all import GPT4All


def forge(model_version: str = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"):
    """
    Simple AI query tool

    :param model_version:
    str: The model to use in the query
    """
    # Getting user's query
    query = input("Query: ")
    print("Generating response...")

    # Query model
    model = GPT4All(model_version)
    with model.chat_session():
        print(model.generate(query, max_tokens=1024))


if __name__ == "__main__":
    forge()
