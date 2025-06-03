from ollama import chat, ChatResponse
from ollama._types import ResponseError


def hammer(model_version: str = "devops_engineer"):
    # Get user's query
    query = input("Query: ")

    # Setup log
    log = []

    try:
        response: ChatResponse = chat(model=model_version, messages=[
            {
                "role": "user",
                "content": query
            }
        ])
    except ResponseError:
        print(
            "Model ('{0}') was not found, please provide a different model.".format(
                model_version
            )
        )
    else:
        print(response.message.content)
