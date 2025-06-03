from gpt4all import GPT4All


def forge(model_version: str = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"):
    """
    Simple AI query tool that can use a specific model

    :param model_version:
    str: The model to use in the query
    """
    # Getting user's query
    query = input("Query: ")
    print("Generating response...")

    # Query model
    try:
        model = GPT4All(model_version)
    except ValueError:
        print("Model ('{0}') was not found, please provide a different model.".format(model_version))
    else:
        with model.chat_session():
            print(model.generate(query, max_tokens=1024))


if __name__ == "__main__":
    forge()

    while input("\nAsk another query (Y/N)? ").lower() == "y":
        forge()
