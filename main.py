import discord
import os
from dotenv import load_dotenv
from jiraiya.create_chat.create_chat import create_chat
from jiraiya.quiz import send_quiz
from jiraiya.scroll import send_scroll
from jiraiya.send_messages import send_message, send_gpt_message, send_random_emoji



def run_discord_bot():

    load_dotenv(".env")
    TOKEN = os.getenv("DISCORD_TOKEN")

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)


    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        user_message = str(message.content)

        if user_message.startswith('/'):
            await create_chat(message, user_message)

        elif user_message.startswith('!') or user_message.startswith('?'):

            is_private = False if user_message.startswith('!') else True

            if "quiz" in user_message:
                await send_quiz(message, user_message, is_private)
            elif "scroll" in user_message:
                await send_scroll(message, user_message, is_private)
            else:
                await send_message(message, user_message, is_private)

        elif any(x in user_message for x in ["Jiraiya","jiraiya","Jiraia","jiraia","ჯირაია","ჯერაია"]):
            if any(x in user_message for x in ["ჯერაია","ჯირაია"]):
                await send_gpt_message(message, user_message, message_lang="ka")
            elif any(x in user_message for x in ["jiraia","Jiraia"]):
                await send_gpt_message(message, user_message, message_lang="ka", is_latin_ka=True)
            else:
                await send_gpt_message(message, user_message)
        else:
            await send_random_emoji(message)


    client.run(TOKEN)


if __name__ == '__main__':
    run_discord_bot()