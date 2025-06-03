import random

from gpt4all import GPT4All

from . import exit_conditions, waiting_messages


def forge(model_version: str = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"):
    """
    Simple AI query tool that can use a specific model

    :param model_version:
    str: The model to use in the query
    """
    # Get user's query
    query = input("Query: ")

    # Setup log
    log = []

    # Initialize model
    try:
        model = GPT4All(model_version)
    except ValueError:
        print("Model ('{0}') was not found, please provide a different model.".format(model_version))
    else:
        # Open up chat session
        with model.chat_session():
            # Check that user doesn't want to exit
            while query.lower() not in exit_conditions:
                # Save user query
                log.append("{0}\nQuery: {1}".format("-" * 15, query))

                # Get response from model
                print("{0}...".format(random.choice(waiting_messages)))
                response = model.generate(query, max_tokens=1024) + "\n"
                log.append(response)
                print(response)

                # Get user's query
                query = input("Query: ")

        # Save log
        if input("Save log (Y/N)? ").lower() == "y":
            save_loc = input("Save location: ")
            while not save_loc.endswith(".txt"):
                save_loc = input("Save location must be .txt, not {0}\nSave location: ".format(save_loc))
            with open(save_loc, "w") as outfile:
                outfile.write("\n".join(log))
                outfile.close()
                print("Saved log to {0}".format(save_loc))
