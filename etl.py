from os import path, listdir
import json
import re


def get_name_from_file(file: str) -> str:
    """
    Extracts the name from a given file path.

    Args:
        file (str): The file path.

    Returns:
        str: The extracted name.
    """

    name = path.basename(file)

    name = name.replace(".txt", "")
    name = name.replace("WhatsApp Chat with ", "")

    if name.endswith(
        "(1)"
    ):  # When a contact exists twice, the file name is appended with "(1)"
        name = name[:-3]

    return name


def extract_messages(path: str) -> tuple:
    """
    Extracts messages from a file and returns the text along with the name of the second person involved.

    Args:
        path (str): The path to the file containing the messages.

    Returns:
        tuple: A tuple containing the extracted text and the name of the second person.
    """

    second_person = get_name_from_file(path)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    return text, second_person


def transform_messages(text: str, second_person: str) -> list:
    """
    Transforms the given text containing WhatsApp messages into a list of dictionaries representing each message.

    Args:
        text (str): The text containing WhatsApp messages.
        second_person (str): The name of the second person in the conversation.

    Returns:
        list: A list of dictionaries representing each message. Each dictionary contains the following keys:
            - date: The date and time of the message.
            - sender: The sender of the message.
            - receiver: The receiver of the message.
            - message: The content of the message.
    """

    messages = []

    pattern = r"(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}) - ([^\n:]+): (.+?)(?=\n\d{2}/\d{2}/\d{2}, \d{2}:\d{2}|\Z)"
    matches = re.finditer(pattern, text, re.DOTALL)

    for ma in matches:
        date_and_time = ma.group(1)
        name = ma.group(2)
        message = ma.group(3).strip()

        if (
            name in [second_person, second_person.replace("_", "/")]
        ):  # When a contact name contains a slash, it is replaced with an underscore in the file name
            messages.append(
                {
                    "date": date_and_time,
                    "sender": second_person,
                    "receiver": "Me",
                    "message": message,
                }
            )
        else:
            messages.append(
                {
                    "date": date_and_time,
                    "sender": "Me",
                    "receiver": second_person,
                    "message": message,
                }
            )

    return messages


def load_messages(messages: list) -> None:
    """
    Load messages into a JSON file.

    Args:
        messages (list): The list of messages to be loaded.

    Returns:
        None
    """

    with open("messages.json", "w", encoding="utf-8") as outfile:
        json.dump(messages, outfile, ensure_ascii=False, indent=4)


def etl(path: str) -> None:
    """
    Extracts, transforms and loads the messages from a WhatsApp conversation.

    Args:
        path (str): The path to the dir containing all the messages files.

    Returns:
        None
    """

    files = listdir(path)
    messages = []
    for file in files:
        text, second_person = extract_messages(path + "/" + file)
        messages.extend(transform_messages(text, second_person))

    load_messages(messages)
