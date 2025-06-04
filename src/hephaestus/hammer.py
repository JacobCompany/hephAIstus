import random
from datetime import datetime

from ollama import chat
from ollama._types import ResponseError

from . import exit_conditions, waiting_messages


def hammer(model_version: str = "devops_engineer"):
    # Get user's query
    query = input("Query: ")

    # Setup logs
    logs = []

    # Check that user doesn't want to exit
    while query.lower() not in exit_conditions:
        # Save user query
        logs.append({"role": "user", "content": query})

        # Get response from model
        print("{0}...".format(random.choice(waiting_messages)))
        try:
            response = chat(model=model_version, messages=logs)
        except ResponseError:
            print(
                "Model ('{0}') was not found, please provide a different model.".format(
                    model_version
                )
            )
        else:
            logs.append({"role": "assistant", "content": response.message.content})
            print(response.message.content)

            # Get user's query
            query = input("\nQuery: ")

    # Save logs
    if input("Save logs (Y/N)? ").lower() == "y":
        # Get save location
        save_loc = input("Save location (leave blank for auto generated location): ")
        while len(save_loc) > 0 and not save_loc.endswith(".txt"):
            save_loc = input(
                "Save location must be .txt, not {0}\nSave location (leave blank for auto generated location): ".format(
                    save_loc
                )
            )
        if len(save_loc) == 0:
            save_loc = "{0}.txt".format(datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))

        # Reformat logs
        logs_formatted = []
        for log in logs:
            if log["role"] == "user":
                logs_formatted.append(
                    "{0}\nQuery: {1}".format("-" * 15, log["content"])
                )
            else:
                logs_formatted.append(log["content"])

        # Write logs
        with open(save_loc, "w") as outfile:
            outfile.write("\n".join(logs_formatted))
            outfile.close()
            print("Saved logs to {0}".format(save_loc))
