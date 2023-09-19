import re
from googletranslate import translate



def remove_emojis(text:str) -> tuple[str,list]:
    """
    Remove emojis from the given text and replace them with '#'.

    :param text: The input text containing emojis.
    :return: A tuple containing the cleaned text and a list of removed emojis.
    """

    emoji_pattern = re.compile("[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|[\U0001F1E0-\U0001F1FF]|[\U00002702-\U000027B0]|[\U000024C2-\U0001F251]")

    # Find emojis in the text
    emojis = re.findall(emoji_pattern, text)

    # Replace emojis with #
    cleaned_text = emoji_pattern.sub('#', text)

    return (cleaned_text, emojis)


def replace_hashtags_with_emojis(text:str, emojis:list) -> str:
    """
    Replace '#' symbols in the given text with corresponding emojis.

    :param text: The input text containing '#' symbols.
    :param emojis: A list of emojis to replace the '#' symbols.
    :return: The text with '#' symbols replaced by emojis.
    """

    for emoji in emojis:
        text = text.replace("#", emoji, 1)

    return text


def translate_text_with_emojis(text:str, dest:str, src:str) -> str:
    """
    Translate the given text from the source language to the destination language,
    while preserving emojis.

    :param text: The input text to be translated.
    :param dest: The destination language for translation.
    :param src: The source language of the input text.
    :return: The translated text with emojis preserved.
    """

    # Remove emojis before translation
    cleaned_text, emojis_removed = remove_emojis(text)

    # Translate the text
    translated_text = translate(cleaned_text, dest=dest, src=src)

    # Add emojis back after translation
    final_text = replace_hashtags_with_emojis(translated_text, emojis_removed)

    return final_text


if __name__ == '__main__':

    user_message = "Ero-Sennin at your service! 🐸 What can this legendary sannin do for you? 🐸🍻"

    message = translate_text_with_emojis(user_message, dest="ka", src="en")
    print(message)