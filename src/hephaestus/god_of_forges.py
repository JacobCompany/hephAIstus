import random
from datetime import datetime

from gpt4all import GPT4All
from ollama import chat, list

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

# Define split condition
new_query_text = "-" * 15


class Hephaestus:
    def __init__(self):
        """
        Creates a new Hephaestus object
        """
        self._reset_logs()
        self._get_hammers()

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
            if not isinstance(log, dict) or "role" not in log or "content" not in log:
                print("Cannot reformat logs")
                return
            elif log["role"] == "user":
                logs_formatted.append(
                    "{0}\nQuery: {1}\n{0}".format(new_query_text, log["content"])
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
        default_save_loc = "{0}.txt".format(
            datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        )
        save_loc = input("Save location (default: {0}): ".format(default_save_loc))
        while len(save_loc) > 0 and not save_loc.endswith(".txt"):
            save_loc = input(
                "Save location must be .txt, not {0}\nSave location (default: {1}): ".format(
                    save_loc, default_save_loc
                )
            )
        if len(save_loc) == 0:
            save_loc = default_save_loc

        # Write logs
        with open(save_loc, "w") as outfile:
            outfile.write("\n".join(self.logs))
            outfile.close()
            print("Saved logs to {0}".format(save_loc))

    def load_logs(self, file_name: str):
        """
        Loads logs to be used by ollama
        """
        # Reset logs
        self._reset_logs()

        # Initialize logs
        logs_unformatted = []

        # Open the log file
        with open(file_name, "r") as input_file:
            # Read the entire log file
            logs_file = input_file.read()
            # Run through each query/response
            for content in logs_file.split(new_query_text):
                # Strip content
                content = content.strip()

                # Ensure there is actually a query/response
                if len(content) > 0:
                    # Get role
                    if content.startswith("Query: "):
                        role = "user"
                        content = content.replace("Query: ", "")
                    else:
                        role = "assistant"

                    # Add query/response
                    logs_unformatted.append({"role": role, "content": content})

        # Update logs
        self.logs = logs_unformatted
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
                    self.logs.append(
                        "{0}\nQuery: {1}\n{0}".format(new_query_text, query)
                    )

                    # Get response from model
                    print("{0}...".format(random.choice(waiting_messages)))
                    response = model.generate(query, max_tokens=1024) + "\n"
                    self.logs.append(response)
                    print("{0}\n{1}".format(new_query_text, response))

                    # Get user's query
                    query = input("Query: ")

            # Save logs
            if input("Save logs (Y/N)? ").lower() == "y":
                self._save_logs()

    def _get_hammers(self):
        """
        Get a list of available ollama models on your local machine
        """
        # Get all models
        models = list()

        # Save models
        self.hammers = [model.model.split(":")[0] for model in models.models]
        self.hammers.sort()

    def list_hammers(self):
        """
        List available ollama models on your local machine
        """
        # Print out available models
        print("Available models:")
        for model in self.hammers:
            print("\t{0}".format(model))

    def hammer(self, model_version: str = "devops_engineer"):
        """
        AI query tool that can use a specific model using ollama

        :param model_version:
        str: The model to use in the query
        """
        # Check that model is available
        if model_version not in self.hammers:
            print(
                "Model ('{0}') was not found, please provide a different model.".format(
                    model_version
                )
            )
            return

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
            response = chat(model=model_version, messages=self.logs)
            # Output response
            self.logs.append({"role": "assistant", "content": response.message.content})
            print("{0}\n{1}".format(new_query_text, response.message.content))

            # Get user's query
            query = input("\nQuery: ")

        # Save logs
        if input("Save logs (Y/N)? ").lower() == "y":
            self._reformat_logs()
            self._save_logs()
