import json

from config.common import HISTORY_SAVE_DIRECTORY


def get_chat_history(chat_id: int, from_message_id: int):
    messages = []
    file_name = f'{HISTORY_SAVE_DIRECTORY}/chat_history_{str(chat_id)}.json'

    with open(file_name, 'r') as file:
        chat_history = json.load(file)

        for message in chat_history["messages"]:
            if (message["message_id"] < from_message_id):
                continue

            messages.append({
                "sender": message["sender"],
                "message": message["message"]
            })

    return messages
