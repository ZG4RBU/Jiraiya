import os



def parameters_chat_add_character(user_message:str) -> tuple[str]:

    # Set default parameters
    character_name, tag = "", ""

    parameters = user_message.split("-")
    for parameter in parameters:

        parameter = parameter.strip()

        if "name" in parameter:
            character_name = parameter.replace("name","",1).strip()
        elif "tag" in parameter:
            tag = parameter.replace("tag","",1).strip()

    return (character_name,tag)


async def chat_add_character(message, profiles:list[dict], user_message:str):
    """
    user_message example: /add -name Naruto -tag narutokun
    """

    character_name, tag = parameters_chat_add_character(user_message)
    if not character_name:
        return

    if message.attachments:  # Check if the message has attachments (images)
        attachment = message.attachments[0]
        if any(extension in attachment.filename.lower() for extension in ['.png', '.jpg', '.jpeg']):

            # Check for duplicate characters
            for filename in os.listdir("data/chat_characters"):
                stem = os.path.splitext(filename)[0]
                stem_character_name = stem.split("#")[0]
                stem_tag = stem.split("#")[1] if "#" in stem else None

                if stem_character_name.lower() == character_name.lower() and (tag == "" or tag == stem_tag):
                    await message.channel.send("Character already exists. Please choose a different name or add character with a tag.")
                    return

            # Split the file name into name and extension
            name, extension = os.path.splitext(attachment.filename)

            # Add the tag to the character name if it exists
            character_name_tagged = f"{character_name} #{tag}" if tag else character_name

            # Download the image
            image_path = f"data/chat_characters/{character_name_tagged}{extension}"
            await attachment.save(image_path)

            # Add the character to the list of characters
            profiles.append({"name": character_name_tagged, "avatar": image_path})

            # Send Success message
            if tag:
                success_message = f"`{character_name}` with tag `{tag}` is now online."
            else:
                success_message = f"`{character_name}` is now online."
            await message.channel.send(success_message)
