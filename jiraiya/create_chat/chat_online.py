import os



async def chat_characters_available(message):
    """
    Get the list of characters.
    """
    characters = [f"`{os.path.splitext(filename)[0]}`" for filename in os.listdir("data/chat_characters")]
    characters = "**Available Characters:**\n" + ", ".join(characters)

    await message.channel.send(characters)