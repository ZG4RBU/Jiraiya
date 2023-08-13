import re
from googletranslate import translate


def remove_emojis(text: str) -> tuple[str,list]:
    # Emoji pattern
    emoji_pattern = re.compile("[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|[\U0001F1E0-\U0001F1FF]|[\U00002702-\U000027B0]|[\U000024C2-\U0001F251]")

    # Find emojis in the text
    emojis = re.findall(emoji_pattern, text)

    # Replace emojis with #
    cleaned_text = emoji_pattern.sub('#', text)
    return cleaned_text, emojis


def replace_hashtags_with_emojis(text: str, emojis: list) -> str:
    # Replace # symbols with corresponding emojis
    for emoji in emojis:
        text = text.replace("#", emoji, 1)
    return text


def translate_text_with_emojis(text: str, dest: str, src: str) -> str:

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