
import random
from jiraiya.utilities.json_utils import read_json, update_json_dict


def get_response(message: str) -> str:
    """ 
    returns Jiraiya' response to the message

    :param message: message to respond to
    :return: response
    """

    if message == '!summon':
        messages_data = read_json()
        language:str = messages_data["jiraiyas_language"]
        messages:list = messages_data["summon"][language]
        message:str = random.choice(messages)
        return message

    elif message == '!help':
        messages_data = read_json()
        language:str = messages_data["jiraiyas_language"]
        message:str = messages_data["help"][language]
        return message

    elif '!language' in message:
        jiraiyas_language = "ka" if "-ka" in message else "en"
        update_json_dict({"jiraiyas_language": jiraiyas_language})
        return f"Jiraiya's language is now {jiraiyas_language}!"




