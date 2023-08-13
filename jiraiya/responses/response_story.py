from googletranslate import translate
import random
from time import sleep
from jiraiya.storytime.storytime import generate_story
from jiraiya.utilities.utilities import write_file, get_emojis, split_text, shorten_text_line_length
from jiraiya.utilities.json_utils import read_json


def translate_story_text(story:str,lang:str) -> str:
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
        sleep(3)

    story = "".join(translated_story_parts)

    #add newlines back
    story = story.replace("#","\n") 

    return story


def translate_story(title:str,story:str,lang:str) -> tuple[str]:

    title = translate(title, dest=lang, src='en')
    story = translate_story_text(story)

    return (title,story)


def get_story(message:str,message_lang:str) -> tuple[str]:
    """ 
    Returns a story based on the message.
    """

    #get character name
    character_names = read_json("data/scroll_characters.json")
    character_names = list(character_names.keys())

    for name in character_names:
        if name.lower() in message:
            character_name = name
            break
        else:
            character_name = random.choice(character_names)

    # generate story
    title,story = generate_story(preset="Naruto",character_name=character_name)

    #shorten story lenght
    story = shorten_text_line_length(story,103)

    story_file = "eng_story.txt"
    write_file(story_file,story)

    # add emojis to story title
    emoji = get_emojis()
    title = f"📜{emoji} {title}"

    # translate story from English to other language
    if message_lang != "en":
        title,story = translate_story(title,story,lang=message_lang)

        story_file = "ka_story.txt"
        write_file(story_file,story)

    return (title,story_file)



if __name__ == '__main__':

    message = "!scroll Naruto"
    get_story(message)