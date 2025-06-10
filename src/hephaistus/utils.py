from os.path import isfile

from pypdf import PdfReader


def read_file(file_name: str):
    """
    Reads the information from a file
    :param file_name:
    str: Location and name of file
    :return:
    str: The extracted text
    """
    # Check that it is a file
    if not isfile(file_name):
        raise ValueError("'{0}' is not a file".format(file_name))

    # Initialize text from file
    text = []

    # Handle PDFs
    if file_name.endswith(".pdf"):
        for page in PdfReader(file_name).pages:
            text.append(page.extract_text())
    # Read file and extract text
    else:
        with open(file_name, "r") as input_file:
            text.append(input_file.read())

    print("Read {0}".format(file_name))
    return "\n".join(text)


def reformat_logs(logs: list, new_query_text: str = "-" * 15):
    """
    Reformats the logs from ollama's format to a more user-friendly one for saving

    :param logs:
    list: A list of logs to be reformatted. Only reformats the ollama log format, i.e. a list of dicts with `role` and `content` keys.
    :param new_query_text:
    str: Text used to break up the different queries and responses
    :return:
    list: The reformatted logs
    """
    # Reformat logs
    logs_formatted = []
    for log in logs:
        if not isinstance(log, dict) or "role" not in log or "content" not in log:
            raise TypeError("Cannot reformat logs")
        elif log["role"] == "user":
            logs_formatted.append(
                "{0}\nQuery: {1}\n{0}".format(new_query_text, log["content"])
            )
        else:
            logs_formatted.append(log["content"])

    return logs_formatted
