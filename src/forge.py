from gpt4all import GPT4All

# Define exit conditions
exit_conditions = ["exit", "goodbye", "bye", "see ya"]


def forge(model_version: str = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"):
    """
    Simple AI query tool that can use a specific model

    :param model_version:
    str: The model to use in the query
    """
    # Get user's query
    query = input("Query: ")
    print("Generating response...")

    # Setup log
    log = []

    # Query model
    try:
        model = GPT4All(model_version)
    except ValueError:
        print("Model ('{0}') was not found, please provide a different model.".format(model_version))
    else:
        with model.chat_session():
            while query.lower() not in exit_conditions:
                # Get response from model
                response = model.generate(query, max_tokens=1024)
                log.append(response)
                print(response)

                # Get user's query
                query = input("Query: ")
                print("Generating response...")

        if input("Save log (Y/N)? ").lower() == "y":
            save_loc = input("Save location: ")
            with open(save_loc, "w") as outfile:
                outfile.write("\n".join(log))
                outfile.close()
                print("Saved log to {0}".format(save_loc))


if __name__ == "__main__":
    forge()
