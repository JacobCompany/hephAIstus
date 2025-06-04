import random
from datetime import datetime

from ollama import chat
from ollama._types import ResponseError

from . import exit_conditions, waiting_messages


from gpt4all import GPT4All


class Hephaestus:
    def __init__(self):
        self._reset_logs()

    def _reset_logs(self):
        # Initialize logs
        self.logs = []

    def _reformat_logs(self):
        # Reformat logs
        logs_formatted = []
        for log in self.logs:
            if log["role"] == "user":
                logs_formatted.append(
                    "{0}\nQuery: {1}".format("-" * 15, log["content"])
                )
            else:
                logs_formatted.append(log["content"])

        # Update logs
        self.logs = logs_formatted

    def _save_logs(self):
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

        # Write logs
        with open(save_loc, "w") as outfile:
            outfile.write("\n".join(self.logs))
            outfile.close()
            print("Saved logs to {0}".format(save_loc))

    def forge(self, model_version: str = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"):
        """
        Simple AI query tool that can use a specific model

        :param model_version:
        str: The model to use in the query
        """
        # Initialize model
        try:
            model = GPT4All(model_version)
        except ValueError:
            print(
                "Model ('{0}') was not found, please provide a different model.".format(
                    model_version
                )
            )
        else:
            # Get user's query
            query = input("Query: ")

            # Reset logs
            self._reset_logs()

            # Open up chat session
            with model.chat_session():
                # Check that user doesn't want to exit
                while query.lower() not in exit_conditions:
                    # Save user query
                    self.logs.append("{0}\nQuery: {1}".format("-" * 15, query))

                    # Get response from model
                    print("{0}...".format(random.choice(waiting_messages)))
                    response = model.generate(query, max_tokens=1024) + "\n"
                    self.logs.append(response)
                    print(response)

                    # Get user's query
                    query = input("Query: ")

            # Save logs
            if input("Save logs (Y/N)? ").lower() == "y":
                self._save_logs()

    def hammer(self, model_version: str = "devops_engineer"):
        # Get user's query
        query = input("Query: ")

        # Reset logs
        self._reset_logs()

        # Check that user doesn't want to exit
        while query.lower() not in exit_conditions:
            # Save user query
            self.logs.append({"role": "user", "content": query})

            # Get response from model
            print("{0}...".format(random.choice(waiting_messages)))
            try:
                response = chat(model=model_version, messages=self.logs)
            except ResponseError:
                print(
                    "Model ('{0}') was not found, please provide a different model.".format(
                        model_version
                    )
                )
            else:
                # Output response
                self.logs.append(
                    {"role": "assistant", "content": response.message.content}
                )
                print(response.message.content)

                # Get user's query
                query = input("\nQuery: ")

        # Save logs
        if input("Save logs (Y/N)? ").lower() == "y":
            self._reformat_logs()
            self._save_logs()
