import os
from jiraiya.create_chat.chat_send_message import chat_send_message
from jiraiya.create_chat.chat_add_character import chat_add_character
from jiraiya.create_chat.chat_online import chat_characters_available



def load_chat_characters(folder_path:str="data/chat_characters") -> list[dict]:

    profiles = []
    valid_extensions = ['.png', '.jpg', '.jpeg']

    for filename in os.listdir(folder_path):

        if any(filename.lower().endswith(ext) for ext in valid_extensions):
            name = os.path.splitext(filename)[0]
            avatar = os.path.join(folder_path, filename)
            profile = {"name": name, "avatar": avatar}
            profiles.append(profile)

    return profiles


# Load all chat characters
profiles = load_chat_characters()

# Create a dictionary to store webhooks
webhooks = {}


async def create_chat(message, user_message:str):

    if "add" in user_message:
        await chat_add_character(message, profiles, user_message)
    elif "online" in user_message:
        await chat_characters_available(message)
    else:
        await chat_send_message(message, webhooks, profiles, user_message)