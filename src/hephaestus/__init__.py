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

from .forge import forge  # noqa: E402
from .hammer import hammer  # noqa: E402

__version__ = "0.1.0"
__all__ = [forge, hammer]
