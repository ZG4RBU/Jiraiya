import discord
import os
import shutil
import asyncio



async def delete_command_message(message):
    command_message = await message.channel.fetch_message(message.id)
    await command_message.delete()


async def remove_channel_webhooks(channel):
    # Fetch all webhooks in the channel
    webhooks = await channel.webhooks()

    # Delete each webhook
    for webhook in webhooks:
        await webhook.delete()


async def webhook_send_message(webhook, message:str, include_attachments:bool=False, attachments_dir:str=None):

    if include_attachments and attachments_dir:

        # Get the list of attachments in the folder
        attachments = [file for file in os.listdir(attachments_dir)]

        # Create a list of discord.File objects from the image files
        attachments = [discord.File(os.path.join(attachments_dir, file)) for file in attachments]

        await webhook.send(message, files=attachments)

    else:
        await webhook.send(message)


async def chat_send_message(message, webhooks:dict, profiles:list[dict], user_message:str):
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
            await asyncio.sleep(2)

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