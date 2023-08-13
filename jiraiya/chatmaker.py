import discord
import os
import shutil
from time import sleep


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


# Create a dictionary to store webhooks
webhooks = {}

# Load all chat characters
profiles = load_chat_characters()


async def delete_command_message(message):
    command_message = await message.channel.fetch_message(message.id)
    await command_message.delete()


async def remove_channel_webhooks(channel):
    # Fetch all webhooks in the channel
    webhooks = await channel.webhooks()

    # Delete each webhook
    for webhook in webhooks:
        await webhook.delete()


def parameters_chatmaker_add_character(user_message:str) -> tuple[str]:

    #set default parameters
    character_name, tag = "", ""

    params = user_message.split()

    if "-name" in user_message:
        character_name = params[params.index("-name") + 1]

    if "-tag" in user_message:
        tag = params[params.index("-tag") + 1]
        tag = f" #{tag}"

    return (character_name,tag)


async def chatmaker_add_character(message, user_message:str):
    """
    user_message example: /add -name Naruto -tag narutokun
    """

    character_name, tag = parameters_chatmaker_add_character(user_message)
    if not character_name:
        return

    if message.attachments:  # Check if the message has attachments (images)
        attachment = message.attachments[0]
        if any(extension in attachment.filename.lower() for extension in ['.png', '.jpg', '.jpeg']):

            # Check for duplicate characters
            for filename in os.listdir("data/chat_characters"):
                stem = os.path.splitext(filename)[0]
                if stem.lower() == character_name.lower():
                    await message.channel.send("Character already exists. Please choose a different name or add character with a tag.")
                    return

            # Split the file name into name and extension
            name, extension = os.path.splitext(attachment.filename)

            # Add the tag to the character name if it exists
            character_name_tagged = f"{character_name}{tag}"

            # Download the image
            image_path = f"data/chat_characters/{character_name_tagged}{extension}"
            await attachment.save(image_path)

            # Add a new webhook
            webhook = await message.channel.create_webhook(name=character_name, avatar=image_path)
            webhooks[character_name_tagged] = webhook


async def webhook_send_message(webhook, message:str, include_attachments:bool=False, attachments_dir:str=None):

    if include_attachments and attachments_dir:

        # Get the list of attachments in the folder
        attachments = [file for file in os.listdir(attachments_dir)]

        # Create a list of discord.File objects from the image files
        attachments = [discord.File(os.path.join(attachments_dir, file)) for file in attachments]

        await webhook.send(message, files=attachments)

    else:
        await webhook.send(message)


async def chatmaker_characters_available(message):
    """
    Get the list of characters.
    """
    characters = [f"`{os.path.splitext(filename)[0]}`" for filename in os.listdir("data/chat_characters")]
    characters = "**Available Characters:**\n" + ", ".join(characters)

    await message.channel.send(characters)


async def send_chatmaker_message(message, user_message:str):
    if not webhooks:
        # Remove all existing webhooks in the channel to prevent duplicates
        await remove_channel_webhooks(message.channel)

    cm_character, _, cm_message_content = user_message[1:].partition(' -')

    for profile in profiles:
        profile_name = profile.get("name")
        profile_name_untagged = profile_name.split("#")[0]
        profile_name_tag = profile_name.split("#")[1] if "#" in profile_name else None
        profile_avatar_path = profile.get("avatar")

        if cm_character == profile_name_untagged or cm_character == profile_name_tag:

            include_attachments = False

            # Extract attachments from the message content if any
            if message.attachments:
                include_attachments = True
                # Create a directory to store downloaded attachments
                os.makedirs('downloaded_attachments', exist_ok=True)

                for attachment in message.attachments:
                    # Download the attachment
                    path = os.path.join('downloaded_attachments', attachment.filename)
                    await attachment.save(path)

            # Delete the command message
            await delete_command_message(message)
            sleep(2)

            # Check if the webhook for the profile already exists
            webhook = webhooks.get(profile_name)
            if webhook is None:
                with open(profile_avatar_path, 'rb') as file:
                    profile_avatar = file.read()

                # Create a new webhook if it doesn't exist
                webhook = await message.channel.create_webhook(name=profile_name_untagged, avatar=profile_avatar)
                webhooks[profile_name] = webhook

            # Send a message using the webhook
            await webhook_send_message(
                webhook,
                cm_message_content,
                include_attachments=include_attachments,
                attachments_dir='downloaded_attachments'
            )

            # Delete previously downloaded attachments if any
            if include_attachments:
                shutil.rmtree('downloaded_attachments')