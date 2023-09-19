import discord
from jiraiya.responses.response_story import get_story



def parameters_scroll(user_message:str) -> tuple[str]:
    """
    Extracts and returns the desired parameters from the user's message for the scroll function.

    :param user_message: The user's message input.
    :return: The selected message language.
    """

    # Set default parameters
    character, message_lang = "", "en"

    parameters = user_message.split("-")
    for parameter in parameters:
        # Skip the parameter
        if "!" in parameter:
            continue

        parameter = parameter.strip()

        if len(parameter) == 2:
            message_lang = parameter
        else:
            character = parameter

    return (character, message_lang)


async def send_scroll(message, user_message:str, is_private:bool):
    """
    Sends a scroll (story) to the Discord channel or user's DM.

    :param message: The message object from the Discord channel.
    :param user_message: The user's message input.
    :param is_private: Boolean indicating whether the scroll should be sent privately to the user.

    :return: None
    """

    character, story_lang = parameters_scroll(user_message)
    title, story_file = await get_story(character,story_lang)

    with open(story_file, "rb") as file:
        if is_private:
            await message.author.send(title, file=discord.File(file, "Ero-sennin - "+title+".txt"))
        else:
            await message.channel.send(title, file=discord.File(file, "Ero-sennin - "+title+".txt"))