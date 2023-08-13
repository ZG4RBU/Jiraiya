import random
from time import sleep
import g4f
from jiraiya.responses.responses import get_response
from jiraiya.utilities.convert_latin_ka import convert_latin_ka
from jiraiya.utilities.translate_text_with_emojis import translate_text_with_emojis


async def send_message(message, user_message:str, is_private:bool):
    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


async def send_random_emoji(message):

    random_emoji = random.choice(["❤️", "👍", "😀", "😃", "😄", "😅", "😂", "🤣", "💀", "🤫", "🤨", "💯", "🐸"])
    random_int = random.randint(1, 15)

    if random_int == 1:
        async for history_message in message.channel.history(limit=1):
            sleep(random.randint(10, 30))

            # Add the heart emoji to the last bot message
            await history_message.add_reaction(random_emoji)
            break


async def send_gpt_message(message,user_message:str,message_lang:str="en",is_latin_ka:bool=False):
    """
    Send message to Discord channel with Jiraiya's response.

    user_message: message from user

    message_lang: language in which the user's message is written. Defaults to English
    Note: ChatGPT doesn't fully support languages other than English, so in order
    to return Jiraiya's message in other languages, First the user message is translated
    with Google Translate from other language to English. Finally, the prompt message
    is translated from English back to other language.

    is_latin_ka: if user message is Georgian and it's written in Latin alphabet
    """

    # Translate message from other language to English
    if message_lang != "en":
        if is_latin_ka:
            user_message = convert_latin_ka(user_message)

        user_message = translate_text_with_emojis(user_message, dest="en", src=message_lang)

    # generate Jiraiya's response
    try:
        prompt = f"Respond to this message as Jiraiya from Naruto. You can also include one or two funny emoji at the end of the response if needed. message: {user_message}"

        # normal response
        jiraiyas_response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.DeepAi, messages=[
                                     {"role": "user", "content": prompt}]) # alterative model setting
    except Exception as e:
        print(e)

    # Translate gpt response from English to other language
    if message_lang != "en":
        jiraiyas_response = translate_text_with_emojis(jiraiyas_response, dest=message_lang, src='en')

    await message.channel.send(jiraiyas_response)