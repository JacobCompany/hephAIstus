import random
from datetime import datetime

from gpt4all import GPT4All
from ollama import chat
from ollama._types import ResponseError

# Define exit conditions for all functions
exit_conditions = [
    "exit",
    "goodbye",
    "bye",
    "good bye",
    "see ya",
    "q",
    "quit",
    "hasta la vista",
]

# Define waiting messages for all functions
waiting_messages = [
    "You sure? Ok then",
    "Working on it",
    "After my smoke break",
    "I'll get right on that",
    "Running the permutations",
    "Beep boop",
    "Getting response",
    "Hold your horses",
    "Hey! I'm working here",
    "Is that a bird? Is that a plane? No! It's your response",
    "I'll be back",
    "Thinking really hard",
    "Waiting for Hermes to return",
]


class Hephaestus:
    def __init__(self):
        """
        Creates a new Hephaestus object
        """
        self._reset_logs()

    def _reset_logs(self):
        """
        Resets the logs to empty
        """
        # Initialize logs
        self.logs = []
        self.logs_loaded = False

    def _reformat_logs(self):
        """
        Reformats the logs from ollama's format to a more user-friendly one for saving
        """
        # Reformat logs
        logs_formatted = []
        for log in self.logs:
            if log["role"] == "user":
                logs_formatted.append(
                    "{0}\nQuery: {1}\n{0}".format("-" * 15, log["content"])
                )
            else:
                logs_formatted.append(log["content"])

        # Update logs
        self.logs = logs_formatted

    def _save_logs(self):
        """
        Saves the logs to a text file
        """
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

    def _load_logs(self, file_name: str):
        """
        Loads logs to be used by ollama
        """
        # Reset logs
        self._reset_logs()

        # Open the log file
        with open(file_name, "r") as input_file:
            input_file.read()
            self.logs = []

        # Set that logs were loaded
        self.logs_loaded = True

    def forge(self, model_version: str = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"):
        """
        AI query tool that can use a specific model using gpt4all

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
                    self.logs.append("{0}\nQuery: {1}\n{0}".format("-" * 15, query))

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
        """
        AI query tool that can use a specific model using ollama

        :param model_version:
        str: The model to use in the query
        """
        # Get user's query
        query = input("Query: ")

        # Reset logs if fresh
        if not self.logs_loaded:
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
