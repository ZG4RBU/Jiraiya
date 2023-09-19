import random
import asyncio
import g4f
from jiraiya.responses.responses import get_response
from jiraiya.utilities.convert_latin_ka import convert_latin_ka
from jiraiya.utilities.translate_text_with_emojis import translate_text_with_emojis



async def send_message(message, user_message: str, is_private: bool):
    """
    Send a message response to the user or the channel, depending on whether it's private or not.

    :param message: The message object from the Discord channel.
    :param user_message: The message input from the user.
    :param is_private: A boolean indicating whether the response should be sent as a private message to the user.

    :return: None
    """
    try:
        # Get the response using a helper function (get_response)
        response = get_response(user_message)

        # Send the response either to the user's private messages or the channel
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)

    except Exception as e:
        print(e)


async def send_random_emoji(message):
    """
    Send a random emoji reaction to the last message in the channel.

    :param message: The message object from the Discord channel.
    :return: None
    """

    # List of emojis to choose from
    emojis = ["❤️", "👍", "😀", "😃", "😄", "😅", "😂", "🤣", "💀", "🤫", "🤨", "💯", "🐸"]

    # Choose a random emoji from the list
    random_emoji = random.choice(emojis)

    # Generate a random integer
    random_int = random.randint(1, 15)

    if random_int == 1:
        async for history_message in message.channel.history(limit=1):
            # Wait for a random duration between 10 and 30 seconds
            await asyncio.sleep(random.randint(10, 30))

            # Add the selected emoji to the last message
            await history_message.add_reaction(random_emoji)
            break


async def send_gpt_message(message, user_message:str, message_lang:str="en", is_latin_ka:bool=False):
    """
    Send a message to Discord channel with Jiraiya's response.

    :param message: The message object from the Discord channel.
    :param user_message: The message input from the user.
    :param message_lang: The language of the user's message. Defaults to English.

    Note: If the user's message is not in English, it will be translated to English using Google Translate.
    This enables Jiraiya's response generation in languages other than English. The final response will be translated
    back to the user's language.

    :param is_latin_ka: Set this to True if the user message is in Georgian and written in the Latin alphabet.

    :return: None
    """

    # Translate user's message to English if it's not already in English or needs translation
    if message_lang != "en":
        if is_latin_ka:
            user_message = convert_latin_ka(user_message)

        user_message = translate_text_with_emojis(user_message, dest="en", src=message_lang)

    try:
        # Prepare the prompt for generating Jiraiya's response
        prompt = f"Respond to this message as Jiraiya from Naruto. Feel free to add a funny emoji at the end if needed. message: {user_message}"

        # Generate Jiraiya's response using GPT model
        jiraiyas_response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.DeepAi, messages=[
                                     {"role": "user", "content": prompt}])
    except Exception as e:
        print(e)

    # Translate Jiraiya's response back to the user's language if needed
    if message_lang != "en":
        jiraiyas_response = translate_text_with_emojis(jiraiyas_response, dest=message_lang, src='en')

    await message.channel.send(jiraiyas_response)