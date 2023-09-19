import random
import asyncio
from googletranslate import translate
from jiraiya.responses.storytime import generate_story
from jiraiya.utilities.utilities import write_file, generate_nude_emojis, split_text, shorten_text_line_length
from jiraiya.utilities.json_utils import read_json



async def translate_story_text(story:str, lang:str) -> str:
    """
    Google translate have 500 character limit for each request.
    So we need to split the story into parts and translate each part separately.
    Then we join the translated parts back together.

    Also translate function removes newline so we replace it with symbol to avoid empty newlines.
    We add newlines back after translating the story.
    """

    #replace newlines
    story = story.replace("\n","#") 

    story_parts = split_text(story, 4999)
    translated_story_parts = []

    for story_part in story_parts:
        translated_story = translate(story_part, dest=lang, src='en')

        translated_story_parts.append(translated_story)
        await asyncio.sleep(3)

    story = "".join(translated_story_parts)

    #add newlines back
    story = story.replace("#","\n") 

    return story


async def translate_story(title:str, story:str, lang:str) -> tuple[str]:

    title = translate(title, dest=lang, src='en')
    story = await translate_story_text(story, lang)

    return (title,story)


async def get_story(character_name:str, story_lang:str) -> tuple[str]:
    """
    Generate a character-based story and return the story title and file.

    :param character_name: The character's name. If not provided, a random character will be chosen.
    :param story_lang: The language in which the story should be generated.

    :return: A tuple containing the story title and the name of the story file.
    """

    # Get available character names
    data_character_names = read_json("data/scroll_characters.json")
    data_character_names = list(data_character_names.keys())

    random_character = True

    # Match provided character_name with available character names
    for data_character_name in data_character_names:
        if data_character_name.lower() == character_name.lower():
            random_character = False
            break

    if random_character:
        character_name = random.choice(data_character_names)

    # Generate the story
    title,story = await generate_story(preset="Naruto",character_name=character_name.capitalize())

    # Shorten the story length
    story = shorten_text_line_length(story,103)

    # Save story in txt file
    story_file = "eng_story.txt"
    write_file(story_file,story)

    # Translate the story if needed
    if story_lang != "en":
        title,story = await translate_story(title,story,lang=story_lang)

        # Save translated story in txt file
        story_file = "translated_story.txt"
        write_file(story_file,story)

    # Shorten the story length again
    story = shorten_text_line_length(story,103)

    # Add emoji to the story title
    emojis = generate_nude_emojis()
    title = f"📜{emojis} {title}"

    return (title,story_file)



if __name__ == '__main__':

    message = "!scroll Naruto"
    get_story(message)