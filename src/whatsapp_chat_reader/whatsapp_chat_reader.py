import re
from enum import Enum
from typing import List, Dict, Optional


class By(Enum):
    Person = 'Person'
    Date = 'Date'
    Message = 'Message'


def split_chat_line(line: str) -> Dict[str, Optional[str]]:
    """
    Splits a chat line into its components: date, time, person, and message.

    Args:
        line (str): A line from the chat file.

    Returns:
        dict: A dictionary with keys 'Date', 'Time', 'Person', and 'Message'.
              If the line does not match the expected format, values will be None.
    """
    line = re.sub(r'[\u200e\u200f]', '', line)
    pattern = re.compile(r'^\[(\d{2}\.\d{2}\.\d{2}), (\d{2}:\d{2}:\d{2})] ([^:]+): (.+)$')
    match = pattern.match(line)

    if match:
        date, time, person, message = match.groups()
        return {
            'Date': date,
            'Time': time,
            'Person': person,
            'Message': message.strip()
        }
    else:
        return {
            'Date': None,
            'Time': None,
            'Person': None,
            'Message': None
        }


class WhatsAppChatReader:
    """
    A class to read WhatsApp chat exports.

    Attributes:
        __path (str): The file path of the chat export.
        __chat (List[Dict[str, Optional[str]]]): A list of dictionaries with chat details.
    """

    def __init__(self, path: str) -> None:
        """
        Initializes the WhatsAppChatReader with the path to the chat file.

        Args:
            path (str): The file path of the WhatsApp chat export.
        """
        self.__path = path
        self.__chat: List[Dict[str, Optional[str]]] = []
        self.__read_messages()

    def __read_messages(self) -> None:
        """
        Read the chat file and populates the chat attribute.
        """
        current_message = None

        with open(self.__path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                chat_line = split_chat_line(line)
                if chat_line['Date']:
                    if current_message is not None:
                        self.__chat.append(current_message)
                    current_message = chat_line
                elif current_message:
                    current_message['Message'] += '\n' + line

            if current_message:
                self.__chat.append(current_message)

    def get_chat(self) -> List[Dict[str, Optional[str]]]:
        """
        Returns the chat as a list of dictionaries.

        Returns:
            List[Dict[str, Optional[str]]]: The list of chat entries.
        """
        return self.__chat

    def get_chat_len(self) -> int:
        """
        Returns the number of chat entries.

        Returns:
            int: The number of chat entries.
        """
        return len(self.__chat)

    def get_persons(self) -> List[str]:
        """
        Returns a list of unique persons from the chat.

        Returns:
            List[str]: The list of unique persons.
        """
        return list({element['Person'] for element in self.__chat if element['Person']})

    def get_messages(self) -> List[str]:
        """
        Returns a list of all messages from the chat.

        Returns:
            List[str]: The list of messages.
        """
        return [element['Message'] for element in self.__chat if element['Message']]

    def remove_person(self, person: str) -> None:
        """
        Removes all messages from a specific person.

        Args:
            person (str): The person whose messages should be removed.
        """
        self.__chat = [element for element in self.__chat if element['Person'] != person]

    def get_filtered_chat(self, filters: List[str], by: By = By.Person) -> List[Dict[str, Optional[str]]]:
        """
        Filters chat messages by given criteria.

        Args:
            filters (List[str]): A list of strings to filter by.
            by (By): The type of filter to apply (Person, Date, Message).

        Returns:
            List[Dict[str, Optional[str]]]: The list of filtered chat entries.
        """
        filtered_chat = self.__chat

        if by == By.Person:
            filtered_chat = [entry for entry in filtered_chat if
                             any(filter_str in entry['Person'] for filter_str in filters)]
        elif by == By.Date:
            filtered_chat = [entry for entry in filtered_chat if
                             any(filter_str in entry['Date'] for filter_str in filters)]
        elif by == By.Message:
            filtered_chat = [entry for entry in filtered_chat if
                             any(filter_str in entry['Message'] for filter_str in filters)]

        return filtered_chat

    def rename_person(self, person: str, new_name: str) -> None:
        """
        Renames a person in the chat.

        Args:
            person (str): The current name of the person.
            new_name (str): The new name for the person.
        """
        for element in self.__chat:
            if element['Person'] == person:
                element['Person'] = new_name
