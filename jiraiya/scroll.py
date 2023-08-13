import discord
from jiraiya.responses.response_story import get_story



def parameters_scroll(message:str) -> str:

    #set default parameters
    message_lang = "en"

    parameters = message.split("-")
    for parameter in parameters:
        # skip the command
        if "!" in parameter:
            continue

        parameter = parameter.strip()

        if len(parameter) == 2:
            message_lang = parameter

    return message_lang


async def send_scroll(message, user_message:str, is_private:bool):

    message_lang = parameters_scroll(user_message)
    title,story_file = get_story(message,message_lang)

    with open(story_file, "rb") as file:
        if is_private:
            await message.author.send(title, file=discord.File(file, "Ero-sennin - "+title+".txt"))
        else:
            await message.channel.send(title, file=discord.File(file, "Ero-sennin - "+title+".txt"))