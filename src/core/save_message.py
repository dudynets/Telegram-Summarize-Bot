import json
import os
from telegram import Message

from config.common import HISTORY_SAVE_DIRECTORY


def save_message(message: Message, is_edited: bool):
    chat_id = message.chat_id
    message_id = message.message_id
    sender = message.from_user.full_name
    message_text = message.text

    file_name = f'{HISTORY_SAVE_DIRECTORY}/chat_history_{str(chat_id)}.json'
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    message_data = {
        "message_id": message_id,
        "sender": sender,
        "message": message_text
    }

    try:
        with open(file_name, 'r') as file:
            chat_history = json.load(file)

            if not chat_history["chat_id"] or not chat_history["messages"]:
                chat_history = {
                    "chat_id": chat_id,
                    "messages": []
                }

    except FileNotFoundError:
        chat_history = {
            "chat_id": chat_id,
            "messages": []
        }

    if is_edited:
        chat_history["messages"] = replaceMessage(chat_history["messages"], message_data)
    else:
        chat_history["messages"].append(message_data)
    
    with open(file_name, 'w') as file:
        json.dump(chat_history, file, ensure_ascii=False, indent=2)


def replaceMessage(messages, updated_message):
    for i in range(len(messages)):
        if messages[i]["message_id"] == updated_message["message_id"]:
            messages[i] = updated_message
            break
    return messages
